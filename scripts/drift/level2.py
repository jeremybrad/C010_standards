"""Level 2 drift detection: Canonical consistency checks.

Runs in minutes. Checks:
- Validator claims across canonical docs
- Internal links in canonical scope only
- META.yaml folder/file drift
- Generator staleness (PROJECT_PRIMER.md)
"""

from __future__ import annotations

import re
import subprocess
import sys
from fnmatch import fnmatch
from pathlib import Path
from typing import Any

from .extractors import (
    extract_internal_links,
    extract_validator_list_from_claude,
    extract_validator_list_from_primer,
    extract_validator_list_from_readme,
    extract_validator_list_from_standards_guide,
    extract_validator_list_from_validators_readme,
    get_available_validators,
)
from .models import Category, Finding, FindingCounter, RepoProfile, Severity


def run_level2(
    repo_root: Path,
    rules: dict[str, Any],
    counter: FindingCounter,
    verbose: bool = False,
    profile: RepoProfile | None = None,
) -> list[Finding]:
    """Run Level 2 drift detection.

    Args:
        repo_root: Repository root path
        rules: Loaded drift_rules.yaml configuration
        counter: Finding ID counter
        verbose: Enable verbose output
        profile: Repository profile for gating C10-specific checks

    Returns:
        List of findings
    """
    findings: list[Finding] = []

    if verbose:
        print("  Level 2: Canonical consistency checks...")

    # 1. Compare validator inventories across docs (only if repo has validators/)
    if profile is None or profile.has_validators:
        findings.extend(_check_validator_consistency(repo_root, rules, counter, verbose))
    elif verbose:
        print("    Skipping validator consistency (no validators/ detected)")

    # 2. Validate internal links in canonical docs
    findings.extend(_check_internal_links(repo_root, rules, counter, verbose))

    # 3. Check META.yaml drift
    findings.extend(_check_meta_yaml(repo_root, counter, verbose))

    # 4. Check for generator drift (PROJECT_PRIMER.md)
    findings.extend(_check_generator_drift(repo_root, rules, counter, verbose, profile))

    return findings


def _check_validator_consistency(
    repo_root: Path,
    rules: dict[str, Any],
    counter: FindingCounter,
    verbose: bool,
) -> list[Finding]:
    """Compare validator inventories across canonical docs."""
    findings = []

    # Ground truth from __init__.py
    ground_truth = get_available_validators(repo_root)
    if not ground_truth:
        findings.append(Finding(
            id=counter.next_id(2),
            level_detected=2,
            severity=Severity.CRITICAL,
            category=Category.INVENTORY_MISMATCH,
            message="Could not load ground truth validators from __init__.py",
            file="validators/__init__.py",
            suggested_fix=["Ensure validators/__init__.py exists with AVAILABLE_VALIDATORS"],
        ))
        return findings

    # Extract inventories from each canonical doc
    inventories: dict[str, set[str]] = {}

    readme_path = repo_root / "README.md"
    if readme_path.exists():
        inventories["README.md"] = extract_validator_list_from_readme(readme_path)

    claude_path = repo_root / "CLAUDE.md"
    if claude_path.exists():
        inventories["CLAUDE.md"] = extract_validator_list_from_claude(claude_path)

    validators_readme = repo_root / "validators" / "README.md"
    if validators_readme.exists():
        inventories["validators/README.md"] = extract_validator_list_from_validators_readme(validators_readme)

    standards_guide = repo_root / "10_docs" / "STANDARDS_GUIDE.md"
    if standards_guide.exists():
        inventories["10_docs/STANDARDS_GUIDE.md"] = extract_validator_list_from_standards_guide(standards_guide)

    primer_path = repo_root / "PROJECT_PRIMER.md"
    if primer_path.exists():
        inventories["PROJECT_PRIMER.md"] = extract_validator_list_from_primer(primer_path)

    # Store inventories for report
    inventory_data = {
        "ground_truth": sorted(ground_truth),
    }

    # Compare each doc against ground truth
    for doc, claimed in inventories.items():
        inventory_data[doc] = sorted(claimed)

        # Filter to only validators that could reasonably be expected
        # (some docs may only mention a subset intentionally)
        missing = ground_truth - claimed

        if missing and len(claimed) > 0:
            # Only report if doc claims to list validators but is incomplete
            # Use MAJOR for significant omissions (>20%), INFO for minor
            omission_ratio = len(missing) / len(ground_truth)
            if omission_ratio > 0.2:
                severity = Severity.MAJOR
            else:
                severity = Severity.INFO

            # Special case: PROJECT_PRIMER.md with significant omissions
            if doc == "PROJECT_PRIMER.md" and len(missing) >= 3:
                severity = Severity.MAJOR

            findings.append(Finding(
                id=counter.next_id(2),
                level_detected=2,
                severity=severity,
                category=Category.DOC_CONTRADICTION,
                message=f"{doc} omits {len(missing)} validators: {sorted(missing)}",
                file=doc,
                suggested_fix=[
                    f"Add missing validators to {doc}",
                    "Or regenerate if this is a derived document",
                ],
                context={
                    "ground_truth_count": len(ground_truth),
                    "claimed_count": len(claimed),
                    "missing": sorted(missing),
                },
            ))

        # Check for extra validators claimed but not in ground truth
        extra = claimed - ground_truth
        if extra:
            findings.append(Finding(
                id=counter.next_id(2),
                level_detected=2,
                severity=Severity.MAJOR,
                category=Category.DOC_CONTRADICTION,
                message=f"{doc} mentions non-existent validators: {sorted(extra)}",
                file=doc,
                suggested_fix=[
                    f"Remove references to non-existent validators from {doc}",
                    "Or create the missing validator files",
                ],
                context={"extra": sorted(extra)},
            ))

    return findings


def _check_internal_links(
    repo_root: Path,
    rules: dict[str, Any],
    counter: FindingCounter,
    verbose: bool,
) -> list[Finding]:
    """Validate internal links in canonical scope docs only."""
    findings = []
    canonical_scope = rules.get("canonical_scope", [])
    excludes = rules.get("excludes", [])

    # Get canonical files to scan
    files_to_scan: list[Path] = []
    for pattern in canonical_scope:
        if "*" in pattern:
            files_to_scan.extend(repo_root.glob(pattern))
        else:
            path = repo_root / pattern
            if path.exists() and path.suffix == ".md":
                files_to_scan.append(path)

    # Filter out excluded paths
    def is_excluded(path: Path) -> bool:
        rel_path = str(path.relative_to(repo_root))
        for excl in excludes:
            if fnmatch(rel_path, excl):
                return True
        return False

    files_to_scan = [f for f in files_to_scan if not is_excluded(f) and f.is_file()]

    for file_path in files_to_scan:
        links = extract_internal_links(file_path, repo_root)
        rel_path = str(file_path.relative_to(repo_root))

        for link in links:
            if not link["is_valid"]:
                findings.append(Finding(
                    id=counter.next_id(2),
                    level_detected=2,
                    severity=Severity.CRITICAL,
                    category=Category.BROKEN_LINK,
                    message=f"Broken link to '{link['target']}'",
                    file=rel_path,
                    line=link["line"],
                    suggested_fix=[
                        f"Fix or remove link to '{link['target']}'",
                        f"Target resolved to: {link['resolved']}",
                    ],
                ))

    return findings


def _check_meta_yaml(
    repo_root: Path,
    counter: FindingCounter,
    verbose: bool,
) -> list[Finding]:
    """Check META.yaml for drift against reality."""
    findings = []
    meta_path = repo_root / "META.yaml"

    if not meta_path.exists():
        findings.append(Finding(
            id=counter.next_id(2),
            level_detected=2,
            severity=Severity.MINOR,
            category=Category.META_MISMATCH,
            message="META.yaml not found",
            suggested_fix=["Create META.yaml with project metadata"],
        ))
        return findings

    # Try to use existing check_meta_yaml_drift.py
    drift_checker = repo_root / "scripts" / "check_meta_yaml_drift.py"
    if drift_checker.exists():
        try:
            result = subprocess.run(
                [sys.executable, str(drift_checker), str(repo_root)],
                cwd=str(repo_root),
                capture_output=True,
                text=True,
                timeout=30,
            )
            if result.returncode != 0:
                output = result.stdout + result.stderr
                findings.append(Finding(
                    id=counter.next_id(2),
                    level_detected=2,
                    severity=Severity.MINOR,
                    category=Category.META_MISMATCH,
                    message="META.yaml drift detected",
                    file="META.yaml",
                    suggested_fix=["Run: python scripts/check_meta_yaml_drift.py --fix"],
                    context={"output": output[:500]},
                ))
        except Exception as e:
            if verbose:
                print(f"    Warning: could not run META.yaml drift checker: {e}")

    return findings


def _get_commit_lag(repo_root: Path, old_sha: str, new_sha: str) -> int | None:
    """Calculate how many commits old_sha is behind new_sha.

    Returns:
        Number of commits between old_sha and new_sha, or None if can't determine.
    """
    try:
        result = subprocess.run(
            ["git", "rev-list", "--count", f"{old_sha}..{new_sha}"],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0:
            return int(result.stdout.strip())
    except Exception:
        pass
    return None


def _check_generator_drift(
    repo_root: Path,
    rules: dict[str, Any],
    counter: FindingCounter,
    verbose: bool,
    profile: RepoProfile | None = None,
) -> list[Finding]:
    """Check for generator drift in PROJECT_PRIMER.md."""
    findings = []
    primer_path = repo_root / "PROJECT_PRIMER.md"

    if not primer_path.exists():
        return findings

    content = primer_path.read_text()
    generator_rules = rules.get("generator_drift", {}).get("PROJECT_PRIMER.md", {})

    # Extract SHA from primer
    sha_pattern = r'\*\*Repo SHA\*\*:\s*([a-f0-9]+)'
    sha_match = re.search(sha_pattern, content)
    primer_sha = sha_match.group(1) if sha_match else None

    # Get current HEAD SHA
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            timeout=10,
        )
        current_sha = result.stdout.strip() if result.returncode == 0 else None
    except Exception:
        current_sha = None

    # Get allowed SHA lag from config (default 0 = must match exactly)
    allowed_lag = generator_rules.get("allowed_sha_lag_commits", 0)

    # Check if primer is stale
    if primer_sha and current_sha and primer_sha != current_sha:
        # Calculate actual commit lag
        sha_lag = _get_commit_lag(repo_root, primer_sha, current_sha)

        # If within allowed lag, downgrade to INFO
        if sha_lag is not None and sha_lag <= allowed_lag:
            findings.append(Finding(
                id=counter.next_id(2),
                level_detected=2,
                severity=Severity.INFO,
                category=Category.GENERATOR_DRIFT,
                message=f"PROJECT_PRIMER.md is {sha_lag} commit(s) behind HEAD (within allowed lag of {allowed_lag})",
                file="PROJECT_PRIMER.md",
                suggested_fix=[
                    "No action needed - primer SHA lag is within allowed tolerance",
                    f"Current: {current_sha}, Primer: {primer_sha}",
                ],
                context={
                    "primer_sha": primer_sha,
                    "current_sha": current_sha,
                    "sha_lag": sha_lag,
                    "allowed_lag": allowed_lag,
                },
            ))
            # Skip the MAJOR finding below
            primer_sha = None  # Prevent falling through to MAJOR block

    if primer_sha and current_sha and primer_sha != current_sha:
        suspected_causes = generator_rules.get("suspected_causes", [
            "Generator uses hardcoded validator list",
            "Directory walker has filter excluding non-houston validators",
        ])
        investigation_steps = generator_rules.get("investigation_steps", [
            "Check generator source for hardcoded validator patterns",
            "Verify template includes all check_*.py files",
            "Regenerate primer with current generator to confirm",
        ])
        fix_command = generator_rules.get("fix_command", "generate-project-primer")

        findings.append(Finding(
            id=counter.next_id(2),
            level_detected=2,
            severity=Severity.MAJOR,
            category=Category.GENERATOR_DRIFT,
            message=f"PROJECT_PRIMER.md is stale (primer SHA: {primer_sha}, current: {current_sha})",
            file="PROJECT_PRIMER.md",
            suggested_fix=[
                f"Regenerate: {fix_command}",
                "Review generator for hardcoded patterns",
            ],
            context={
                "primer_sha": primer_sha,
                "current_sha": current_sha,
                "suspected_causes": suspected_causes,
                "investigation_steps": investigation_steps,
            },
        ))

    # Check for specific known drift: validators in directory map
    # Only relevant when the repo actually has a validators/ directory
    if profile is not None and not profile.has_validators:
        return findings

    ground_truth = get_available_validators(repo_root)
    primer_validators = extract_validator_list_from_primer(primer_path)

    missing_in_primer = ground_truth - primer_validators
    if missing_in_primer and len(missing_in_primer) >= 2:
        # Find approximate line number of validators section
        line_num = None
        for i, line in enumerate(content.splitlines(), 1):
            if "validators/" in line.lower() and ("├──" in line or "│" in line):
                line_num = i
                break

        findings.append(Finding(
            id=counter.next_id(2),
            level_detected=2,
            severity=Severity.MAJOR,
            category=Category.GENERATOR_DRIFT,
            message=f"PROJECT_PRIMER.md directory map omits {len(missing_in_primer)} validators",
            file="PROJECT_PRIMER.md",
            line=line_num,
            suggested_fix=[
                "Regenerate PROJECT_PRIMER.md with current generator",
                f"Missing validators: {', '.join(sorted(missing_in_primer))}",
            ],
            context={
                "ground_truth_count": len(ground_truth),
                "primer_count": len(primer_validators),
                "missing": sorted(missing_in_primer),
                "suspected_cause": "Generator directory walker may have filter excluding portable validators",
            },
        ))

    return findings
