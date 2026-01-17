#!/usr/bin/env python3
"""Validator for Epoch-as-Code (c010.epoch.v1) documents.

Validates EPOCH.yaml repo state snapshots against the epoch specification.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, cast

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from validators.common import safe_print

try:
    import yaml

    HAS_YAML = True
except ImportError:
    HAS_YAML = False

EPOCH_SPEC_V1 = "c010.epoch.v1"
GIT_HASH_PATTERN = re.compile(r"^[a-f0-9]{7,40}$")
DEFAULT_PRIMER_PATH = "PROJECT_PRIMER.md"
DEFAULT_EPOCH_PATH = "00_admin/EPOCH.yaml"

KNOWN_TOP_LEVEL_FIELDS = {
    "epoch_schema",
    "repo_id",
    "repo_head",
    "generated_at_utc",
    "primer",
    "standards",
    "generator",
    "custom",
}

# ISO 8601 datetime pattern (simplified, handles common formats)
ISO8601_PATTERN = re.compile(
    r"^\d{4}-\d{2}-\d{2}"  # Date: YYYY-MM-DD
    r"(T\d{2}:\d{2}:\d{2}"  # Time: THH:MM:SS
    r"(\.\d+)?"  # Optional fractional seconds
    r"(Z|[+-]\d{2}:?\d{2})?"  # Optional timezone
    r")?$"
)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate Epoch-as-Code (c010.epoch.v1) documents"
    )
    parser.add_argument(
        "paths",
        nargs="*",
        default=["."],
        help="Repository paths to validate (default: current directory)",
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Show detailed output"
    )
    parser.add_argument(
        "--json-output",
        type=Path,
        help="Write results to JSON file",
    )
    parser.add_argument(
        "--require",
        action="store_true",
        help="Require EPOCH.yaml to exist (exit 1 if missing)",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Strict mode: implies --require, verify repo_head matches git HEAD, unknown fields are errors",
    )
    return parser.parse_args(argv)


def find_git_root(start_path: Path) -> Path | None:
    """Walk up from start_path to find .git directory."""
    current = start_path.resolve()
    while current != current.parent:
        if (current / ".git").exists():
            return current
        current = current.parent
    return None


def get_git_head(repo_path: Path) -> str | None:
    """Get current git HEAD SHA for a repository."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=repo_path,
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        pass
    return None


def calculate_file_sha256(file_path: Path) -> str | None:
    """Calculate SHA256 hash of a file's content."""
    try:
        content = file_path.read_bytes()
        return hashlib.sha256(content).hexdigest()
    except (OSError, IOError):
        return None


def load_epoch_yaml(file_path: Path) -> dict[str, Any] | None:
    """Load and parse EPOCH.yaml file.

    Returns None if:
    - File doesn't exist
    - YAML parsing fails
    """
    if not HAS_YAML:
        return None

    if not file_path.exists():
        return None

    try:
        content = file_path.read_text(encoding="utf-8")
        data = yaml.safe_load(content)
        return cast(dict[str, Any], data) if isinstance(data, dict) else None
    except yaml.YAMLError:
        return None
    except (OSError, IOError):
        return None


def validate_iso8601(value: str) -> bool:
    """Validate that a string is valid ISO 8601 datetime format."""
    if not isinstance(value, str):
        return False
    return bool(ISO8601_PATTERN.match(value))


def validate_required_fields(
    data: dict[str, Any],
    verbose: bool = False,
) -> list[str]:
    """Validate required fields in EPOCH.yaml.

    Returns list of error messages.
    """
    errors: list[str] = []

    # R1: epoch_schema must equal "c010.epoch.v1"
    epoch_schema = data.get("epoch_schema")
    if epoch_schema != EPOCH_SPEC_V1:
        errors.append(
            f"epoch_schema must be '{EPOCH_SPEC_V1}', got '{epoch_schema}'"
        )

    # R2: repo_id must be non-empty string
    repo_id = data.get("repo_id")
    if not repo_id or not isinstance(repo_id, str) or not repo_id.strip():
        errors.append("repo_id is required and must be non-empty string")

    # R3: repo_head must match git hash pattern
    repo_head = data.get("repo_head")
    if not repo_head or not isinstance(repo_head, str):
        errors.append("repo_head is required and must be a string")
    elif not GIT_HASH_PATTERN.match(repo_head):
        errors.append(
            f"repo_head must be 7-40 lowercase hex characters, got '{repo_head}'"
        )

    # R4: generated_at_utc must be valid ISO 8601
    generated_at = data.get("generated_at_utc")
    if not generated_at:
        errors.append("generated_at_utc is required")
    elif not validate_iso8601(str(generated_at)):
        errors.append(
            f"generated_at_utc must be valid ISO 8601 datetime, got '{generated_at}'"
        )

    return errors


def validate_primer_sync(
    data: dict[str, Any],
    repo_path: Path,
    verbose: bool = False,
) -> list[str]:
    """Validate primer block matches actual file.

    Rules R5-R6: If PROJECT_PRIMER.md exists, primer block required and sha256 must match.
    """
    errors: list[str] = []

    primer_path_str = DEFAULT_PRIMER_PATH
    primer_block = data.get("primer")

    if primer_block and isinstance(primer_block, dict):
        primer_path_str = primer_block.get("path", DEFAULT_PRIMER_PATH)

    primer_file = repo_path / primer_path_str

    # R5: If primer file exists, primer block required
    if primer_file.exists():
        if not primer_block:
            errors.append(
                f"{primer_path_str} exists but primer block is missing in EPOCH.yaml"
            )
        elif isinstance(primer_block, dict):
            # R6: primer.sha256 must match actual file content
            expected_sha = primer_block.get("sha256")
            if not expected_sha:
                errors.append("primer.sha256 is required when primer block exists")
            else:
                actual_sha = calculate_file_sha256(primer_file)
                if actual_sha is None:
                    errors.append(f"Could not read {primer_path_str} to verify SHA256")
                elif expected_sha != actual_sha:
                    errors.append(
                        f"primer.sha256 mismatch: expected '{expected_sha[:16]}...', "
                        f"got '{actual_sha[:16]}...' (file may have changed)"
                    )
                elif verbose:
                    safe_print(f"  ✓ primer.sha256 matches {primer_path_str}")
        else:
            errors.append("primer must be an object with sha256 and optional path")

    return errors


def validate_strict_mode(
    data: dict[str, Any],
    repo_path: Path,
    verbose: bool = False,
) -> list[str]:
    """Validate strict mode rules.

    Rule R7: repo_head must match current git HEAD.
    """
    errors: list[str] = []

    repo_head = data.get("repo_head")
    if not repo_head or not isinstance(repo_head, str):
        return errors  # Already caught by validate_required_fields

    current_head = get_git_head(repo_path)
    if current_head is None:
        errors.append("Could not determine current git HEAD for strict validation")
    else:
        # Allow prefix match (short hash vs full hash)
        matches = (
            current_head.startswith(repo_head) or repo_head.startswith(current_head)
        )
        if not matches:
            errors.append(
                f"repo_head '{repo_head[:7]}' does not match current git HEAD "
                f"'{current_head[:7]}' (epoch is stale)"
            )
        elif verbose:
            safe_print(f"  ✓ repo_head matches current git HEAD")

    return errors


def validate_unknown_fields(
    data: dict[str, Any],
    strict: bool = False,
    verbose: bool = False,
) -> tuple[list[str], list[str]]:
    """Check for unknown top-level fields.

    Rule R8: Unknown fields generate warnings (default mode).
    Rule R9: Unknown fields generate errors (strict mode).
    """
    errors: list[str] = []
    warnings: list[str] = []

    unknown_fields = set(data.keys()) - KNOWN_TOP_LEVEL_FIELDS
    if unknown_fields:
        msg = f"Unknown top-level fields: {sorted(unknown_fields)}"
        if strict:
            errors.append(msg)
        else:
            warnings.append(msg)

    return errors, warnings


def validate_epoch(
    repo_path: Path,
    epoch_data: dict[str, Any],
    strict: bool = False,
    verbose: bool = False,
) -> tuple[list[str], list[str]]:
    """Validate a single EPOCH.yaml document.

    Returns tuple of (errors, warnings).
    """
    errors: list[str] = []
    warnings: list[str] = []

    # Required field validation
    errors.extend(validate_required_fields(epoch_data, verbose))

    # Primer sync validation
    errors.extend(validate_primer_sync(epoch_data, repo_path, verbose))

    # Strict mode validation
    if strict:
        errors.extend(validate_strict_mode(epoch_data, repo_path, verbose))

    # Unknown field validation
    field_errors, field_warnings = validate_unknown_fields(epoch_data, strict, verbose)
    errors.extend(field_errors)
    warnings.extend(field_warnings)

    return errors, warnings


def cli(argv: list[str] | None = None) -> int:
    """Entry point for epoch validator.

    Exit codes:
        0 - All checks passed (or no EPOCH.yaml in default mode)
        1 - Validation failure (missing required field, invalid value, unknown field in strict)
        2 - Parse/config error (invalid YAML, file not found when required)
    """
    args = parse_args(sys.argv[1:] if argv is None else argv)

    if not HAS_YAML:
        safe_print("ERROR: PyYAML library not installed. Install with: pip install pyyaml")
        return 2

    # Strict implies require
    require_epoch = args.require or args.strict

    all_errors: list[str] = []
    all_warnings: list[str] = []
    results: dict[str, dict] = {}
    validated_count = 0

    for path_str in args.paths:
        path = Path(path_str).resolve()

        # Determine repo root
        if path.is_file():
            repo_path = path.parent
            epoch_file = path
        else:
            repo_path = find_git_root(path) or path
            epoch_file = repo_path / DEFAULT_EPOCH_PATH

        display_path = str(repo_path.name)

        if not epoch_file.exists():
            if require_epoch:
                msg = f"{display_path}: EPOCH.yaml not found at {DEFAULT_EPOCH_PATH}"
                all_errors.append(msg)
                results[display_path] = {
                    "status": "fail",
                    "errors": [msg],
                    "warnings": [],
                }
            else:
                if args.verbose:
                    safe_print(f"  ⚠ {display_path}: No EPOCH.yaml found (skipping)")
                results[display_path] = {
                    "status": "skip",
                    "errors": [],
                    "warnings": ["EPOCH.yaml not found"],
                }
            continue

        # Load EPOCH.yaml
        epoch_data = load_epoch_yaml(epoch_file)
        if epoch_data is None:
            msg = f"{display_path}: Failed to parse EPOCH.yaml (invalid YAML)"
            if args.verbose:
                safe_print(f"  ERROR: {msg}")
            results[display_path] = {
                "status": "error",
                "errors": [msg],
                "warnings": [],
            }
            return 2

        validated_count += 1

        # Validate
        errors, warnings = validate_epoch(
            repo_path,
            epoch_data,
            strict=args.strict,
            verbose=args.verbose,
        )

        # Prefix errors/warnings with display path
        prefixed_errors = [f"{display_path}: {e}" for e in errors]
        prefixed_warnings = [f"{display_path}: {w}" for w in warnings]

        all_errors.extend(prefixed_errors)
        all_warnings.extend(prefixed_warnings)

        status = "fail" if errors else "pass"
        results[display_path] = {
            "status": status,
            "errors": prefixed_errors,
            "warnings": prefixed_warnings,
        }

        if args.verbose and not errors:
            safe_print(f"  ✓ {display_path}: All epoch checks passed")

    # Write JSON output if requested
    if args.json_output:
        try:
            args.json_output.parent.mkdir(parents=True, exist_ok=True)
            output_data = {
                "total_paths": len(args.paths),
                "validated_epochs": validated_count,
                "passed": sum(1 for r in results.values() if r["status"] == "pass"),
                "failed": sum(1 for r in results.values() if r["status"] == "fail"),
                "skipped": sum(1 for r in results.values() if r["status"] == "skip"),
                "results": results,
            }
            args.json_output.write_text(json.dumps(output_data, indent=2))
            if args.verbose:
                safe_print(f"\nResults written to {args.json_output}")
        except Exception as e:
            safe_print(f"ERROR: Failed to write JSON output: {e}")
            return 2

    # Print warnings
    if all_warnings and args.verbose:
        safe_print("\nWarnings:")
        for warning in all_warnings:
            safe_print(f"  ⚠ {warning}")

    # Report summary
    if all_errors:
        safe_print(f"\n❌ Epoch validation FAILED ({len(all_errors)} issues):\n")
        for i, error in enumerate(all_errors, 1):
            safe_print(f"  {i}. {error}")

        safe_print("\n💡 Remediation suggestions:")
        safe_print(f"  - Ensure epoch_schema equals '{EPOCH_SPEC_V1}'")
        safe_print("  - Provide a non-empty repo_id")
        safe_print("  - Use 7-40 character lowercase hex for repo_head")
        safe_print("  - Use ISO 8601 format for generated_at_utc (e.g., 2026-01-17T14:30:00Z)")
        safe_print("  - If PROJECT_PRIMER.md exists, include primer block with matching sha256")
        if args.strict:
            safe_print("  - Run after git commit to ensure repo_head matches HEAD")
            safe_print(f"  - Remove unknown fields or add to schema: {KNOWN_TOP_LEVEL_FIELDS}")

        return 1
    else:
        if validated_count == 0:
            if require_epoch:
                # This case is already handled above with errors
                pass
            else:
                if args.verbose:
                    safe_print("No EPOCH.yaml files found to validate")
                else:
                    safe_print("✅ Epoch validation passed (0 epochs)")
        else:
            if args.verbose:
                safe_print(f"\n✅ All epoch validation checks passed ({validated_count} epochs)")
            else:
                safe_print(f"✅ Epoch validation passed ({validated_count} epochs)")
        return 0


if __name__ == "__main__":
    raise SystemExit(cli())
