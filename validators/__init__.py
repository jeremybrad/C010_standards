"""Validator package scaffolding for Houston metadata governance."""

from collections.abc import Callable
from importlib import import_module
from typing import cast

ValidatorFn = Callable[[list], int]


def load_validator(name: str) -> ValidatorFn:
    """Dynamically import a validator module and return its `cli` entry point."""
    module = import_module(f"validators.{name}")
    if not hasattr(module, "cli"):
        raise AttributeError(f"Validator '{name}' missing required 'cli' callable")
    return cast(ValidatorFn, module.cli)


AVAILABLE_VALIDATORS: dict[str, str] = {
    "houston_docmeta": "check_houston_docmeta",
    "houston_features": "check_houston_features",
    "houston_tools": "check_houston_tools",
    "houston_models": "check_houston_models",
    "houston_telemetry": "check_houston_telemetry",
    "repo_contract": "check_repo_contract",
    "constitution": "check_constitution",
    "capsulemeta": "check_capsulemeta",
    "epoch": "check_epoch",
}
"""Mapping between CLI-friendly validator names and module suffixes."""
