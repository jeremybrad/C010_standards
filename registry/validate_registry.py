#!/usr/bin/env python3
"""
Validate registry/repos.yaml against schema v1.2.

Usage:
    python registry/validate_registry.py
    python registry/validate_registry.py --verbose
    python registry/validate_registry.py --strict  # require onboarding fields for active repos

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

# Schema definition v1.3
REQUIRED_FIELDS = {"repo_id", "name", "purpose", "authoritative_sources", "contracts", "status"}
OPTIONAL_CARD_FIELDS = {"philosophy", "interfaces", "tags"}
OPTIONAL_ONBOARDING_FIELDS = {
    "story", "how_it_fits", "architecture",
    "onboarding", "entry_points", "key_concepts",
    "common_tasks", "gotchas", "integration_points",
    "commands", "glossary_refs"
}
# Standards applicability fields (v1.3)
OPTIONAL_APPLICABILITY_FIELDS = {"tier", "pool", "enforcement"}
# Legacy/internal fields (widely used, not in schema docs)
OPTIONAL_INTERNAL_FIELDS = {"bot_active", "path_rel"}
OPTIONAL_FIELDS = OPTIONAL_CARD_FIELDS | OPTIONAL_ONBOARDING_FIELDS | OPTIONAL_APPLICABILITY_FIELDS | OPTIONAL_INTERNAL_FIELDS

VALID_STATUS = {"active", "deprecated", "incubating", "experimental", "archived"}

# Standards applicability enums (v1.3)
# Defaults: tier=1, pool=personal, enforcement=advisory (applied during validation, not written back)
VALID_TIER = {1, 2, 3}
VALID_POOL = {"personal", "work", "archive"}
VALID_ENFORCEMENT = {"none", "advisory", "hard_gated"}

# Type enforcement
LIST_STRING_FIELDS = {
    "authoritative_sources", "contracts", "interfaces", "tags",
    "onboarding", "entry_points", "key_concepts", "common_tasks",
    "gotchas", "integration_points", "commands", "glossary_refs"
}
STRING_FIELDS = {"story", "how_it_fits", "architecture", "philosophy", "purpose", "name", "repo_id"}

# Strict mode requirements
STRICT_REQUIRED_FOR_ACTIVE = {"onboarding", "entry_points"}


def validate_entry(entry: dict, verbose: bool = False, strict: bool = False) -> list[str]:
    """Validate a single repo entry. Returns list of error messages."""
    errors = []
    repo_id = entry.get("repo_id", "<unknown>")
    status = entry.get("status")

    # Check required fields
    for field in REQUIRED_FIELDS:
        if field not in entry:
            errors.append(f"[{repo_id}] Missing required field: {field}")

    # Check status enum
    if status and status not in VALID_STATUS:
        errors.append(f"[{repo_id}] Invalid status '{status}'. Must be one of: {VALID_STATUS}")

    # Check standards applicability enums (v1.3) - validate if present, don't require
    tier = entry.get("tier")
    if tier is not None and tier not in VALID_TIER:
        errors.append(f"[{repo_id}] Invalid tier '{tier}'. Must be one of: {sorted(VALID_TIER)}")

    pool = entry.get("pool")
    if pool is not None and pool not in VALID_POOL:
        errors.append(f"[{repo_id}] Invalid pool '{pool}'. Must be one of: {sorted(VALID_POOL)}")

    enforcement = entry.get("enforcement")
    if enforcement is not None and enforcement not in VALID_ENFORCEMENT:
        errors.append(f"[{repo_id}] Invalid enforcement '{enforcement}'. Must be one of: {sorted(VALID_ENFORCEMENT)}")

    # Strict mode: require onboarding fields for active repos
    if strict and status == "active":
        for field in STRICT_REQUIRED_FOR_ACTIVE:
            if field not in entry:
                errors.append(f"[{repo_id}] Strict mode: missing '{field}' for active repo")

    # Check string fields are actually strings
    for field in STRING_FIELDS:
        value = entry.get(field)
        if value is None:
            continue
        if not isinstance(value, str):
            errors.append(f"[{repo_id}] Field '{field}' must be string, got {type(value).__name__}")

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
    strict = "--strict" in argv

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
        errors = validate_entry(entry, verbose, strict)
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
