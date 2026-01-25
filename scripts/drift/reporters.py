"""Report generation for drift detection results.

Generates markdown and JSON reports with provenance, executive summary,
and detailed findings.
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from .models import Category, DriftReport, Finding, Severity


def write_markdown_report(
    report: DriftReport,
    out_dir: Path,
) -> Path:
    """Write a markdown drift report.

    Args:
        report: The drift report to write
        out_dir: Output directory

    Returns:
        Path to the written report
    """
    out_dir.mkdir(parents=True, exist_ok=True)

    # Generate filename with collision handling
    base_name = f"drift_report_{datetime.now().strftime('%Y-%m-%d')}_{report.repo_sha}"
    md_path = out_dir / f"{base_name}.md"

    # Handle collisions
    counter = 1
    while md_path.exists():
        md_path = out_dir / f"{base_name}_{counter}.md"
        counter += 1

    lines: list[str] = []

    # Header with provenance
    lines.append(f"# Drift Report: {report.repo_name}")
    lines.append("")
    lines.append(f"**Generated**: {report.generated_at}")
    lines.append(f"**Repo SHA**: {report.repo_sha}")
    lines.append(f"**Repo Branch**: {report.repo_branch}")
    lines.append(f"**Level**: {report.level} ({_level_name(report.level)})")
    lines.append("**Detector Version**: 1.0.0")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Executive Summary
    counts = report.counts_by_severity()
    lines.append("## Executive Summary")
    lines.append("")
    lines.append("| Severity | Count |")
    lines.append("|----------|-------|")
    lines.append(f"| CRITICAL | {counts[Severity.CRITICAL]} |")
    lines.append(f"| MAJOR | {counts[Severity.MAJOR]} |")
    lines.append(f"| MINOR | {counts[Severity.MINOR]} |")
    lines.append(f"| INFO | {counts[Severity.INFO]} |")
    lines.append(f"| **Total** | **{len(report.findings)}** |")
    lines.append("")

    # Group findings by category
    by_category: dict[Category, list[Finding]] = {}
    for f in report.findings:
        if f.category not in by_category:
            by_category[f.category] = []
        by_category[f.category].append(f)

    # Inventory Diffs Section
    if Category.INVENTORY_MISMATCH in by_category or report.inventories:
        lines.append("## Inventory Diffs")
        lines.append("")

        if report.inventories.get("validators"):
            inv = report.inventories["validators"]
            lines.append("### Validators")
            lines.append(f"- **Ground truth** (`validators/__init__.py`): {len(inv.get('ground_truth', []))} validators")
            for doc, claimed in inv.items():
                if doc != "ground_truth":
                    lines.append(f"- **{doc}**: {len(claimed)} validators found")
            lines.append("")

        for finding in by_category.get(Category.INVENTORY_MISMATCH, []):
            lines.extend(_format_finding(finding))
        lines.append("")

    # Broken Links Section
    if Category.BROKEN_LINK in by_category:
        lines.append("## Broken Links")
        lines.append("")
        for finding in by_category[Category.BROKEN_LINK]:
            lines.extend(_format_finding(finding))
        lines.append("")

    # Doc Contradictions Section
    if Category.DOC_CONTRADICTION in by_category:
        lines.append("## Canonical Doc Contradictions")
        lines.append("")
        for finding in by_category[Category.DOC_CONTRADICTION]:
            lines.extend(_format_finding(finding))
        lines.append("")

    # Generator Drift Section
    if Category.GENERATOR_DRIFT in by_category:
        lines.append("## Generator Drift Suspects")
        lines.append("")
        for finding in by_category[Category.GENERATOR_DRIFT]:
            lines.extend(_format_finding(finding))

            # Add suspected cause section for generator drift
            if finding.context.get("suspected_causes"):
                lines.append("")
                lines.append("**Suspected Causes**:")
                for cause in finding.context["suspected_causes"]:
                    lines.append(f"- {cause}")

            if finding.context.get("investigation_steps"):
                lines.append("")
                lines.append("**Investigation Steps**:")
                for i, step in enumerate(finding.context["investigation_steps"], 1):
                    lines.append(f"{i}. {step}")

            lines.append("")

    # Stale Paths Section
    if Category.STALE_PATH in by_category:
        lines.append("## Stale Path References")
        lines.append("")
        for finding in by_category[Category.STALE_PATH]:
            lines.extend(_format_finding(finding))
        lines.append("")

    # META Mismatch Section
    if Category.META_MISMATCH in by_category:
        lines.append("## META.yaml Drift")
        lines.append("")
        for finding in by_category[Category.META_MISMATCH]:
            lines.extend(_format_finding(finding))
        lines.append("")

    # Orphan Candidates Section (Level 3)
    if Category.ORPHAN_CANDIDATE in by_category:
        lines.append("## Orphan/Archive Candidates")
        lines.append("")
        lines.append("Files that may be candidates for archiving. Items marked with")
        lines.append("`requires_review: true` need manual verification before action.")
        lines.append("")

        # Group by confidence
        high_conf = [f for f in by_category[Category.ORPHAN_CANDIDATE] if f.confidence == "high"]
        low_conf = [f for f in by_category[Category.ORPHAN_CANDIDATE] if f.confidence != "high"]

        if high_conf:
            lines.append("### High Confidence")
            lines.append("")
            for finding in high_conf:
                lines.extend(_format_finding(finding))

        if low_conf:
            lines.append("### Low Confidence (Manual Review Required)")
            lines.append("")
            for finding in low_conf:
                lines.extend(_format_finding(finding))
        lines.append("")

    # Misplaced Artifacts Section
    if Category.MISPLACED_ARTIFACT in by_category:
        lines.append("## Misplaced Artifacts")
        lines.append("")
        for finding in by_category[Category.MISPLACED_ARTIFACT]:
            lines.extend(_format_finding(finding))
        lines.append("")

    # Config Warnings Section
    if Category.CONFIG_WARNING in by_category:
        lines.append("## Configuration Warnings")
        lines.append("")
        for finding in by_category[Category.CONFIG_WARNING]:
            lines.extend(_format_finding(finding))
        lines.append("")

    # Proposed Patch Plan
    if report.findings:
        lines.append("## Proposed Patch Plan")
        lines.append("")
        lines.append("Priority actions based on findings:")
        lines.append("")

        critical = [f for f in report.findings if f.severity == Severity.CRITICAL]
        major = [f for f in report.findings if f.severity == Severity.MAJOR]

        if critical:
            lines.append("### Critical (Address Immediately)")
            for f in critical:
                lines.append(f"1. **{f.id}**: {f.message}")
                for fix in f.suggested_fix[:2]:
                    lines.append(f"   - {fix}")
            lines.append("")

        if major:
            lines.append("### Major (Address Soon)")
            for f in major:
                lines.append(f"1. **{f.id}**: {f.message}")
                for fix in f.suggested_fix[:2]:
                    lines.append(f"   - {fix}")
            lines.append("")

    # Footer
    lines.append("---")
    lines.append("")
    lines.append("*Generated by `scripts/repo_drift_detector.py`*")

    md_path.write_text("\n".join(lines))
    return md_path


def write_json_report(
    report: DriftReport,
    out_dir: Path,
) -> Path:
    """Write a JSON drift report.

    Args:
        report: The drift report to write
        out_dir: Output directory

    Returns:
        Path to the written report
    """
    out_dir.mkdir(parents=True, exist_ok=True)

    # Generate filename with collision handling
    base_name = f"drift_report_{datetime.now().strftime('%Y-%m-%d')}_{report.repo_sha}"
    json_path = out_dir / f"{base_name}.json"

    # Handle collisions
    counter = 1
    while json_path.exists():
        json_path = out_dir / f"{base_name}_{counter}.json"
        counter += 1

    data = report.to_dict()
    json_path.write_text(json.dumps(data, indent=2))
    return json_path


def _level_name(level: int) -> str:
    """Get human-readable level name."""
    names = {
        1: "Fast Inventory",
        2: "Canonical Consistency",
        3: "Deep Dive + Archive Candidates",
    }
    return names.get(level, "Unknown")


def _format_finding(finding: Finding) -> list[str]:
    """Format a single finding for markdown output."""
    lines = []

    # Header with ID and severity
    severity_emoji = {
        Severity.CRITICAL: "🔴",
        Severity.MAJOR: "🟠",
        Severity.MINOR: "🟡",
        Severity.INFO: "🔵",
    }
    emoji = severity_emoji.get(finding.severity, "⚪")

    lines.append(f"### {finding.id} ({finding.severity.value}) {emoji}")
    lines.append("")

    if finding.file:
        loc = f"**File**: `{finding.file}`"
        if finding.line:
            loc += f" (line {finding.line})"
        lines.append(loc)

    lines.append(f"**Issue**: {finding.message}")

    if finding.requires_review:
        lines.append("**Note**: Requires manual review")

    if finding.suggested_fix:
        lines.append("")
        lines.append("**Suggested Fix**:")
        for fix in finding.suggested_fix:
            lines.append(f"- {fix}")

    lines.append("")
    return lines
