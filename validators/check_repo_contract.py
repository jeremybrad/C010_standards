#!/usr/bin/env python3
"""Validator for repository contract compliance.

Checks that repositories meet minimum structural requirements for standards compliance.
This is a general-purpose validator that can be applied to any git repository.
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from validators.common import safe_print


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate repository contract compliance"
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=None,
        help="Repository root (default: REPO_CONTRACT_ROOT env or git root)",
    )
    parser.add_argument(
        "--mode",
        choices=["generic", "work", "personal"],
        default="generic",
        help="Validation mode (default: generic)",
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Show detailed output"
    )
    return parser.parse_args(argv)


def find_git_root() -> Path | None:
    """Walk up from current directory to find .git directory."""
    current = Path.cwd().resolve()
    while current != current.parent:
        if (current / ".git").exists():
            return current
        current = current.parent
    return None


def resolve_repo_root(cli_path: Path | None) -> Path | None:
    """Resolve repo root from CLI arg, env var, or git discovery."""
    # CLI argument takes precedence
    if cli_path is not None:
        return cli_path.resolve()

    # Check environment variable
    env_root = os.environ.get("REPO_CONTRACT_ROOT")
    if env_root:
        return Path(env_root).resolve()

    # Fall back to git root discovery
    return find_git_root()


def check_is_git_repo(repo_root: Path, verbose: bool = False) -> list[str]:
    """Verify repo_root is a git repository."""
    errors = []
    git_dir = repo_root / ".git"

    if not git_dir.exists():
        errors.append(f"Not a git repository: {repo_root} (missing .git)")
    elif verbose:
        safe_print(f"[OK] Git repository: {repo_root}")

    return errors


def check_required_files(repo_root: Path, verbose: bool = False) -> list[str]:
    """Check for required files that must exist (FAIL if missing)."""
    errors = []
    required = [
        ("README.md", "file"),
        (".gitignore", "file"),
        ("20_receipts", "dir"),
    ]

    for name, kind in required:
        path = repo_root / name
        exists = path.is_dir() if kind == "dir" else path.is_file()

        if not exists:
            errors.append(f"Missing required {kind}: {name}")
        elif verbose:
            safe_print(f"[OK] Found {kind}: {name}")

    return errors


def check_recommended_files(repo_root: Path, verbose: bool = False) -> list[str]:
    """Check for recommended files (WARN if missing, do not fail)."""
    warnings = []
    recommended = [
        ("CLAUDE.md", "file"),
        (".gitattributes", "file"),
    ]

    for name, kind in recommended:
        path = repo_root / name
        exists = path.is_dir() if kind == "dir" else path.is_file()

        if not exists:
            warnings.append(f"[TIP] Recommended {kind} missing: {name}")
        elif verbose:
            safe_print(f"[OK] Found recommended {kind}: {name}")

    return warnings


def check_verify_entrypoints(repo_root: Path, verbose: bool = False) -> list[str]:
    """Check for verify entrypoints (advisory only, does not affect exit code).

    Detection priority order:
    1. make verify target (Makefile with "verify:" line)
    2. 00_run/verify.* files
    3. scripts/verify*.py files

    Returns first match by priority, then lexicographic within category.
    """
    warnings: list[str] = []

    # Priority 1: Check for make verify target
    makefile = repo_root / "Makefile"
    if makefile.is_file():
        try:
            content = makefile.read_text(encoding="utf-8")
            # Look for "verify:" at start of line (make target)
            if any(line.startswith("verify:") for line in content.splitlines()):
                if verbose:
                    safe_print("[OK] Verify entrypoint found: make verify")
                return warnings  # Found, no warning needed
        except Exception:
            pass  # Can't read Makefile, continue to other checks

    # Priority 2: Check for 00_run/verify.* files
    run_dir = repo_root / "00_run"
    if run_dir.is_dir():
        verify_files = sorted(run_dir.glob("verify.*"))
        if verify_files:
            found = verify_files[0].name
            if verbose:
                safe_print(f"[OK] Verify entrypoint found: 00_run/{found}")
            return warnings

    # Priority 3: Check for scripts/verify*.py files
    scripts_dir = repo_root / "scripts"
    if scripts_dir.is_dir():
        verify_scripts = sorted(scripts_dir.glob("verify*.py"))
        if verify_scripts:
            found = verify_scripts[0].name
            if verbose:
                safe_print(f"[OK] Verify entrypoint found: scripts/{found}")
            return warnings

    # No verify entrypoint found - advisory tip
    warnings.append(
        "[TIP] No verify entrypoint found. Consider: make verify, 00_run/verify.*, scripts/verify*.py"
    )
    return warnings


def check_repo_card_markers(repo_root: Path, verbose: bool = False) -> list[str]:
    """If README has repo_card:start marker, ensure it also has :end marker."""
    errors: list[str] = []
    readme_path = repo_root / "README.md"

    if not readme_path.is_file():
        # Already caught by required files check
        return errors

    try:
        content = readme_path.read_text(encoding="utf-8")
    except Exception as e:
        errors.append(f"Failed to read README.md: {e}")
        return errors

    start_marker = "<!-- BOT:repo_card:start -->"
    end_marker = "<!-- BOT:repo_card:end -->"

    has_start = start_marker in content
    has_end = end_marker in content

    if has_start and not has_end:
        errors.append(f"README.md has '{start_marker}' but missing '{end_marker}'")
    elif has_start and has_end:
        if verbose:
            safe_print("[OK] Repo card markers are properly paired")
    elif verbose:
        safe_print("[OK] No repo card markers (optional)")

    return errors


def cli(argv: list[str] | None = None) -> int:
    """Entry point for repo contract validator.

    Exit codes:
        0 - All checks passed
        1 - Error (bad args, unreadable paths, unexpected exception)
        2 - Contract violations (validation failures)
    """
    args = parse_args(sys.argv[1:] if argv is None else argv)

    # Resolve repo root
    repo_root = resolve_repo_root(args.repo_root)

    if repo_root is None:
        safe_print("[FAIL] Could not determine repository root.")
        safe_print("  Specify --repo-root or set REPO_CONTRACT_ROOT env var")
        return 1

    if not repo_root.is_dir():
        safe_print(f"[FAIL] Repository root is not a directory: {repo_root}")
        return 1

    if args.verbose:
        safe_print(f"Validating repository: {repo_root}")
        safe_print(f"Mode: {args.mode}")
        safe_print("")

    # Collect errors and warnings
    errors: list[str] = []
    warnings: list[str] = []

    # Run checks
    errors.extend(check_is_git_repo(repo_root, args.verbose))
    errors.extend(check_required_files(repo_root, args.verbose))
    warnings.extend(check_recommended_files(repo_root, args.verbose))
    errors.extend(check_repo_card_markers(repo_root, args.verbose))
    warnings.extend(check_verify_entrypoints(repo_root, args.verbose))

    # Report results
    if args.verbose:
        safe_print("")

    # Print warnings (these don't cause failure)
    for warning in warnings:
        safe_print(warning)

    if errors:
        safe_print(
            f"\n[FAIL] Repo contract validation FAILED ({len(errors)} issues):\n"
        )
        for i, error in enumerate(errors, 1):
            safe_print(f"  {i}. {error}")

        safe_print("\n[TIP] Remediation:")
        safe_print("  - Create missing required files/directories")
        safe_print("  - Run: mkdir -p 20_receipts")
        safe_print("  - Ensure .gitignore exists (can be empty)")
        return 2

    safe_print("[OK] Repo contract validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(cli())
