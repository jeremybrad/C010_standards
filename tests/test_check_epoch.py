"""Tests for check_epoch validator."""

from __future__ import annotations

import hashlib
import subprocess
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from validators.check_epoch import (
    EPOCH_SPEC_V1,
    GIT_HASH_PATTERN,
    KNOWN_TOP_LEVEL_FIELDS,
    calculate_file_sha256,
    cli,
    get_git_head,
    load_epoch_yaml,
    validate_epoch,
    validate_iso8601,
    validate_primer_sync,
    validate_required_fields,
    validate_strict_mode,
    validate_unknown_fields,
)


class TestLoadEpochYaml:
    """Tests for load_epoch_yaml function."""

    def test_valid_epoch_yaml(self, tmp_path: Path):
        """Test loading valid EPOCH.yaml."""
        content = """
epoch_schema: "c010.epoch.v1"
repo_id: "test-repo"
repo_head: "abc1234"
generated_at_utc: "2026-01-17T14:30:00Z"
"""
        file_path = tmp_path / "EPOCH.yaml"
        file_path.write_text(content)

        result = load_epoch_yaml(file_path)
        assert result is not None
        assert result["epoch_schema"] == "c010.epoch.v1"
        assert result["repo_id"] == "test-repo"

    def test_missing_epoch_yaml(self, tmp_path: Path):
        """Test missing EPOCH.yaml returns None."""
        file_path = tmp_path / "EPOCH.yaml"
        result = load_epoch_yaml(file_path)
        assert result is None

    def test_invalid_yaml_syntax(self, tmp_path: Path):
        """Test invalid YAML syntax returns None."""
        content = """
epoch_schema: "c010.epoch.v1"
  bad indentation: here
"""
        file_path = tmp_path / "EPOCH.yaml"
        file_path.write_text(content)

        result = load_epoch_yaml(file_path)
        assert result is None

    def test_non_dict_yaml(self, tmp_path: Path):
        """Test YAML that doesn't parse to dict returns None."""
        content = "- item1\n- item2\n"
        file_path = tmp_path / "EPOCH.yaml"
        file_path.write_text(content)

        result = load_epoch_yaml(file_path)
        assert result is None


class TestEpochRequiredFields:
    """Tests for required field validation."""

    def test_valid_all_required_fields(self):
        """Test validation passes with all required fields."""
        data = {
            "epoch_schema": EPOCH_SPEC_V1,
            "repo_id": "test-repo",
            "repo_head": "abc1234",
            "generated_at_utc": "2026-01-17T14:30:00Z",
        }
        errors = validate_required_fields(data)
        assert errors == []

    def test_missing_epoch_schema(self):
        """Test validation fails with missing epoch_schema."""
        data = {
            "repo_id": "test-repo",
            "repo_head": "abc1234",
            "generated_at_utc": "2026-01-17T14:30:00Z",
        }
        errors = validate_required_fields(data)
        assert len(errors) == 1
        assert "epoch_schema" in errors[0]

    def test_wrong_epoch_schema(self):
        """Test validation fails with wrong epoch_schema."""
        data = {
            "epoch_schema": "wrong.schema.v1",
            "repo_id": "test-repo",
            "repo_head": "abc1234",
            "generated_at_utc": "2026-01-17T14:30:00Z",
        }
        errors = validate_required_fields(data)
        assert len(errors) == 1
        assert "epoch_schema" in errors[0]
        assert "wrong.schema.v1" in errors[0]

    def test_empty_repo_id(self):
        """Test validation fails with empty repo_id."""
        data = {
            "epoch_schema": EPOCH_SPEC_V1,
            "repo_id": "   ",
            "repo_head": "abc1234",
            "generated_at_utc": "2026-01-17T14:30:00Z",
        }
        errors = validate_required_fields(data)
        assert len(errors) == 1
        assert "repo_id" in errors[0]

    def test_missing_repo_id(self):
        """Test validation fails with missing repo_id."""
        data = {
            "epoch_schema": EPOCH_SPEC_V1,
            "repo_head": "abc1234",
            "generated_at_utc": "2026-01-17T14:30:00Z",
        }
        errors = validate_required_fields(data)
        assert len(errors) == 1
        assert "repo_id" in errors[0]

    def test_invalid_repo_head_format(self):
        """Test validation fails with invalid repo_head format."""
        data = {
            "epoch_schema": EPOCH_SPEC_V1,
            "repo_id": "test-repo",
            "repo_head": "not-a-hash",
            "generated_at_utc": "2026-01-17T14:30:00Z",
        }
        errors = validate_required_fields(data)
        assert len(errors) == 1
        assert "repo_head" in errors[0]

    def test_short_git_hash_valid(self):
        """Test 7-character git hash is valid."""
        data = {
            "epoch_schema": EPOCH_SPEC_V1,
            "repo_id": "test-repo",
            "repo_head": "abc1234",  # 7 chars
            "generated_at_utc": "2026-01-17T14:30:00Z",
        }
        errors = validate_required_fields(data)
        assert errors == []

    def test_full_git_hash_valid(self):
        """Test 40-character git hash is valid."""
        data = {
            "epoch_schema": EPOCH_SPEC_V1,
            "repo_id": "test-repo",
            "repo_head": "a" * 40,  # 40 chars
            "generated_at_utc": "2026-01-17T14:30:00Z",
        }
        errors = validate_required_fields(data)
        assert errors == []

    def test_too_short_git_hash_invalid(self):
        """Test 6-character git hash is invalid."""
        data = {
            "epoch_schema": EPOCH_SPEC_V1,
            "repo_id": "test-repo",
            "repo_head": "abc123",  # 6 chars
            "generated_at_utc": "2026-01-17T14:30:00Z",
        }
        errors = validate_required_fields(data)
        assert len(errors) == 1
        assert "repo_head" in errors[0]

    def test_uppercase_git_hash_invalid(self):
        """Test uppercase characters in git hash are invalid."""
        data = {
            "epoch_schema": EPOCH_SPEC_V1,
            "repo_id": "test-repo",
            "repo_head": "ABC1234",  # uppercase
            "generated_at_utc": "2026-01-17T14:30:00Z",
        }
        errors = validate_required_fields(data)
        assert len(errors) == 1
        assert "repo_head" in errors[0]

    def test_invalid_generated_at_utc(self):
        """Test validation fails with invalid timestamp."""
        data = {
            "epoch_schema": EPOCH_SPEC_V1,
            "repo_id": "test-repo",
            "repo_head": "abc1234",
            "generated_at_utc": "not-a-date",
        }
        errors = validate_required_fields(data)
        assert len(errors) == 1
        assert "generated_at_utc" in errors[0]
        assert "ISO 8601" in errors[0]

    def test_missing_generated_at_utc(self):
        """Test validation fails with missing timestamp."""
        data = {
            "epoch_schema": EPOCH_SPEC_V1,
            "repo_id": "test-repo",
            "repo_head": "abc1234",
        }
        errors = validate_required_fields(data)
        assert len(errors) == 1
        assert "generated_at_utc" in errors[0]


class TestValidateIso8601:
    """Tests for validate_iso8601 function."""

    def test_valid_datetime_with_z(self):
        """Test valid ISO 8601 datetime with Z timezone."""
        assert validate_iso8601("2026-01-17T14:30:00Z") is True

    def test_valid_datetime_with_offset(self):
        """Test valid ISO 8601 datetime with timezone offset."""
        assert validate_iso8601("2026-01-17T14:30:00+05:00") is True
        assert validate_iso8601("2026-01-17T14:30:00-08:00") is True

    def test_valid_date_only(self):
        """Test valid ISO 8601 date only."""
        assert validate_iso8601("2026-01-17") is True

    def test_valid_with_milliseconds(self):
        """Test valid ISO 8601 with milliseconds."""
        assert validate_iso8601("2026-01-17T14:30:00.123Z") is True

    def test_invalid_format(self):
        """Test invalid datetime format."""
        assert validate_iso8601("01/17/2026") is False
        assert validate_iso8601("2026-1-17") is False
        assert validate_iso8601("not a date") is False

    def test_non_string(self):
        """Test non-string input."""
        assert validate_iso8601(12345) is False
        assert validate_iso8601(None) is False


class TestEpochPrimerSync:
    """Tests for primer synchronization validation."""

    def test_primer_exists_and_matches(self, tmp_path: Path):
        """Test validation passes when primer exists and SHA matches."""
        primer_content = "# Test Primer\n\nSome content."
        primer_file = tmp_path / "PROJECT_PRIMER.md"
        primer_file.write_text(primer_content)

        expected_sha = hashlib.sha256(primer_content.encode()).hexdigest()

        data = {
            "primer": {
                "sha256": expected_sha,
                "path": "PROJECT_PRIMER.md",
            }
        }

        errors = validate_primer_sync(data, tmp_path)
        assert errors == []

    def test_primer_exists_sha256_mismatch(self, tmp_path: Path):
        """Test validation fails when primer SHA doesn't match."""
        primer_content = "# Test Primer\n\nSome content."
        primer_file = tmp_path / "PROJECT_PRIMER.md"
        primer_file.write_text(primer_content)

        data = {
            "primer": {
                "sha256": "0" * 64,  # Wrong hash
                "path": "PROJECT_PRIMER.md",
            }
        }

        errors = validate_primer_sync(data, tmp_path)
        assert len(errors) == 1
        assert "mismatch" in errors[0]

    def test_primer_file_exists_but_block_missing(self, tmp_path: Path):
        """Test validation fails when primer file exists but block is missing."""
        primer_file = tmp_path / "PROJECT_PRIMER.md"
        primer_file.write_text("# Test Primer")

        data = {}  # No primer block

        errors = validate_primer_sync(data, tmp_path)
        assert len(errors) == 1
        assert "missing" in errors[0].lower()

    def test_primer_block_without_sha256(self, tmp_path: Path):
        """Test validation fails when primer block lacks sha256."""
        primer_file = tmp_path / "PROJECT_PRIMER.md"
        primer_file.write_text("# Test Primer")

        data = {
            "primer": {
                "path": "PROJECT_PRIMER.md",
                # Missing sha256
            }
        }

        errors = validate_primer_sync(data, tmp_path)
        assert len(errors) == 1
        assert "sha256" in errors[0]

    def test_no_primer_file_no_block_ok(self, tmp_path: Path):
        """Test validation passes when no primer file and no block."""
        # tmp_path has no PROJECT_PRIMER.md
        data = {}

        errors = validate_primer_sync(data, tmp_path)
        assert errors == []

    def test_custom_primer_path(self, tmp_path: Path):
        """Test validation works with custom primer path."""
        custom_path = "docs/PRIMER.md"
        (tmp_path / "docs").mkdir()
        primer_file = tmp_path / custom_path
        primer_content = "Custom primer content"
        primer_file.write_text(primer_content)

        expected_sha = hashlib.sha256(primer_content.encode()).hexdigest()

        data = {
            "primer": {
                "sha256": expected_sha,
                "path": custom_path,
            }
        }

        errors = validate_primer_sync(data, tmp_path)
        assert errors == []


class TestEpochStrictMode:
    """Tests for strict mode validation."""

    def test_repo_head_matches_git_head(self, tmp_path: Path):
        """Test validation passes when repo_head matches git HEAD."""
        # Initialize git repo
        subprocess.run(["git", "init"], cwd=tmp_path, capture_output=True)
        subprocess.run(
            ["git", "config", "user.email", "test@test.com"],
            cwd=tmp_path,
            capture_output=True,
        )
        subprocess.run(
            ["git", "config", "user.name", "Test"],
            cwd=tmp_path,
            capture_output=True,
        )
        (tmp_path / "test.txt").write_text("test")
        subprocess.run(["git", "add", "."], cwd=tmp_path, capture_output=True)
        subprocess.run(
            ["git", "commit", "-m", "initial"],
            cwd=tmp_path,
            capture_output=True,
        )

        # Get actual HEAD
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=tmp_path,
            capture_output=True,
            text=True,
        )
        head_sha = result.stdout.strip()

        data = {"repo_head": head_sha}
        errors = validate_strict_mode(data, tmp_path)
        assert errors == []

    def test_repo_head_short_matches_full(self, tmp_path: Path):
        """Test short hash matches full hash."""
        # Initialize git repo
        subprocess.run(["git", "init"], cwd=tmp_path, capture_output=True)
        subprocess.run(
            ["git", "config", "user.email", "test@test.com"],
            cwd=tmp_path,
            capture_output=True,
        )
        subprocess.run(
            ["git", "config", "user.name", "Test"],
            cwd=tmp_path,
            capture_output=True,
        )
        (tmp_path / "test.txt").write_text("test")
        subprocess.run(["git", "add", "."], cwd=tmp_path, capture_output=True)
        subprocess.run(
            ["git", "commit", "-m", "initial"],
            cwd=tmp_path,
            capture_output=True,
        )

        # Get actual HEAD
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=tmp_path,
            capture_output=True,
            text=True,
        )
        head_sha = result.stdout.strip()

        # Use short hash
        data = {"repo_head": head_sha[:7]}
        errors = validate_strict_mode(data, tmp_path)
        assert errors == []

    def test_repo_head_stale_strict_fails(self, tmp_path: Path):
        """Test validation fails when repo_head doesn't match HEAD."""
        # Initialize git repo
        subprocess.run(["git", "init"], cwd=tmp_path, capture_output=True)
        subprocess.run(
            ["git", "config", "user.email", "test@test.com"],
            cwd=tmp_path,
            capture_output=True,
        )
        subprocess.run(
            ["git", "config", "user.name", "Test"],
            cwd=tmp_path,
            capture_output=True,
        )
        (tmp_path / "test.txt").write_text("test")
        subprocess.run(["git", "add", "."], cwd=tmp_path, capture_output=True)
        subprocess.run(
            ["git", "commit", "-m", "initial"],
            cwd=tmp_path,
            capture_output=True,
        )

        # Use a different hash
        data = {"repo_head": "0" * 7}
        errors = validate_strict_mode(data, tmp_path)
        assert len(errors) == 1
        assert "stale" in errors[0]

    def test_unknown_fields_warn_default(self):
        """Test unknown fields generate warnings in default mode."""
        data = {
            "unknown_field": "value",
            "another_unknown": 123,
        }
        errors, warnings = validate_unknown_fields(data, strict=False)
        assert errors == []
        assert len(warnings) == 1
        assert "unknown_field" in warnings[0] or "another_unknown" in warnings[0]

    def test_unknown_fields_error_strict(self):
        """Test unknown fields generate errors in strict mode."""
        data = {
            "unknown_field": "value",
        }
        errors, warnings = validate_unknown_fields(data, strict=True)
        assert len(errors) == 1
        assert "unknown_field" in errors[0]
        assert warnings == []


class TestEpochMissingBehavior:
    """Tests for missing EPOCH.yaml behavior."""

    def test_missing_epoch_default_warn_exit_0(self, tmp_path: Path):
        """Test default mode warns but exits 0 when EPOCH.yaml missing."""
        result = cli([str(tmp_path)])
        assert result == 0

    def test_missing_epoch_require_exit_1(self, tmp_path: Path):
        """Test --require mode exits 1 when EPOCH.yaml missing."""
        result = cli([str(tmp_path), "--require"])
        assert result == 1

    def test_missing_epoch_strict_exit_1(self, tmp_path: Path):
        """Test --strict mode exits 1 when EPOCH.yaml missing (implies --require)."""
        result = cli([str(tmp_path), "--strict"])
        assert result == 1


class TestEpochCli:
    """Tests for CLI entry point."""

    def test_exit_0_valid_epoch(self, tmp_path: Path):
        """Test exit code 0 for valid EPOCH.yaml."""
        admin_dir = tmp_path / "00_admin"
        admin_dir.mkdir()

        content = """
epoch_schema: "c010.epoch.v1"
repo_id: "test-repo"
repo_head: "abc1234"
generated_at_utc: "2026-01-17T14:30:00Z"
"""
        (admin_dir / "EPOCH.yaml").write_text(content)

        result = cli([str(tmp_path)])
        assert result == 0

    def test_exit_0_no_epoch_file_default(self, tmp_path: Path):
        """Test exit code 0 when no EPOCH.yaml in default mode."""
        result = cli([str(tmp_path)])
        assert result == 0

    def test_exit_1_no_epoch_file_require(self, tmp_path: Path):
        """Test exit code 1 when no EPOCH.yaml with --require."""
        result = cli([str(tmp_path), "--require"])
        assert result == 1

    def test_exit_1_validation_failure(self, tmp_path: Path):
        """Test exit code 1 for validation failure."""
        admin_dir = tmp_path / "00_admin"
        admin_dir.mkdir()

        content = """
epoch_schema: "wrong.schema"
repo_id: ""
repo_head: "not-valid"
generated_at_utc: "not-a-date"
"""
        (admin_dir / "EPOCH.yaml").write_text(content)

        result = cli([str(tmp_path)])
        assert result == 1

    def test_exit_2_yaml_parse_error(self, tmp_path: Path):
        """Test exit code 2 for YAML parse error."""
        admin_dir = tmp_path / "00_admin"
        admin_dir.mkdir()

        content = """
epoch_schema: "c010.epoch.v1"
  bad: indentation
"""
        (admin_dir / "EPOCH.yaml").write_text(content)

        result = cli([str(tmp_path)])
        assert result == 2


class TestExitCodes:
    """Tests for exit code contract."""

    def test_exit_0_all_pass(self, tmp_path: Path):
        """Test exit 0 when all validations pass."""
        admin_dir = tmp_path / "00_admin"
        admin_dir.mkdir()

        content = """
epoch_schema: "c010.epoch.v1"
repo_id: "pass-test"
repo_head: "abc1234"
generated_at_utc: "2026-01-17T14:30:00Z"
"""
        (admin_dir / "EPOCH.yaml").write_text(content)

        assert cli([str(tmp_path)]) == 0

    def test_exit_1_validation_failure(self, tmp_path: Path):
        """Test exit 1 for validation failure."""
        admin_dir = tmp_path / "00_admin"
        admin_dir.mkdir()

        content = """
epoch_schema: "c010.epoch.v1"
repo_id: ""
repo_head: "invalid"
generated_at_utc: "invalid"
"""
        (admin_dir / "EPOCH.yaml").write_text(content)

        assert cli([str(tmp_path)]) == 1

    def test_exit_0_for_paths_without_epoch(self, tmp_path: Path):
        """Test exit 0 when scanning paths without EPOCH.yaml."""
        # Empty directory, no EPOCH.yaml
        assert cli([str(tmp_path)]) == 0


class TestValidateEpoch:
    """Tests for validate_epoch function."""

    def test_valid_minimal_epoch(self, tmp_path: Path):
        """Test validation of minimal valid epoch."""
        data = {
            "epoch_schema": EPOCH_SPEC_V1,
            "repo_id": "test-repo",
            "repo_head": "abc1234",
            "generated_at_utc": "2026-01-17T14:30:00Z",
        }
        errors, warnings = validate_epoch(tmp_path, data)
        assert errors == []
        assert warnings == []

    def test_valid_full_epoch(self, tmp_path: Path):
        """Test validation of full epoch with all optional fields."""
        # Create primer file
        primer_content = "# Test Primer"
        (tmp_path / "PROJECT_PRIMER.md").write_text(primer_content)
        primer_sha = hashlib.sha256(primer_content.encode()).hexdigest()

        data = {
            "epoch_schema": EPOCH_SPEC_V1,
            "repo_id": "test-repo",
            "repo_head": "abc1234",
            "generated_at_utc": "2026-01-17T14:30:00Z",
            "primer": {
                "sha256": primer_sha,
                "path": "PROJECT_PRIMER.md",
            },
            "generator": {
                "tool": "test-tool",
                "version": "1.0.0",
            },
            "custom": {
                "extra": "data",
            },
        }
        errors, warnings = validate_epoch(tmp_path, data)
        assert errors == []
        assert warnings == []


class TestGitHashPattern:
    """Tests for git hash pattern regex."""

    def test_valid_7_char_hash(self):
        """Test 7-character hash is valid."""
        assert GIT_HASH_PATTERN.match("abc1234") is not None

    def test_valid_40_char_hash(self):
        """Test 40-character hash is valid."""
        assert GIT_HASH_PATTERN.match("a" * 40) is not None

    def test_invalid_6_char_hash(self):
        """Test 6-character hash is invalid."""
        assert GIT_HASH_PATTERN.match("abc123") is None

    def test_invalid_41_char_hash(self):
        """Test 41-character hash is invalid."""
        assert GIT_HASH_PATTERN.match("a" * 41) is None

    def test_invalid_uppercase(self):
        """Test uppercase characters are invalid."""
        assert GIT_HASH_PATTERN.match("ABC1234") is None

    def test_invalid_non_hex(self):
        """Test non-hex characters are invalid."""
        assert GIT_HASH_PATTERN.match("ghijklm") is None


class TestCalculateFileSha256:
    """Tests for calculate_file_sha256 function."""

    def test_calculates_correct_sha256(self, tmp_path: Path):
        """Test SHA256 calculation is correct."""
        content = "test content"
        file_path = tmp_path / "test.txt"
        file_path.write_text(content)

        expected = hashlib.sha256(content.encode()).hexdigest()
        actual = calculate_file_sha256(file_path)
        assert actual == expected

    def test_missing_file_returns_none(self, tmp_path: Path):
        """Test missing file returns None."""
        file_path = tmp_path / "nonexistent.txt"
        result = calculate_file_sha256(file_path)
        assert result is None


class TestJsonOutput:
    """Tests for JSON output functionality."""

    def test_json_output_created(self, tmp_path: Path):
        """Test JSON output file is created."""
        admin_dir = tmp_path / "00_admin"
        admin_dir.mkdir()

        content = """
epoch_schema: "c010.epoch.v1"
repo_id: "test-repo"
repo_head: "abc1234"
generated_at_utc: "2026-01-17T14:30:00Z"
"""
        (admin_dir / "EPOCH.yaml").write_text(content)

        output_file = tmp_path / "results.json"
        result = cli([str(tmp_path), "--json-output", str(output_file)])

        assert result == 0
        assert output_file.exists()

        import json

        data = json.loads(output_file.read_text())
        assert data["validated_epochs"] == 1
        assert data["passed"] == 1
        assert data["failed"] == 0
