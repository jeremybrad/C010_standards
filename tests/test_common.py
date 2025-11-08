"""Tests for validators.common module."""
from __future__ import annotations

import json
from pathlib import Path
import tempfile

import pytest

from validators.common import (
    load_json_config,
    report_validation_results,
    get_remediation_suggestions,
    verbose_check,
)


class TestLoadJsonConfig:
    """Tests for load_json_config function."""

    def test_load_valid_json(self, tmp_path: Path):
        """Test loading a valid JSON file."""
        test_file = tmp_path / "test.json"
        test_data = {"key": "value", "number": 42}
        test_file.write_text(json.dumps(test_data))

        result = load_json_config(test_file)
        assert result == test_data

    def test_load_missing_file(self, tmp_path: Path):
        """Test loading a non-existent file raises FileNotFoundError."""
        test_file = tmp_path / "missing.json"

        with pytest.raises(FileNotFoundError):
            load_json_config(test_file)

    def test_load_invalid_json(self, tmp_path: Path):
        """Test loading invalid JSON raises JSONDecodeError."""
        test_file = tmp_path / "invalid.json"
        test_file.write_text("{invalid json}")

        with pytest.raises(json.JSONDecodeError):
            load_json_config(test_file)


class TestReportValidationResults:
    """Tests for report_validation_results function."""

    def test_report_success(self, capsys):
        """Test reporting successful validation."""
        result = report_validation_results("Test validator", [], verbose=False)

        assert result == 0
        captured = capsys.readouterr()
        assert "✅" in captured.out
        assert "Test validator validation passed" in captured.out

    def test_report_success_verbose(self, capsys):
        """Test reporting successful validation in verbose mode."""
        result = report_validation_results("Test validator", [], verbose=True)

        assert result == 0
        captured = capsys.readouterr()
        assert "✅" in captured.out
        assert "All Test validator validation checks passed" in captured.out

    def test_report_failures(self, capsys):
        """Test reporting validation failures."""
        errors = ["Error 1", "Error 2"]
        result = report_validation_results("Test validator", errors, verbose=False)

        assert result == 1
        captured = capsys.readouterr()
        assert "❌" in captured.out
        assert "Test validator validation FAILED" in captured.out
        assert "Error 1" in captured.out
        assert "Error 2" in captured.out

    def test_report_with_suggestions(self, capsys):
        """Test reporting with remediation suggestions."""
        errors = ["Phase error"]
        suggestions = {"phase_config": ["Fix phase setting"]}
        result = report_validation_results(
            "Test validator", errors, suggestions, verbose=False
        )

        assert result == 1
        captured = capsys.readouterr()
        assert "💡 Remediation suggestions:" in captured.out
        assert "Fix phase setting" in captured.out


class TestGetRemediationSuggestions:
    """Tests for get_remediation_suggestions function."""

    def test_autonomous_suggestions(self):
        """Test autonomous error suggestions."""
        errors = ["CRITICAL: autonomous mode misconfigured"]
        suggestions = get_remediation_suggestions(errors)

        assert "autonomous_mode" in suggestions
        assert any("safety controls" in s.lower() for s in suggestions["autonomous_mode"])

    def test_phase_suggestions(self):
        """Test phase error suggestions."""
        errors = ["Phase 3 required but current is 1"]
        suggestions = get_remediation_suggestions(errors)

        assert "phase_config" in suggestions
        assert any("changelog" in s.lower() for s in suggestions["phase_config"])

    def test_schema_suggestions(self):
        """Test schema error suggestions."""
        errors = ["Schema validation failed"]
        suggestions = get_remediation_suggestions(errors)

        assert "schema_validation" in suggestions
        assert any("jsonschema" in s.lower() for s in suggestions["schema_validation"])


class TestVerboseCheck:
    """Tests for verbose_check function."""

    def test_verbose_true_prints(self, capsys):
        """Test that verbose_check prints when verbose=True."""
        verbose_check(True, "Test message", verbose=True)

        captured = capsys.readouterr()
        assert "✓ Test message" in captured.out

    def test_verbose_false_no_print(self, capsys):
        """Test that verbose_check doesn't print when verbose=False."""
        verbose_check(True, "Test message", verbose=False)

        captured = capsys.readouterr()
        assert captured.out == ""

    def test_condition_false_no_print(self, capsys):
        """Test that verbose_check doesn't print when condition=False."""
        verbose_check(False, "Test message", verbose=True)

        captured = capsys.readouterr()
        assert captured.out == ""
