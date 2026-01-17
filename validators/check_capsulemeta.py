#!/usr/bin/env python3
"""Validator for CapsuleMeta (c010.capsule.v1) documents.

Validates capsule frontmatter in markdown files against the capsule specification.
"""

from __future__ import annotations

import argparse
import json
import re
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

CAPSULE_SPEC_V1 = "c010.capsule.v1"
VALID_KINDS = {"handoff", "memory_export", "activity", "other"}
KNOWN_TOP_LEVEL_FIELDS = {
    "capsule_spec",
    "capsule_id",
    "created_at",
    "kind",
    "producer",
    "title",
    "summary",
    "tags",
    "expires_at",
    "related_capsules",
    "provenance",
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
        description="Validate CapsuleMeta (c010.capsule.v1) documents"
    )
    parser.add_argument(
        "paths",
        nargs="*",
        default=["."],
        help="Files or directories to validate (default: current directory)",
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
        "--strict",
        action="store_true",
        help="Treat unknown fields as errors (default: warnings only)",
    )
    parser.add_argument(
        "--absolute-paths",
        action="store_true",
        help="Output absolute paths (default: repo-relative)",
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


def make_relative_path(path: Path, git_root: Path | None) -> str:
    """Convert path to repo-relative string if possible."""
    if git_root is None:
        return str(path)
    try:
        return str(path.relative_to(git_root))
    except ValueError:
        return str(path)


def load_capsule_frontmatter(file_path: Path) -> dict[str, Any] | None:
    """Extract YAML frontmatter from markdown file.

    Returns None if:
    - File doesn't start with ---
    - YAML parsing fails
    - No valid frontmatter found
    """
    if not HAS_YAML:
        return None

    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception:
        return None

    if not content.startswith("---"):
        return None

    # Extract YAML between --- delimiters
    parts = content.split("---", 2)
    if len(parts) < 3:
        return None

    try:
        data = yaml.safe_load(parts[1])
        return cast(dict[str, Any], data) if isinstance(data, dict) else None
    except yaml.YAMLError:
        return None


def is_capsule_document(metadata: dict[str, Any]) -> bool:
    """Check if document has capsule_spec field indicating it's a capsule."""
    return "capsule_spec" in metadata


def validate_iso8601(value: str) -> bool:
    """Validate that a string is valid ISO 8601 datetime format."""
    if not isinstance(value, str):
        return False
    return bool(ISO8601_PATTERN.match(value))


def validate_capsule(
    file_path: Path,
    metadata: dict[str, Any],
    strict: bool = False,
    verbose: bool = False,
    display_path: str | None = None,
) -> tuple[list[str], list[str]]:
    """Validate a single capsule document.

    Returns tuple of (errors, warnings).
    """
    errors: list[str] = []
    warnings: list[str] = []
    path_str = display_path or str(file_path)

    # Rule 1: capsule_spec must equal "c010.capsule.v1"
    capsule_spec = metadata.get("capsule_spec")
    if capsule_spec != CAPSULE_SPEC_V1:
        errors.append(
            f"{path_str}: capsule_spec must be '{CAPSULE_SPEC_V1}', got '{capsule_spec}'"
        )

    # Rule 2: capsule_id must be non-empty string
    capsule_id = metadata.get("capsule_id")
    if not capsule_id or not isinstance(capsule_id, str) or not capsule_id.strip():
        errors.append(f"{path_str}: capsule_id is required and must be non-empty string")

    # Rule 3: created_at must be valid ISO 8601
    created_at = metadata.get("created_at")
    if not created_at:
        errors.append(f"{path_str}: created_at is required")
    elif not validate_iso8601(str(created_at)):
        errors.append(
            f"{path_str}: created_at must be valid ISO 8601 datetime, got '{created_at}'"
        )

    # Rule 4: kind must be in allowed enum
    kind = metadata.get("kind")
    if not kind:
        errors.append(f"{path_str}: kind is required")
    elif kind not in VALID_KINDS:
        errors.append(
            f"{path_str}: kind must be one of {sorted(VALID_KINDS)}, got '{kind}'"
        )

    # Rule 5: producer.tool must be non-empty string
    producer = metadata.get("producer", {})
    if not isinstance(producer, dict):
        errors.append(f"{path_str}: producer must be an object")
    else:
        tool = producer.get("tool")
        if not tool or not isinstance(tool, str) or not tool.strip():
            errors.append(
                f"{path_str}: producer.tool is required and must be non-empty string"
            )

    # Rule 6: Unknown top-level fields
    unknown_fields = set(metadata.keys()) - KNOWN_TOP_LEVEL_FIELDS
    if unknown_fields:
        msg = f"{path_str}: Unknown top-level fields: {sorted(unknown_fields)}"
        if strict:
            errors.append(msg)
        else:
            warnings.append(msg)

    if verbose and not errors and not warnings:
        safe_print(f"  ✓ {path_str}: All checks passed")

    return errors, warnings


def find_markdown_files(paths: list[str | Path]) -> list[Path]:
    """Find all markdown files in given paths."""
    files = []
    for path_str in paths:
        path = Path(path_str)
        if path.is_file():
            if path.suffix in {".md", ".markdown"}:
                files.append(path)
        elif path.is_dir():
            files.extend(path.rglob("*.md"))
            files.extend(path.rglob("*.markdown"))
    return files


def cli(argv: list[str] | None = None) -> int:
    """Entry point for capsule metadata validator.

    Exit codes:
        0 - All checks passed
        1 - Validation failure (missing required field, invalid value, unknown field in strict)
        2 - Parse/config error (invalid YAML, file not found)
    """
    args = parse_args(sys.argv[1:] if argv is None else argv)

    if not HAS_YAML:
        safe_print("ERROR: PyYAML library not installed. Install with: pip install pyyaml")
        return 2

    # Determine git root for relative paths
    git_root = None if args.absolute_paths else find_git_root()

    # Find all markdown files
    try:
        files = find_markdown_files(args.paths)
    except Exception as e:
        safe_print(f"ERROR: Failed to scan paths: {e}")
        return 2

    if args.verbose:
        safe_print(f"Scanning {len(files)} markdown files for capsule frontmatter...\n")

    # Validate each file
    results: dict[str, dict] = {}
    all_errors: list[str] = []
    all_warnings: list[str] = []
    validated_count = 0

    for file_path in files:
        # Load frontmatter
        metadata = load_capsule_frontmatter(file_path)
        if metadata is None:
            continue

        # Skip if not a capsule document
        if not is_capsule_document(metadata):
            continue

        validated_count += 1
        display_path = make_relative_path(file_path, git_root)

        errors, warnings = validate_capsule(
            file_path,
            metadata,
            strict=args.strict,
            verbose=args.verbose,
            display_path=display_path,
        )

        all_errors.extend(errors)
        all_warnings.extend(warnings)

        status = "fail" if errors else "pass"
        results[display_path] = {
            "status": status,
            "errors": errors,
            "warnings": warnings,
        }

    # Write JSON output if requested
    if args.json_output:
        try:
            args.json_output.parent.mkdir(parents=True, exist_ok=True)
            output_data = {
                "total_files": len(files),
                "validated_files": validated_count,
                "passed": sum(1 for r in results.values() if r["status"] == "pass"),
                "failed": sum(1 for r in results.values() if r["status"] == "fail"),
                "results": results,
            }
            args.json_output.write_text(json.dumps(output_data, indent=2))
            if args.verbose:
                safe_print(f"\nResults written to {args.json_output}")
        except Exception as e:
            safe_print(f"ERROR: Failed to write JSON output: {e}")
            return 2

    # Print warnings (these don't cause failure in normal mode)
    if all_warnings and args.verbose:
        safe_print("\nWarnings:")
        for warning in all_warnings:
            safe_print(f"  ⚠ {warning}")

    # Report summary
    if all_errors:
        safe_print(f"\n❌ CapsuleMeta validation FAILED ({len(all_errors)} issues):\n")
        for i, error in enumerate(all_errors, 1):
            safe_print(f"  {i}. {error}")

        safe_print("\n💡 Remediation suggestions:")
        safe_print(f"  - Ensure capsule_spec equals '{CAPSULE_SPEC_V1}'")
        safe_print("  - Provide a unique capsule_id (UUID recommended)")
        safe_print("  - Use ISO 8601 format for created_at (e.g., 2026-01-17T14:30:00Z)")
        safe_print(f"  - Use valid kind: {sorted(VALID_KINDS)}")
        safe_print("  - Include producer.tool with non-empty value")
        if args.strict:
            safe_print(f"  - Remove unknown fields or add to schema: {KNOWN_TOP_LEVEL_FIELDS}")

        return 1
    else:
        if validated_count == 0:
            if args.verbose:
                safe_print("No capsule documents found to validate")
            else:
                safe_print("✅ CapsuleMeta validation passed (0 capsules)")
        else:
            if args.verbose:
                safe_print(f"\n✅ All CapsuleMeta validation checks passed ({validated_count} capsules)")
            else:
                safe_print(f"✅ CapsuleMeta validation passed ({validated_count} capsules)")
        return 0


if __name__ == "__main__":
    raise SystemExit(cli())
