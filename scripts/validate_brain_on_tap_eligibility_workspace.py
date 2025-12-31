#!/usr/bin/env python3
"""Validate all registry repos for Brain on Tap (BBOT) eligibility.

Reads registry/repos.yaml and validates each repo with bot_active field.
Outputs eligibility report as CSV and Markdown.

Usage:
    python scripts/validate_brain_on_tap_eligibility_workspace.py
    python scripts/validate_brain_on_tap_eligibility_workspace.py --verbose
    python scripts/validate_brain_on_tap_eligibility_workspace.py --all  # Include bot_active=false

Output:
    70_evidence/exports/Brain_on_Tap_Eligibility.csv
    70_evidence/exports/Brain_on_Tap_Eligibility.md

Exit codes:
    0 - Report generated (may include failures)
    2 - Configuration/file error
"""
from __future__ import annotations

import argparse
import csv
import sys
from datetime import datetime
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML required. Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(2)

# Import the single-repo validator
from validate_brain_on_tap_eligibility import validate_repo, load_registry


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


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate all registry repos for BBOT eligibility"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Print detailed output"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Include repos with bot_active=false (default: only bot_active=true)"
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
    parser.add_argument(
        "--output-dir",
        type=Path,
        help="Output directory (default: 70_evidence/exports/)"
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

    # Workspace root
    workspace = args.workspace or c010_root.parent

    # Output directory
    output_dir = args.output_dir or (c010_root / "70_evidence" / "exports")
    output_dir.mkdir(parents=True, exist_ok=True)

    if args.verbose:
        print(f"Registry: {registry_path}")
        print(f"Workspace: {workspace}")
        print(f"Output: {output_dir}")

    # Collect repos to validate
    repos = registry_data.get("repos", [])
    results = []

    for entry in repos:
        repo_id = entry.get("repo_id", "<unknown>")
        bot_active = entry.get("bot_active")
        path_rel = entry.get("path_rel")

        # Skip if no BBOT fields
        if bot_active is None and path_rel is None:
            if args.verbose:
                print(f"SKIP: {repo_id} (no BBOT fields)")
            continue

        # Skip bot_active=false unless --all
        if not args.all and bot_active is False:
            if args.verbose:
                print(f"SKIP: {repo_id} (bot_active=false)")
            results.append({
                "repo_id": repo_id,
                "bot_active": False,
                "eligible": "N/A",
                "errors": "",
                "warnings": "Excluded (bot_active=false)",
                "path_rel": path_rel or "",
            })
            continue

        # Resolve path
        if path_rel:
            repo_path = workspace / path_rel
        else:
            repo_path = workspace / repo_id

        if not repo_path.is_dir():
            if args.verbose:
                print(f"MISSING: {repo_id} -> {repo_path}")
            results.append({
                "repo_id": repo_id,
                "bot_active": bot_active,
                "eligible": "FAIL",
                "errors": "Directory not found",
                "warnings": "",
                "path_rel": path_rel or "",
            })
            continue

        # Validate
        errors, warnings = validate_repo(repo_id, repo_path, registry_data, args.verbose)

        eligible = "PASS" if not errors else "FAIL"
        results.append({
            "repo_id": repo_id,
            "bot_active": bot_active,
            "eligible": eligible,
            "errors": "; ".join(errors) if errors else "",
            "warnings": "; ".join(warnings) if warnings else "",
            "path_rel": path_rel or "",
        })

    # Sort: PASS first, then FAIL, then N/A
    order = {"PASS": 0, "FAIL": 1, "N/A": 2}
    results.sort(key=lambda r: (order.get(r["eligible"], 3), r["repo_id"]))

    # Write CSV
    csv_path = output_dir / "Brain_on_Tap_Eligibility.csv"
    with csv_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "repo_id", "bot_active", "eligible", "path_rel", "errors", "warnings"
        ])
        writer.writeheader()
        writer.writerows(results)

    # Write Markdown
    md_path = output_dir / "Brain_on_Tap_Eligibility.md"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    pass_count = sum(1 for r in results if r["eligible"] == "PASS")
    fail_count = sum(1 for r in results if r["eligible"] == "FAIL")
    skip_count = sum(1 for r in results if r["eligible"] == "N/A")

    with md_path.open("w") as f:
        f.write("# Brain on Tap Eligibility Report\n\n")
        f.write(f"**Generated**: {timestamp}\n")
        f.write(f"**Registry**: `{registry_path.name}`\n\n")
        f.write("## Summary\n\n")
        f.write(f"| Status | Count |\n")
        f.write(f"|--------|-------|\n")
        f.write(f"| PASS (eligible) | {pass_count} |\n")
        f.write(f"| FAIL (not eligible) | {fail_count} |\n")
        f.write(f"| N/A (excluded) | {skip_count} |\n")
        f.write(f"| **Total** | **{len(results)}** |\n\n")

        # Eligible repos
        eligible_repos = [r for r in results if r["eligible"] == "PASS"]
        if eligible_repos:
            f.write("## Eligible Repos\n\n")
            f.write("| Repo ID | Path |\n")
            f.write("|---------|------|\n")
            for r in eligible_repos:
                f.write(f"| `{r['repo_id']}` | `{r['path_rel']}` |\n")
            f.write("\n")

        # Failed repos
        failed_repos = [r for r in results if r["eligible"] == "FAIL"]
        if failed_repos:
            f.write("## Failed Repos\n\n")
            f.write("| Repo ID | Errors |\n")
            f.write("|---------|--------|\n")
            for r in failed_repos:
                errors = r["errors"].replace("|", "\\|")
                f.write(f"| `{r['repo_id']}` | {errors} |\n")
            f.write("\n")

        # Excluded repos
        excluded_repos = [r for r in results if r["eligible"] == "N/A"]
        if excluded_repos:
            f.write("## Excluded Repos (bot_active=false)\n\n")
            for r in excluded_repos:
                f.write(f"- `{r['repo_id']}`\n")
            f.write("\n")

    # Print summary
    print("\n" + "=" * 60)
    print("BRAIN ON TAP ELIGIBILITY WORKSPACE REPORT")
    print("=" * 60)
    print(f"\nPASS (eligible):      {pass_count}")
    print(f"FAIL (not eligible):  {fail_count}")
    print(f"N/A (excluded):       {skip_count}")
    print(f"Total:                {len(results)}")
    print(f"\nOutputs:")
    print(f"  CSV: {csv_path}")
    print(f"  MD:  {md_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
