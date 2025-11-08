"""Tests for check_houston_telemetry validator."""
from __future__ import annotations

import sys
from datetime import datetime, timedelta
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from validators.check_houston_telemetry import (
    validate_freshness,
    validate_required_fields,
    validate_latency_thresholds,
    validate_fallback_loops,
)


class TestValidateFreshness:
    """Tests for validate_freshness function."""

    def test_empty_entries(self):
        """Test with no telemetry entries."""
        errors = validate_freshness([], max_age_seconds=300, verbose=False)
        assert len(errors) == 1
        assert "No telemetry entries" in errors[0]

    def test_fresh_entry(self):
        """Test with recent entry within max age."""
        now = datetime.now()
        entries = [
            {"timestamp": now.isoformat()}
        ]

        errors = validate_freshness(entries, max_age_seconds=300, verbose=False)
        assert errors == []

    def test_stale_entry(self):
        """Test with stale entry beyond max age."""
        old_time = datetime.now() - timedelta(seconds=600)
        entries = [
            {"timestamp": old_time.isoformat()}
        ]

        errors = validate_freshness(entries, max_age_seconds=300, verbose=False)
        assert len(errors) == 1
        assert "stale" in errors[0].lower()

    def test_missing_timestamp(self):
        """Test with missing timestamp field."""
        entries = [
            {"host": "localhost"}
        ]

        errors = validate_freshness(entries, max_age_seconds=300, verbose=False)
        assert len(errors) == 1
        assert "missing timestamp" in errors[0].lower()

    def test_invalid_timestamp_format(self):
        """Test with invalid timestamp format."""
        entries = [
            {"timestamp": "not-a-valid-timestamp"}
        ]

        errors = validate_freshness(entries, max_age_seconds=300, verbose=False)
        assert len(errors) == 1
        assert "Invalid timestamp" in errors[0]


class TestValidateRequiredFields:
    """Tests for validate_required_fields function."""

    def test_all_fields_present(self):
        """Test with all required fields present."""
        entries = [
            {
                "host": "localhost",
                "model": "gpt-4",
                "latency_ms": 1000,
                "fallback_chain": [],
                "manual_override": False
            }
        ]

        errors = validate_required_fields(entries, verbose=False)
        assert errors == []

    def test_missing_single_field(self):
        """Test with one missing required field."""
        entries = [
            {
                "host": "localhost",
                "model": "gpt-4",
                "latency_ms": 1000,
                "manual_override": False
                # Missing fallback_chain
            }
        ]

        errors = validate_required_fields(entries, verbose=False)
        assert len(errors) == 1
        assert "missing required fields" in errors[0].lower()

    def test_missing_multiple_fields(self):
        """Test with multiple missing required fields."""
        entries = [
            {
                "host": "localhost"
                # Missing model, latency_ms, fallback_chain, manual_override
            }
        ]

        errors = validate_required_fields(entries, verbose=False)
        assert len(errors) == 1

    def test_some_entries_missing_fields(self):
        """Test with some entries missing fields."""
        entries = [
            {
                "host": "localhost",
                "model": "gpt-4",
                "latency_ms": 1000,
                "fallback_chain": [],
                "manual_override": False
            },
            {
                "host": "localhost",
                "model": "gpt-4"
                # Missing fields
            }
        ]

        errors = validate_required_fields(entries, verbose=False)
        assert len(errors) == 1


class TestValidateLatencyThresholds:
    """Tests for validate_latency_thresholds function."""

    def test_normal_latency(self):
        """Test with normal latency values."""
        entries = [
            {"latency_ms": 1000},
            {"latency_ms": 2000},
            {"latency_ms": 1500}
        ]

        errors = validate_latency_thresholds(entries, verbose=False)
        assert errors == []

    def test_high_average_latency(self):
        """Test with high average latency."""
        entries = [
            {"latency_ms": 6000},
            {"latency_ms": 7000},
            {"latency_ms": 8000}
        ]

        errors = validate_latency_thresholds(entries, verbose=False)
        assert len(errors) == 1
        assert "Average latency" in errors[0]

    def test_individual_high_latency(self):
        """Test with individual high latency spike that affects average."""
        entries = [
            {"latency_ms": 1000},
            {"latency_ms": 15000},  # Spike over 10s
            {"latency_ms": 1000}
        ]

        # Average is 5666ms which exceeds 5s threshold
        errors = validate_latency_thresholds(entries, verbose=False)
        assert len(errors) == 1
        assert "Average latency" in errors[0]

    def test_missing_latency_values(self):
        """Test handling of missing latency values."""
        entries = [
            {"other_field": "value"}
        ]

        errors = validate_latency_thresholds(entries, verbose=False)
        # Should not error if no latency data
        assert errors == []


class TestValidateFallbackLoops:
    """Tests for validate_fallback_loops function."""

    def test_no_fallback(self):
        """Test with no fallback chain."""
        entries = [
            {"fallback_chain": []}
        ]

        errors = validate_fallback_loops(entries, verbose=False)
        assert errors == []

    def test_short_fallback_chain(self):
        """Test with acceptable fallback chain length."""
        entries = [
            {"fallback_chain": ["model1", "model2", "model3"]}
        ]

        errors = validate_fallback_loops(entries, verbose=False)
        assert errors == []

    def test_excessive_fallback_chain(self):
        """Test with excessive fallback chain indicating loop."""
        entries = [
            {"fallback_chain": ["model1", "model2", "model3", "model4", "model5"]}
        ]

        errors = validate_fallback_loops(entries, verbose=False)
        assert len(errors) == 1
        assert "Excessive fallback" in errors[0]

    def test_multiple_entries_some_excessive(self):
        """Test with multiple entries, some with excessive chains."""
        entries = [
            {"fallback_chain": ["model1"]},
            {"fallback_chain": ["model1", "model2", "model3", "model4"]},
            {"fallback_chain": ["model1", "model2"]}
        ]

        errors = validate_fallback_loops(entries, verbose=False)
        assert len(errors) == 1

    def test_missing_fallback_chain_field(self):
        """Test handling of missing fallback_chain field."""
        entries = [
            {"other_field": "value"}
        ]

        errors = validate_fallback_loops(entries, verbose=False)
        # Should not error if field is missing
        assert errors == []
