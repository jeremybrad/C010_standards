#!/usr/bin/env python3
"""Placeholder validator for Houston model inventory and fallbacks."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import List

DEFAULT_CONFIG = Path("30_config/houston.json")
DEFAULT_FEATURES = Path("30_config/houston-features.json")
DEFAULT_MODELS = Path("~/models/config/houston-models.json").expanduser()


def parse_args(argv: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate Houston model configuration")
    parser.add_argument("--houston-config", default=DEFAULT_CONFIG, type=Path)
    parser.add_argument("--features-config", default=DEFAULT_FEATURES, type=Path)
    parser.add_argument("--model-inventory", default=DEFAULT_MODELS, type=Path, help="Path to houston-models.json")
    parser.add_argument("--installed-models", type=Path, help="Optional JSON list from `ollama list --json`")
    return parser.parse_args(argv)


def _load_json(path: Path) -> bool:
    try:
        json.loads(path.read_text())
        return True
    except json.JSONDecodeError as exc:
        print(f"JSON decode error in {path}: {exc}")
        return False


def cli(argv: List[str] | None = None) -> int:
    args = parse_args(argv or [])

    required_paths = [args.houston_config, args.features_config, args.model_inventory]
    missing = [path for path in required_paths if not path.exists()]
    if missing:
        for path in missing:
            print(f"Required configuration missing: {path}")
        return 1

    for path in required_paths:
        if not _load_json(path):
            return 2

    if args.installed_models and args.installed_models.exists():
        if not _load_json(args.installed_models):
            return 2

    print("Model inventory validation stub. TODO: confirm fallback chains and trust phasing.")
    return 99


if __name__ == "__main__":
    raise SystemExit(cli())
