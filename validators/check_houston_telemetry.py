#!/usr/bin/env python3
"""Validator for Houston telemetry freshness and quality.

Ensures health monitoring data feeding Houston is current and complete.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from validators.common import safe_print

DEFAULT_TELEMETRY = Path("70_evidence/houston_telemetry.jsonl")


def parse_args(argv: list[str]) -> argparse.Namespace:
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
    parser.add_argument(
        "--watch", action="store_true", help="Watch mode (not implemented)"
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Show detailed output"
    )
    parser.add_argument(
        "--json-output",
        type=Path,
        help="Write results to JSON file (e.g., 70_evidence/validator_telemetry.json)",
    )
    return parser.parse_args(argv)


def parse_jsonl(telemetry_path: Path) -> list[dict[str, Any]]:
    """Parse JSONL telemetry file."""
    entries: list[dict[str, Any]] = []
    if not telemetry_path.exists():
        return entries

    for line in telemetry_path.read_text().strip().split("\n"):
        if not line:
            continue
        try:
            entries.append(json.loads(line))
        except json.JSONDecodeError:
            continue

    return entries


def validate_freshness(
    entries: list[dict], max_age_seconds: int, verbose: bool = False
) -> list[str]:
    """Check if most recent entry is within allowed staleness."""
    errors = []

    if not entries:
        errors.append("No telemetry entries found")
        return errors

    # Get most recent entry (assume entries are ordered chronologically)
    last_entry = entries[-1]
    timestamp_str = last_entry.get("timestamp")

    if not timestamp_str:
        errors.append("Most recent entry missing timestamp field")
        return errors

    try:
        # Parse ISO format timestamp
        timestamp = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
        now = datetime.now(timestamp.tzinfo)
        age = (now - timestamp).total_seconds()

        if age > max_age_seconds:
            errors.append(
                f"Telemetry stale: {int(age)}s old (max {max_age_seconds}s). "
                f"Last: {timestamp_str}"
            )
        elif verbose:
            safe_print(
                f"✓ Freshness check passed (age={int(age)}s, max={max_age_seconds}s)"
            )

    except (ValueError, TypeError) as e:
        errors.append(f"Invalid timestamp format: {timestamp_str} ({e})")

    return errors


def validate_required_fields(entries: list[dict], verbose: bool = False) -> list[str]:
    """Check that entries contain required fields."""
    errors = []
    required = {"host", "model", "latency_ms", "fallback_chain", "manual_override"}

    missing_fields_per_entry = {}
    for i, entry in enumerate(entries):
        missing = required - set(entry.keys())
        if missing:
            missing_fields_per_entry[i] = missing

    if missing_fields_per_entry:
        errors.append(
            f"{len(missing_fields_per_entry)} entries missing required fields. "
            f"First entry example: {list(missing_fields_per_entry.values())[0]}"
        )
    elif verbose:
        safe_print(f"✓ Required fields check passed ({len(entries)} entries)")

    return errors


def validate_latency_thresholds(
    entries: list[dict], verbose: bool = False
) -> list[str]:
    """Check latency thresholds and averages."""
    errors = []
    warnings = []

    # Check individual entries
    for i, entry in enumerate(entries):
        latency = entry.get("latency_ms")
        if latency is None:
            continue

        if latency > 10000:  # 10s threshold
            warnings.append(f"Entry {i}: High latency {latency}ms (>10s)")

    # Check average over last 20 entries
    recent_entries = entries[-20:]
    latencies: list[float] = [
        float(e["latency_ms"])
        for e in recent_entries
        if e.get("latency_ms") is not None
    ]

    if latencies:
        avg_latency = sum(latencies) / len(latencies)
        if avg_latency > 5000:  # 5s average threshold
            errors.append(
                f"Avg latency {int(avg_latency)}ms over {len(latencies)} entries "
                "(>5s threshold)"
            )
        elif verbose:
            safe_print(f"✓ Latency OK (avg={int(avg_latency)}ms, n={len(latencies)})")

    if warnings and verbose:
        for warning in warnings[:3]:  # Show first 3 warnings
            print(f"  ⚠️  {warning}")

    return errors


def validate_fallback_loops(entries: list[dict], verbose: bool = False) -> list[str]:
    """Flag excessive fallback chain lengths."""
    errors = []

    for i, entry in enumerate(entries):
        chain = entry.get("fallback_chain", [])
        if isinstance(chain, list) and len(chain) > 3:
            errors.append(
                f"Entry {i}: Excessive fallback chain length {len(chain)} (>3). "
                "May indicate fallback loop."
            )

    if not errors and verbose:
        safe_print("✓ Fallback loop check passed")

    return errors


def cli(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)

    if args.watch:
        print("ERROR: --watch mode not yet implemented")
        return 2

    # Parse telemetry file
    if not args.telemetry.exists():
        print(f"NOTE: Telemetry file not found: {args.telemetry}")
        safe_print("✅ Houston telemetry validation passed (no telemetry to validate)")
        return 0

    entries = parse_jsonl(args.telemetry)

    if args.verbose:
        print(f"Loaded {len(entries)} telemetry entries from {args.telemetry}\n")

    # Run validation checks
    all_errors: list[str] = []

    all_errors.extend(validate_freshness(entries, args.max_age, args.verbose))
    all_errors.extend(validate_required_fields(entries, args.verbose))
    all_errors.extend(validate_latency_thresholds(entries, args.verbose))
    all_errors.extend(validate_fallback_loops(entries, args.verbose))

    # Write JSON output if requested
    if args.json_output:
        args.json_output.parent.mkdir(parents=True, exist_ok=True)
        output_data = {
            "total_entries": len(entries),
            "validation_time": datetime.now().isoformat(),
            "max_age_seconds": args.max_age,
            "passed": len(all_errors) == 0,
            "errors": all_errors,
        }
        args.json_output.write_text(json.dumps(output_data, indent=2))
        if args.verbose:
            print(f"\nResults written to {args.json_output}")

    # Report results
    if all_errors:
        safe_print(
            f"\n❌ Houston telemetry validation FAILED ({len(all_errors)} issues):\n"
        )
        for i, error in enumerate(all_errors, 1):
            safe_print(f"  {i}. {error}")

        safe_print("\n💡 Remediation suggestions:")
        safe_print("  - Ensure telemetry collection is running")
        safe_print("  - Check Mission Control health monitoring service")
        safe_print("  - Review fallback chain configuration if loops detected")
        safe_print("  - Investigate latency spikes in model inference")

        return 1
    else:
        if args.verbose:
            safe_print("\n✅ All Houston telemetry validation checks passed")
        else:
            safe_print("✅ Houston telemetry validation passed")
        return 0


if __name__ == "__main__":
    raise SystemExit(cli())
