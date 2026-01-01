"""Tests for check_houston_tools validator."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from validators.check_houston_tools import (
    validate_dangerous_operations,
    validate_phase_consistency,
    validate_vps_endpoint,
)


class TestValidatePhaseConsistency:
    """Tests for validate_phase_consistency function."""

    def test_matching_phases(self):
        """Test when tool phase matches features phase."""
        tools_config = {"phase_settings": {"current_phase": 2}}
        features_config = {"gradual_trust_building": {"current_phase": 2}}

        errors = validate_phase_consistency(
            tools_config, features_config, verbose=False
        )
        assert errors == []

    def test_tools_phase_exceeds_features(self):
        """Test when tools phase exceeds features phase."""
        tools_config = {"phase_settings": {"current_phase": 3}}
        features_config = {"gradual_trust_building": {"current_phase": 1}}

        errors = validate_phase_consistency(
            tools_config, features_config, verbose=False
        )
        assert len(errors) == 1
        assert "exceeds" in errors[0]

    def test_tools_phase_lower_than_features(self):
        """Test when tools phase is lower than features phase (allowed)."""
        tools_config = {"phase_settings": {"current_phase": 1}}
        features_config = {"gradual_trust_building": {"current_phase": 2}}

        errors = validate_phase_consistency(
            tools_config, features_config, verbose=False
        )
        assert errors == []

    def test_no_features_config(self):
        """Test when no features config provided."""
        tools_config = {"phase_settings": {"current_phase": 1}}

        errors = validate_phase_consistency(tools_config, None, verbose=False)
        assert errors == []

    def test_missing_phase_field(self):
        """Test with missing required field."""
        tools_config = {}
        features_config = {"gradual_trust_building": {"current_phase": 1}}

        errors = validate_phase_consistency(
            tools_config, features_config, verbose=False
        )
        # Should not error if tools phase is None
        assert errors == []


class TestValidateDangerousOperations:
    """Tests for validate_dangerous_operations function."""

    def test_no_dangerous_ops_in_early_phase(self):
        """Test that no dangerous operations in phase 1 passes."""
        config = {
            "phase_settings": {"current_phase": 1},
            "tool_access": {
                "local_tools": {
                    "phase_overrides": {
                        "1": {
                            "filesystem": {"read": True, "write": False}
                        }
                    }
                }
            }
        }

        errors = validate_dangerous_operations(config, verbose=False)
        assert errors == []

    def test_dangerous_ops_in_phase_1_fails(self):
        """Test that dangerous operations in phase 1 generates warning."""
        config = {
            "phase_settings": {"current_phase": 1},
            "tool_access": {
                "local_tools": {
                    "phase_overrides": {
                        "phase_1": ["kill_processes", "system_shutdown"]
                    }
                }
            }
        }

        errors = validate_dangerous_operations(config, verbose=False)
        assert len(errors) == 1
        assert "WARNING" in errors[0]
        assert "kill_processes" in errors[0] or "system_shutdown" in errors[0]

    def test_dangerous_ops_in_phase_3_passes(self):
        """Test that dangerous operations in phase 3 is allowed."""
        config = {
            "phase_settings": {"current_phase": 3},
            "tool_access": {
                "local_tools": {
                    "phase_overrides": {
                        "phase_3": ["kill_processes", "system_shutdown"]
                    }
                }
            }
        }

        errors = validate_dangerous_operations(config, verbose=False)
        assert errors == []

    def test_rm_recursive_in_phase_2_warns(self):
        """Test that rm_recursive in phase 2 generates warning."""
        config = {
            "phase_settings": {"current_phase": 2},
            "tool_access": {
                "local_tools": {
                    "phase_overrides": {
                        "phase_2": ["rm_recursive"]
                    }
                }
            }
        }

        errors = validate_dangerous_operations(config, verbose=False)
        assert len(errors) == 1
        assert "rm_recursive" in errors[0]


class TestValidateVpsEndpoint:
    """Tests for validate_vps_endpoint function."""

    def test_vps_disabled(self):
        """Test that disabled VPS tools pass regardless of endpoint."""
        config = {
            "tool_access": {
                "vps_tools": {
                    "enabled": False,
                    "endpoint": "example.com"
                }
            }
        }

        errors = validate_vps_endpoint(config, verbose=False)
        assert errors == []

    def test_vps_enabled_with_placeholder(self):
        """Test that enabled VPS with placeholder endpoint fails."""
        config = {
            "tool_access": {
                "vps_tools": {
                    "enabled": True,
                    "endpoint": "example.com"
                }
            }
        }

        errors = validate_vps_endpoint(config, verbose=False)
        assert len(errors) == 1
        assert "endpoint" in errors[0].lower()

    def test_vps_enabled_with_empty_endpoint(self):
        """Test that enabled VPS with empty endpoint fails."""
        config = {
            "tool_access": {
                "vps_tools": {
                    "enabled": True,
                    "endpoint": ""
                }
            }
        }

        errors = validate_vps_endpoint(config, verbose=False)
        assert len(errors) == 1

    def test_vps_enabled_with_valid_endpoint(self):
        """Test that enabled VPS with valid endpoint passes."""
        config = {
            "tool_access": {
                "vps_tools": {
                    "enabled": True,
                    "endpoint": "https://real-vps.example.com"
                }
            }
        }

        errors = validate_vps_endpoint(config, verbose=False)
        assert errors == []
