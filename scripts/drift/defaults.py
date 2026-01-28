"""Default drift rules for repo-agnostic scanning.

Provides universal rules that work for any Betty Protocol repo,
plus resolution logic for finding and loading repo-specific overrides.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any


def universal_rules() -> dict[str, Any]:
    """Return minimal rules that work for any Betty Protocol repo.

    These avoid C10-specific expectations (validators, schemas, taxonomies)
    and focus on canonical docs that every repo should have.
    """
    return {
        "canonical_scope": [
            "README.md",
            "CLAUDE.md",
            "META.yaml",
            "CHANGELOG.md",
            "PROJECT_PRIMER.md",
        ],
        "excludes": [
            "20_receipts/**",
            "70_evidence/**",
            "90_archive/**",
            "__pycache__/**",
            ".git/**",
            "node_modules/**",
            "venv/**",
            ".venv/**",
            "*-env/**",
        ],
        "protected_from_archive": [
            "20_receipts/**",
            "70_evidence/**",
            "README.md",
            "CLAUDE.md",
            "META.yaml",
            "CHANGELOG.md",
            "PROJECT_PRIMER.md",
        ],
        "stale_path_patterns": [],
    }


# Top-level keys recognised in drift_rules.yaml
_KNOWN_KEYS = {
    "canonical_scope",
    "excludes",
    "protected_from_archive",
    "stale_path_patterns",
    "validator_inventory",
    "link_validation",
    "archive_candidates",
    "generator_drift",
}


def resolve_rules(
    cli_rules_path: Path | None,
    repo_root: Path,
    verbose: bool = False,
) -> dict[str, Any]:
    """Resolve drift rules using precedence: CLI flag > repo file > universal defaults.

    Args:
        cli_rules_path: Explicit --rules path from CLI (highest priority).
        repo_root: Target repo root for locating ``30_config/drift_rules.yaml``.
        verbose: Log which source was selected.

    Returns:
        Parsed rules dictionary.
    """
    try:
        import yaml
        has_yaml = True
    except ImportError:
        has_yaml = False

    # 1. Explicit CLI path
    if cli_rules_path is not None:
        rules = _load_yaml(cli_rules_path, has_yaml, verbose)
        if rules is not None:
            if verbose:
                print(f"  Loaded rules from: {cli_rules_path}")
            _warn_unknown_keys(rules, str(cli_rules_path), verbose)
            return rules

    # 2. Repo-local drift_rules.yaml
    repo_rules_path = repo_root / "30_config" / "drift_rules.yaml"
    if repo_rules_path.is_file():
        rules = _load_yaml(repo_rules_path, has_yaml, verbose)
        if rules is not None:
            if verbose:
                print(f"  Loaded rules from: {repo_rules_path}")
            _warn_unknown_keys(rules, str(repo_rules_path), verbose)
            return rules

    # 3. Universal defaults
    if verbose:
        print("  Using universal defaults (no drift_rules.yaml found)")
    return universal_rules()


def _load_yaml(path: Path, has_yaml: bool, verbose: bool) -> dict[str, Any] | None:
    """Attempt to load a YAML file, returning None on failure."""
    if not path.exists():
        if verbose:
            print(f"  Warning: Rules file not found: {path}")
        return None

    if not has_yaml:
        if verbose:
            print("  Warning: PyYAML not installed, falling back to defaults")
        return None

    import yaml

    try:
        data = yaml.safe_load(path.read_text())
        return data if isinstance(data, dict) else None
    except Exception as e:
        if verbose:
            print(f"  Warning: Could not parse {path}: {e}")
        return None


def _warn_unknown_keys(rules: dict[str, Any], source: str, verbose: bool) -> None:
    """Warn about unrecognised top-level keys (don't fail)."""
    unknown = set(rules.keys()) - _KNOWN_KEYS
    if unknown and verbose:
        print(f"  Warning: Unknown keys in {source}: {sorted(unknown)}")
    if verbose:
        consumed = sorted(set(rules.keys()) & _KNOWN_KEYS)
        print(f"  Consumed keys: {consumed}")
