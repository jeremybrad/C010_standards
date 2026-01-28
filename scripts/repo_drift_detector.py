#!/usr/bin/env python3
"""Repo Drift Detector - Detect documentation drift in repositories.

Non-blocking by default (exit 0 unless --strict with CRITICAL findings).
Produces markdown and JSON reports with provenance.

Usage:
    python scripts/repo_drift_detector.py --level 1 --verbose
    python scripts/repo_drift_detector.py --level 2 --format both
    python scripts/repo_drift_detector.py --level 3 --strict
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# Add repo root to path for imports
SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(REPO_ROOT))

from scripts.drift import (
    DriftReport,
    FindingCounter,
    RepoProfile,
    Severity,
    resolve_rules,
    run_level1,
    run_level2,
    run_level3,
    write_json_report,
    write_markdown_report,
)


def get_git_info(repo_root: Path) -> tuple[str, str]:
    """Get current git SHA and branch.

    Args:
        repo_root: Repository root path

    Returns:
        Tuple of (short_sha, branch_name)
    """
    try:
        sha_result = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            timeout=10,
        )
        sha = sha_result.stdout.strip() if sha_result.returncode == 0 else "unknown"

        branch_result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            timeout=10,
        )
        branch = branch_result.stdout.strip() if branch_result.returncode == 0 else "unknown"

        return sha, branch
    except Exception:
        return "unknown", "unknown"


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Detect documentation drift in repositories",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Fast Level 1 scan
  python scripts/repo_drift_detector.py --level 1 --verbose

  # Full Level 2 consistency check with reports
  python scripts/repo_drift_detector.py --level 2 --format both

  # Level 3 deep dive
  python scripts/repo_drift_detector.py --level 3 --format both

  # Strict mode for CI (exit 1 on CRITICAL)
  python scripts/repo_drift_detector.py --strict

Exit Codes:
  0 - Success (no --strict) or no CRITICAL findings (--strict)
  1 - CRITICAL findings detected (--strict mode only)
  2 - Configuration/parse error
        """
    )

    parser.add_argument(
        "--repo", type=Path, default=REPO_ROOT,
        help="Repository root (default: C010_standards)"
    )
    parser.add_argument(
        "--level", type=int, choices=[1, 2, 3], default=1,
        help="Detection level: 1=fast, 2=consistency, 3=deep (default: 1)"
    )
    parser.add_argument(
        "--format", choices=["md", "json", "both"], default="md",
        help="Output format (default: md)"
    )
    parser.add_argument(
        "--out-dir", type=Path, default=None,
        help="Output directory (default: 70_evidence/drift/<repo>/)"
    )
    parser.add_argument(
        "--rules", type=Path, default=None,
        help="Path to drift_rules.yaml (default: 30_config/drift_rules.yaml)"
    )
    parser.add_argument(
        "--strict", action="store_true",
        help="Exit 1 if any CRITICAL findings"
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true",
        help="Show detailed output"
    )

    return parser.parse_args(argv if argv is not None else [])


def main(argv: list[str] | None = None) -> int:
    """Main entry point.

    Args:
        argv: Command line arguments (default: sys.argv[1:])

    Returns:
        Exit code: 0=success, 1=critical findings (strict), 2=config error
    """
    args = parse_args(argv)

    repo_root = args.repo.resolve()
    repo_name = repo_root.name

    if not repo_root.is_dir():
        print(f"ERROR: Repository not found: {repo_root}", file=sys.stderr)
        return 2

    # Detect repo profile
    profile = RepoProfile.detect(repo_root)

    # Resolve rules (CLI flag > repo file > universal defaults)
    rules = resolve_rules(args.rules, repo_root, verbose=args.verbose)

    # Get git info
    repo_sha, repo_branch = get_git_info(repo_root)

    # Determine output directory — use 70_evidence/drift/ if it exists,
    # otherwise fall back to console-only output
    evidence_dir = repo_root / "70_evidence" / "drift"
    if args.out_dir:
        out_dir = args.out_dir
    elif evidence_dir.exists() or (repo_root / "70_evidence").exists():
        out_dir = evidence_dir / repo_name
    else:
        out_dir = None  # console-only

    if args.verbose:
        print(f"Repo Drift Detector")
        print(f"  Repository: {repo_name}")
        print(f"  SHA: {repo_sha}")
        print(f"  Branch: {repo_branch}")
        print(f"  Level: {args.level}")
        print(f"  Profile: validators={profile.has_validators}, schemas={profile.has_schemas}, "
              f"taxonomies={profile.has_taxonomies}")
        if out_dir:
            print(f"  Output: {out_dir}")
        else:
            print(f"  Output: console only (no 70_evidence/ directory)")
        print()

    # Create finding counter
    counter = FindingCounter()

    # Run detection levels
    findings = []

    if args.verbose:
        print("Running drift detection...")

    # Level 1 always runs
    findings.extend(run_level1(repo_root, rules, counter, verbose=args.verbose, profile=profile))

    # Level 2 if requested
    if args.level >= 2:
        findings.extend(run_level2(repo_root, rules, counter, verbose=args.verbose, profile=profile))

    # Level 3 if requested
    if args.level >= 3:
        findings.extend(run_level3(repo_root, rules, counter, verbose=args.verbose, profile=profile))

    # Create report
    report = DriftReport(
        repo_name=repo_name,
        repo_sha=repo_sha,
        repo_branch=repo_branch,
        level=args.level,
        generated_at=datetime.now().isoformat(),
        findings=findings,
    )

    # Extract inventory data for report (only if repo has validators/)
    if args.level >= 2 and profile.has_validators:
        from scripts.drift.extractors import (
            extract_validator_list_from_claude,
            extract_validator_list_from_primer,
            extract_validator_list_from_readme,
            extract_validator_list_from_standards_guide,
            extract_validator_list_from_validators_readme,
            get_available_validators,
        )

        ground_truth = get_available_validators(repo_root)
        report.inventories["validators"] = {
            "ground_truth": sorted(ground_truth),
            "README.md": sorted(extract_validator_list_from_readme(repo_root / "README.md")),
            "CLAUDE.md": sorted(extract_validator_list_from_claude(repo_root / "CLAUDE.md")),
            "validators/README.md": sorted(extract_validator_list_from_validators_readme(repo_root / "validators" / "README.md")),
            "PROJECT_PRIMER.md": sorted(extract_validator_list_from_primer(repo_root / "PROJECT_PRIMER.md")),
        }

    # Print summary
    counts = report.counts_by_severity()
    print()
    print(f"Drift Detection Complete (Level {args.level})")
    print(f"  CRITICAL: {counts[Severity.CRITICAL]}")
    print(f"  MAJOR:    {counts[Severity.MAJOR]}")
    print(f"  MINOR:    {counts[Severity.MINOR]}")
    print(f"  INFO:     {counts[Severity.INFO]}")
    print(f"  Total:    {len(findings)}")

    # Write reports (skip file output when no output directory)
    if out_dir is not None:
        if args.format in ("md", "both"):
            md_path = write_markdown_report(report, out_dir)
            print(f"\nMarkdown report: {md_path}")

        if args.format in ("json", "both"):
            json_path = write_json_report(report, out_dir)
            print(f"JSON report: {json_path}")
    else:
        if args.format != "md":
            print("\nNote: No 70_evidence/ directory found; skipping file output.")

    # Determine exit code
    if args.strict and counts[Severity.CRITICAL] > 0:
        print(f"\nSTRICT MODE: {counts[Severity.CRITICAL]} CRITICAL finding(s) - exiting with code 1")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
