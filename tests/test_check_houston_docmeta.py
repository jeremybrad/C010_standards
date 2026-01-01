"""Tests for check_houston_docmeta validator."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from validators.check_houston_docmeta import (
    is_houston_document,
    validate_document,
)


class TestIsHoustonDocument:
    """Tests for is_houston_document function."""

    def test_agent_houston_tag(self):
        """Test document with agent:houston tag."""
        metadata = {
            "routing": {
                "tags": ["agent:houston", "sensitivity:internal"]
            }
        }
        assert is_houston_document(metadata) is True

    def test_source_mission_control_tag(self):
        """Test document with source:mission-control tag."""
        metadata = {
            "routing": {
                "tags": ["source:mission-control"]
            }
        }
        assert is_houston_document(metadata) is True

    def test_no_houston_tags(self):
        """Test document without Houston tags."""
        metadata = {
            "routing": {
                "tags": ["source:other", "priority:low"]
            }
        }
        assert is_houston_document(metadata) is False

    def test_tags_as_string(self):
        """Test with tags as single string instead of list."""
        metadata = {
            "routing": {
                "tags": "agent:houston"
            }
        }
        assert is_houston_document(metadata) is True

    def test_missing_routing_section(self):
        """Test with missing routing section."""
        metadata = {
            "doc": {"title": "Test"}
        }
        assert is_houston_document(metadata) is False


class TestValidateDocument:
    """Tests for validate_document function."""

    def test_valid_houston_document(self, tmp_path):
        """Test with fully valid Houston document."""
        file_path = tmp_path / "test.yaml"
        metadata = {
            "doc": {
                "projects": ["Mission Control", "C010"],
                "topics": ["monitoring", "deployment"]
            },
            "routing": {
                "tags": ["agent:houston", "sensitivity:internal"]
            },
            "connections": {
                "related_docs": []
            }
        }
        allowed_topics = {"monitoring", "deployment", "automation"}

        errors = validate_document(file_path, metadata, allowed_topics, verbose=False)
        assert errors == []

    def test_missing_mission_control_project(self, tmp_path):
        """Test missing Mission Control in projects."""
        file_path = tmp_path / "test.yaml"
        metadata = {
            "doc": {
                "projects": ["Other Project"],
                "topics": ["monitoring"]
            },
            "routing": {
                "tags": ["agent:houston", "sensitivity:internal"]
            }
        }
        allowed_topics = {"monitoring"}

        errors = validate_document(file_path, metadata, allowed_topics, verbose=False)
        assert len(errors) == 1
        assert "Missing required project" in errors[0]

    def test_old_p210_project_accepted(self, tmp_path):
        """Test that old P210 project name is still accepted."""
        file_path = tmp_path / "test.yaml"
        metadata = {
            "doc": {
                "projects": ["P210"],
                "topics": ["monitoring"]
            },
            "routing": {
                "tags": ["agent:houston", "sensitivity:internal"]
            }
        }
        allowed_topics = {"monitoring"}

        errors = validate_document(file_path, metadata, allowed_topics, verbose=False)
        assert errors == []

    def test_missing_agent_houston_tag(self, tmp_path):
        """Test document without agent:houston tag is not validated."""
        file_path = tmp_path / "test.yaml"
        metadata = {
            "doc": {
                "projects": ["Mission Control"],
                "topics": ["monitoring"]
            },
            "routing": {
                "tags": ["sensitivity:internal"]
            }
        }
        allowed_topics = {"monitoring"}

        # Document without agent:houston should be skipped (not a Houston document)
        errors = validate_document(file_path, metadata, allowed_topics, verbose=False)
        assert errors == []

    def test_missing_sensitivity_tag(self, tmp_path):
        """Test missing sensitivity:internal tag."""
        file_path = tmp_path / "test.yaml"
        metadata = {
            "doc": {
                "projects": ["Mission Control"],
                "topics": ["monitoring"]
            },
            "routing": {
                "tags": ["agent:houston"]
            }
        }
        allowed_topics = {"monitoring"}

        errors = validate_document(file_path, metadata, allowed_topics, verbose=False)
        assert len(errors) == 1
        assert "sensitivity:internal" in errors[0]

    def test_invalid_topic(self, tmp_path):
        """Test with topic not in taxonomy."""
        file_path = tmp_path / "test.yaml"
        metadata = {
            "doc": {
                "projects": ["Mission Control"],
                "topics": ["invalid_topic", "monitoring"]
            },
            "routing": {
                "tags": ["agent:houston", "sensitivity:internal"]
            }
        }
        allowed_topics = {"monitoring", "deployment"}

        errors = validate_document(file_path, metadata, allowed_topics, verbose=False)
        assert len(errors) == 1
        assert "invalid_topic" in errors[0]
        assert "taxonomy" in errors[0]

    def test_playbook_success_without_related_docs(self, tmp_path):
        """Test playbook:success tag without related_docs."""
        file_path = tmp_path / "test.yaml"
        metadata = {
            "doc": {
                "projects": ["Mission Control"],
                "topics": ["monitoring"]
            },
            "routing": {
                "tags": ["agent:houston", "sensitivity:internal", "playbook:success"]
            },
            "connections": {
                "related_docs": []
            }
        }
        allowed_topics = {"monitoring"}

        errors = validate_document(file_path, metadata, allowed_topics, verbose=False)
        assert len(errors) == 1
        assert "playbook:success" in errors[0]
        assert "related_docs" in errors[0]

    def test_playbook_success_with_related_docs(self, tmp_path):
        """Test playbook:success tag with related_docs."""
        file_path = tmp_path / "test.yaml"
        metadata = {
            "doc": {
                "projects": ["Mission Control"],
                "topics": ["monitoring"]
            },
            "routing": {
                "tags": ["agent:houston", "sensitivity:internal", "playbook:success"]
            },
            "connections": {
                "related_docs": ["doc1.md", "doc2.md"]
            }
        }
        allowed_topics = {"monitoring"}

        errors = validate_document(file_path, metadata, allowed_topics, verbose=False)
        assert errors == []

    def test_non_houston_document_skipped(self, tmp_path):
        """Test that non-Houston documents are skipped."""
        file_path = tmp_path / "test.yaml"
        metadata = {
            "doc": {
                "projects": ["Other"],
                "topics": []
            },
            "routing": {
                "tags": ["source:other"]
            }
        }
        allowed_topics = set()

        # Should return empty errors since it's not a Houston document
        errors = validate_document(file_path, metadata, allowed_topics, verbose=False)
        assert errors == []

    def test_empty_taxonomy_no_topic_validation(self, tmp_path):
        """Test that empty taxonomy skips topic validation."""
        file_path = tmp_path / "test.yaml"
        metadata = {
            "doc": {
                "projects": ["Mission Control"],
                "topics": ["anything"]
            },
            "routing": {
                "tags": ["agent:houston", "sensitivity:internal"]
            }
        }
        allowed_topics = set()  # Empty taxonomy

        errors = validate_document(file_path, metadata, allowed_topics, verbose=False)
        # Should only have errors for other validations, not topics
        assert all("topic" not in e.lower() for e in errors)
