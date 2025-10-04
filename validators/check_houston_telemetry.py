#!/usr/bin/env python3
"""Placeholder validator for Houston telemetry freshness."""
from __future__ import annotations

import argparse
from pathlib import Path
from typing import List

DEFAULT_TELEMETRY = Path("70_evidence/houston_telemetry.jsonl")


def parse_args(argv: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate Houston telemetry feeds")
    parser.add_argument(
        "--telemetry",
        default=DEFAULT_TELEMETRY,
        type=Path,
        help="Path to telemetry JSONL file",
    )
    parser.add_argument(
        "--max-age",
        default=300,
        type=int,
        help="Maximum allowed staleness in seconds (default: 5 minutes)",
    )
    return parser.parse_args(argv)


def cli(argv: List[str] | None = None) -> int:
    args = parse_args(argv or [])

    if not args.telemetry.exists():
        print(f"Telemetry file not found: {args.telemetry}")
        return 1

    print(
        "Telemetry validation stub. TODO: check freshness, required fields, and latency thresholds (max_age=%s)."
        % args.max_age
    )
    return 99


if __name__ == "__main__":
    raise SystemExit(cli())
