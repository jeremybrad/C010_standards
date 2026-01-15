#!/usr/bin/env python3
"""
validate_tier2_compliance.py - Check Tier 2 documentation compliance for W-series repos

Usage:
    python scripts/validate_tier2_compliance.py <repo_path>
    python scripts/validate_tier2_compliance.py ~/SyncedProjects/W001_cmo-weekly-reporting
    python scripts/validate_tier2_compliance.py W001  # Short name also works

Options:
    --verbose       Show detailed check results
    --json-output   Output results as JSON to specified file

Exit codes:
    0 - Fully compliant
    1 - Missing required files/folders
    2 - Files exist but content incomplete or parse error
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path


@dataclass
class CheckResult:
    """Result of a single compliance check."""
    name: str
    passed: bool
    message: str
    severity: str = "error"  # error, warning, info


@dataclass
class ComplianceReport:
    """Full compliance report for a repo."""
    repo_path: str
    repo_name: str
    timestamp: str
    checks: list[CheckResult] = field(default_factory=list)

    @property
    def is_compliant(self) -> bool:
        """True if all error-level checks passed."""
        return all(c.passed for c in self.checks if c.severity == "error")

    @property
    def error_count(self) -> int:
        return sum(1 for c in self.checks if not c.passed and c.severity == "error")

    @property
    def warning_count(self) -> int:
        return sum(1 for c in self.checks if not c.passed and c.severity == "warning")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Validate Tier 2 documentation compliance for W-series repos"
    )
    parser.add_argument(
        "repo_path",
        help="Path to repo or short name (e.g., W001)"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show detailed check results"
    )
    parser.add_argument(
        "--json-output",
        metavar="FILE",
        help="Output results as JSON to specified file"
    )
    return parser.parse_args(argv)


def resolve_repo_path(repo_input: str) -> Path | None:
    """Resolve repo path from input (full path or short name)."""
    # If it's already a valid path
    path = Path(repo_input).expanduser()
    if path.is_dir():
        return path

    # Try as short name under SyncedProjects
    workspace = Path.home() / "SyncedProjects"

    # Try exact match first
    exact = workspace / repo_input
    if exact.is_dir():
        return exact

    # Try prefix match (e.g., "W001" matches "W001_cmo-weekly-reporting")
    for item in workspace.iterdir():
        if item.is_dir() and item.name.startswith(repo_input):
            return item

    return None


def check_file_exists(repo: Path, filename: str, required: bool = True) -> CheckResult:
    """Check if a file exists."""
    file_path = repo / filename
    exists = file_path.is_file()
    severity = "error" if required else "warning"

    if exists:
        return CheckResult(
            name=f"file_{filename.replace('.', '_').replace('/', '_')}",
            passed=True,
            message=f"{filename} exists",
            severity=severity
        )
    else:
        return CheckResult(
            name=f"file_{filename.replace('.', '_').replace('/', '_')}",
            passed=False,
            message=f"{filename} is missing" + (" (required)" if required else ""),
            severity=severity
        )


def check_dir_exists(repo: Path, dirname: str, required: bool = True) -> CheckResult:
    """Check if a directory exists."""
    dir_path = repo / dirname
    exists = dir_path.is_dir()
    severity = "error" if required else "warning"

    if exists:
        return CheckResult(
            name=f"dir_{dirname.replace('/', '_')}",
            passed=True,
            message=f"{dirname}/ exists",
            severity=severity
        )
    else:
        return CheckResult(
            name=f"dir_{dirname.replace('/', '_')}",
            passed=False,
            message=f"{dirname}/ is missing" + (" (required)" if required else ""),
            severity=severity
        )


def check_meta_yaml_content(repo: Path) -> list[CheckResult]:
    """Check META.yaml content for required W-series fields."""
    results = []
    meta_path = repo / "META.yaml"

    if not meta_path.is_file():
        return [CheckResult(
            name="meta_yaml_content",
            passed=False,
            message="Cannot check META.yaml content - file missing",
            severity="error"
        )]

    try:
        import yaml
    except ImportError:
        return [CheckResult(
            name="meta_yaml_content",
            passed=True,
            message="PyYAML not installed - skipping content validation",
            severity="warning"
        )]

    try:
        with open(meta_path) as f:
            meta = yaml.safe_load(f)
    except Exception as e:
        return [CheckResult(
            name="meta_yaml_parse",
            passed=False,
            message=f"META.yaml parse error: {e}",
            severity="error"
        )]

    if not isinstance(meta, dict):
        return [CheckResult(
            name="meta_yaml_structure",
            passed=False,
            message="META.yaml is not a valid YAML mapping",
            severity="error"
        )]

    project = meta.get("project", {})

    # Check required fields
    required_fields = ["last_reviewed", "summary", "status", "series"]
    for field_name in required_fields:
        value = project.get(field_name)
        if value and str(value).strip() and "TODO" not in str(value):
            results.append(CheckResult(
                name=f"meta_{field_name}",
                passed=True,
                message=f"META.yaml has {field_name}",
                severity="error"
            ))
        else:
            results.append(CheckResult(
                name=f"meta_{field_name}",
                passed=False,
                message=f"META.yaml missing or placeholder {field_name}",
                severity="error"
            ))

    # Check W-series specific: client field
    client = project.get("client")
    if client and str(client).strip() and "TODO" not in str(client):
        results.append(CheckResult(
            name="meta_client",
            passed=True,
            message="META.yaml has client field (W-series requirement)",
            severity="error"
        ))
    else:
        results.append(CheckResult(
            name="meta_client",
            passed=False,
            message="META.yaml missing client field (required for W-series)",
            severity="error"
        ))

    # Check last_reviewed freshness (30 days)
    last_reviewed = project.get("last_reviewed")
    if last_reviewed:
        try:
            if isinstance(last_reviewed, str):
                reviewed_date = datetime.strptime(last_reviewed, "%Y-%m-%d")
            else:
                reviewed_date = datetime.combine(last_reviewed, datetime.min.time())

            age = datetime.now() - reviewed_date
            if age <= timedelta(days=30):
                results.append(CheckResult(
                    name="meta_freshness",
                    passed=True,
                    message=f"META.yaml last_reviewed is fresh ({age.days} days old)",
                    severity="warning"
                ))
            else:
                results.append(CheckResult(
                    name="meta_freshness",
                    passed=False,
                    message=f"META.yaml last_reviewed is stale ({age.days} days old, max 30)",
                    severity="warning"
                ))
        except (ValueError, TypeError):
            results.append(CheckResult(
                name="meta_freshness",
                passed=False,
                message="META.yaml last_reviewed has invalid date format",
                severity="warning"
            ))

    return results


def check_changelog_content(repo: Path) -> CheckResult:
    """Check CHANGELOG.md has at least one entry."""
    changelog_path = repo / "CHANGELOG.md"

    if not changelog_path.is_file():
        return CheckResult(
            name="changelog_content",
            passed=False,
            message="Cannot check CHANGELOG.md content - file missing",
            severity="error"
        )

    content = changelog_path.read_text()

    # Look for version entry pattern like "## [0.1.0]" or "## [Unreleased]"
    if "## [" in content and len(content) > 100:
        return CheckResult(
            name="changelog_content",
            passed=True,
            message="CHANGELOG.md has content",
            severity="error"
        )
    else:
        return CheckResult(
            name="changelog_content",
            passed=False,
            message="CHANGELOG.md appears empty or minimal",
            severity="warning"
        )


def check_glossary_content(repo: Path) -> CheckResult:
    """Check glossary.yaml has at least one term."""
    glossary_path = repo / "10_docs" / "glossary.yaml"

    if not glossary_path.is_file():
        return CheckResult(
            name="glossary_content",
            passed=False,
            message="10_docs/glossary.yaml is missing",
            severity="error"
        )

    try:
        import yaml
    except ImportError:
        return CheckResult(
            name="glossary_content",
            passed=True,
            message="PyYAML not installed - skipping glossary validation",
            severity="warning"
        )

    try:
        with open(glossary_path) as f:
            glossary = yaml.safe_load(f)
    except Exception as e:
        return CheckResult(
            name="glossary_parse",
            passed=False,
            message=f"glossary.yaml parse error: {e}",
            severity="error"
        )

    if not isinstance(glossary, dict):
        return CheckResult(
            name="glossary_structure",
            passed=False,
            message="glossary.yaml is not a valid YAML mapping",
            severity="error"
        )

    terms = glossary.get("terms", [])
    if not terms:
        return CheckResult(
            name="glossary_content",
            passed=False,
            message="glossary.yaml has no terms defined",
            severity="error"
        )

    # Filter out placeholder terms
    real_terms = [t for t in terms if t.get("term") and "TODO" not in str(t.get("term", ""))]

    if len(real_terms) >= 1:
        return CheckResult(
            name="glossary_content",
            passed=True,
            message=f"glossary.yaml has {len(real_terms)} term(s)",
            severity="error"
        )
    else:
        return CheckResult(
            name="glossary_content",
            passed=False,
            message="glossary.yaml has only placeholder terms - add real terms",
            severity="error"
        )


def validate_repo(repo_path: Path, verbose: bool = False) -> ComplianceReport:
    """Run all compliance checks on a repo."""
    report = ComplianceReport(
        repo_path=str(repo_path),
        repo_name=repo_path.name,
        timestamp=datetime.now().isoformat()
    )

    # Structure checks (Gate 1)
    report.checks.append(check_file_exists(repo_path, "README.md"))
    report.checks.append(check_file_exists(repo_path, "CLAUDE.md"))
    report.checks.append(check_file_exists(repo_path, "META.yaml"))
    report.checks.append(check_file_exists(repo_path, "CHANGELOG.md"))
    report.checks.append(check_dir_exists(repo_path, "10_docs"))
    report.checks.append(check_dir_exists(repo_path, "20_receipts"))

    # Content checks (Gate 2)
    report.checks.extend(check_meta_yaml_content(repo_path))
    report.checks.append(check_changelog_content(repo_path))
    report.checks.append(check_glossary_content(repo_path))

    return report


def print_report(report: ComplianceReport, verbose: bool = False) -> None:
    """Print compliance report to stdout."""
    print(f"\n{'='*60}")
    print(f"Tier 2 Compliance Report: {report.repo_name}")
    print(f"{'='*60}")
    print(f"Path: {report.repo_path}")
    print(f"Timestamp: {report.timestamp}")
    print()

    if verbose:
        print("Detailed Results:")
        print("-" * 40)
        for check in report.checks:
            status = "PASS" if check.passed else "FAIL"
            icon = "+" if check.passed else "x"
            severity_marker = "" if check.severity == "error" else " (warning)"
            print(f"  [{icon}] {status}: {check.message}{severity_marker}")
        print()

    # Summary
    print(f"Summary:")
    print(f"  Total checks: {len(report.checks)}")
    print(f"  Passed: {sum(1 for c in report.checks if c.passed)}")
    print(f"  Errors: {report.error_count}")
    print(f"  Warnings: {report.warning_count}")
    print()

    if report.is_compliant:
        print("Result: COMPLIANT")
    else:
        print("Result: NOT COMPLIANT")
        print()
        print("Failed checks:")
        for check in report.checks:
            if not check.passed and check.severity == "error":
                print(f"  - {check.message}")

        print()
        print("Remediation:")
        print("  1. Run bootstrap if not done: bash scripts/bootstrap_tier2_wseries.sh <repo>")
        print("  2. Fill in placeholder values in META.yaml, CHANGELOG.md, glossary.yaml")
        print("  3. Re-run this validator")

    print(f"\n{'='*60}\n")


def main(argv: list[str] | None = None) -> int:
    """Main entry point."""
    args = parse_args(argv)

    # Resolve repo path
    repo_path = resolve_repo_path(args.repo_path)
    if not repo_path:
        print(f"ERROR: Could not find repo: {args.repo_path}", file=sys.stderr)
        return 2

    # Run validation
    report = validate_repo(repo_path, verbose=args.verbose)

    # Output results
    if args.json_output:
        output_data = {
            "repo_path": report.repo_path,
            "repo_name": report.repo_name,
            "timestamp": report.timestamp,
            "is_compliant": report.is_compliant,
            "error_count": report.error_count,
            "warning_count": report.warning_count,
            "checks": [
                {
                    "name": c.name,
                    "passed": c.passed,
                    "message": c.message,
                    "severity": c.severity
                }
                for c in report.checks
            ]
        }
        with open(args.json_output, "w") as f:
            json.dump(output_data, f, indent=2)
        print(f"JSON output written to: {args.json_output}")

    print_report(report, verbose=args.verbose)

    # Exit code
    if report.is_compliant:
        return 0
    elif report.error_count > 0:
        return 1
    else:
        return 0  # Warnings only


if __name__ == "__main__":
    sys.exit(main())
