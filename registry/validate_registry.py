#!/usr/bin/env python3
"""
Validate registry/repos.yaml against schema v1.1.

Usage:
    python registry/validate_registry.py
    python registry/validate_registry.py --verbose

Exit codes:
    0 - Valid
    1 - Validation errors
    2 - File/parse error

Requirements:
    PyYAML (pip install pyyaml)
"""
from __future__ import annotations

import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML required. Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(2)

# Schema definition
REQUIRED_FIELDS = {"repo_id", "name", "purpose", "authoritative_sources", "contracts", "status"}
OPTIONAL_FIELDS = {"philosophy", "interfaces", "tags"}
VALID_STATUS = {"active", "deprecated"}
LIST_STRING_FIELDS = {"authoritative_sources", "contracts", "interfaces", "tags"}


def validate_entry(entry: dict, verbose: bool = False) -> list[str]:
    """Validate a single repo entry. Returns list of error messages."""
    errors = []
    repo_id = entry.get("repo_id", "<unknown>")

    # Check required fields
    for field in REQUIRED_FIELDS:
        if field not in entry:
            errors.append(f"[{repo_id}] Missing required field: {field}")

    # Check status enum
    status = entry.get("status")
    if status and status not in VALID_STATUS:
        errors.append(f"[{repo_id}] Invalid status '{status}'. Must be one of: {VALID_STATUS}")

    # Check list[string] fields are actually list[str]
    for field in LIST_STRING_FIELDS:
        value = entry.get(field)
        if value is None:
            continue
        if not isinstance(value, list):
            errors.append(f"[{repo_id}] Field '{field}' must be a list, got {type(value).__name__}")
            continue
        for i, item in enumerate(value):
            if not isinstance(item, str):
                errors.append(
                    f"[{repo_id}] Field '{field}[{i}]' must be string, got {type(item).__name__}: {item!r}"
                )

    # Check for unknown fields
    all_fields = REQUIRED_FIELDS | OPTIONAL_FIELDS
    for field in entry:
        if field not in all_fields:
            if verbose:
                print(f"  WARN [{repo_id}] Unknown field: {field}")

    return errors


def main(argv: list[str] | None = None) -> int:
    argv = argv or sys.argv[1:]
    verbose = "--verbose" in argv or "-v" in argv

    # Locate registry file
    script_dir = Path(__file__).resolve().parent
    registry_path = script_dir / "repos.yaml"

    if not registry_path.exists():
        print(f"ERROR: Registry not found: {registry_path}", file=sys.stderr)
        return 2

    # Parse YAML
    try:
        data = yaml.safe_load(registry_path.read_text())
    except yaml.YAMLError as e:
        print(f"ERROR: YAML parse error: {e}", file=sys.stderr)
        return 2

    if not isinstance(data, dict) or "repos" not in data:
        print("ERROR: Registry must have top-level 'repos' key", file=sys.stderr)
        return 2

    repos = data["repos"]
    if not isinstance(repos, list):
        print("ERROR: 'repos' must be a list", file=sys.stderr)
        return 2

    # Validate each entry
    all_errors = []
    repo_ids = []

    for entry in repos:
        if not isinstance(entry, dict):
            all_errors.append(f"Entry is not a dict: {entry!r}")
            continue
        repo_ids.append(entry.get("repo_id", "<unknown>"))
        errors = validate_entry(entry, verbose)
        all_errors.extend(errors)

    # Check for duplicate repo_ids
    seen = set()
    for rid in repo_ids:
        if rid in seen:
            all_errors.append(f"Duplicate repo_id: {rid}")
        seen.add(rid)

    # Report results
    if verbose:
        print(f"Validated {len(repos)} entries: {repo_ids}")

    if all_errors:
        print(f"\n❌ Validation FAILED ({len(all_errors)} errors):\n", file=sys.stderr)
        for err in all_errors:
            print(f"  - {err}", file=sys.stderr)
        return 1

    print(f"✅ Registry valid: {len(repos)} entries")
    return 0


if __name__ == "__main__":
    sys.exit(main())
