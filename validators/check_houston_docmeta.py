#!/usr/bin/env python3
"""Placeholder for Houston DocMeta tag validator.

Current behaviour: validate required paths exist, then exit with status 99 to
signal unimplemented logic. This keeps CI honest while the implementation is
under construction.
"""
from __future__ import annotations

import argparse
from pathlib import Path
from typing import List

DEFAULT_TARGETS = (
    "schemas",
    "notes",
)


def parse_args(argv: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check Houston DocMeta tagging")
    parser.add_argument(
        "paths",
        nargs="*",
        default=DEFAULT_TARGETS,
        help="Directories or files to inspect for Houston-tagged DocMeta entries",
    )
    return parser.parse_args(argv)


def cli(argv: List[str] | None = None) -> int:
    args = parse_args(argv or [])

    missing = [path for path in args.paths if not Path(path).exists()]
    if missing:
        for item in missing:
            print(f"WARN: Missing path (skipped for stub): {item}")
        # Allow missing paths during stub phase; warn but don't fail

    print("DocMeta tag validation not yet implemented. TODO: enforce routing tags, projects, and topic taxonomy alignment.")
    return 99


if __name__ == "__main__":
    raise SystemExit(cli())
