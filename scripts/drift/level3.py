"""Level 3 drift detection: Deep dive + archive candidates.

Runs in minutes. Checks:
- Reference graph for canonical docs
- Orphan candidates (with safety rules)
- Misplaced artifacts
- Archive plan generation
"""

from __future__ import annotations

import subprocess
from datetime import datetime, timedelta
from fnmatch import fnmatch
from pathlib import Path
from typing import Any

from .extractors import extract_internal_links, extract_path_references
from .models import Category, Finding, FindingCounter, Severity


def run_level3(
    repo_root: Path,
    rules: dict[str, Any],
    counter: FindingCounter,
    verbose: bool = False,
) -> list[Finding]:
    """Run Level 3 drift detection.

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
        print("  Level 3: Deep dive + archive candidates...")

    # 1. Build reference graph
    ref_graph, reverse_graph = _build_reference_graph(repo_root, rules, verbose)

    # 2. Identify orphan candidates
    findings.extend(_find_orphan_candidates(repo_root, rules, reverse_graph, counter, verbose))

    # 3. Identify misplaced artifacts
    findings.extend(_find_misplaced_artifacts(repo_root, rules, counter, verbose))

    return findings


def _build_reference_graph(
    repo_root: Path,
    rules: dict[str, Any],
    verbose: bool,
) -> tuple[dict[str, set[str]], dict[str, set[str]]]:
    """Build a reference graph for all markdown files.

    Returns:
        Tuple of (forward_graph, reverse_graph)
        forward_graph: file -> set of files it references
        reverse_graph: file -> set of files that reference it
    """
    canonical_scope = rules.get("canonical_scope", [])
    excludes = rules.get("excludes", [])

    # Get all markdown files in canonical scope
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

    forward_graph: dict[str, set[str]] = {}
    reverse_graph: dict[str, set[str]] = {}

    for file_path in files_to_scan:
        rel_path = str(file_path.relative_to(repo_root))
        forward_graph[rel_path] = set()

        # Get links
        links = extract_internal_links(file_path, repo_root)
        for link in links:
            target = link["target"]
            # Normalize target path
            if not target.startswith("/"):
                # Resolve relative to file's directory
                resolved = (file_path.parent / target).resolve()
                try:
                    target = str(resolved.relative_to(repo_root))
                except ValueError:
                    continue

            forward_graph[rel_path].add(target)

            # Update reverse graph
            if target not in reverse_graph:
                reverse_graph[target] = set()
            reverse_graph[target].add(rel_path)

        # Also check path references
        refs = extract_path_references(file_path, repo_root)
        for ref in refs:
            target = ref["path"]
            forward_graph[rel_path].add(target)

            if target not in reverse_graph:
                reverse_graph[target] = set()
            reverse_graph[target].add(rel_path)

    return forward_graph, reverse_graph


def _find_orphan_candidates(
    repo_root: Path,
    rules: dict[str, Any],
    reverse_graph: dict[str, set[str]],
    counter: FindingCounter,
    verbose: bool,
) -> list[Finding]:
    """Find orphan candidates that might be archivable.

    Safety rules:
    - Must have NO inbound references from canonical docs
    - Must match a candidate class
    - Must NOT be in protected paths
    - Tags low-confidence items as "manual review required"
    """
    findings = []
    protected = rules.get("protected_from_archive", [])
    archive_rules = rules.get("archive_candidates", {})
    candidate_classes = archive_rules.get("candidate_classes", [])
    min_age_days = archive_rules.get("min_age_days", 90)

    def is_protected(rel_path: str) -> bool:
        for pattern in protected:
            if fnmatch(rel_path, pattern):
                return True
        return False

    def get_file_age_days(path: Path) -> int:
        """Get file age in days from last modification."""
        try:
            mtime = datetime.fromtimestamp(path.stat().st_mtime)
            return (datetime.now() - mtime).days
        except Exception:
            return 0

    def matches_candidate_class(rel_path: str) -> tuple[bool, str]:
        """Check if file matches a candidate class and return description."""
        for cc in candidate_classes:
            pattern = cc.get("path_pattern", "")
            excludes = cc.get("exclude", [])

            if fnmatch(rel_path, pattern):
                # Check excludes
                excluded = False
                for excl in excludes:
                    if fnmatch(rel_path, excl):
                        excluded = True
                        break
                if not excluded:
                    return True, cc.get("description", "Matched candidate class")

        return False, ""

    # Scan for candidate files
    all_md_files = list(repo_root.rglob("*.md"))

    for file_path in all_md_files:
        rel_path = str(file_path.relative_to(repo_root))

        # Skip protected paths
        if is_protected(rel_path):
            continue

        # Check if file has inbound references
        inbound_refs = reverse_graph.get(rel_path, set())
        if inbound_refs:
            continue  # Has references, not an orphan

        # Check if matches candidate class
        matches, description = matches_candidate_class(rel_path)
        if not matches:
            continue  # Doesn't match any candidate class

        # Check file age
        age_days = get_file_age_days(file_path)
        age_threshold_met = age_days >= min_age_days

        # Determine confidence
        if age_threshold_met:
            confidence = "high"
            requires_review = False
        else:
            confidence = "low"
            requires_review = True

        findings.append(Finding(
            id=counter.next_id(3),
            level_detected=3,
            severity=Severity.INFO,
            category=Category.ORPHAN_CANDIDATE,
            message=f"Orphan candidate: {rel_path}",
            file=rel_path,
            suggested_fix=[
                "Review if file is still needed",
                "If obsolete, move to 90_archive/",
                "If needed, add reference from canonical doc",
            ],
            confidence=confidence,
            requires_review=requires_review,
            context={
                "candidate_class": description,
                "age_days": age_days,
                "age_threshold": min_age_days,
                "inbound_refs": list(inbound_refs),
            },
        ))

    return findings


def _find_misplaced_artifacts(
    repo_root: Path,
    rules: dict[str, Any],
    counter: FindingCounter,
    verbose: bool,
) -> list[Finding]:
    """Find misplaced artifacts that should be elsewhere per Betty Protocol."""
    findings = []
    protected = rules.get("protected_from_archive", [])

    def is_protected(rel_path: str) -> bool:
        for pattern in protected:
            if fnmatch(rel_path, pattern):
                return True
        return False

    # Check for non-Python files in validators/ (except allowed ones)
    validators_dir = repo_root / "validators"
    if validators_dir.exists():
        allowed_non_py = {"README.md", "__init__.py", "__pycache__"}
        for item in validators_dir.iterdir():
            if item.is_file():
                if not item.suffix == ".py" and item.name not in allowed_non_py:
                    rel_path = str(item.relative_to(repo_root))
                    if not is_protected(rel_path):
                        findings.append(Finding(
                            id=counter.next_id(3),
                            level_detected=3,
                            severity=Severity.MINOR,
                            category=Category.MISPLACED_ARTIFACT,
                            message=f"Non-Python file in validators/: {item.name}",
                            file=rel_path,
                            suggested_fix=[
                                f"Move {item.name} to appropriate location",
                                "validators/ should only contain Python validators",
                            ],
                        ))

    # Check for config files outside 30_config/
    config_extensions = {".json", ".yaml", ".yml", ".toml", ".ini"}
    config_allowed_locations = {"30_config", "schemas", "taxonomies", "policy", "examples"}

    for ext in config_extensions:
        for config_file in repo_root.glob(f"*{ext}"):
            if config_file.is_file():
                # Skip root-level configs that are allowed
                if config_file.name in {"pyproject.toml", "package.json", "META.yaml",
                                         "RELATIONS.yaml", "glossary.yaml"}:
                    continue

                rel_path = str(config_file.relative_to(repo_root))
                parent = config_file.parent.name if config_file.parent != repo_root else ""

                if parent not in config_allowed_locations and not is_protected(rel_path):
                    # This is a potential misplacement, but may be intentional
                    findings.append(Finding(
                        id=counter.next_id(3),
                        level_detected=3,
                        severity=Severity.INFO,
                        category=Category.MISPLACED_ARTIFACT,
                        message=f"Config file at root level: {config_file.name}",
                        file=rel_path,
                        suggested_fix=[
                            f"Consider moving {config_file.name} to 30_config/",
                            "Or leave if root-level placement is intentional",
                        ],
                        confidence="low",
                        requires_review=True,
                    ))

    return findings
