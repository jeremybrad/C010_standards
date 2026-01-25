#!/usr/bin/env python3
"""Validator for Windows filename compatibility.

Checks that filenames are compatible with Windows filesystem constraints.
This validator can scan any directory and report Windows-incompatible names.

Windows filename restrictions:
- Reserved characters: \\ / : * ? " < > |
- Reserved names: CON, PRN, AUX, NUL, COM1-9, LPT1-9
- No trailing dots or spaces
- No control characters (0x00-0x1F)
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from validators.common import safe_print

# Windows reserved characters (cannot appear anywhere in filename)
RESERVED_CHARS = set('\\/:*?"<>|')

# Windows reserved names (case-insensitive, with or without extension)
RESERVED_NAMES = {
    "CON", "PRN", "AUX", "NUL",
    "COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9",
    "LPT1", "LPT2", "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9",
}

# Control characters (0x00-0x1F)
CONTROL_CHAR_PATTERN = re.compile(r'[\x00-\x1f]')


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate filenames for Windows compatibility"
    )
    parser.add_argument(
        "path",
        type=Path,
        nargs="?",
        default=None,
        help="Path to scan (default: current directory)",
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Show detailed output"
    )
    parser.add_argument(
        "--json-output",
        type=Path,
        default=None,
        help="Write results to JSON file",
    )
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Attempt to fix issues (rename files)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what --fix would do without making changes",
    )
    parser.add_argument(
        "--exclude",
        action="append",
        default=[],
        help="Exclude paths matching pattern (can specify multiple)",
    )
    return parser.parse_args(argv)


def is_reserved_name(name: str) -> bool:
    """Check if filename is a Windows reserved name."""
    # Get name without extension
    base = name.split(".")[0].upper()
    return base in RESERVED_NAMES


def has_reserved_chars(name: str) -> list[str]:
    """Return list of reserved characters found in filename."""
    return [c for c in name if c in RESERVED_CHARS]


def has_control_chars(name: str) -> bool:
    """Check if filename contains control characters."""
    return bool(CONTROL_CHAR_PATTERN.search(name))


def has_trailing_dot_or_space(name: str) -> bool:
    """Check if filename ends with dot or space."""
    return name.endswith(".") or name.endswith(" ")


class Issue:
    """Represents a Windows filename compatibility issue."""

    def __init__(
        self, path: Path, issue_type: str, details: str, suggested_fix: str | None = None
    ):
        self.path = path
        self.issue_type = issue_type
        self.details = details
        self.suggested_fix = suggested_fix

    def to_dict(self) -> dict:
        return {
            "path": str(self.path),
            "issue_type": self.issue_type,
            "details": self.details,
            "suggested_fix": self.suggested_fix,
        }


def check_filename(path: Path) -> list[Issue]:
    """Check a single file/directory name for Windows compatibility issues."""
    issues = []
    name = path.name

    # Check for reserved characters
    reserved = has_reserved_chars(name)
    if reserved:
        # Suggest replacement
        fixed_name = name
        for char in reserved:
            fixed_name = fixed_name.replace(char, "-")
        issues.append(
            Issue(
                path,
                "reserved_char",
                f"Contains reserved character(s): {reserved}",
                fixed_name,
            )
        )

    # Check for reserved names
    if is_reserved_name(name):
        issues.append(
            Issue(
                path,
                "reserved_name",
                f"'{name}' is a Windows reserved name",
                f"{name}_placeholder",
            )
        )

    # Check for control characters
    if has_control_chars(name):
        # Find which control chars
        ctrl_chars = [f"0x{ord(c):02x}" for c in name if ord(c) < 32]
        issues.append(
            Issue(
                path,
                "control_char",
                f"Contains control character(s): {ctrl_chars}",
                None,  # Can't easily suggest fix for control chars
            )
        )

    # Check for trailing dots/spaces
    if has_trailing_dot_or_space(name):
        fixed_name = name.rstrip(". ")
        issues.append(
            Issue(
                path,
                "trailing_char",
                f"Ends with dot or space",
                fixed_name if fixed_name else f"_{name.rstrip('. ')}",
            )
        )

    return issues


def should_exclude(path: Path, exclude_patterns: list[str]) -> bool:
    """Check if path should be excluded based on patterns."""
    path_str = str(path)
    for pattern in exclude_patterns:
        if pattern in path_str:
            return True
    return False


def scan_directory(
    root: Path, verbose: bool = False, exclude_patterns: list[str] | None = None
) -> list[Issue]:
    """Scan directory recursively for Windows-incompatible filenames."""
    all_issues = []
    exclude_patterns = exclude_patterns or []

    # Default exclusions for common directories/files that shouldn't be scanned
    default_excludes = [
        ".git",
        "__pycache__",
        "node_modules",
        ".venv",
        "venv",
        "/Icon",  # macOS folder icons (Icon\r) - valid on macOS, not on Windows
    ]
    exclude_patterns.extend(default_excludes)

    for dirpath, dirnames, filenames in os.walk(root):
        current_path = Path(dirpath)

        # Check if we should skip this directory
        if should_exclude(current_path, exclude_patterns):
            dirnames.clear()  # Don't descend into excluded dirs
            continue

        # Check directory names
        for dirname in list(dirnames):
            dir_full_path = current_path / dirname
            if should_exclude(dir_full_path, exclude_patterns):
                dirnames.remove(dirname)
                continue
            issues = check_filename(dir_full_path)
            all_issues.extend(issues)

        # Check filenames
        for filename in filenames:
            file_path = current_path / filename
            if should_exclude(file_path, exclude_patterns):
                continue
            issues = check_filename(file_path)
            all_issues.extend(issues)

    return all_issues


def apply_fixes(issues: list[Issue], dry_run: bool = False) -> tuple[int, int]:
    """Attempt to fix issues by renaming files.

    Returns:
        Tuple of (successful_fixes, failed_fixes)
    """
    # Sort by path depth (deepest first) to handle nested renames
    sorted_issues = sorted(issues, key=lambda i: str(i.path).count("/"), reverse=True)

    success = 0
    failed = 0

    for issue in sorted_issues:
        if issue.suggested_fix is None:
            safe_print(f"  [SKIP] {issue.path}: No automatic fix available")
            failed += 1
            continue

        new_path = issue.path.parent / issue.suggested_fix

        if dry_run:
            safe_print(f"  [DRY-RUN] Would rename: {issue.path.name} -> {issue.suggested_fix}")
            success += 1
        else:
            try:
                if new_path.exists():
                    safe_print(f"  [SKIP] {issue.path}: Target already exists")
                    failed += 1
                    continue
                issue.path.rename(new_path)
                safe_print(f"  [FIXED] {issue.path.name} -> {issue.suggested_fix}")
                success += 1
            except OSError as e:
                safe_print(f"  [ERROR] {issue.path}: {e}")
                failed += 1

    return success, failed


def cli(argv: list[str] | None = None) -> int:
    """Entry point for Windows filename validator.

    Exit codes:
        0 - All checks passed (no issues found)
        1 - Error (bad args, unreadable paths)
        2 - Validation issues found
    """
    args = parse_args(sys.argv[1:] if argv is None else argv)

    # Resolve scan path
    scan_path = args.path if args.path else Path.cwd()
    scan_path = scan_path.resolve()

    if not scan_path.exists():
        safe_print(f"[FAIL] Path does not exist: {scan_path}")
        return 1

    if args.verbose:
        safe_print(f"Scanning for Windows-incompatible filenames: {scan_path}")
        safe_print("")

    # Scan for issues
    issues = scan_directory(scan_path, args.verbose, args.exclude)

    # Output results
    if args.json_output:
        import json

        output = {
            "scan_path": str(scan_path),
            "issue_count": len(issues),
            "issues": [i.to_dict() for i in issues],
        }
        args.json_output.write_text(json.dumps(output, indent=2))
        if args.verbose:
            safe_print(f"Results written to: {args.json_output}")

    if not issues:
        safe_print("[OK] Windows filename validation passed - no issues found")
        return 0

    # Report issues
    safe_print(f"\n[FAIL] Found {len(issues)} Windows-incompatible filename(s):\n")

    # Group by issue type
    by_type: dict[str, list[Issue]] = {}
    for issue in issues:
        by_type.setdefault(issue.issue_type, []).append(issue)

    type_labels = {
        "reserved_char": "Reserved Characters (: * ? \" < > | \\ /)",
        "reserved_name": "Reserved Names (CON, NUL, COM1, etc.)",
        "control_char": "Control Characters",
        "trailing_char": "Trailing Dots/Spaces",
    }

    for issue_type, type_issues in by_type.items():
        label = type_labels.get(issue_type, issue_type)
        safe_print(f"  {label}: {len(type_issues)} issue(s)")
        for issue in type_issues[:5]:  # Show first 5 of each type
            safe_print(f"    - {issue.path}")
            if issue.suggested_fix and args.verbose:
                safe_print(f"      Suggested: {issue.suggested_fix}")
        if len(type_issues) > 5:
            safe_print(f"    ... and {len(type_issues) - 5} more")
        safe_print("")

    # Apply fixes if requested
    if args.fix or args.dry_run:
        safe_print("Applying fixes..." if not args.dry_run else "Dry run - no changes made:")
        success, failed = apply_fixes(issues, dry_run=args.dry_run)
        safe_print(f"\nFix summary: {success} successful, {failed} failed/skipped")

        if args.dry_run:
            return 2  # Still report issues in dry-run mode
        elif failed == 0 and success == len(issues):
            return 0  # All fixed

    safe_print("\n[TIP] Remediation:")
    safe_print("  - Rename files to remove reserved characters")
    safe_print("  - Use --fix to attempt automatic fixes")
    safe_print("  - Use --dry-run to preview fixes without making changes")
    safe_print("  - Add problematic patterns to .stignore if sync is not needed")

    return 2


if __name__ == "__main__":
    raise SystemExit(cli())
