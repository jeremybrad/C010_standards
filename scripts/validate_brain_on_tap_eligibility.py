#!/usr/bin/env python3
"""Validate repos for Brain on Tap (BBOT) eligibility.

Checks:
1. README repo card block present and valid
2. Registry entry exists in repos.yaml
3. Required BBOT fields: repo_id, name, bot_active, path_rel
4. bot_active is boolean (not string)
5. path_rel is relative (no absolute paths)

Usage:
    python scripts/validate_brain_on_tap_eligibility.py C010_standards
    python scripts/validate_brain_on_tap_eligibility.py C010_standards --verbose
    python scripts/validate_brain_on_tap_eligibility.py C010_standards C017_brain-on-tap

Exit codes:
    0 - All repos pass
    1 - Validation errors
    2 - Configuration/file error

Requirements:
    PyYAML (pip install pyyaml)
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML required. Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(2)


# Required fields for BBOT eligibility
BBOT_REQUIRED_FIELDS = {"repo_id", "name", "bot_active", "path_rel"}

# README repo card markers (from validate_readme_repo_card.py)
START_MARKER = "<!-- BOT:repo_card:start -->"
END_MARKER = "<!-- BOT:repo_card:end -->"

REQUIRED_HEADINGS = [
    "What this repo is",
    "What it is not",
    "When to use it",
    "Entry points",
    "Core architecture",
    "Interfaces and contracts",
    "Common workflows",
    "Footguns and gotchas",
    "Related repos",
    "Provenance",
]


def find_repo_root(start: Path) -> Path | None:
    """Find C010_standards repo root by looking for registry/repos.yaml."""
    current = start.resolve()
    for _ in range(10):  # Max depth
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


def validate_readme_repo_card(repo_path: Path, verbose: bool = False) -> list[str]:
    """Validate README.md has a valid repo card block.

    Returns list of error messages (empty = pass).
    """
    errors = []
    readme_path = repo_path / "README.md"

    if not readme_path.exists():
        errors.append("README.md not found")
        return errors

    readme_text = readme_path.read_text(encoding="utf-8")

    # Check markers
    start_count = readme_text.count(START_MARKER)
    end_count = readme_text.count(END_MARKER)

    if start_count == 0:
        errors.append(f"Missing start marker: {START_MARKER}")
        return errors

    if end_count == 0:
        errors.append(f"Missing end marker: {END_MARKER}")
        return errors

    if start_count > 1:
        errors.append(f"Multiple start markers ({start_count})")
        return errors

    if end_count > 1:
        errors.append(f"Multiple end markers ({end_count})")
        return errors

    # Extract block
    start_idx = readme_text.find(START_MARKER)
    end_idx = readme_text.find(END_MARKER)

    if end_idx <= start_idx:
        errors.append("End marker before start marker")
        return errors

    block_content = readme_text[start_idx + len(START_MARKER):end_idx].strip()

    if verbose:
        print(f"  README: found repo card block ({len(block_content)} chars)")

    # Check required headings
    missing = []
    for heading in REQUIRED_HEADINGS:
        pattern = rf"^##\s+{re.escape(heading)}\s*$"
        if not re.search(pattern, block_content, re.MULTILINE | re.IGNORECASE):
            missing.append(heading)

    if missing:
        errors.append(f"Missing headings: {', '.join(missing)}")

    if verbose and not missing:
        print(f"  README: all 10 required headings present")

    return errors


def validate_registry_entry(
    repo_id: str,
    registry_data: dict,
    verbose: bool = False
) -> tuple[list[str], list[str]]:
    """Validate registry entry for BBOT eligibility.

    Returns (errors, warnings).
    """
    errors = []
    warnings = []

    repos = registry_data.get("repos", [])
    entry = None

    for r in repos:
        if r.get("repo_id") == repo_id:
            entry = r
            break

    if entry is None:
        errors.append(f"No registry entry for repo_id='{repo_id}'")
        return errors, warnings

    if verbose:
        print(f"  Registry: found entry for {repo_id}")

    # Check required BBOT fields
    for field in BBOT_REQUIRED_FIELDS:
        if field not in entry:
            errors.append(f"Missing required field: {field}")

    # Validate bot_active is boolean
    bot_active = entry.get("bot_active")
    if bot_active is not None:
        if not isinstance(bot_active, bool):
            errors.append(
                f"bot_active must be boolean, got {type(bot_active).__name__}: {bot_active!r}"
            )
        elif verbose:
            print(f"  Registry: bot_active={bot_active}")

    # Validate path_rel is relative
    path_rel = entry.get("path_rel")
    if path_rel is not None:
        if not isinstance(path_rel, str):
            errors.append(f"path_rel must be string, got {type(path_rel).__name__}")
        else:
            # Check for absolute path patterns
            absolute_patterns = [
                (path_rel.startswith("/"), "starts with /"),
                (path_rel.startswith("~"), "starts with ~"),
                (path_rel.startswith("./"), "starts with ./"),
                (len(path_rel) > 1 and path_rel[1] == ":", "contains drive letter (C:)"),
            ]
            for is_match, reason in absolute_patterns:
                if is_match:
                    errors.append(f"path_rel must be relative: {path_rel!r} ({reason})")
                    break

            if verbose and not errors:
                print(f"  Registry: path_rel={path_rel!r} (relative)")

    # Advisory checks (warnings)
    advisory_fields = ["onboarding", "entry_points", "tags", "commands"]
    missing_advisory = [f for f in advisory_fields if f not in entry]
    if missing_advisory:
        warnings.append(f"Missing SHOULD fields: {', '.join(missing_advisory)}")

    return errors, warnings


def validate_repo(
    repo_id: str,
    repo_path: Path,
    registry_data: dict,
    verbose: bool = False
) -> tuple[list[str], list[str]]:
    """Full BBOT eligibility validation for a repo.

    Returns (errors, warnings).
    """
    all_errors = []
    all_warnings = []

    if verbose:
        print(f"\nValidating {repo_id}...")

    # 1. Check README repo card
    readme_errors = validate_readme_repo_card(repo_path, verbose)
    for err in readme_errors:
        all_errors.append(f"README: {err}")

    # 2. Check registry entry
    reg_errors, reg_warnings = validate_registry_entry(repo_id, registry_data, verbose)
    all_errors.extend(reg_errors)
    all_warnings.extend(reg_warnings)

    return all_errors, all_warnings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate repos for Brain on Tap (BBOT) eligibility"
    )
    parser.add_argument(
        "repo_ids",
        nargs="+",
        help="Repo IDs to validate (e.g., C010_standards)"
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

    # Validate each repo
    results = {}
    for repo_id in args.repo_ids:
        repo_path = workspace / repo_id
        if not repo_path.is_dir():
            print(f"ERROR: Repo not found: {repo_path}", file=sys.stderr)
            results[repo_id] = (["Repo directory not found"], [])
            continue

        errors, warnings = validate_repo(repo_id, repo_path, registry_data, args.verbose)
        results[repo_id] = (errors, warnings)

    # Print summary
    print("\n" + "=" * 60)
    print("BRAIN ON TAP ELIGIBILITY REPORT")
    print("=" * 60)

    any_failures = False
    for repo_id in args.repo_ids:
        errors, warnings = results[repo_id]

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
    if any_failures:
        failed = sum(1 for e, _ in results.values() if e)
        print(f"Result: {failed}/{len(args.repo_ids)} repos FAILED eligibility")
        return 1
    else:
        print(f"Result: {len(args.repo_ids)}/{len(args.repo_ids)} repos ELIGIBLE")
        return 0


if __name__ == "__main__":
    sys.exit(main())
