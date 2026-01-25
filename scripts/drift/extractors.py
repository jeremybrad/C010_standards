"""Document parsing utilities for extracting inventories and references.

Provides functions to extract validator lists, links, and path references
from various canonical document formats.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any


def get_available_validators(repo_root: Path) -> set[str]:
    """Extract ground truth validator list from validators/__init__.py.

    Args:
        repo_root: Repository root path

    Returns:
        Set of validator CLI names (e.g., {"houston_docmeta", "repo_contract", ...})
    """
    init_path = repo_root / "validators" / "__init__.py"
    if not init_path.exists():
        return set()

    content = init_path.read_text()
    validators = set()

    # Match lines like: "houston_docmeta": "check_houston_docmeta",
    pattern = r'"(\w+)":\s*"check_\w+"'
    for match in re.finditer(pattern, content):
        validators.add(match.group(1))

    return validators


def get_validator_files(repo_root: Path) -> set[str]:
    """Get actual validator Python files from validators/ directory.

    Args:
        repo_root: Repository root path

    Returns:
        Set of validator file basenames (e.g., {"check_houston_docmeta.py", ...})
    """
    validators_dir = repo_root / "validators"
    if not validators_dir.exists():
        return set()

    return {
        f.name for f in validators_dir.glob("check_*.py")
    }


def extract_validator_list_from_readme(readme_path: Path) -> set[str]:
    """Extract validator names mentioned in README.md.

    Looks for patterns like:
    - `python validators/check_houston_docmeta.py`
    - `check_repo_contract`
    - validator mentions in tables

    Args:
        readme_path: Path to README.md

    Returns:
        Set of validator names found
    """
    if not readme_path.exists():
        return set()

    content = readme_path.read_text()
    validators = set()

    # Pattern 1: python validators/check_*.py mentions
    for match in re.finditer(r'validators/check_(\w+)\.py', content):
        validators.add(match.group(1))

    # Pattern 2: check_* module mentions
    for match in re.finditer(r'\bcheck_(\w+)\b', content):
        name = match.group(1)
        # Filter out non-validator mentions and partial captures from wildcards
        if name not in {"exists", "your", "that", "if", "for", "this", "the"}:
            # Skip partial captures that end with _ (from wildcards like check_houston_*.py)
            if not name.endswith("_"):
                validators.add(name)

    return validators


def extract_validator_list_from_claude(claude_path: Path) -> set[str]:
    """Extract validator names from CLAUDE.md.

    Looks for the "Available Validators" section with lines like:
    - `houston_docmeta` - Document metadata validation

    Args:
        claude_path: Path to CLAUDE.md

    Returns:
        Set of validator CLI names found
    """
    if not claude_path.exists():
        return set()

    content = claude_path.read_text()
    validators = set()

    # Look for Available Validators section
    in_section = False
    for line in content.splitlines():
        if "Available Validators" in line:
            in_section = True
            continue
        if in_section:
            # End section on next header
            if line.startswith("#") or line.startswith("**"):
                if "validator" not in line.lower():
                    break
            # Match: - `validator_name` - description
            match = re.match(r'^\s*-\s*`(\w+)`\s*-', line)
            if match:
                validators.add(match.group(1))

    # Also check for check_*.py patterns
    for match in re.finditer(r'check_(\w+)\.py', content):
        validators.add(match.group(1))

    return validators


def extract_validator_list_from_validators_readme(readme_path: Path) -> set[str]:
    """Extract validator names from validators/README.md.

    Looks for table rows like:
    | `houston_docmeta` | `check_houston_docmeta.py` | ...

    Args:
        readme_path: Path to validators/README.md

    Returns:
        Set of validator CLI names found
    """
    if not readme_path.exists():
        return set()

    content = readme_path.read_text()
    validators = set()

    # Pattern 1: Table format | `name` | `check_name.py` |
    for match in re.finditer(r'\|\s*`(\w+)`\s*\|\s*`check_\w+\.py`', content):
        validators.add(match.group(1))

    # Pattern 2: check_*.py mentions
    for match in re.finditer(r'check_(\w+)\.py', content):
        validators.add(match.group(1))

    return validators


def extract_validator_list_from_standards_guide(guide_path: Path) -> set[str]:
    """Extract validator names from STANDARDS_GUIDE.md.

    Args:
        guide_path: Path to STANDARDS_GUIDE.md

    Returns:
        Set of validator names found
    """
    if not guide_path.exists():
        return set()

    content = guide_path.read_text()
    validators = set()

    # Pattern: check_*.py mentions
    for match in re.finditer(r'check_(\w+)\.py', content):
        validators.add(match.group(1))

    return validators


def extract_validator_list_from_primer(primer_path: Path) -> set[str]:
    """Extract validator names from PROJECT_PRIMER.md directory map.

    Looks for directory tree entries like:
    │   ├── check_houston_docmeta.py

    Args:
        primer_path: Path to PROJECT_PRIMER.md

    Returns:
        Set of validator names found
    """
    if not primer_path.exists():
        return set()

    content = primer_path.read_text()
    validators = set()

    # Pattern: Directory tree entries with check_*.py
    for match in re.finditer(r'check_(\w+)\.py', content):
        validators.add(match.group(1))

    return validators


def extract_internal_links(file_path: Path, repo_root: Path) -> list[dict[str, Any]]:
    """Extract internal links from a markdown file.

    Args:
        file_path: Path to the markdown file
        repo_root: Repository root for resolving relative paths

    Returns:
        List of dicts with keys: target, line, column, is_valid
    """
    if not file_path.exists():
        return []

    content = file_path.read_text()
    links = []
    in_code_block = False

    # Pattern for markdown links: [text](target)
    link_pattern = r'\[([^\]]*)\]\(([^)]+)\)'

    for line_num, line in enumerate(content.splitlines(), 1):
        # Track code block state (``` or ~~~)
        stripped = line.strip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_code_block = not in_code_block
            continue

        # Skip lines inside code blocks
        if in_code_block:
            continue

        for match in re.finditer(link_pattern, line):
            target = match.group(2)

            # Skip external URLs
            if target.startswith(("http://", "https://", "mailto:")):
                continue

            # Skip anchors only
            if target.startswith("#"):
                continue

            # Remove anchor from target
            target_path = target.split("#")[0]
            if not target_path:
                continue

            # Resolve relative path
            if target_path.startswith("/"):
                resolved = repo_root / target_path.lstrip("/")
            else:
                resolved = file_path.parent / target_path

            links.append({
                "target": target_path,
                "line": line_num,
                "column": match.start(),
                "resolved": str(resolved),
                "is_valid": resolved.exists(),
            })

    return links


def extract_path_references(file_path: Path, repo_root: Path) -> list[dict[str, Any]]:
    """Extract path references from a file (not just links).

    Looks for paths in backticks, code blocks, and plain text.

    Args:
        file_path: Path to the file
        repo_root: Repository root for resolving paths

    Returns:
        List of dicts with keys: path, line, context
    """
    if not file_path.exists():
        return []

    content = file_path.read_text()
    references = []

    # Pattern for paths: backticked paths or bare paths with /
    # Match: `path/to/file.md` or paths/with/slashes
    path_pattern = r'`([^`]+/[^`]+)`|(?<![a-zA-Z])([a-zA-Z0-9_-]+/[a-zA-Z0-9_/./-]+)'

    for line_num, line in enumerate(content.splitlines(), 1):
        for match in re.finditer(path_pattern, line):
            path_str = match.group(1) or match.group(2)
            if not path_str:
                continue

            # Skip URLs
            if path_str.startswith(("http://", "https://")):
                continue

            # Skip common false positives
            if path_str in ("and/or", "w/", "n/a"):
                continue

            references.append({
                "path": path_str,
                "line": line_num,
                "in_backticks": match.group(1) is not None,
            })

    return references


def check_path_context(line: str, match_start: int, match_end: int) -> bool:
    """Check if a path match is in a path-like context.

    Returns True if the match is in backticks or adjacent to path-like chars.

    Args:
        line: The full line of text
        match_start: Start index of the match
        match_end: End index of the match

    Returns:
        True if the match is in a path-like context
    """
    # Check for backticks around the match
    before = line[:match_start]
    after = line[match_end:]

    # In backticks?
    if before.count("`") % 2 == 1:  # Odd number of backticks before = inside backticks
        return True

    # Adjacent to path chars?
    if match_start > 0 and line[match_start - 1] in "/\\.":
        return True
    if match_end < len(line) and line[match_end] in "/\\.":
        return True

    # After a markdown link syntax
    if before.rstrip().endswith("]("):
        return True

    return False
