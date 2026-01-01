"""Tests for check_houston_features validator."""
from __future__ import annotations

# Import validator functions
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from validators.check_houston_features import (
    validate_autonomous_deploy_permission,
    validate_autonomous_safety,
    validate_supported_editors,
)


class TestValidateSupportedEditors:
    """Tests for validate_supported_editors function."""

    def test_valid_editors(self):
        """Test with valid editors list."""
        config = {
            "features": {
                "ide_integration": {
                    "supported_editors": ["cursor", "vscode"]
                }
            }
        }
        errors = validate_supported_editors(config, verbose=False)
        assert errors == []

    def test_invalid_editors(self):
        """Test with invalid editors list."""
        config = {
            "features": {
                "ide_integration": {
                    "supported_editors": ["cursor", "invalid_editor"]
                }
            }
        }
        errors = validate_supported_editors(config, verbose=False)
        assert len(errors) == 1
        assert "invalid_editor" in errors[0]

    def test_missing_field(self):
        """Test with missing required field."""
        config = {"features": {}}
        errors = validate_supported_editors(config, verbose=False)
        assert len(errors) == 1
        assert "Missing required field" in errors[0]


class TestValidateAutonomousSafety:
    """Tests for validate_autonomous_safety function."""

    def test_autonomous_without_password(self):
        """Test autonomous mode without password requirement fails."""
        config = {
            "features": {
                "agency_levels": {
                    "current_level": "autonomous"
                }
            },
            "safety_controls": {
                "destructive_actions": {
                    "require_password": False
                }
            }
        }
        errors = validate_autonomous_safety(config, verbose=False)
        assert len(errors) == 1
        assert "CRITICAL" in errors[0]
        assert "autonomous" in errors[0]

    def test_autonomous_with_password(self):
        """Test autonomous mode with password requirement passes."""
        config = {
            "features": {
                "agency_levels": {
                    "current_level": "autonomous"
                }
            },
            "safety_controls": {
                "destructive_actions": {
                    "require_password": True
                }
            }
        }
        errors = validate_autonomous_safety(config, verbose=False)
        assert errors == []

    def test_supervisory_mode(self):
        """Test supervisory mode passes regardless of password."""
        config = {
            "features": {
                "agency_levels": {
                    "current_level": "supervisory"
                }
            },
            "safety_controls": {
                "destructive_actions": {
                    "require_password": False
                }
            }
        }
        errors = validate_autonomous_safety(config, verbose=False)
        assert errors == []


class TestValidateAutonomousDeployPermission:
    """Tests for validate_autonomous_deploy_permission function."""

    def test_deploy_in_phase_1_fails(self):
        """Test that can_deploy_updates=true in phase 1 fails."""
        config = {
            "gradual_trust_building": {
                "current_phase": 1
            },
            "features": {
                "agency_levels": {
                    "autonomous": {
                        "can_deploy_updates": True
                    }
                }
            }
        }
        errors = validate_autonomous_deploy_permission(config, verbose=False)
        assert len(errors) == 1
        assert "CRITICAL" in errors[0]
        assert "phase >= 3" in errors[0]

    def test_deploy_in_phase_3_passes(self):
        """Test that can_deploy_updates=true in phase 3 passes."""
        config = {
            "gradual_trust_building": {
                "current_phase": 3
            },
            "features": {
                "agency_levels": {
                    "autonomous": {
                        "can_deploy_updates": True
                    }
                }
            }
        }
        errors = validate_autonomous_deploy_permission(config, verbose=False)
        assert errors == []

    def test_no_deploy_in_phase_1_passes(self):
        """Test that can_deploy_updates=false in phase 1 passes."""
        config = {
            "gradual_trust_building": {
                "current_phase": 1
            },
            "features": {
                "agency_levels": {
                    "autonomous": {
                        "can_deploy_updates": False
                    }
                }
            }
        }
        errors = validate_autonomous_deploy_permission(config, verbose=False)
        assert errors == []
