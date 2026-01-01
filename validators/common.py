"""Common utilities for Houston validators.

Provides shared functionality for loading configs, reporting results,
and handling errors consistently across all validators.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, cast

# Unicode to ASCII fallback mapping for Windows console compatibility
_UNICODE_FALLBACK = {
    "▶": ">",
    "✔": "[PASS]",
    "✖": "[FAIL]",
    "❌": "[FAIL]",
    "✅": "[OK]",
    "💡": "[TIP]",
    "✓": "[OK]",
}


def safe_print(*args, **kwargs) -> None:
    """Print with Unicode fallback for Windows console compatibility.

    Replaces Unicode characters with ASCII equivalents when the console
    encoding cannot handle them (common on Windows with cp1252).
    """
    message = " ".join(str(arg) for arg in args)
    try:
        print(message, **kwargs)
    except UnicodeEncodeError:
        for unicode_char, ascii_fallback in _UNICODE_FALLBACK.items():
            message = message.replace(unicode_char, ascii_fallback)
        print(message, **kwargs)


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
        data = json.loads(path.read_text())
        return cast(dict[str, Any], data)
    except json.JSONDecodeError as exc:
        print(f"ERROR: JSON parse error in {path}: {exc}")
        raise


def report_validation_results(
    validator_name: str,
    errors: list[str],
    suggestions: dict[str, list[str]] | None = None,
    verbose: bool = False,
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
        safe_print(f"\n❌ {validator_name} validation FAILED ({len(errors)} issues):\n")
        for i, error in enumerate(errors, 1):
            safe_print(f"  {i}. {error}")

        # Print remediation suggestions if provided
        if suggestions:
            safe_print("\n💡 Remediation suggestions:")
            for _category, steps in suggestions.items():
                for step in steps:
                    safe_print(f"  - {step}")

        return 1
    else:
        if verbose:
            safe_print(f"\n✅ All {validator_name} validation checks passed")
        else:
            safe_print(f"✅ {validator_name} validation passed")
        return 0


def get_remediation_suggestions(errors: list[str]) -> dict[str, list[str]]:
    """Generate remediation suggestions based on error content.

    Args:
        errors: List of error messages

    Returns:
        Dictionary mapping categories to remediation steps
    """
    suggestions: dict[str, list[str]] = {}

    # Analyze error patterns and provide relevant suggestions
    error_text = " ".join(errors).lower()

    if "autonomous" in error_text:
        suggestions.setdefault("autonomous_mode", []).extend(
            [
                "Review autonomous mode safety controls",
                "Ensure current_phase >= 3 before enabling deployment",
            ]
        )

    if "phase" in error_text:
        suggestions.setdefault("phase_config", []).extend(
            [
                "Update agency_levels.current_level to match phase requirements",
                "Document phase activation in notes/CHANGELOG.md",
            ]
        )

    if "schema" in error_text or "jsonschema" in error_text:
        suggestions.setdefault("schema_validation", []).extend(
            [
                "Install jsonschema: pip install jsonschema",
                "Review config structure against relevant schema file",
            ]
        )

    if "taxonomy" in error_text or "topic" in error_text:
        suggestions.setdefault("taxonomy", []).extend(
            [
                "Validate topics against taxonomies/topic_taxonomy.yaml",
                "Add missing topics to taxonomy or remove from config",
            ]
        )

    if "routing" in error_text or "tags" in error_text:
        suggestions.setdefault("routing_tags", []).extend(
            [
                "Add required routing tags (e.g., agent:houston, sensitivity:internal)",
                "Review DocMeta schema documentation",
            ]
        )

    return suggestions


def verbose_check(condition: bool, message: str, verbose: bool = False) -> None:
    """Print verbose check result if verbose mode is enabled.

    Args:
        condition: Whether check passed
        message: Message describing the check
        verbose: Whether to print the message
    """
    if verbose and condition:
        safe_print(f"✓ {message}")
