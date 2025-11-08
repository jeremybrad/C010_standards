"""Tests for check_houston_models validator."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from validators.check_houston_models import validate_phase_deployment_consistency


class TestValidatePhaseDeploymentConsistency:
    """Tests for validate_phase_deployment_consistency function."""

    def test_deploy_disabled_in_phase_1(self):
        """Test that can_deploy_updates=false in phase 1 passes."""
        config = {
            "gradual_trust_building": {"current_phase": 1},
            "features": {
                "agency_levels": {
                    "autonomous": {"can_deploy_updates": False}
                }
            }
        }

        errors = validate_phase_deployment_consistency(config, verbose=False)
        assert errors == []

    def test_deploy_enabled_in_phase_1_fails(self):
        """Test that can_deploy_updates=true in phase 1 fails."""
        config = {
            "gradual_trust_building": {"current_phase": 1},
            "features": {
                "agency_levels": {
                    "autonomous": {"can_deploy_updates": True}
                }
            }
        }

        errors = validate_phase_deployment_consistency(config, verbose=False)
        assert len(errors) == 1
        assert "phase >= 3" in errors[0]

    def test_deploy_enabled_in_phase_2_fails(self):
        """Test that can_deploy_updates=true in phase 2 fails."""
        config = {
            "gradual_trust_building": {"current_phase": 2},
            "features": {
                "agency_levels": {
                    "autonomous": {"can_deploy_updates": True}
                }
            }
        }

        errors = validate_phase_deployment_consistency(config, verbose=False)
        assert len(errors) == 1
        assert "phase >= 3" in errors[0]

    def test_deploy_enabled_in_phase_3_passes(self):
        """Test that can_deploy_updates=true in phase 3 passes."""
        config = {
            "gradual_trust_building": {"current_phase": 3},
            "features": {
                "agency_levels": {
                    "autonomous": {"can_deploy_updates": True}
                }
            }
        }

        errors = validate_phase_deployment_consistency(config, verbose=False)
        assert errors == []

    def test_deploy_disabled_in_phase_3_passes(self):
        """Test that can_deploy_updates=false in phase 3 passes."""
        config = {
            "gradual_trust_building": {"current_phase": 3},
            "features": {
                "agency_levels": {
                    "autonomous": {"can_deploy_updates": False}
                }
            }
        }

        errors = validate_phase_deployment_consistency(config, verbose=False)
        assert errors == []

    def test_missing_can_deploy_field(self):
        """Test handling of missing can_deploy_updates field."""
        config = {
            "gradual_trust_building": {"current_phase": 1},
            "features": {
                "agency_levels": {
                    "autonomous": {}
                }
            }
        }

        # Should default to False if field missing
        errors = validate_phase_deployment_consistency(config, verbose=False)
        assert errors == []

    def test_missing_phase_field(self):
        """Test handling of missing required field."""
        config = {
            "features": {
                "agency_levels": {
                    "autonomous": {"can_deploy_updates": False}
                }
            }
        }

        errors = validate_phase_deployment_consistency(config, verbose=False)
        assert len(errors) == 1
        assert "Missing required field" in errors[0]
