#!/usr/bin/env python3
"""Placeholder validator for Houston tool pipeline configuration."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import List

TOOLS_PATH = Path("30_config/houston-tools.json")


def parse_args(argv: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate Houston tool pipelines")
    parser.add_argument("--config", default=TOOLS_PATH, type=Path, help="Path to houston-tools.json")
    parser.add_argument(
        "--features-config",
        default=Path("30_config/houston-features.json"),
        type=Path,
        help="Optional path to houston-features.json for phase cross-checks",
    )
    parser.add_argument(
        "--tooling-notes",
        default=Path("notes/HOUSTON_TOOLING.md"),
        type=Path,
        help="Reference documentation for pipeline definitions",
    )
    return parser.parse_args(argv)


def cli(argv: List[str] | None = None) -> int:
    args = parse_args(argv or [])

    if not args.config.exists():
        print(f"Required config missing: {args.config}")
        return 1

    try:
        json.loads(args.config.read_text())
    except json.JSONDecodeError as exc:
        print(f"Invalid JSON in {args.config}: {exc}")
        return 2

    if args.features_config and args.features_config.exists():
        try:
            json.loads(args.features_config.read_text())
        except json.JSONDecodeError as exc:
            print(f"Invalid JSON in {args.features_config}: {exc}")
            return 2

    print("Tool pipeline validation stub. TODO: align phases, pipelines, and capabilities.")
    return 99


if __name__ == "__main__":
    raise SystemExit(cli())
