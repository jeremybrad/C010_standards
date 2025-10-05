#!/usr/bin/env python3
"""Validator for Houston feature configuration.

Validates houston-features.json against JSON schema and enforces trust phase requirements.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, List

try:
    import jsonschema
    HAS_JSONSCHEMA = True
except ImportError:
    HAS_JSONSCHEMA = False

FEATURES_PATH = Path("30_config/houston-features.json")
SCHEMA_PATH = Path("schemas/houston_features.schema.json")
CHANGELOG_PATH = Path("notes/CHANGELOG.md")


def parse_args(argv: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate Houston features config")
    parser.add_argument(
        "--config", default=FEATURES_PATH, type=Path, help="Path to houston-features.json"
    )
    parser.add_argument(
        "--schema", default=SCHEMA_PATH, type=Path, help="Path to JSON schema definition"
    )
    parser.add_argument(
        "--changelog", default=CHANGELOG_PATH, type=Path, help="Path to CHANGELOG.md"
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Show detailed output"
    )
    return parser.parse_args(argv)


def load_json(path: Path) -> dict[str, Any]:
    """Load and parse JSON file."""
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        print(f"ERROR: JSON parse error in {path}: {exc}")
        raise


def validate_json_schema(config: dict, schema: dict, verbose: bool = False) -> list[str]:
    """Validate config against JSON schema. Returns list of errors."""
    if not HAS_JSONSCHEMA:
        return ["WARNING: jsonschema library not installed, schema validation skipped"]

    errors = []
    validator = jsonschema.Draft7Validator(schema)
    for error in validator.iter_errors(config):
        errors.append(f"Schema validation error at {'.'.join(str(p) for p in error.path)}: {error.message}")

    if verbose and not errors:
        print("✓ JSON schema validation passed")

    return errors


def validate_supported_editors(config: dict, verbose: bool = False) -> list[str]:
    """Validate supported_editors are in allowed list."""
    errors = []
    allowed = {"cursor", "vscode", "jetbrains"}

    try:
        editors = set(config["features"]["ide_integration"]["supported_editors"])
        invalid = editors - allowed
        if invalid:
            errors.append(f"Invalid editors in supported_editors: {invalid}. Allowed: {allowed}")
        elif verbose:
            print(f"✓ Supported editors valid: {editors}")
    except KeyError as e:
        errors.append(f"Missing required field: {e}")

    return errors


def validate_autonomous_safety(config: dict, verbose: bool = False) -> list[str]:
    """If agency level is autonomous, require password for destructive actions."""
    errors = []

    try:
        current_level = config["features"]["agency_levels"]["current_level"]
        require_password = config["safety_controls"]["destructive_actions"]["require_password"]

        if current_level == "autonomous" and not require_password:
            errors.append(
                "CRITICAL: agency_levels.current_level is 'autonomous' but "
                "safety_controls.destructive_actions.require_password is false. "
                "Must be true for autonomous mode."
            )
        elif verbose:
            print(f"✓ Autonomous safety check passed (level={current_level}, require_password={require_password})")
    except KeyError as e:
        errors.append(f"Missing required field for safety check: {e}")

    return errors


def validate_phase_consistency(config: dict, changelog_path: Path, verbose: bool = False) -> list[str]:
    """Validate current_phase is within bounds and check changelog for manual approval."""
    errors = []

    try:
        phases = config["gradual_trust_building"]["phases"]
        current_phase = config["gradual_trust_building"]["current_phase"]
        auto_advance = config["gradual_trust_building"]["auto_advance"]

        max_phase = len(phases)
        if current_phase > max_phase:
            errors.append(
                f"current_phase ({current_phase}) exceeds number of defined phases ({max_phase})"
            )

        # Check agency level matches phase
        phase_def = next((p for p in phases if p["phase"] == current_phase), None)
        if phase_def:
            expected_level = phase_def["agency_level"]
            actual_level = config["features"]["agency_levels"]["current_level"]
            if expected_level != actual_level:
                errors.append(
                    f"Phase {current_phase} requires agency_level '{expected_level}' "
                    f"but current_level is '{actual_level}'"
                )
            elif verbose:
                print(f"✓ Phase {current_phase} agency level matches: {actual_level}")

        # Check for manual approval in changelog if auto_advance is false
        if not auto_advance and current_phase > 1 and changelog_path.exists():
            changelog_text = changelog_path.read_text()
            phase_pattern = f"Phase {current_phase} activated"
            if phase_pattern not in changelog_text:
                errors.append(
                    f"WARNING: auto_advance is false and current_phase is {current_phase}, "
                    f"but no '{phase_pattern}' entry found in {changelog_path}. "
                    "Manual approval should be documented."
                )
            elif verbose:
                print(f"✓ Phase {current_phase} activation found in changelog")
        elif verbose and auto_advance:
            print(f"✓ Auto-advance enabled, changelog check skipped")

    except KeyError as e:
        errors.append(f"Missing required field for phase validation: {e}")

    return errors


def validate_autonomous_deploy_permission(config: dict, verbose: bool = False) -> list[str]:
    """Ensure can_deploy_updates is only true in phase 3+."""
    errors = []

    try:
        current_phase = config["gradual_trust_building"]["current_phase"]
        autonomous_config = config["features"]["agency_levels"]["autonomous"]
        can_deploy = autonomous_config.get("can_deploy_updates", False)

        if can_deploy and current_phase < 3:
            errors.append(
                f"CRITICAL: autonomous.can_deploy_updates is true but current_phase is {current_phase}. "
                "Deployment permission requires phase >= 3."
            )
        elif verbose:
            print(f"✓ Deploy permissions check passed (can_deploy={can_deploy}, phase={current_phase})")
    except KeyError as e:
        errors.append(f"Missing required field for deploy permission check: {e}")

    return errors


def cli(argv: List[str] | None = None) -> int:
    args = parse_args(argv or [])

    # Check required files exist
    for path in (args.config, args.schema):
        if not path.exists():
            print(f"ERROR: Required file not found: {path}")
            return 1

    # Load config and schema
    try:
        config = load_json(args.config)
        schema = load_json(args.schema)
    except Exception as e:
        print(f"ERROR: Failed to load JSON: {e}")
        return 2

    # Run all validation checks
    all_errors: list[str] = []

    all_errors.extend(validate_json_schema(config, schema, args.verbose))
    all_errors.extend(validate_supported_editors(config, args.verbose))
    all_errors.extend(validate_autonomous_safety(config, args.verbose))
    all_errors.extend(validate_phase_consistency(config, args.changelog, args.verbose))
    all_errors.extend(validate_autonomous_deploy_permission(config, args.verbose))

    # Report results
    if all_errors:
        print(f"\n❌ Houston features validation FAILED ({len(all_errors)} issues):\n")
        for i, error in enumerate(all_errors, 1):
            print(f"  {i}. {error}")

        # Suggest remediation
        print("\n💡 Remediation suggestions:")
        if any("autonomous" in e.lower() for e in all_errors):
            print("  - Review autonomous mode safety controls")
            print("  - Ensure current_phase >= 3 before enabling deployment")
        if any("phase" in e.lower() for e in all_errors):
            print("  - Update agency_levels.current_level to match phase requirements")
            print("  - Document phase activation in notes/CHANGELOG.md")
        if any("schema" in e.lower() for e in all_errors):
            print("  - Install jsonschema: pip install jsonschema")
            print("  - Review config structure against schemas/houston_features.schema.json")

        return 1
    else:
        if args.verbose:
            print("\n✅ All Houston features validation checks passed")
        else:
            print("✅ Houston features validation passed")
        return 0


if __name__ == "__main__":
    raise SystemExit(cli())
