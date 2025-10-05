#!/usr/bin/env python3
"""Validator for Houston tool pipeline configuration.

Verifies tool pipelines align with capability flags and phase gating.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, List

TOOLS_PATH = Path("30_config/houston-tools.json")
FEATURES_PATH = Path("30_config/houston-features.json")


def parse_args(argv: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate Houston tool pipelines")
    parser.add_argument(
        "--config", default=TOOLS_PATH, type=Path, help="Path to houston-tools.json"
    )
    parser.add_argument(
        "--features-config",
        default=FEATURES_PATH,
        type=Path,
        help="Path to houston-features.json for phase cross-checks",
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


def validate_phase_consistency(
    tools_config: dict, features_config: dict | None, verbose: bool = False
) -> list[str]:
    """Validate tool phase_settings align with features gradual_trust_building."""
    errors = []

    if not features_config:
        if verbose:
            print("⊘ Skipping phase consistency check (no features config)")
        return errors

    try:
        tools_phase = tools_config.get("phase_settings", {}).get("current_phase")
        features_phase = features_config["gradual_trust_building"]["current_phase"]

        if tools_phase is not None and tools_phase > features_phase:
            errors.append(
                f"Tools phase_settings.current_phase ({tools_phase}) exceeds "
                f"features gradual_trust_building.current_phase ({features_phase}). "
                "Tool permissions cannot exceed trust phase."
            )
        elif verbose and tools_phase is not None:
            print(f"✓ Phase consistency check passed (tools={tools_phase}, features={features_phase})")

    except KeyError as e:
        errors.append(f"Missing required field for phase validation: {e}")

    return errors


def validate_dangerous_operations(tools_config: dict, verbose: bool = False) -> list[str]:
    """Warn if dangerous operations are enabled without phase 3."""
    errors = []

    dangerous_tools = {"kill_processes", "system_shutdown", "rm_recursive"}
    current_phase = tools_config.get("phase_settings", {}).get("current_phase", 1)

    # Check for dangerous tools in phase overrides
    phase_overrides = (
        tools_config.get("tool_access", {})
        .get("local_tools", {})
        .get("phase_overrides", {})
    )

    for phase_key, tools in phase_overrides.items():
        if isinstance(tools, list):
            phase_num = int(phase_key.replace("phase_", ""))
            dangerous_found = set(tools) & dangerous_tools

            if dangerous_found and phase_num < 3:
                errors.append(
                    f"WARNING: Dangerous operations {dangerous_found} enabled in {phase_key}. "
                    "Consider restricting to phase 3+."
                )

    if verbose and not errors:
        print("✓ Dangerous operations check passed")

    return errors


def validate_vps_endpoint(tools_config: dict, verbose: bool = False) -> list[str]:
    """Warn if VPS tools enabled with placeholder endpoint."""
    errors = []

    vps_tools = tools_config.get("tool_access", {}).get("vps_tools", {})
    enabled = vps_tools.get("enabled", False)
    endpoint = vps_tools.get("endpoint", "")

    if enabled and endpoint in {"", "example.com", "placeholder"}:
        errors.append(
            f"WARNING: vps_tools.enabled is true but endpoint is placeholder ('{endpoint}'). "
            "Provide real VPS endpoint before enabling."
        )
    elif verbose:
        print(f"✓ VPS endpoint check passed (enabled={enabled}, endpoint={endpoint})")

    return errors


def cli(argv: List[str] | None = None) -> int:
    args = parse_args(argv or [])

    # Check tools config exists
    if not args.config.exists():
        print(f"ERROR: Tools config not found: {args.config}")
        return 1

    # Load configs
    try:
        tools_config = load_json(args.config)
    except Exception as e:
        print(f"ERROR: Failed to load tools config: {e}")
        return 2

    features_config = None
    if args.features_config.exists():
        try:
            features_config = load_json(args.features_config)
        except Exception:
            if args.verbose:
                print(f"WARNING: Could not load features config for cross-validation")

    # Run validation checks
    all_errors: list[str] = []

    all_errors.extend(validate_phase_consistency(tools_config, features_config, args.verbose))
    all_errors.extend(validate_dangerous_operations(tools_config, args.verbose))
    all_errors.extend(validate_vps_endpoint(tools_config, args.verbose))

    # Report results
    if all_errors:
        print(f"\n❌ Houston tools validation FAILED ({len(all_errors)} issues):\n")
        for i, error in enumerate(all_errors, 1):
            print(f"  {i}. {error}")

        print("\n💡 Remediation suggestions:")
        print("  - Align phase_settings.current_phase with gradual_trust_building.current_phase")
        print("  - Restrict dangerous operations (kill_processes, system_shutdown) to phase 3+")
        print("  - Provide real VPS endpoint before enabling remote tool access")

        return 1
    else:
        if args.verbose:
            print("\n✅ All Houston tools validation checks passed")
        else:
            print("✅ Houston tools validation passed")
        return 0


if __name__ == "__main__":
    raise SystemExit(cli())
