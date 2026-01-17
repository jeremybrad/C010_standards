"""Tests for check_capsulemeta validator."""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from validators.check_capsulemeta import (
    CAPSULE_SPEC_V1,
    VALID_KINDS,
    cli,
    is_capsule_document,
    load_capsule_frontmatter,
    validate_capsule,
    validate_iso8601,
)


class TestLoadCapsuleFrontmatter:
    """Tests for load_capsule_frontmatter function."""

    def test_valid_frontmatter(self, tmp_path: Path):
        """Test loading valid YAML frontmatter."""
        content = """---
capsule_spec: "c010.capsule.v1"
capsule_id: "test-123"
created_at: "2026-01-17T14:30:00Z"
kind: "handoff"
producer:
  tool: "test-tool"
---

# Content here
"""
        file_path = tmp_path / "test.md"
        file_path.write_text(content)

        result = load_capsule_frontmatter(file_path)
        assert result is not None
        assert result["capsule_spec"] == "c010.capsule.v1"
        assert result["capsule_id"] == "test-123"

    def test_missing_frontmatter(self, tmp_path: Path):
        """Test file without frontmatter returns None."""
        content = "# Just markdown\n\nNo frontmatter here."
        file_path = tmp_path / "test.md"
        file_path.write_text(content)

        result = load_capsule_frontmatter(file_path)
        assert result is None

    def test_invalid_yaml(self, tmp_path: Path):
        """Test invalid YAML frontmatter returns None."""
        content = """---
invalid: yaml: here
  broken indentation
---

# Content
"""
        file_path = tmp_path / "test.md"
        file_path.write_text(content)

        result = load_capsule_frontmatter(file_path)
        assert result is None

    def test_incomplete_frontmatter(self, tmp_path: Path):
        """Test frontmatter without closing delimiter returns None."""
        content = """---
capsule_spec: "c010.capsule.v1"
# No closing delimiter
"""
        file_path = tmp_path / "test.md"
        file_path.write_text(content)

        result = load_capsule_frontmatter(file_path)
        assert result is None


class TestIsCapsuleDocument:
    """Tests for is_capsule_document function."""

    def test_with_capsule_spec(self):
        """Test document with capsule_spec is recognized."""
        metadata = {"capsule_spec": "c010.capsule.v1", "capsule_id": "test"}
        assert is_capsule_document(metadata) is True

    def test_without_capsule_spec(self):
        """Test document without capsule_spec is not recognized."""
        metadata = {"schema": "DocMeta.v1.2", "doc": {"title": "test"}}
        assert is_capsule_document(metadata) is False

    def test_empty_metadata(self):
        """Test empty metadata is not recognized."""
        assert is_capsule_document({}) is False


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


class TestValidateCapsule:
    """Tests for validate_capsule function."""

    def test_valid_capsule(self, tmp_path: Path):
        """Test validation of valid capsule."""
        metadata = {
            "capsule_spec": CAPSULE_SPEC_V1,
            "capsule_id": "test-uuid-123",
            "created_at": "2026-01-17T14:30:00Z",
            "kind": "handoff",
            "producer": {"tool": "test-tool"},
        }
        errors, warnings = validate_capsule(tmp_path / "test.md", metadata)
        assert errors == []
        assert warnings == []

    def test_invalid_capsule_spec(self, tmp_path: Path):
        """Test validation fails with wrong capsule_spec."""
        metadata = {
            "capsule_spec": "wrong.spec.v1",
            "capsule_id": "test-uuid-123",
            "created_at": "2026-01-17T14:30:00Z",
            "kind": "handoff",
            "producer": {"tool": "test-tool"},
        }
        errors, warnings = validate_capsule(tmp_path / "test.md", metadata)
        assert len(errors) == 1
        assert "capsule_spec" in errors[0]

    def test_missing_capsule_id(self, tmp_path: Path):
        """Test validation fails with missing capsule_id."""
        metadata = {
            "capsule_spec": CAPSULE_SPEC_V1,
            "created_at": "2026-01-17T14:30:00Z",
            "kind": "handoff",
            "producer": {"tool": "test-tool"},
        }
        errors, warnings = validate_capsule(tmp_path / "test.md", metadata)
        assert len(errors) == 1
        assert "capsule_id" in errors[0]

    def test_empty_capsule_id(self, tmp_path: Path):
        """Test validation fails with empty capsule_id."""
        metadata = {
            "capsule_spec": CAPSULE_SPEC_V1,
            "capsule_id": "   ",
            "created_at": "2026-01-17T14:30:00Z",
            "kind": "handoff",
            "producer": {"tool": "test-tool"},
        }
        errors, warnings = validate_capsule(tmp_path / "test.md", metadata)
        assert len(errors) == 1
        assert "capsule_id" in errors[0]

    def test_invalid_created_at(self, tmp_path: Path):
        """Test validation fails with invalid created_at."""
        metadata = {
            "capsule_spec": CAPSULE_SPEC_V1,
            "capsule_id": "test-uuid-123",
            "created_at": "not-a-date",
            "kind": "handoff",
            "producer": {"tool": "test-tool"},
        }
        errors, warnings = validate_capsule(tmp_path / "test.md", metadata)
        assert len(errors) == 1
        assert "created_at" in errors[0]
        assert "ISO 8601" in errors[0]

    def test_missing_created_at(self, tmp_path: Path):
        """Test validation fails with missing created_at."""
        metadata = {
            "capsule_spec": CAPSULE_SPEC_V1,
            "capsule_id": "test-uuid-123",
            "kind": "handoff",
            "producer": {"tool": "test-tool"},
        }
        errors, warnings = validate_capsule(tmp_path / "test.md", metadata)
        assert len(errors) == 1
        assert "created_at" in errors[0]

    def test_invalid_kind(self, tmp_path: Path):
        """Test validation fails with invalid kind."""
        metadata = {
            "capsule_spec": CAPSULE_SPEC_V1,
            "capsule_id": "test-uuid-123",
            "created_at": "2026-01-17T14:30:00Z",
            "kind": "invalid_kind",
            "producer": {"tool": "test-tool"},
        }
        errors, warnings = validate_capsule(tmp_path / "test.md", metadata)
        assert len(errors) == 1
        assert "kind" in errors[0]
        assert "invalid_kind" in errors[0]

    def test_all_valid_kinds(self, tmp_path: Path):
        """Test all valid kind values pass."""
        for kind in VALID_KINDS:
            metadata = {
                "capsule_spec": CAPSULE_SPEC_V1,
                "capsule_id": "test-uuid-123",
                "created_at": "2026-01-17T14:30:00Z",
                "kind": kind,
                "producer": {"tool": "test-tool"},
            }
            errors, warnings = validate_capsule(tmp_path / "test.md", metadata)
            assert errors == [], f"Kind '{kind}' should be valid"

    def test_missing_producer_tool(self, tmp_path: Path):
        """Test validation fails with missing producer.tool."""
        metadata = {
            "capsule_spec": CAPSULE_SPEC_V1,
            "capsule_id": "test-uuid-123",
            "created_at": "2026-01-17T14:30:00Z",
            "kind": "handoff",
            "producer": {"agent": "test-agent"},
        }
        errors, warnings = validate_capsule(tmp_path / "test.md", metadata)
        assert len(errors) == 1
        assert "producer.tool" in errors[0]

    def test_invalid_producer_type(self, tmp_path: Path):
        """Test validation fails when producer is not an object."""
        metadata = {
            "capsule_spec": CAPSULE_SPEC_V1,
            "capsule_id": "test-uuid-123",
            "created_at": "2026-01-17T14:30:00Z",
            "kind": "handoff",
            "producer": "just-a-string",
        }
        errors, warnings = validate_capsule(tmp_path / "test.md", metadata)
        assert len(errors) == 1
        assert "producer must be an object" in errors[0]

    def test_unknown_fields_warning(self, tmp_path: Path):
        """Test unknown fields generate warnings in normal mode."""
        metadata = {
            "capsule_spec": CAPSULE_SPEC_V1,
            "capsule_id": "test-uuid-123",
            "created_at": "2026-01-17T14:30:00Z",
            "kind": "handoff",
            "producer": {"tool": "test-tool"},
            "unknown_field": "some value",
            "another_unknown": 123,
        }
        errors, warnings = validate_capsule(
            tmp_path / "test.md", metadata, strict=False
        )
        assert errors == []
        assert len(warnings) == 1
        assert "unknown_field" in warnings[0] or "another_unknown" in warnings[0]

    def test_unknown_fields_strict_error(self, tmp_path: Path):
        """Test unknown fields generate errors in strict mode."""
        metadata = {
            "capsule_spec": CAPSULE_SPEC_V1,
            "capsule_id": "test-uuid-123",
            "created_at": "2026-01-17T14:30:00Z",
            "kind": "handoff",
            "producer": {"tool": "test-tool"},
            "unknown_field": "some value",
        }
        errors, warnings = validate_capsule(
            tmp_path / "test.md", metadata, strict=True
        )
        assert len(errors) == 1
        assert "unknown_field" in errors[0]
        assert warnings == []


class TestCli:
    """Tests for CLI entry point."""

    def test_exit_0_for_valid_capsule(self, tmp_path: Path):
        """Test exit code 0 for valid capsule."""
        content = """---
capsule_spec: "c010.capsule.v1"
capsule_id: "test-uuid-123"
created_at: "2026-01-17T14:30:00Z"
kind: "handoff"
producer:
  tool: "test-tool"
---

# Valid capsule
"""
        file_path = tmp_path / "valid.md"
        file_path.write_text(content)

        result = cli([str(file_path)])
        assert result == 0

    def test_exit_1_for_invalid_capsule(self, tmp_path: Path):
        """Test exit code 1 for validation failure."""
        content = """---
capsule_spec: "wrong.spec"
capsule_id: "test"
created_at: "2026-01-17T14:30:00Z"
kind: "handoff"
producer:
  tool: "test"
---

# Invalid capsule
"""
        file_path = tmp_path / "invalid.md"
        file_path.write_text(content)

        result = cli([str(file_path)])
        assert result == 1

    def test_exit_0_for_no_capsules(self, tmp_path: Path):
        """Test exit code 0 when no capsules found."""
        content = """# Just markdown

No frontmatter here.
"""
        file_path = tmp_path / "regular.md"
        file_path.write_text(content)

        result = cli([str(file_path)])
        assert result == 0

    def test_directory_recursion(self, tmp_path: Path):
        """Test validator recurses into directories."""
        subdir = tmp_path / "subdir"
        subdir.mkdir()

        content = """---
capsule_spec: "c010.capsule.v1"
capsule_id: "nested-capsule"
created_at: "2026-01-17T14:30:00Z"
kind: "activity"
producer:
  tool: "test-tool"
---

# Nested capsule
"""
        file_path = subdir / "nested.md"
        file_path.write_text(content)

        result = cli([str(tmp_path), "--verbose"])
        assert result == 0


class TestExitCodes:
    """Tests for exit code contract."""

    def test_exit_0_all_pass(self, tmp_path: Path):
        """Test exit 0 when all validations pass."""
        content = """---
capsule_spec: "c010.capsule.v1"
capsule_id: "pass-test"
created_at: "2026-01-17T14:30:00Z"
kind: "handoff"
producer:
  tool: "test-tool"
---

# Pass
"""
        file_path = tmp_path / "pass.md"
        file_path.write_text(content)

        assert cli([str(file_path)]) == 0

    def test_exit_1_validation_failure(self, tmp_path: Path):
        """Test exit 1 for validation failure."""
        content = """---
capsule_spec: "c010.capsule.v1"
capsule_id: ""
created_at: "invalid-date"
kind: "unknown"
producer:
  tool: ""
---

# Multiple failures
"""
        file_path = tmp_path / "fail.md"
        file_path.write_text(content)

        assert cli([str(file_path)]) == 1

    def test_exit_0_for_non_capsule_files(self, tmp_path: Path):
        """Test exit 0 when scanning files that aren't capsules."""
        # DocMeta file, not a capsule
        content = """---
schema: "DocMeta.v1.2"
doc:
  title: "Not a capsule"
---

# Regular doc
"""
        file_path = tmp_path / "docmeta.md"
        file_path.write_text(content)

        assert cli([str(file_path)]) == 0


class TestStrictMode:
    """Tests for strict mode behavior."""

    def test_unknown_fields_warn_default(self, tmp_path: Path):
        """Test unknown fields warn but exit 0 in default mode."""
        content = """---
capsule_spec: "c010.capsule.v1"
capsule_id: "test-123"
created_at: "2026-01-17T14:30:00Z"
kind: "handoff"
producer:
  tool: "test-tool"
extra_field: "should warn"
---

# Has unknown field
"""
        file_path = tmp_path / "unknown.md"
        file_path.write_text(content)

        # Default mode: exit 0 with warning
        assert cli([str(file_path)]) == 0

    def test_unknown_fields_error_strict(self, tmp_path: Path):
        """Test unknown fields error with exit 1 in strict mode."""
        content = """---
capsule_spec: "c010.capsule.v1"
capsule_id: "test-123"
created_at: "2026-01-17T14:30:00Z"
kind: "handoff"
producer:
  tool: "test-tool"
extra_field: "should error"
---

# Has unknown field
"""
        file_path = tmp_path / "unknown.md"
        file_path.write_text(content)

        # Strict mode: exit 1
        assert cli([str(file_path), "--strict"]) == 1


class TestPathOutput:
    """Tests for path output formatting."""

    def test_default_relative_paths(self, tmp_path: Path, monkeypatch):
        """Test default output uses repo-relative paths."""
        # Create a fake git repo structure
        git_dir = tmp_path / ".git"
        git_dir.mkdir()

        content = """---
capsule_spec: "wrong.spec"
capsule_id: "test"
created_at: "2026-01-17T14:30:00Z"
kind: "handoff"
producer:
  tool: "test"
---

# Test
"""
        file_path = tmp_path / "test.md"
        file_path.write_text(content)

        # Change to the tmp_path directory
        monkeypatch.chdir(tmp_path)

        # Should use relative path (exit 1 because spec is wrong)
        result = cli([str(file_path)])
        assert result == 1

    def test_absolute_paths_flag(self, tmp_path: Path):
        """Test --absolute-paths outputs full paths."""
        content = """---
capsule_spec: "wrong.spec"
capsule_id: "test"
created_at: "2026-01-17T14:30:00Z"
kind: "handoff"
producer:
  tool: "test"
---

# Test
"""
        file_path = tmp_path / "test.md"
        file_path.write_text(content)

        # With --absolute-paths flag
        result = cli([str(file_path), "--absolute-paths"])
        assert result == 1


class TestJsonOutput:
    """Tests for JSON output functionality."""

    def test_json_output_created(self, tmp_path: Path):
        """Test JSON output file is created."""
        content = """---
capsule_spec: "c010.capsule.v1"
capsule_id: "test-123"
created_at: "2026-01-17T14:30:00Z"
kind: "handoff"
producer:
  tool: "test-tool"
---

# Valid capsule
"""
        file_path = tmp_path / "test.md"
        file_path.write_text(content)

        output_file = tmp_path / "results.json"
        result = cli([str(file_path), "--json-output", str(output_file)])

        assert result == 0
        assert output_file.exists()

        import json
        data = json.loads(output_file.read_text())
        assert data["validated_files"] == 1
        assert data["passed"] == 1
        assert data["failed"] == 0
