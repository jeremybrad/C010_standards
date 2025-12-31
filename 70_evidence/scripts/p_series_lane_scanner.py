#!/usr/bin/env python3
"""
P-series Lane Scanner for Folder Audit Remediation
Classifies repos into: compliant, quick_win_exception, manual_migration, local_only

Version: 1.0.0
Date: 2025-12-31
"""

import os
import subprocess
import csv
import re
import json
from datetime import datetime
from pathlib import Path
from typing import NamedTuple, Optional

# Betty Protocol allowed directories
ALLOWED_DIRS = {
    "00_admin", "00_run", "10_docs", "20_receipts", "20_approvals",
    "20_inbox", "30_config", "40_src", "50_data", "70_evidence",
    "80_evidence_packages", "90_archive"
}

# Required files for compliance (P-series: 00_run is optional)
REQUIRED_FILES = ["README.md"]  # rules_now.md and RELATIONS.yaml are recommended but not required for P-series

# Import risk patterns
IMPORT_RISK_PATTERNS = [
    (r"sys\.path\.(insert|append)", "sys.path manipulation"),
    (r"from\s+\.\.\s+import", "parent directory import"),
    (r"importlib\.import_module", "dynamic import"),
    (r'__file__.*dirname', "path-relative import setup"),
    (r"from\s+(?!\.)[a-z_]+\s+import", "absolute import from legacy dir"),  # May need context
]

# Directories that suggest "this IS the content" (risky to move)
CONTENT_DIR_PATTERNS = [
    "src", "lib", "scripts", "tests", "docs", "config", "data",
    "prompts", "templates", "examples", "assets", "resources",
    "models", "schemas", "migrations", "fixtures", "plugins"
]

class RepoScan(NamedTuple):
    repo_name: str
    repo_path: str
    has_remote_origin: bool
    current_branch: str
    default_branch_detected: str
    audit_status: str
    missing_required_files: str
    missing_00_run: bool
    non_compliant_dirs_count: int
    non_compliant_dirs_list: str
    import_risk_hits: int
    import_risk_examples: str
    lane: str
    rationale: str
    recommended_next_action: str


def run_git(repo_path: str, *args) -> tuple[int, str]:
    """Run git command and return (returncode, output)"""
    try:
        result = subprocess.run(
            ["git", "-C", repo_path] + list(args),
            capture_output=True, text=True, timeout=10
        )
        return result.returncode, result.stdout.strip()
    except Exception as e:
        return 1, str(e)


def get_remote_origin(repo_path: str) -> Optional[str]:
    """Get origin remote URL or None"""
    code, out = run_git(repo_path, "remote", "get-url", "origin")
    return out if code == 0 else None


def get_current_branch(repo_path: str) -> str:
    """Get current branch name"""
    code, out = run_git(repo_path, "branch", "--show-current")
    return out if code == 0 else "(detached)"


def get_default_branch(repo_path: str) -> str:
    """Detect default branch (origin/main, origin/master, or none)"""
    code, _ = run_git(repo_path, "show-ref", "--verify", "--quiet", "refs/remotes/origin/main")
    if code == 0:
        return "origin/main"
    code, _ = run_git(repo_path, "show-ref", "--verify", "--quiet", "refs/remotes/origin/master")
    if code == 0:
        return "origin/master"
    return "none"


def get_top_level_dirs(repo_path: str) -> set[str]:
    """Get top-level directories (excluding hidden)"""
    dirs = set()
    try:
        for item in os.listdir(repo_path):
            item_path = os.path.join(repo_path, item)
            if os.path.isdir(item_path) and not item.startswith("."):
                dirs.add(item)
    except Exception:
        pass
    return dirs


def find_non_compliant_dirs(repo_path: str) -> list[str]:
    """Find directories that don't match Betty Protocol"""
    top_dirs = get_top_level_dirs(repo_path)
    non_compliant = []
    for d in sorted(top_dirs):
        if d not in ALLOWED_DIRS:
            non_compliant.append(d)
    return non_compliant


def check_required_files(repo_path: str) -> list[str]:
    """Check for missing required files"""
    missing = []
    for f in REQUIRED_FILES:
        if not os.path.exists(os.path.join(repo_path, f)):
            missing.append(f)
    return missing


def check_00_run(repo_path: str) -> bool:
    """Check if 00_run directory is missing"""
    return not os.path.isdir(os.path.join(repo_path, "00_run"))


def scan_import_risks(repo_path: str) -> tuple[int, list[str]]:
    """Scan for import risk patterns in Python files"""
    hits = 0
    examples = []
    max_examples = 5

    for root, dirs, files in os.walk(repo_path):
        # Skip hidden dirs, venvs, node_modules
        dirs[:] = [d for d in dirs if not d.startswith(".") and d not in
                   {"venv", ".venv", "node_modules", "__pycache__", "env", ".env"}]

        for f in files:
            if f.endswith(".py"):
                fpath = os.path.join(root, f)
                try:
                    with open(fpath, "r", encoding="utf-8", errors="ignore") as fp:
                        content = fp.read()
                        for pattern, desc in IMPORT_RISK_PATTERNS:
                            matches = re.findall(pattern, content)
                            if matches:
                                hits += len(matches)
                                if len(examples) < max_examples:
                                    relpath = os.path.relpath(fpath, repo_path)
                                    examples.append(f"{relpath}: {desc}")
                except Exception:
                    pass

    return hits, examples


def has_content_dir_patterns(non_compliant: list[str]) -> bool:
    """Check if non-compliant dirs match content patterns (risky to move)"""
    for d in non_compliant:
        if d.lower() in CONTENT_DIR_PATTERNS:
            return True
    return False


def check_existing_exception_file(repo_path: str) -> bool:
    """Check if exception file already exists"""
    return os.path.exists(os.path.join(repo_path, "00_admin", "audit_exceptions.yaml"))


def check_existing_gitattributes(repo_path: str) -> bool:
    """Check if .gitattributes already exists"""
    return os.path.exists(os.path.join(repo_path, ".gitattributes"))


def classify_lane(
    has_remote: bool,
    non_compliant: list[str],
    import_risks: int,
    missing_files: list[str],
    has_exception_file: bool
) -> tuple[str, str, str]:
    """
    Classify repo into lane with rationale and recommended action.
    Returns: (lane, rationale, recommended_action)
    """

    # Local only - no remote
    if not has_remote:
        if len(non_compliant) == 0 and not missing_files:
            return (
                "local_only",
                "No remote; already compliant structure",
                "Add GitHub remote or mark for archive"
            )
        return (
            "local_only",
            f"No remote; {len(non_compliant)} non-compliant dirs",
            "Add GitHub remote first, then remediate"
        )

    # Already compliant
    if len(non_compliant) == 0 and not missing_files:
        if has_exception_file:
            return (
                "compliant",
                "Structure compliant; has exception file (may have legacy exceptions)",
                "Review exception file for stale entries"
            )
        return (
            "compliant",
            "Structure fully compliant",
            "Add .gitattributes if missing"
        )

    # Check if this is a "declare everything forever" mess
    if len(non_compliant) > 15:
        return (
            "manual_migration",
            f"Too many violations ({len(non_compliant)} dirs) for exception-only approach",
            "Schedule dedicated migration session"
        )

    # Check if non-compliant dirs are content dirs with import risks
    has_content_dirs = has_content_dir_patterns(non_compliant)

    # Quick win: content dirs that would be risky to move
    if has_content_dirs or import_risks > 0:
        return (
            "quick_win_exception",
            f"{len(non_compliant)} legacy dirs with {'import risks' if import_risks else 'content patterns'}; safe to declare",
            "Add exception file + .gitattributes + stubs"
        )

    # Few non-compliant dirs that aren't content patterns - could go either way
    if len(non_compliant) <= 5:
        return (
            "quick_win_exception",
            f"{len(non_compliant)} non-standard dirs; low complexity",
            "Add exception file + .gitattributes"
        )

    # Medium complexity - still quick win territory
    if len(non_compliant) <= 10:
        return (
            "quick_win_exception",
            f"{len(non_compliant)} legacy dirs; exception approach viable",
            "Add exception file + .gitattributes + document rationale"
        )

    # Fallback to manual migration for complex cases
    return (
        "manual_migration",
        f"{len(non_compliant)} dirs; structural review recommended",
        "Assess which dirs can be migrated vs declared"
    )


def scan_repo(repo_path: str) -> RepoScan:
    """Scan a single repo and return classification"""
    repo_name = os.path.basename(repo_path)

    # Git info
    remote = get_remote_origin(repo_path)
    has_remote = remote is not None
    current_branch = get_current_branch(repo_path)
    default_branch = get_default_branch(repo_path) if has_remote else "none"

    # Structure audit
    non_compliant = find_non_compliant_dirs(repo_path)
    missing_files = check_required_files(repo_path)
    missing_00_run = check_00_run(repo_path)

    # Import risk scan
    import_hits, import_examples = scan_import_risks(repo_path)

    # Existing remediation artifacts
    has_exception_file = check_existing_exception_file(repo_path)

    # Determine audit status
    audit_status = "compliant" if (len(non_compliant) == 0 and not missing_files) else "violations"

    # Classify lane
    lane, rationale, action = classify_lane(
        has_remote, non_compliant, import_hits, missing_files, has_exception_file
    )

    return RepoScan(
        repo_name=repo_name,
        repo_path=repo_path,
        has_remote_origin=has_remote,
        current_branch=current_branch,
        default_branch_detected=default_branch,
        audit_status=audit_status,
        missing_required_files="; ".join(missing_files) if missing_files else "",
        missing_00_run=missing_00_run,
        non_compliant_dirs_count=len(non_compliant),
        non_compliant_dirs_list="; ".join(non_compliant) if non_compliant else "",
        import_risk_hits=import_hits,
        import_risk_examples="; ".join(import_examples[:3]) if import_examples else "",
        lane=lane,
        rationale=rationale,
        recommended_next_action=action
    )


def main():
    base_path = "/Users/jeremybradford/SyncedProjects"
    output_dir = Path("/Users/jeremybradford/SyncedProjects/C010_standards/70_evidence/exports")
    receipt_dir = Path("/Users/jeremybradford/SyncedProjects/C010_standards/70_evidence/receipts")

    output_dir.mkdir(parents=True, exist_ok=True)
    receipt_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    date_str = datetime.now().strftime("%Y-%m-%d")

    csv_path = output_dir / f"p_series_lane_scan_{timestamp}.csv"
    latest_path = output_dir / "p_series_lane_scan_latest.csv"
    receipt_path = receipt_dir / f"p_series_lane_scan_{date_str}.md"

    # Get C010 git SHA
    code, sha = run_git(str(Path(base_path) / "C010_standards"), "rev-parse", "--short", "HEAD")
    c010_sha = sha if code == 0 else "unknown"

    # Find and scan P-series repos
    results = []
    for item in sorted(os.listdir(base_path)):
        if item.startswith("P") and item[1:4].isdigit():
            repo_path = os.path.join(base_path, item)
            if os.path.isdir(os.path.join(repo_path, ".git")):
                print(f"Scanning {item}...")
                scan = scan_repo(repo_path)
                results.append(scan)

    # Write CSV
    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "repo_name", "repo_path", "has_remote_origin", "current_branch",
            "default_branch_detected", "audit_status", "missing_required_files",
            "missing_00_run", "non_compliant_dirs_count", "non_compliant_dirs_list",
            "import_risk_hits", "import_risk_examples", "lane", "rationale",
            "recommended_next_action"
        ])
        for r in results:
            writer.writerow([
                r.repo_name, r.repo_path, r.has_remote_origin, r.current_branch,
                r.default_branch_detected, r.audit_status, r.missing_required_files,
                r.missing_00_run, r.non_compliant_dirs_count, r.non_compliant_dirs_list,
                r.import_risk_hits, r.import_risk_examples, r.lane, r.rationale,
                r.recommended_next_action
            ])

    # Copy to latest
    import shutil
    shutil.copy(csv_path, latest_path)

    # Calculate stats
    lane_counts = {"compliant": 0, "quick_win_exception": 0, "manual_migration": 0, "local_only": 0}
    for r in results:
        lane_counts[r.lane] += 1

    # Top 10 highest risk (by non_compliant + import_risk)
    risk_sorted = sorted(results, key=lambda r: r.non_compliant_dirs_count + r.import_risk_hits, reverse=True)[:10]

    # Quick wins sorted by size (smallest first)
    quick_wins = [r for r in results if r.lane == "quick_win_exception"]
    quick_wins_sorted = sorted(quick_wins, key=lambda r: r.non_compliant_dirs_count)

    # Archive candidates (local_only with high violation count or no activity)
    archive_candidates = [r for r in results if r.lane == "local_only" and r.non_compliant_dirs_count > 5]

    # Generate receipt
    receipt_content = f"""# P-series Lane Scan Receipt
## Date: {date_str}

### Scan Metadata
- **Timestamp**: {timestamp}
- **C010_standards SHA**: {c010_sha}
- **Scanner Version**: 1.0.0
- **Script**: `70_evidence/scripts/p_series_lane_scanner.py`

### Summary

| Lane | Count |
|------|-------|
| compliant | {lane_counts['compliant']} |
| quick_win_exception | {lane_counts['quick_win_exception']} |
| manual_migration | {lane_counts['manual_migration']} |
| local_only | {lane_counts['local_only']} |
| **Total** | **{len(results)}** |

### Output Files
- CSV: `70_evidence/exports/p_series_lane_scan_{timestamp}.csv`
- Latest: `70_evidence/exports/p_series_lane_scan_latest.csv`

### Top 10 Highest Risk Repos
(by non_compliant_dirs + import_risk_hits)

| Repo | Non-Compliant Dirs | Import Risks | Lane |
|------|-------------------|--------------|------|
"""
    for r in risk_sorted:
        receipt_content += f"| {r.repo_name} | {r.non_compliant_dirs_count} | {r.import_risk_hits} | {r.lane} |\n"

    receipt_content += f"""
### Recommended Quick Win Run Order
(smallest non_compliant_dirs_count first)

"""
    for i, r in enumerate(quick_wins_sorted[:15], 1):
        receipt_content += f"{i}. **{r.repo_name}** ({r.non_compliant_dirs_count} dirs): {r.rationale}\n"

    if archive_candidates:
        receipt_content += f"""
### Archive Candidates
(local_only with >5 violations - consider archiving)

"""
        for r in archive_candidates:
            receipt_content += f"- **{r.repo_name}**: {r.non_compliant_dirs_count} non-compliant dirs, no remote\n"

    receipt_content += f"""
### Lane Definitions
- **compliant**: No non-compliant dirs, required files present
- **quick_win_exception**: Can be remediated with exception file + .gitattributes only (no moves)
- **manual_migration**: Requires structural changes or dedicated session
- **local_only**: No GitHub remote - needs remote added or archive decision

### Session Attribution
Generated by Claude Code session on {date_str}
"""

    with open(receipt_path, "w") as f:
        f.write(receipt_content)

    # Print summary
    print("\n" + "=" * 60)
    print("P-SERIES LANE SCAN COMPLETE")
    print("=" * 60)
    print(f"\nLane Counts:")
    for lane, count in lane_counts.items():
        print(f"  {lane}: {count}")
    print(f"\nTotal repos scanned: {len(results)}")
    print(f"\nOutputs:")
    print(f"  CSV: {csv_path}")
    print(f"  Latest: {latest_path}")
    print(f"  Receipt: {receipt_path}")

    return lane_counts, csv_path, receipt_path


if __name__ == "__main__":
    main()
