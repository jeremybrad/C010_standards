#!/usr/bin/env python3
"""
workspace_triage.py - Generate remediation triage CSV for SyncedProjects repos.

Scans all repos under SyncedProjects and produces a CSV categorizing each repo
into: safe_autofix, needs_exception, or manual_migration.

Usage:
    python3 scripts/workspace_triage.py [workspace_path]

Outputs:
    - CSV: 10_docs/notes/workspace_triage/workspace_triage_<timestamp>.csv
    - Receipt: 20_receipts/workspace_triage/workspace_triage_<timestamp>.md
"""

import csv
import hashlib
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional


# Configuration
ALLOWED_DIRS = {
    "00_admin", "00_run", "10_docs", "20_receipts", "20_approvals", "20_inbox",
    "30_config", "40_src", "50_data", "70_evidence", "80_evidence_packages", "90_archive"
}

DEFAULT_REQUIRED_FILES = {"README.md", "rules_now.md", "RELATIONS.yaml"}

# Import risk patterns (sibling-dir coupling)
IMPORT_RISK_PATTERNS = [
    r"from scripts\b",
    r"import scripts\b",
    r"from validators\b",
    r"import validators\b",
    r"from tests\b",
    r"import tests\b",
    r"sys\.path\.(append|insert)",
    r"PYTHONPATH",
]


def is_git_repo(path: Path) -> bool:
    """Check if path is a git repository."""
    return (path / ".git").exists() or (path / ".git").is_file()


def get_repo_series(name: str) -> str:
    """Extract series (C/P/W/U) from repo name."""
    if re.match(r"^C\d", name):
        return "C"
    elif re.match(r"^P\d", name):
        return "P"
    elif re.match(r"^W\d", name):
        return "W"
    elif re.match(r"^U\d", name):
        return "U"
    return "-"


def get_invalid_dirs(repo_path: Path) -> list[str]:
    """Get list of non-compliant top-level directories."""
    invalid = []
    try:
        for item in repo_path.iterdir():
            if item.is_dir() and not item.name.startswith("."):
                if item.name not in ALLOWED_DIRS:
                    invalid.append(item.name)
    except PermissionError:
        pass
    return sorted(invalid)


def get_missing_files(repo_path: Path, series: str) -> list[str]:
    """Get list of missing required files."""
    missing = []
    for f in DEFAULT_REQUIRED_FILES:
        if not (repo_path / f).exists():
            missing.append(f)

    # Check 00_run for C/W series
    if series in ("C", "W") and not (repo_path / "00_run").is_dir():
        missing.append("00_run/")

    return sorted(missing)


def has_python(repo_path: Path) -> bool:
    """Check if repo has Python files or config."""
    python_markers = ["pyproject.toml", "setup.py", "setup.cfg", "requirements.txt"]
    for marker in python_markers:
        if (repo_path / marker).exists():
            return True

    # Check for .py files (limit search depth for performance)
    try:
        result = subprocess.run(
            ["find", str(repo_path), "-maxdepth", "4", "-name", "*.py", "-type", "f"],
            capture_output=True, text=True, timeout=10
        )
        return bool(result.stdout.strip())
    except (subprocess.TimeoutExpired, Exception):
        return False


def get_import_risk_hits(repo_path: Path) -> tuple[int, list[str]]:
    """Search for sibling-dir import patterns that indicate coupling."""
    hits = []
    pattern = "|".join(IMPORT_RISK_PATTERNS)

    try:
        # Try ripgrep first (faster) - short timeout, limited depth
        result = subprocess.run(
            ["rg", "-n", "--no-heading", "-e", pattern, str(repo_path),
             "--type", "py", "--max-count", "10", "--max-depth", "4"],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0 and result.stdout:
            lines = result.stdout.strip().split("\n")
            for line in lines[:5]:  # Limit examples
                # Shorten path for readability
                short = line.replace(str(repo_path) + "/", "")
                if len(short) > 80:
                    short = short[:77] + "..."
                hits.append(short)
    except (FileNotFoundError, subprocess.TimeoutExpired):
        # Fallback: simple check for known risk patterns in top-level dirs
        try:
            for risk_dir in ["validators", "scripts", "tests"]:
                init_file = repo_path / risk_dir / "__init__.py"
                if init_file.exists():
                    hits.append(f"{risk_dir}/__init__.py exists (likely package)")
                    break
        except Exception:
            pass
    except Exception:
        pass

    return len(hits), hits[:5]


def has_gitmodules(repo_path: Path) -> bool:
    """Check if repo has .gitmodules file."""
    return (repo_path / ".gitmodules").exists()


def count_submodule_references(repo_name: str, workspace: Path) -> int:
    """Count how many OTHER repos reference this repo in .gitmodules."""
    count = 0
    try:
        # Only search .gitmodules files directly (faster than grep -r)
        for item in workspace.iterdir():
            if item.is_dir() and item.name != repo_name:
                gitmodules = item / ".gitmodules"
                if gitmodules.exists():
                    try:
                        content = gitmodules.read_text()
                        if repo_name in content:
                            count += 1
                    except Exception:
                        pass
    except Exception:
        pass
    return count


def get_noncompliant_stats(repo_path: Path, invalid_dirs: list[str]) -> tuple[int, float]:
    """Get file count and size (MB) under non-compliant directories."""
    total_files = 0
    total_bytes = 0

    for dirname in invalid_dirs:
        dirpath = repo_path / dirname
        if dirpath.is_dir():
            try:
                result = subprocess.run(
                    ["find", str(dirpath), "-type", "f"],
                    capture_output=True, text=True, timeout=30
                )
                if result.returncode == 0:
                    files = [f for f in result.stdout.strip().split("\n") if f]
                    total_files += len(files)

                result = subprocess.run(
                    ["du", "-sb", str(dirpath)],
                    capture_output=True, text=True, timeout=30
                )
                if result.returncode == 0 and result.stdout:
                    parts = result.stdout.strip().split()
                    if parts:
                        total_bytes += int(parts[0])
            except Exception:
                pass

    size_mb = round(total_bytes / (1024 * 1024), 2)
    return total_files, size_mb


def determine_route(
    invalid_dirs: list[str],
    missing_files: list[str],
    has_py: bool,
    import_hits: int,
    submodule_refs: int,
    repo_name: str
) -> tuple[str, str]:
    """Determine recommended remediation route and justification."""

    # No violations at all
    if not invalid_dirs and not missing_files:
        return "compliant", "No violations detected"

    # Safe autofix: only missing files, no invalid dirs
    if not invalid_dirs and missing_files:
        return "safe_autofix", f"Only missing: {', '.join(missing_files)}"

    # Needs exception: Python with import coupling
    if has_py and import_hits > 0:
        return "needs_exception", f"Python repo with {import_hits} sibling-dir import patterns"

    # Needs exception: Referenced as submodule by other repos
    if submodule_refs > 0:
        return "needs_exception", f"Referenced as submodule by {submodule_refs} other repo(s)"

    # Needs exception: Known "content is deliverable" repos
    content_repos = {
        "C010_standards",  # Standards definitions
        "C003_sadb_canonical",  # Canonical SADB pipeline
    }
    if repo_name in content_repos:
        return "needs_exception", "Canonical content repository"

    # Check for core deliverable patterns in invalid dirs
    deliverable_dirs = {"schemas", "taxonomies", "protocols", "templates"}
    if deliverable_dirs & set(invalid_dirs):
        if has_py:
            return "needs_exception", f"Has core deliverable dirs: {deliverable_dirs & set(invalid_dirs)}"

    # Default: manual migration
    return "manual_migration", f"Invalid dirs: {', '.join(invalid_dirs[:5])}"


def scan_workspace(workspace: Path) -> list[dict]:
    """Scan workspace and collect triage data for all repos."""
    results = []

    for item in sorted(workspace.iterdir()):
        # Skip meta-folders (underscore prefix)
        if item.name.startswith("_"):
            continue

        # Skip non-directories
        if not item.is_dir():
            continue

        # Must be a git repo or have project markers
        if not is_git_repo(item) and not (item / "README.md").exists():
            continue

        repo_name = item.name
        series = get_repo_series(repo_name)

        try:
            invalid_dirs = get_invalid_dirs(item)
            missing_files = get_missing_files(item, series)
            has_py = has_python(item)
            import_hits, import_examples = get_import_risk_hits(item)
            has_submodules = has_gitmodules(item)
            submodule_refs = count_submodule_references(repo_name, workspace)

            if invalid_dirs:
                file_count, size_mb = get_noncompliant_stats(item, invalid_dirs)
            else:
                file_count, size_mb = 0, 0.0

            # Determine compliance
            compliant = not invalid_dirs and not missing_files
            violations = len(invalid_dirs) + len(missing_files)

            # Determine route
            route, notes = determine_route(
                invalid_dirs, missing_files, has_py, import_hits,
                submodule_refs, repo_name
            )

            results.append({
                "repo_name": repo_name,
                "repo_path": str(item),
                "series": series,
                "audit_compliant": str(compliant).lower(),
                "violations_count": violations,
                "invalid_top_level_dirs": ";".join(invalid_dirs),
                "missing_required_files": ";".join(missing_files),
                "has_python": str(has_py).lower(),
                "python_import_risk_hits": import_hits,
                "import_risk_examples": " | ".join(import_examples),
                "has_gitmodules": str(has_submodules).lower(),
                "referenced_as_submodule": submodule_refs,
                "noncompliant_file_count": file_count,
                "noncompliant_size_mb": size_mb,
                "recommended_route": route,
                "notes": notes,
            })
        except Exception as e:
            results.append({
                "repo_name": repo_name,
                "repo_path": str(item),
                "series": series,
                "audit_compliant": "error",
                "violations_count": -1,
                "invalid_top_level_dirs": "",
                "missing_required_files": "",
                "has_python": "unknown",
                "python_import_risk_hits": 0,
                "import_risk_examples": "",
                "has_gitmodules": "unknown",
                "referenced_as_submodule": 0,
                "noncompliant_file_count": 0,
                "noncompliant_size_mb": 0.0,
                "recommended_route": "manual_migration",
                "notes": f"Error scanning: {str(e)[:50]}",
            })

    return results


def write_csv(results: list[dict], output_path: Path) -> str:
    """Write results to CSV and return SHA256 hash."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "repo_name", "repo_path", "series", "audit_compliant", "violations_count",
        "invalid_top_level_dirs", "missing_required_files", "has_python",
        "python_import_risk_hits", "import_risk_examples", "has_gitmodules",
        "referenced_as_submodule", "noncompliant_file_count", "noncompliant_size_mb",
        "recommended_route", "notes"
    ]

    with open(output_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    # Calculate SHA256
    with open(output_path, "rb") as f:
        sha256 = hashlib.sha256(f.read()).hexdigest()

    return sha256


def write_receipt(
    results: list[dict],
    csv_path: Path,
    csv_sha256: str,
    receipt_path: Path,
    workspace: Path,
    timestamp: str
) -> None:
    """Write receipt markdown."""
    receipt_path.parent.mkdir(parents=True, exist_ok=True)

    # Count by route
    route_counts = {}
    for r in results:
        route = r["recommended_route"]
        route_counts[route] = route_counts.get(route, 0) + 1

    # Top 10 by size
    top_by_size = sorted(
        [r for r in results if r["noncompliant_size_mb"] > 0],
        key=lambda x: x["noncompliant_size_mb"],
        reverse=True
    )[:10]

    # Count by series
    series_counts = {}
    for r in results:
        s = r["series"]
        series_counts[s] = series_counts.get(s, 0) + 1

    receipt = f"""# Workspace Triage Receipt

**Timestamp:** {timestamp}
**Workspace:** {workspace}
**Python version:** {sys.version.split()[0]}
**Script:** scripts/workspace_triage.py

## Command

```bash
python3 scripts/workspace_triage.py {workspace}
```

## Output Files

| File | Path | SHA256 |
|------|------|--------|
| CSV | `{csv_path.relative_to(csv_path.parent.parent.parent.parent)}` | `{csv_sha256[:16]}...` |
| Receipt | `{receipt_path.relative_to(receipt_path.parent.parent.parent.parent)}` | (this file) |

## Summary

| Metric | Value |
|--------|-------|
| Repos scanned | {len(results)} |
| Compliant | {route_counts.get('compliant', 0)} |
| Safe autofix | {route_counts.get('safe_autofix', 0)} |
| Needs exception | {route_counts.get('needs_exception', 0)} |
| Manual migration | {route_counts.get('manual_migration', 0)} |

## By Series

| Series | Count |
|--------|-------|
| C (Core) | {series_counts.get('C', 0)} |
| P (Projects) | {series_counts.get('P', 0)} |
| W (Work) | {series_counts.get('W', 0)} |
| U (Utility) | {series_counts.get('U', 0)} |
| Other | {series_counts.get('-', 0)} |

## Recommended Route Breakdown

| Route | Count | Description |
|-------|-------|-------------|
| compliant | {route_counts.get('compliant', 0)} | Already compliant, no action needed |
| safe_autofix | {route_counts.get('safe_autofix', 0)} | Only missing files, can use --autofix-safe |
| needs_exception | {route_counts.get('needs_exception', 0)} | Has Python imports or submodule refs, needs exception file |
| manual_migration | {route_counts.get('manual_migration', 0)} | Invalid dirs need manual moves |

## Top 10 Repos by Non-Compliant Size

| Rank | Repo | Size (MB) | File Count | Route |
|------|------|-----------|------------|-------|
"""

    for i, r in enumerate(top_by_size, 1):
        receipt += f"| {i} | {r['repo_name']} | {r['noncompliant_size_mb']} | {r['noncompliant_file_count']} | {r['recommended_route']} |\n"

    if not top_by_size:
        receipt += "| - | (none with non-compliant content) | - | - | - |\n"

    receipt += f"""
## Repos Needing Exception (Detail)

"""
    exception_repos = [r for r in results if r["recommended_route"] == "needs_exception"]
    if exception_repos:
        for r in exception_repos:
            receipt += f"### {r['repo_name']}\n"
            receipt += f"- **Reason:** {r['notes']}\n"
            receipt += f"- **Invalid dirs:** {r['invalid_top_level_dirs'] or '(none)'}\n"
            receipt += f"- **Import risk hits:** {r['python_import_risk_hits']}\n"
            if r['import_risk_examples']:
                receipt += f"- **Examples:** `{r['import_risk_examples'][:100]}`\n"
            receipt += "\n"
    else:
        receipt += "(No repos flagged for exception)\n"

    receipt += f"""
---
*Generated by workspace_triage.py at {timestamp}*
"""

    with open(receipt_path, "w") as f:
        f.write(receipt)


def main():
    # Parse args
    if len(sys.argv) > 1:
        workspace = Path(sys.argv[1])
    else:
        workspace = Path.home() / "SyncedProjects"

    if not workspace.is_dir():
        print(f"ERROR: Workspace not found: {workspace}")
        sys.exit(1)

    # Get script location to determine C010 root
    script_dir = Path(__file__).parent
    c010_root = script_dir.parent

    # Timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    date_stamp = datetime.now().strftime("%Y%m%d")

    # Output paths
    csv_path = c010_root / "10_docs" / "notes" / "workspace_triage" / f"workspace_triage_{date_stamp}.csv"
    receipt_path = c010_root / "20_receipts" / "workspace_triage" / f"workspace_triage_{date_stamp}.md"

    print(f"Workspace Triage Generator")
    print(f"==========================")
    print(f"Workspace: {workspace}")
    print(f"Timestamp: {timestamp}")
    print()

    # Scan
    print("Scanning repos...")
    results = scan_workspace(workspace)
    print(f"Scanned {len(results)} repos")
    print()

    # Write CSV
    print(f"Writing CSV: {csv_path}")
    csv_sha256 = write_csv(results, csv_path)
    print(f"SHA256: {csv_sha256[:16]}...")
    print()

    # Write receipt
    print(f"Writing receipt: {receipt_path}")
    write_receipt(results, csv_path, csv_sha256, receipt_path, workspace, timestamp)
    print()

    # Summary
    route_counts = {}
    for r in results:
        route = r["recommended_route"]
        route_counts[route] = route_counts.get(route, 0) + 1

    print("Summary by Route:")
    print(f"  compliant:        {route_counts.get('compliant', 0)}")
    print(f"  safe_autofix:     {route_counts.get('safe_autofix', 0)}")
    print(f"  needs_exception:  {route_counts.get('needs_exception', 0)}")
    print(f"  manual_migration: {route_counts.get('manual_migration', 0)}")
    print()
    print("Done!")


if __name__ == "__main__":
    main()
