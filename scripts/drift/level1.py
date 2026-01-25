"""Level 1 drift detection: Fast inventory checks.

Runs in seconds. Checks:
- Top-level directory inventory
- Validator inventory vs README claims
- Schema/taxonomy inventory
- README repo card validation
- Repo contract validation
- Stale path patterns from drift_rules.yaml
"""

from __future__ import annotations

import re
import subprocess
import sys
from fnmatch import fnmatch
from pathlib import Path
from typing import Any

from .models import Category, Finding, FindingCounter, Severity


def run_level1(
    repo_root: Path,
    rules: dict[str, Any],
    counter: FindingCounter,
    verbose: bool = False,
) -> list[Finding]:
    """Run Level 1 drift detection.

    Args:
        repo_root: Repository root path
        rules: Loaded drift_rules.yaml configuration
        counter: Finding ID counter
        verbose: Enable verbose output

    Returns:
        List of findings
    """
    findings: list[Finding] = []

    if verbose:
        print("  Level 1: Fast inventory checks...")

    # 1. Check canonical scope globs for empty matches
    findings.extend(_check_canonical_scope(repo_root, rules, counter, verbose))

    # 2. Validate top-level directories
    findings.extend(_check_top_level_dirs(repo_root, counter, verbose))

    # 3. Check validator inventory
    findings.extend(_check_validator_inventory(repo_root, rules, counter, verbose))

    # 4. Check schema/taxonomy inventory
    findings.extend(_check_schema_inventory(repo_root, counter, verbose))

    # 5. Run stale path pattern checks
    findings.extend(_check_stale_paths(repo_root, rules, counter, verbose))

    # 6. Run repo contract validator (if available)
    findings.extend(_run_repo_contract(repo_root, counter, verbose))

    # 7. Run README repo card validator (if available)
    findings.extend(_run_readme_repo_card(repo_root, counter, verbose))

    return findings


def _check_canonical_scope(
    repo_root: Path,
    rules: dict[str, Any],
    counter: FindingCounter,
    verbose: bool,
) -> list[Finding]:
    """Check that canonical scope globs match files."""
    findings = []
    canonical_scope = rules.get("canonical_scope", [])

    for pattern in canonical_scope:
        if "*" in pattern:
            # Glob pattern
            matches = list(repo_root.glob(pattern))
            if not matches:
                findings.append(Finding(
                    id=counter.next_id(1),
                    level_detected=1,
                    severity=Severity.INFO,
                    category=Category.CONFIG_WARNING,
                    message=f"Canonical scope glob '{pattern}' matches zero files",
                    suggested_fix=[
                        f"Check if pattern '{pattern}' is correct",
                        "Remove pattern if directory doesn't exist",
                    ],
                ))
        else:
            # Exact file
            if not (repo_root / pattern).exists():
                findings.append(Finding(
                    id=counter.next_id(1),
                    level_detected=1,
                    severity=Severity.INFO,
                    category=Category.CONFIG_WARNING,
                    message=f"Canonical scope file '{pattern}' does not exist",
                    suggested_fix=[
                        f"Create file '{pattern}' or remove from canonical_scope",
                    ],
                ))

    return findings


def _check_top_level_dirs(
    repo_root: Path,
    counter: FindingCounter,
    verbose: bool,
) -> list[Finding]:
    """Check that top-level directories follow Betty Protocol."""
    findings = []

    # Allowed top-level directories per Betty Protocol
    allowed_dirs = {
        "00_admin", "00_run", "10_docs", "20_approvals", "20_inbox",
        "20_receipts", "30_config", "40_src", "50_data", "50_reference_reports",
        "60_tests", "70_evidence", "80_evidence_packages", "80_reports",
        "90_archive", "schemas", "protocols", "taxonomies", "validators",
        "scripts", "tests", "examples", "policy", "registry", "docs",
        "workspace",  # Legacy but may still exist
    }

    # Get actual top-level directories
    actual_dirs = {
        d.name for d in repo_root.iterdir()
        if d.is_dir() and not d.name.startswith(".")
    }

    # Check for unexpected directories
    unexpected = actual_dirs - allowed_dirs
    for dir_name in sorted(unexpected):
        findings.append(Finding(
            id=counter.next_id(1),
            level_detected=1,
            severity=Severity.MINOR,
            category=Category.INVENTORY_MISMATCH,
            message=f"Unexpected top-level directory: {dir_name}",
            file=dir_name,
            suggested_fix=[
                f"Move {dir_name}/ to appropriate location per Betty Protocol",
                "Or add to allowed list if intentional",
            ],
        ))

    return findings


def _check_validator_inventory(
    repo_root: Path,
    rules: dict[str, Any],
    counter: FindingCounter,
    verbose: bool,
) -> list[Finding]:
    """Check validator files match __init__.py registry."""
    from .extractors import get_available_validators, get_validator_files

    findings = []

    # Get ground truth from __init__.py
    registered = get_available_validators(repo_root)

    # Get actual files
    actual_files = get_validator_files(repo_root)
    actual_names = {f.replace("check_", "").replace(".py", "") for f in actual_files}

    # Check for unregistered validators
    unregistered = actual_names - registered
    if unregistered:
        findings.append(Finding(
            id=counter.next_id(1),
            level_detected=1,
            severity=Severity.CRITICAL,
            category=Category.INVENTORY_MISMATCH,
            message=f"Validators exist but not in AVAILABLE_VALIDATORS: {sorted(unregistered)}",
            file="validators/__init__.py",
            suggested_fix=[
                "Add missing validators to AVAILABLE_VALIDATORS dict",
                f"Validators to add: {', '.join(sorted(unregistered))}",
            ],
        ))

    # Check for registered but missing files
    missing = registered - actual_names
    if missing:
        findings.append(Finding(
            id=counter.next_id(1),
            level_detected=1,
            severity=Severity.CRITICAL,
            category=Category.INVENTORY_MISMATCH,
            message=f"Validators registered but files missing: {sorted(missing)}",
            file="validators/__init__.py",
            suggested_fix=[
                "Create missing validator files",
                "Or remove from AVAILABLE_VALIDATORS if intentional",
            ],
        ))

    return findings


def _check_schema_inventory(
    repo_root: Path,
    counter: FindingCounter,
    verbose: bool,
) -> list[Finding]:
    """Check schema and taxonomy directories exist and have files."""
    findings = []

    for dir_name in ["schemas", "taxonomies"]:
        dir_path = repo_root / dir_name
        if not dir_path.exists():
            findings.append(Finding(
                id=counter.next_id(1),
                level_detected=1,
                severity=Severity.MAJOR,
                category=Category.INVENTORY_MISMATCH,
                message=f"Missing {dir_name}/ directory",
                suggested_fix=[f"Create {dir_name}/ directory with appropriate files"],
            ))
        else:
            yaml_files = list(dir_path.glob("*.yaml")) + list(dir_path.glob("*.yml"))
            json_files = list(dir_path.glob("*.json"))
            if not yaml_files and not json_files:
                findings.append(Finding(
                    id=counter.next_id(1),
                    level_detected=1,
                    severity=Severity.MINOR,
                    category=Category.INVENTORY_MISMATCH,
                    message=f"{dir_name}/ directory is empty",
                    file=dir_name,
                    suggested_fix=[f"Add schema/taxonomy files to {dir_name}/"],
                ))

    return findings


def _check_stale_paths(
    repo_root: Path,
    rules: dict[str, Any],
    counter: FindingCounter,
    verbose: bool,
) -> list[Finding]:
    """Check for stale path patterns in canonical docs."""
    from .extractors import check_path_context

    findings = []
    stale_patterns = rules.get("stale_path_patterns", [])
    canonical_scope = rules.get("canonical_scope", [])
    excludes = rules.get("excludes", [])

    # Get canonical files to scan
    files_to_scan: list[Path] = []
    for pattern in canonical_scope:
        if "*" in pattern:
            files_to_scan.extend(repo_root.glob(pattern))
        else:
            path = repo_root / pattern
            if path.exists():
                files_to_scan.append(path)

    # Filter out excluded paths
    def is_excluded(path: Path) -> bool:
        rel_path = str(path.relative_to(repo_root))
        for excl in excludes:
            if fnmatch(rel_path, excl):
                return True
        return False

    files_to_scan = [f for f in files_to_scan if not is_excluded(f)]

    for file_path in files_to_scan:
        if not file_path.is_file():
            continue

        try:
            content = file_path.read_text()
        except Exception:
            continue

        for rule in stale_patterns:
            pattern = rule.get("pattern", "")
            if not pattern:
                continue

            severity_str = rule.get("severity", "MINOR")
            severity = Severity[severity_str]
            check_exists = rule.get("check_exists", False)
            require_path_context = rule.get("require_path_context", False)
            replacement = rule.get("replacement", "")

            # Check exists condition
            if check_exists:
                replacement_path = repo_root / replacement.rstrip("/")
                if not replacement_path.exists():
                    continue  # Skip rule if replacement doesn't exist

            try:
                regex = re.compile(pattern)
            except re.error:
                continue

            for line_num, line in enumerate(content.splitlines(), 1):
                for match in regex.finditer(line):
                    # Check path context if required
                    if require_path_context:
                        if not check_path_context(line, match.start(), match.end()):
                            continue

                    rel_path = str(file_path.relative_to(repo_root))
                    findings.append(Finding(
                        id=counter.next_id(1),
                        level_detected=1,
                        severity=severity,
                        category=Category.STALE_PATH,
                        message=rule.get("message", f"Stale path pattern: {pattern}"),
                        file=rel_path,
                        line=line_num,
                        suggested_fix=rule.get("suggested_fix", []),
                        context={"matched": match.group(0), "replacement": replacement},
                    ))

    return findings


def _run_repo_contract(
    repo_root: Path,
    counter: FindingCounter,
    verbose: bool,
) -> list[Finding]:
    """Run the repo contract validator if available."""
    findings = []
    validator_path = repo_root / "validators" / "check_repo_contract.py"

    if not validator_path.exists():
        return findings

    try:
        result = subprocess.run(
            [sys.executable, str(validator_path)],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.returncode != 0:
            # Extract error messages from output
            output = result.stdout + result.stderr
            findings.append(Finding(
                id=counter.next_id(1),
                level_detected=1,
                severity=Severity.MAJOR,
                category=Category.INVENTORY_MISMATCH,
                message="Repo contract validation failed",
                file="validators/check_repo_contract.py",
                suggested_fix=["Review validator output and fix issues"],
                context={"output": output[:500]},  # Truncate long output
            ))
    except subprocess.TimeoutExpired:
        if verbose:
            print("    Warning: repo contract validator timed out")
    except Exception as e:
        if verbose:
            print(f"    Warning: could not run repo contract validator: {e}")

    return findings


def _run_readme_repo_card(
    repo_root: Path,
    counter: FindingCounter,
    verbose: bool,
) -> list[Finding]:
    """Run the README repo card validator if available."""
    findings = []
    validator_path = repo_root / "scripts" / "validate_readme_repo_card.py"

    if not validator_path.exists():
        return findings

    try:
        result = subprocess.run(
            [sys.executable, str(validator_path), str(repo_root)],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.returncode != 0:
            output = result.stdout + result.stderr
            findings.append(Finding(
                id=counter.next_id(1),
                level_detected=1,
                severity=Severity.MAJOR,
                category=Category.BROKEN_LINK,
                message="README repo card validation failed",
                file="README.md",
                suggested_fix=["Fix README repo card issues"],
                context={"output": output[:500]},
            ))
    except subprocess.TimeoutExpired:
        if verbose:
            print("    Warning: README repo card validator timed out")
    except Exception as e:
        if verbose:
            print(f"    Warning: could not run README repo card validator: {e}")

    return findings
