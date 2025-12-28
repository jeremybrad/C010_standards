#!/usr/bin/env python3
"""Validate README.md repo card blocks against C010 standard.

Checks:
- README.md exists at repo root
- Exactly one BOT:repo_card block present
- All 10 required headings inside block
- Provenance section contains version info

Usage:
    python validate_readme_repo_card.py /path/to/repo
    python validate_readme_repo_card.py /path/to/repo --strict
    python validate_readme_repo_card.py /path/to/repo --verbose
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# Required headings inside repo card block
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

START_MARKER = "<!-- BOT:repo_card:start -->"
END_MARKER = "<!-- BOT:repo_card:end -->"


def extract_repo_card_block(readme_text: str) -> tuple[str | None, list[str]]:
    """Extract repo card block from README text.

    Returns:
        Tuple of (block_content, errors)
    """
    errors = []

    start_count = readme_text.count(START_MARKER)
    end_count = readme_text.count(END_MARKER)

    if start_count == 0:
        errors.append(f"Missing start marker: {START_MARKER}")
        return None, errors

    if end_count == 0:
        errors.append(f"Missing end marker: {END_MARKER}")
        return None, errors

    if start_count > 1:
        errors.append(f"Multiple start markers found ({start_count}). Expected exactly 1.")
        return None, errors

    if end_count > 1:
        errors.append(f"Multiple end markers found ({end_count}). Expected exactly 1.")
        return None, errors

    # Extract content between markers
    start_idx = readme_text.find(START_MARKER)
    end_idx = readme_text.find(END_MARKER)

    if end_idx <= start_idx:
        errors.append("End marker appears before start marker")
        return None, errors

    block_content = readme_text[start_idx + len(START_MARKER):end_idx]
    return block_content.strip(), errors


def check_required_headings(block_content: str) -> tuple[list[str], list[str]]:
    """Check for required headings in block content.

    Returns:
        Tuple of (missing_headings, found_headings)
    """
    missing = []
    found = []

    for heading in REQUIRED_HEADINGS:
        # Match ## heading (case-insensitive)
        pattern = rf"^##\s+{re.escape(heading)}\s*$"
        if re.search(pattern, block_content, re.MULTILINE | re.IGNORECASE):
            found.append(heading)
        else:
            missing.append(heading)

    return missing, found


def check_provenance_content(block_content: str) -> list[str]:
    """Check provenance section for required fields.

    Returns:
        List of warnings (not errors)
    """
    warnings = []

    # Find provenance section
    provenance_match = re.search(
        r"^##\s+Provenance\s*$(.+?)(?=^##|\Z)",
        block_content,
        re.MULTILINE | re.IGNORECASE | re.DOTALL
    )

    if not provenance_match:
        return warnings  # Already caught by missing heading check

    provenance_text = provenance_match.group(1).lower()

    if "version" not in provenance_text:
        warnings.append("Provenance section missing 'Version' field")

    if "git sha" not in provenance_text and "sha" not in provenance_text:
        warnings.append("Provenance section missing 'Git SHA' field")

    return warnings


def validate_readme_repo_card(
    repo_path: Path,
    strict: bool = False,
    verbose: bool = False
) -> int:
    """Validate README.md repo card block.

    Args:
        repo_path: Path to repository root
        strict: Treat warnings as errors
        verbose: Print detailed output

    Returns:
        Exit code (0 = pass, 1 = fail)
    """
    errors = []
    warnings = []
    repo_name = repo_path.name

    # Check README exists
    readme_path = repo_path / "README.md"
    if not readme_path.exists():
        print(f"ERROR: {repo_name}: README.md not found")
        return 1

    if verbose:
        print(f"Checking {repo_name}/README.md...")

    readme_text = readme_path.read_text(encoding="utf-8")

    # Extract repo card block
    block_content, block_errors = extract_repo_card_block(readme_text)
    errors.extend(block_errors)

    if block_content is None:
        # Can't continue without block
        for error in errors:
            print(f"ERROR: {repo_name}: {error}")
        return 1

    if verbose:
        print(f"  Found repo card block ({len(block_content)} chars)")

    # Check required headings
    missing, found = check_required_headings(block_content)

    if verbose:
        print(f"  Found {len(found)}/10 required headings")

    for heading in missing:
        errors.append(f"Missing required heading: ## {heading}")

    # Check provenance content
    provenance_warnings = check_provenance_content(block_content)
    warnings.extend(provenance_warnings)

    # Report results
    if errors:
        for error in errors:
            print(f"ERROR: {repo_name}: {error}")

    if warnings:
        for warning in warnings:
            print(f"WARNING: {repo_name}: {warning}")

    # Determine exit code
    if errors:
        print(f"FAIL: {repo_name}")
        return 1

    if warnings and strict:
        print(f"FAIL: {repo_name} (strict mode)")
        return 1

    print(f"PASS: {repo_name}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate README.md repo card blocks"
    )
    parser.add_argument(
        "repo_path",
        type=Path,
        help="Path to repository root"
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat warnings as errors"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Print detailed output"
    )

    args = parser.parse_args()

    if not args.repo_path.is_dir():
        print(f"ERROR: Not a directory: {args.repo_path}")
        return 1

    return validate_readme_repo_card(
        args.repo_path,
        strict=args.strict,
        verbose=args.verbose
    )


if __name__ == "__main__":
    sys.exit(main())
