#!/usr/bin/env python3
"""Orchestrate Houston validator suite.

This harness intentionally stops early once a validator exits with a non-zero
status so failures surface quickly during Phase 2 tooling bring-up.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import List

CURRENT_DIR = Path(__file__).resolve().parent
REPO_ROOT = CURRENT_DIR.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from validators import AVAILABLE_VALIDATORS, load_validator
from validators.common import safe_print


def parse_args(argv: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Houston validators")
    parser.add_argument(
        "--targets",
        nargs="*",
        default=list(AVAILABLE_VALIDATORS.keys()),
        help="Subset of validators to execute (default: all configured)",
    )
    parser.add_argument(
        "--pass-args",
        nargs=argparse.REMAINDER,
        help="Additional arguments forwarded verbatim to each validator",
    )
    return parser.parse_args(argv)


def main(argv: List[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])

    unknown = [name for name in args.targets if name not in AVAILABLE_VALIDATORS]
    if unknown:
        print(f"Unknown validator(s): {', '.join(unknown)}", file=sys.stderr)
        print(f"Available: {', '.join(sorted(AVAILABLE_VALIDATORS))}", file=sys.stderr)
        return 2

    extra_args = args.pass_args or []

    for target in args.targets:
        module_name = AVAILABLE_VALIDATORS[target]
        cli = load_validator(module_name)
        safe_print(f"▶ Running {target} ({module_name})")
        result = cli(extra_args)
        if result != 0:
            safe_print(f"✖ {target} exited with status {result}", file=sys.stderr)
            return result
        safe_print(f"✔ {target} passed")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
