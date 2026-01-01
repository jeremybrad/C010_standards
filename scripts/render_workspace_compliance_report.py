#!/usr/bin/env python3
"""
render_workspace_compliance_report.py - Generate human-friendly compliance report

Reads the latest folder structure audit CSV and produces a categorized markdown
report that answers: "What broke, where, why, and what do we do?"

Usage:
    python3 scripts/render_workspace_compliance_report.py [--output PATH]

Outputs:
    - 00_admin/WORKSPACE_COMPLIANCE_LATEST.md (default)
    - Prints summary to stdout

Exit codes:
    0 - Report generated successfully
    1 - Violations found with no bucket classification (STOP condition)
    2 - Configuration/file error
"""

from __future__ import annotations

import argparse
import csv
import glob
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

# Repo root discovery
SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent

# Paths
EXPORTS_DIR = REPO_ROOT / "70_evidence" / "exports"
EXCEPTIONS_REGISTER = REPO_ROOT / "00_admin" / "TEMP_EXCEPTIONS_REGISTER.md"
DEFAULT_OUTPUT = REPO_ROOT / "00_admin" / "WORKSPACE_COMPLIANCE_LATEST.md"

# Bucket definitions
PERMANENT_EXCEPTIONS = {"C010_standards"}  # Standards repo defines the rules
EXCLUDED_REPOS = {"U01_comfyUI"}  # External tools, not maintained


@dataclass
class RepoStatus:
    """Status for a single repository."""
    name: str
    series: str
    compliant: bool
    missing_files: list[str] = field(default_factory=list)
    invalid_dirs: list[str] = field(default_factory=list)
    requires_00_run: bool = False
    missing_00_run: bool = False
    has_exception_file: bool = False
    recommended_action: str = ""

    @property
    def bucket(self) -> str:
        """Determine which bucket this repo belongs to."""
        if self.compliant:
            return "compliant"
        if self.name in PERMANENT_EXCEPTIONS:
            return "permanent_exception"
        if self.name in EXCLUDED_REPOS:
            return "excluded"
        if self.has_exception_file:
            return "temporary_exception"
        return "unclassified"  # STOP condition


def parse_audit_csv(csv_path: Path) -> list[RepoStatus]:
    """Parse audit CSV into RepoStatus objects."""
    repos = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Parse semicolon-separated lists
            missing_files = [x for x in row.get("missing_required_files", "").split(";") if x]
            invalid_dirs = [x for x in row.get("invalid_top_level_dirs", "").split(";") if x]

            repo = RepoStatus(
                name=row["repo_name"],
                series=row.get("repo_series", "-"),
                compliant=row.get("compliant", "").lower() == "true",
                missing_files=missing_files,
                invalid_dirs=invalid_dirs,
                requires_00_run=row.get("requires_00_run", "").lower() == "true",
                missing_00_run=row.get("missing_00_run", "").lower() == "true",
                has_exception_file=row.get("exceptions_applied", "").lower() == "true",
                recommended_action=row.get("recommended_action", ""),
            )
            repos.append(repo)
    return repos


def get_latest_audit_csv() -> Path | None:
    """Find the most recent audit CSV."""
    pattern = str(EXPORTS_DIR / "folder_structure_audit_*.csv")
    files = sorted(glob.glob(pattern))
    # Filter out "latest" symlink
    files = [f for f in files if "latest" not in f]
    return Path(files[-1]) if files else None


def check_temp_register_entry(repo_name: str) -> bool:
    """Check if repo has entry in TEMP_EXCEPTIONS_REGISTER.md."""
    if not EXCEPTIONS_REGISTER.exists():
        return False
    content = EXCEPTIONS_REGISTER.read_text()
    return f"### {repo_name}" in content


def render_report(repos: list[RepoStatus], audit_path: Path) -> str:
    """Render the markdown report."""
    # Bucket repos
    buckets: dict[str, list[RepoStatus]] = {
        "compliant": [],
        "permanent_exception": [],
        "temporary_exception": [],
        "excluded": [],
        "unclassified": [],
    }

    for repo in repos:
        buckets[repo.bucket].append(repo)

    # Stats
    total = len(repos)
    compliant_count = len(buckets["compliant"])
    violation_count = total - compliant_count
    unclassified_count = len(buckets["unclassified"])

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    audit_timestamp = audit_path.stem.split("_")[-2] + "_" + audit_path.stem.split("_")[-1]

    lines = [
        "# Workspace Compliance Report",
        "",
        f"**Generated:** {timestamp}",
        f"**Source:** `{audit_path.name}`",
        f"**Audit timestamp:** {audit_timestamp}",
        "",
        "---",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "|--------|-------|",
        f"| Total repos | {total} |",
        f"| Compliant | {compliant_count} ({100*compliant_count//total}%) |",
        f"| With violations | {violation_count} |",
        f"| Unclassified violations | {unclassified_count} |",
        "",
    ]

    # STOP condition warning
    if unclassified_count > 0:
        lines.extend([
            "## STOP: Unclassified Violations",
            "",
            "These repos have violations but no declared exception. **Classify before proceeding.**",
            "",
            "| Repo | Series | Invalid Dirs | Missing Files | Action |",
            "|------|--------|--------------|---------------|--------|",
        ])
        for repo in buckets["unclassified"]:
            dirs = ", ".join(repo.invalid_dirs[:3]) + ("..." if len(repo.invalid_dirs) > 3 else "")
            files = ", ".join(repo.missing_files[:3]) + ("..." if len(repo.missing_files) > 3 else "")
            lines.append(f"| {repo.name} | {repo.series} | {dirs or '-'} | {files or '-'} | Create exception file |")
        lines.append("")

    # Compliant repos (collapsed)
    lines.extend([
        "## Compliant Repos",
        "",
        f"<details><summary>{compliant_count} repos fully compliant</summary>",
        "",
        "| Repo | Series |",
        "|------|--------|",
    ])
    for repo in sorted(buckets["compliant"], key=lambda r: r.name):
        lines.append(f"| {repo.name} | {repo.series} |")
    lines.extend(["", "</details>", ""])

    # Permanent exceptions
    if buckets["permanent_exception"]:
        lines.extend([
            "## Permanent Exceptions",
            "",
            "These repos have justified permanent exceptions (e.g., standards repos).",
            "",
            "| Repo | Series | Reason |",
            "|------|--------|--------|",
        ])
        for repo in buckets["permanent_exception"]:
            reason = "Standards repository (defines the rules)" if repo.name == "C010_standards" else "Declared permanent"
            lines.append(f"| {repo.name} | {repo.series} | {reason} |")
        lines.append("")

    # Temporary exceptions (detailed)
    if buckets["temporary_exception"]:
        lines.extend([
            "## Temporary Exceptions",
            "",
            "These repos have declared exceptions with remediation plans.",
            "",
        ])
        for repo in buckets["temporary_exception"]:
            has_register = check_temp_register_entry(repo.name)
            register_status = "documented" if has_register else "**MISSING**"

            lines.extend([
                f"### {repo.name}",
                "",
                f"- **Series:** {repo.series}",
                f"- **Register entry:** {register_status}",
                f"- **Recommended action:** {repo.recommended_action}",
                "",
            ])

            if repo.invalid_dirs:
                lines.append("**Invalid directories:**")
                for d in repo.invalid_dirs:
                    lines.append(f"- `{d}`")
                lines.append("")

            if repo.missing_files:
                lines.append("**Missing required files:**")
                for f in repo.missing_files:
                    lines.append(f"- `{f}`")
                lines.append("")

    # Excluded repos
    if buckets["excluded"]:
        lines.extend([
            "## Excluded Repos",
            "",
            "External tools not maintained by this workspace.",
            "",
            "| Repo | Series | Reason |",
            "|------|--------|--------|",
        ])
        for repo in buckets["excluded"]:
            reason = "External tool (ComfyUI)" if "comfy" in repo.name.lower() else "External"
            lines.append(f"| {repo.name} | {repo.series} | {reason} |")
        lines.append("")

    # Series breakdown
    series_stats: dict[str, dict[str, int]] = {}
    for repo in repos:
        s = repo.series or "-"
        if s not in series_stats:
            series_stats[s] = {"total": 0, "compliant": 0}
        series_stats[s]["total"] += 1
        if repo.compliant:
            series_stats[s]["compliant"] += 1

    lines.extend([
        "## Compliance by Series",
        "",
        "| Series | Compliant | Total | Rate |",
        "|--------|-----------|-------|------|",
    ])
    for s in ["C", "W", "P", "U", "-"]:
        if s in series_stats:
            stats = series_stats[s]
            rate = 100 * stats["compliant"] // stats["total"] if stats["total"] > 0 else 0
            series_name = {"C": "Core", "W": "Work", "P": "Projects", "U": "Utility", "-": "Other"}.get(s, s)
            lines.append(f"| {s} ({series_name}) | {stats['compliant']} | {stats['total']} | {rate}% |")
    lines.append("")

    # Footer
    lines.extend([
        "---",
        "",
        "*This report is auto-generated by `scripts/render_workspace_compliance_report.py`*",
        "",
        "**Next steps:**",
        "1. Resolve any UNCLASSIFIED violations (create exception files)",
        "2. Review TEMPORARY exceptions and work toward remediation",
        "3. Re-run audit after changes: `bash scripts/audit_folder_structure.sh`",
        "",
    ])

    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate workspace compliance report")
    parser.add_argument("--output", "-o", type=Path, default=DEFAULT_OUTPUT,
                        help="Output path for markdown report")
    parser.add_argument("--audit-csv", type=Path, default=None,
                        help="Specific audit CSV to use (default: latest)")
    args = parser.parse_args(argv)

    # Find audit CSV
    if args.audit_csv:
        audit_path = args.audit_csv
    else:
        audit_path = get_latest_audit_csv()

    if not audit_path or not audit_path.exists():
        print("ERROR: No audit CSV found. Run: bash scripts/audit_folder_structure.sh", file=sys.stderr)
        return 2

    print(f"Reading: {audit_path}")

    # Parse and render
    repos = parse_audit_csv(audit_path)
    report = render_report(repos, audit_path)

    # Write output
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(report)
    print(f"Written: {args.output}")

    # Summary
    unclassified = [r for r in repos if r.bucket == "unclassified"]
    compliant = [r for r in repos if r.compliant]

    print(f"\nSummary: {len(compliant)}/{len(repos)} compliant ({100*len(compliant)//len(repos)}%)")

    if unclassified:
        print(f"\nSTOP: {len(unclassified)} unclassified violations:")
        for r in unclassified:
            print(f"  - {r.name}")
        return 1

    print("\nAll violations are classified.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
