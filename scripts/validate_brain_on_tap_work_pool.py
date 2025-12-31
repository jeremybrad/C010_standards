#!/usr/bin/env python3
"""Validate work pool repos for Brain on Tap (BBOT) Work Pool v1.

Work pool repos require stricter requirements beyond basic BBOT eligibility:
1. README repo card present (BOT:repo_card markers)
2. DATA_SOURCES.md present with sensitivity classification
3. 20_receipts/ directory exists
4. 80_evidence_packages/ directory exists
5. Verify entry point exists (make verify, 00_run/verify.command, scripts/verify_claims.py)
6. Export hygiene (.gitignore patterns, no tracked exports)

Usage:
    python scripts/validate_brain_on_tap_work_pool.py
    python scripts/validate_brain_on_tap_work_pool.py --repo W005_BigQuery
    python scripts/validate_brain_on_tap_work_pool.py --verbose

Exit codes:
    0 - All repos pass
    1 - Validation errors
    2 - Configuration/file error

Requirements:
    PyYAML (pip install pyyaml)
"""
from __future__ import annotations

import argparse
import csv
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML required. Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(2)


# README repo card markers
START_MARKER = "<!-- BOT:repo_card:start -->"
END_MARKER = "<!-- BOT:repo_card:end -->"

# Export patterns that should be in .gitignore
EXPORT_PATTERNS = ["*.csv", "*.xlsx", "*.parquet", "exports/", "data/"]

# Allowed cross-pool dependencies
ALLOWED_CROSS_POOL = ["C010_standards", "C001_mission-control", "C017_brain-on-tap"]


def find_repo_root(start: Path) -> Path | None:
    """Find C010_standards repo root by looking for registry/repos.yaml."""
    current = start.resolve()
    for _ in range(10):
        if (current / "registry" / "repos.yaml").exists():
            return current
        if current.parent == current:
            break
        current = current.parent
    return None


def load_registry(registry_path: Path) -> dict | None:
    """Load and parse registry/repos.yaml."""
    try:
        data = yaml.safe_load(registry_path.read_text())
        if isinstance(data, dict) and "repos" in data:
            return data
    except yaml.YAMLError as e:
        print(f"ERROR: YAML parse error: {e}", file=sys.stderr)
    return None


def get_work_pool_repos(registry_data: dict) -> list[dict]:
    """Get all repos with pool=work and bot_active=true."""
    repos = registry_data.get("repos", [])
    work_repos = []
    for r in repos:
        pool = r.get("pool", "personal")
        bot_active = r.get("bot_active", False)
        if pool == "work" and bot_active is True:
            work_repos.append(r)
    return work_repos


def check_readme_repo_card(repo_path: Path, verbose: bool = False) -> list[str]:
    """Check for README repo card markers.

    Returns list of error messages (empty = pass).
    """
    errors = []
    readme_path = repo_path / "README.md"

    if not readme_path.exists():
        errors.append("README.md not found")
        return errors

    readme_text = readme_path.read_text(encoding="utf-8")

    if START_MARKER not in readme_text:
        errors.append(f"Missing start marker: {START_MARKER}")
    elif END_MARKER not in readme_text:
        errors.append(f"Missing end marker: {END_MARKER}")
    elif verbose:
        print(f"  README: repo card markers present")

    return errors


def check_data_sources(repo_path: Path, verbose: bool = False) -> tuple[list[str], list[str]]:
    """Check for DATA_SOURCES.md with sensitivity classification.

    Returns (errors, warnings).
    """
    errors = []
    warnings = []
    data_sources_path = repo_path / "DATA_SOURCES.md"

    if not data_sources_path.exists():
        errors.append("DATA_SOURCES.md not found")
        return errors, warnings

    if verbose:
        print(f"  DATA_SOURCES.md: found")

    content = data_sources_path.read_text(encoding="utf-8")

    # Check for sensitivity classification section
    sensitivity_patterns = [
        r"sensitivity",
        r"PUBLIC",
        r"INTERNAL",
        r"CONFIDENTIAL",
        r"RESTRICTED",
    ]
    has_sensitivity = any(re.search(p, content, re.IGNORECASE) for p in sensitivity_patterns)

    if not has_sensitivity:
        warnings.append("DATA_SOURCES.md lacks sensitivity classification")
    elif verbose:
        print(f"  DATA_SOURCES.md: sensitivity classification present")

    return errors, warnings


def check_receipts_dir(repo_path: Path, verbose: bool = False) -> list[str]:
    """Check for 20_receipts/ directory."""
    errors = []
    receipts_path = repo_path / "20_receipts"

    if not receipts_path.is_dir():
        errors.append("20_receipts/ directory not found")
    elif verbose:
        print(f"  20_receipts/: found")

    return errors


def check_evidence_packages(repo_path: Path, verbose: bool = False) -> list[str]:
    """Check for 80_evidence_packages/ directory."""
    errors = []
    evidence_path = repo_path / "80_evidence_packages"

    if not evidence_path.is_dir():
        errors.append("80_evidence_packages/ directory not found")
    elif verbose:
        print(f"  80_evidence_packages/: found")

    return errors


def check_verify_entry_point(repo_path: Path, verbose: bool = False) -> list[str]:
    """Check for verify entry point.

    Valid entry points:
    - Makefile with 'verify' target
    - 00_run/verify.command or 00_run/verify.sh
    - scripts/verify_claims.py
    """
    errors = []
    found = False

    # Check Makefile for verify target
    makefile_path = repo_path / "Makefile"
    if makefile_path.exists():
        makefile_text = makefile_path.read_text(encoding="utf-8")
        if re.search(r"^verify\s*:", makefile_text, re.MULTILINE):
            found = True
            if verbose:
                print(f"  Verify: Makefile target 'verify' found")

    # Check 00_run/verify.*
    if not found:
        for variant in ["verify.command", "verify.sh"]:
            verify_run = repo_path / "00_run" / variant
            if verify_run.exists():
                found = True
                if verbose:
                    print(f"  Verify: 00_run/{variant} found")
                break

    # Check scripts/verify_claims.py
    if not found:
        verify_script = repo_path / "scripts" / "verify_claims.py"
        if verify_script.exists():
            found = True
            if verbose:
                print(f"  Verify: scripts/verify_claims.py found")

    if not found:
        errors.append("No verify entry point (make verify, 00_run/verify.*, scripts/verify_claims.py)")

    return errors


def check_export_hygiene(repo_path: Path, verbose: bool = False) -> list[str]:
    """Check export hygiene: .gitignore patterns and no tracked exports."""
    errors = []

    gitignore_path = repo_path / ".gitignore"
    if not gitignore_path.exists():
        errors.append(".gitignore not found")
        return errors

    gitignore_text = gitignore_path.read_text(encoding="utf-8")

    # Check for export patterns
    missing_patterns = []
    for pattern in EXPORT_PATTERNS:
        if pattern not in gitignore_text:
            missing_patterns.append(pattern)

    if missing_patterns:
        errors.append(f".gitignore missing patterns: {', '.join(missing_patterns)}")
    elif verbose:
        print(f"  Export hygiene: .gitignore patterns present")

    # Check for tracked exports (git ls-files)
    # Excludes: 20_receipts/, 80_evidence_packages/ (evidence files are allowed)
    try:
        result = subprocess.run(
            ["git", "ls-files"],
            cwd=repo_path,
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0:
            tracked_files = result.stdout.strip().split("\n")
            export_tracked = []
            excluded_prefixes = ("20_receipts/", "80_evidence_packages/")
            for f in tracked_files:
                # Skip evidence directories (receipts and evidence packages)
                if any(f.startswith(prefix) for prefix in excluded_prefixes):
                    continue
                if f.endswith((".csv", ".xlsx", ".parquet")) and not f.endswith(".gitkeep"):
                    export_tracked.append(f)

            if export_tracked:
                errors.append(f"Tracked export files: {', '.join(export_tracked[:5])}")
            elif verbose:
                print(f"  Export hygiene: no tracked exports (outside evidence dirs)")
    except (subprocess.TimeoutExpired, FileNotFoundError):
        if verbose:
            print(f"  Export hygiene: git ls-files skipped (not a git repo or git not found)")

    return errors


def validate_work_pool_repo(
    entry: dict,
    workspace: Path,
    verbose: bool = False
) -> tuple[list[str], list[str]]:
    """Full work pool validation for a repo.

    Returns (errors, warnings).
    """
    all_errors = []
    all_warnings = []

    repo_id = entry.get("repo_id", "unknown")
    path_rel = entry.get("path_rel", repo_id)
    repo_path = workspace / path_rel

    if verbose:
        print(f"\nValidating {repo_id} (work pool)...")

    if not repo_path.is_dir():
        all_errors.append(f"Repo directory not found: {repo_path}")
        return all_errors, all_warnings

    # 1. Check README repo card
    errors = check_readme_repo_card(repo_path, verbose)
    all_errors.extend(errors)

    # 2. Check DATA_SOURCES.md
    errors, warnings = check_data_sources(repo_path, verbose)
    all_errors.extend(errors)
    all_warnings.extend(warnings)

    # 3. Check 20_receipts/
    errors = check_receipts_dir(repo_path, verbose)
    all_errors.extend(errors)

    # 4. Check 80_evidence_packages/
    errors = check_evidence_packages(repo_path, verbose)
    all_errors.extend(errors)

    # 5. Check verify entry point
    errors = check_verify_entry_point(repo_path, verbose)
    all_errors.extend(errors)

    # 6. Check export hygiene
    errors = check_export_hygiene(repo_path, verbose)
    all_errors.extend(errors)

    return all_errors, all_warnings


def write_reports(
    results: dict[str, tuple[list[str], list[str]]],
    output_dir: Path
) -> None:
    """Write markdown and CSV reports."""
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Count results
    pass_count = sum(1 for errors, _ in results.values() if not errors)
    fail_count = len(results) - pass_count

    # Markdown report
    md_path = output_dir / "Brain_on_Tap_Work_Pool.md"
    md_lines = [
        "# Brain on Tap Work Pool Report",
        "",
        f"**Generated**: {timestamp}",
        f"**Registry**: `repos.yaml`",
        "",
        "## Summary",
        "",
        "| Status | Count |",
        "|--------|-------|",
        f"| PASS (eligible) | {pass_count} |",
        f"| FAIL (not eligible) | {fail_count} |",
        f"| **Total** | **{len(results)}** |",
        "",
    ]

    if pass_count > 0:
        md_lines.extend([
            "## Eligible Repos",
            "",
            "| Repo ID | Path |",
            "|---------|------|",
        ])
        for repo_id, (errors, _) in sorted(results.items()):
            if not errors:
                md_lines.append(f"| `{repo_id}` | `{repo_id}` |")
        md_lines.append("")

    if fail_count > 0:
        md_lines.extend([
            "## Failed Repos",
            "",
        ])
        for repo_id, (errors, warnings) in sorted(results.items()):
            if errors:
                md_lines.append(f"### {repo_id}")
                md_lines.append("")
                md_lines.append("**Errors:**")
                for err in errors:
                    md_lines.append(f"- {err}")
                if warnings:
                    md_lines.append("")
                    md_lines.append("**Warnings:**")
                    for warn in warnings:
                        md_lines.append(f"- {warn}")
                md_lines.append("")

    md_path.write_text("\n".join(md_lines), encoding="utf-8")

    # CSV report
    csv_path = output_dir / "Brain_on_Tap_Work_Pool.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["repo_id", "pool", "bot_active", "pass", "fail_reasons"])
        for repo_id, (errors, _) in sorted(results.items()):
            status = "PASS" if not errors else "FAIL"
            fail_reasons = "; ".join(errors) if errors else ""
            writer.writerow([repo_id, "work", "true", status, fail_reasons])


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate work pool repos for Brain on Tap Work Pool v1"
    )
    parser.add_argument(
        "--repo",
        help="Validate specific repo ID (default: all work pool repos)"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Print detailed output"
    )
    parser.add_argument(
        "--registry",
        type=Path,
        help="Path to repos.yaml (default: auto-detect)"
    )
    parser.add_argument(
        "--workspace",
        type=Path,
        help="Path to SyncedProjects workspace (default: auto-detect)"
    )

    args = parser.parse_args(argv)

    # Find C010 repo root
    script_path = Path(__file__).resolve()
    c010_root = find_repo_root(script_path)

    if c010_root is None:
        print("ERROR: Could not find C010_standards repo root", file=sys.stderr)
        return 2

    # Load registry
    registry_path = args.registry or (c010_root / "registry" / "repos.yaml")
    if not registry_path.exists():
        print(f"ERROR: Registry not found: {registry_path}", file=sys.stderr)
        return 2

    registry_data = load_registry(registry_path)
    if registry_data is None:
        return 2

    if args.verbose:
        print(f"Using registry: {registry_path}")
        print(f"C010 root: {c010_root}")

    # Determine workspace root (SyncedProjects)
    workspace = args.workspace or c010_root.parent
    if args.verbose:
        print(f"Workspace: {workspace}")

    # Get work pool repos
    work_repos = get_work_pool_repos(registry_data)

    if args.repo:
        # Filter to specific repo
        work_repos = [r for r in work_repos if r.get("repo_id") == args.repo]
        if not work_repos:
            print(f"ERROR: '{args.repo}' not found in work pool", file=sys.stderr)
            return 2

    if not work_repos:
        print("No work pool repos found (pool=work AND bot_active=true)")
        return 0

    if args.verbose:
        print(f"Found {len(work_repos)} work pool repos")

    # Validate each repo
    results: dict[str, tuple[list[str], list[str]]] = {}
    for entry in work_repos:
        repo_id = entry.get("repo_id", "unknown")
        errors, warnings = validate_work_pool_repo(entry, workspace, args.verbose)
        results[repo_id] = (errors, warnings)

    # Write reports
    output_dir = c010_root / "70_evidence" / "exports"
    write_reports(results, output_dir)

    if args.verbose:
        print(f"\nReports written to: {output_dir}")

    # Print summary
    print("\n" + "=" * 60)
    print("BRAIN ON TAP WORK POOL REPORT")
    print("=" * 60)

    any_failures = False
    for repo_id, (errors, warnings) in sorted(results.items()):
        if errors:
            any_failures = True
            print(f"\n{repo_id}: FAIL ({len(errors)} errors)")
            for err in errors:
                print(f"  ERROR: {err}")
        else:
            status = "PASS" if not warnings else "PASS (with warnings)"
            print(f"\n{repo_id}: {status}")

        if warnings:
            for warn in warnings:
                print(f"  WARNING: {warn}")

    print("\n" + "-" * 60)
    pass_count = sum(1 for errors, _ in results.values() if not errors)
    fail_count = len(results) - pass_count

    if any_failures:
        print(f"Result: {fail_count}/{len(results)} repos FAILED work pool eligibility")
        return 1
    else:
        print(f"Result: {pass_count}/{len(results)} repos ELIGIBLE for work pool")
        return 0


if __name__ == "__main__":
    sys.exit(main())
