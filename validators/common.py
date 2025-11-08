"""Common utilities for Houston validators.

Provides shared functionality for loading configs, reporting results,
and handling errors consistently across all validators.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_json_config(path: Path) -> dict[str, Any]:
    """Load and parse JSON configuration file.

    Args:
        path: Path to JSON file

    Returns:
        Parsed JSON as dictionary

    Raises:
        json.JSONDecodeError: If JSON is malformed
        FileNotFoundError: If file doesn't exist
    """
    if not path.exists():
        raise FileNotFoundError(f"Configuration file not found: {path}")

    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        print(f"ERROR: JSON parse error in {path}: {exc}")
        raise


def report_validation_results(
    validator_name: str,
    errors: list[str],
    suggestions: dict[str, list[str]] | None = None,
    verbose: bool = False
) -> int:
    """Report validation results with consistent formatting.

    Args:
        validator_name: Human-readable validator name (e.g., "Houston features")
        errors: List of error messages
        suggestions: Optional dict mapping error categories to remediation steps
        verbose: Enable detailed output

    Returns:
        Exit code: 0 if passed, 1 if failed
    """
    if errors:
        print(f"\n❌ {validator_name} validation FAILED ({len(errors)} issues):\n")
        for i, error in enumerate(errors, 1):
            print(f"  {i}. {error}")

        # Print remediation suggestions if provided
        if suggestions:
            print("\n💡 Remediation suggestions:")
            for category, steps in suggestions.items():
                for step in steps:
                    print(f"  - {step}")

        return 1
    else:
        if verbose:
            print(f"\n✅ All {validator_name} validation checks passed")
        else:
            print(f"✅ {validator_name} validation passed")
        return 0


def get_remediation_suggestions(errors: list[str]) -> dict[str, list[str]]:
    """Generate remediation suggestions based on error content.

    Args:
        errors: List of error messages

    Returns:
        Dictionary mapping categories to remediation steps
    """
    suggestions = {}

    # Analyze error patterns and provide relevant suggestions
    error_text = " ".join(errors).lower()

    if "autonomous" in error_text:
        suggestions.setdefault("autonomous_mode", []).extend([
            "Review autonomous mode safety controls",
            "Ensure current_phase >= 3 before enabling deployment"
        ])

    if "phase" in error_text:
        suggestions.setdefault("phase_config", []).extend([
            "Update agency_levels.current_level to match phase requirements",
            "Document phase activation in notes/CHANGELOG.md"
        ])

    if "schema" in error_text or "jsonschema" in error_text:
        suggestions.setdefault("schema_validation", []).extend([
            "Install jsonschema: pip install jsonschema",
            "Review config structure against relevant schema file"
        ])

    if "taxonomy" in error_text or "topic" in error_text:
        suggestions.setdefault("taxonomy", []).extend([
            "Validate topics against taxonomies/topic_taxonomy.yaml",
            "Add missing topics to taxonomy or remove from config"
        ])

    if "routing" in error_text or "tags" in error_text:
        suggestions.setdefault("routing_tags", []).extend([
            "Add required routing tags (e.g., agent:houston, sensitivity:internal)",
            "Review DocMeta schema documentation"
        ])

    return suggestions


def verbose_check(condition: bool, message: str, verbose: bool = False) -> None:
    """Print verbose check result if verbose mode is enabled.

    Args:
        condition: Whether check passed
        message: Message describing the check
        verbose: Whether to print the message
    """
    if verbose and condition:
        print(f"✓ {message}")
