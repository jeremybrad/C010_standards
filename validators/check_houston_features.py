#!/usr/bin/env python3
"""Placeholder validator for Houston feature configuration."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import List

FEATURES_PATH = Path("30_config/houston-features.json")
SCHEMA_PATH = Path("schemas/houston_features.schema.json")


def parse_args(argv: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate Houston features config")
    parser.add_argument("--config", default=FEATURES_PATH, type=Path, help="Path to houston-features.json")
    parser.add_argument("--schema", default=SCHEMA_PATH, type=Path, help="Path to JSON schema definition")
    return parser.parse_args(argv)


def cli(argv: List[str] | None = None) -> int:
    args = parse_args(argv or [])

    for path in (args.config, args.schema):
        if not path.exists():
            print(f"Required file not found: {path}")
            return 1

    try:
        json.loads(args.config.read_text())
        json.loads(args.schema.read_text())
    except json.JSONDecodeError as exc:
        print(f"JSON parse error: {exc}")
        return 2

    print("Feature toggle validation stub. TODO: validate against schema and trust phases.")
    return 99


if __name__ == "__main__":
    raise SystemExit(cli())
