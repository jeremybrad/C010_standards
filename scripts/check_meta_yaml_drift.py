#!/usr/bin/env python3
"""
META.yaml drift detection for nightly health checks.

Checks:
1. Folders in META.yaml vs actual directories
2. last_reviewed age (warns if > 30 days)
3. Key files (Makefile, README.md) missing from META.yaml

Usage:
    python3 check_meta_yaml_drift.py [--fix] [--series C|P|W] [project_path]

Options:
    --series C|P|W  Filter to specific series (Core, Projects, Work)
    --fix           (reserved for future auto-fix functionality)

Exit codes:
    0 = No drift detected
    1 = Drift detected (details printed)

Migrated from: ~/SyncedProjects/_scripts/check_meta_yaml_drift.py
"""

import yaml
import os
import sys
from pathlib import Path
from datetime import datetime, timedelta

WORKSPACE = Path.home() / "SyncedProjects"
KEY_FILES = ["Makefile", "README.md", "CLAUDE.md", "package.json", "pyproject.toml", "requirements.txt"]
IGNORE_DIRS = {"node_modules", ".git", "__pycache__", "venv", ".venv", "*-env", "dist", "build"}
MAX_REVIEW_AGE_DAYS = 30


def load_meta_yaml(project_path: Path) -> dict | None:
    meta_path = project_path / "META.yaml"
    if not meta_path.exists():
        return None
    with open(meta_path) as f:
        return yaml.safe_load(f)


def get_actual_folders(project_path: Path) -> set:
    """Get top-level directories, excluding common ignores."""
    folders = set()
    for item in project_path.iterdir():
        if item.is_dir() and item.name not in IGNORE_DIRS and not item.name.startswith("."):
            folders.add(item.name)
    return folders


def get_actual_key_files(project_path: Path) -> set:
    """Get key files that exist in project."""
    return {f for f in KEY_FILES if (project_path / f).exists()}


def check_project(project_path: Path) -> list[str]:
    """Check single project for drift. Returns list of issues."""
    issues = []
    meta = load_meta_yaml(project_path)

    if meta is None:
        issues.append(f"MISSING: No META.yaml")
        return issues

    project_name = project_path.name

    # Check last_reviewed age
    project_block = meta.get("project", {})
    last_reviewed = project_block.get("last_reviewed")
    if last_reviewed:
        try:
            if isinstance(last_reviewed, str):
                review_date = datetime.strptime(last_reviewed, "%Y-%m-%d")
            else:
                review_date = datetime.combine(last_reviewed, datetime.min.time())
            age = (datetime.now() - review_date).days
            if age > MAX_REVIEW_AGE_DAYS:
                issues.append(f"STALE: last_reviewed is {age} days old")
        except (ValueError, TypeError):
            issues.append(f"INVALID: last_reviewed format '{last_reviewed}'")
    else:
        issues.append("MISSING: No last_reviewed date")

    # Check folders drift
    meta_folders = set(meta.get("folders", {}).keys())
    actual_folders = get_actual_folders(project_path)

    missing_in_meta = actual_folders - meta_folders
    extra_in_meta = meta_folders - actual_folders

    # Filter out common Betty Protocol folders that might be missing
    betty_folders = {"00_admin", "10_docs", "20_receipts", "30_config", "40_src", "70_evidence", "90_archive"}
    missing_notable = missing_in_meta - betty_folders

    if missing_notable:
        issues.append(f"DRIFT: Folders exist but not in META.yaml: {sorted(missing_notable)}")
    if extra_in_meta:
        issues.append(f"DRIFT: Folders in META.yaml but don't exist: {sorted(extra_in_meta)}")

    # Check key files
    meta_files = set(meta.get("files", {}).keys())
    actual_key_files = get_actual_key_files(project_path)
    missing_key_files = actual_key_files - meta_files

    if missing_key_files:
        issues.append(f"DRIFT: Key files exist but not in META.yaml: {sorted(missing_key_files)}")

    return issues


def main():
    fix_mode = "--fix" in sys.argv

    # Parse --series flag
    series_filter = None
    for i, arg in enumerate(sys.argv[1:], 1):
        if arg == "--series" and i < len(sys.argv) - 1:
            series_filter = sys.argv[i + 1].upper()
            if series_filter not in ("C", "P", "W"):
                print(f"ERROR: Invalid series '{series_filter}'. Use C, P, or W.")
                sys.exit(2)

    # Get non-flag arguments
    args = [a for a in sys.argv[1:] if not a.startswith("--") and a.upper() not in ("C", "P", "W")]

    if args:
        # Check specific project
        projects = [Path(args[0])]
    else:
        # Check all C/P/W projects (or filtered series)
        allowed_series = series_filter if series_filter else "CPW"
        projects = sorted([
            p for p in WORKSPACE.iterdir()
            if p.is_dir() and p.name[0] in allowed_series and p.name[1:4].replace("_", "").replace("-", "")[:3].isdigit()
        ])

    total_issues = 0
    projects_with_issues = []

    for project in projects:
        issues = check_project(project)
        if issues:
            total_issues += len(issues)
            projects_with_issues.append((project.name, issues))

    # Output
    series_label = f" ({series_filter}-series only)" if series_filter else ""
    if projects_with_issues:
        print(f"META.yaml Drift Report{series_label} - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        print("=" * 60)
        for name, issues in projects_with_issues:
            print(f"\n{name}:")
            for issue in issues:
                print(f"  - {issue}")
        print(f"\n{'=' * 60}")
        print(f"SUMMARY: {len(projects_with_issues)} projects with {total_issues} issues")
        print("READY: META.yaml drift check FAILED")
        sys.exit(1)
    else:
        print(f"READY: META.yaml drift check PASSED ({len(projects)} projects checked){series_label}")
        sys.exit(0)


if __name__ == "__main__":
    main()
