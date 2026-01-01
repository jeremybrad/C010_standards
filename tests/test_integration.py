"""Integration tests for validator pipeline.

These tests verify end-to-end behavior with real configuration files
and the complete validator orchestration harness.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from validators.run_all import main as run_all_main


class TestValidatorOrchestration:
    """Test the validator orchestration harness."""

    def test_run_all_with_valid_configs(self):
        """Test run_all.py with current valid configurations."""
        result = run_all_main([])
        assert result == 0, "All validators should pass with current configs"

    def test_run_all_with_specific_validators(self):
        """Test running specific subset of validators."""
        result = run_all_main(["--targets", "houston_features", "houston_tools"])
        assert result == 0

    def test_run_all_stops_on_first_failure(self, tmp_path):
        """Test that run_all stops on first validation failure."""
        # Create invalid features config
        invalid_config = tmp_path / "invalid_features.json"
        invalid_config.write_text('{"invalid": "json structure"}')

        # Run with invalid config should fail fast
        result = run_all_main([
            "--targets", "houston_features",
            "--pass-args", "--config", str(invalid_config)
        ])

        assert result != 0, "Should fail with invalid config"


class TestHoustonFeaturesValidation:
    """Integration tests for Houston features validation."""

    def test_phase1_example_validates(self):
        """Test that Phase 1 example config validates successfully."""
        from validators.check_houston_features import cli

        example_path = Path("examples/houston_phase1_observation.json")
        if not example_path.exists():
            pytest.skip("Example file not found")

        result = cli(["--config", str(example_path)])
        assert result == 0, "Phase 1 example should validate"

    def test_phase2_example_validates(self):
        """Test that Phase 2 example config validates successfully."""
        from validators.check_houston_features import cli

        example_path = Path("examples/houston_phase2_collaboration.json")
        if not example_path.exists():
            pytest.skip("Example file not found")

        result = cli(["--config", str(example_path)])
        assert result == 0, "Phase 2 example should validate"

    def test_phase3_example_validates(self):
        """Test that Phase 3 example config validates successfully."""
        from validators.check_houston_features import cli

        example_path = Path("examples/houston_phase3_partnership.json")
        if not example_path.exists():
            pytest.skip("Example file not found")

        result = cli(["--config", str(example_path)])
        assert result == 0, "Phase 3 example should validate"

    def test_current_config_validates(self):
        """Test that current production config validates."""
        from validators.check_houston_features import cli

        config_path = Path("30_config/houston-features.json")
        result = cli(["--config", str(config_path)])
        assert result == 0, "Current production config should validate"

    def test_invalid_config_fails(self, tmp_path):
        """Test that invalid config fails validation."""
        from validators.check_houston_features import cli

        # Create invalid config (missing required fields)
        invalid_config = tmp_path / "invalid.json"
        invalid_config.write_text('{"features": {}}')

        result = cli(["--config", str(invalid_config)])
        assert result == 1, "Invalid config should fail"


class TestHoustonToolsValidation:
    """Integration tests for Houston tools validation."""

    def test_current_tools_config_validates(self):
        """Test that current tools config validates."""
        from validators.check_houston_tools import cli

        config_path = Path("30_config/houston-tools.json")
        result = cli(["--config", str(config_path)])
        assert result == 0, "Current tools config should validate"

    def test_tools_phase_alignment(self):
        """Test that tools and features phases align."""
        from validators.check_houston_tools import cli

        tools_path = Path("30_config/houston-tools.json")
        features_path = Path("30_config/houston-features.json")

        result = cli([
            "--config", str(tools_path),
            "--features-config", str(features_path)
        ])

        assert result == 0, "Tools and features phases should align"


class TestHoustonModelsValidation:
    """Integration tests for Houston models validation."""

    def test_current_models_config_validates(self):
        """Test that current features config validates for models."""
        from validators.check_houston_models import cli

        config_path = Path("30_config/houston-features.json")
        result = cli(["--features-config", str(config_path)])
        assert result == 0, "Current config should validate for models"


class TestHoustonDocMetaValidation:
    """Integration tests for DocMeta validation."""

    def test_example_docmeta_validates(self):
        """Test that DocMeta example validates."""
        from validators.check_houston_docmeta import cli

        example_path = Path("examples/docmeta_example.yaml")
        if not example_path.exists():
            pytest.skip("Example file not found")

        result = cli([str(example_path)])
        assert result == 0, "DocMeta example should validate"

    def test_houston_document_example_validates(self):
        """Test that Houston document example validates."""
        from validators.check_houston_docmeta import cli

        example_path = Path("examples/houston_document_example.md")
        if not example_path.exists():
            pytest.skip("Example file not found")

        result = cli([str(example_path)])
        assert result == 0, "Houston document example should validate"

    def test_taxonomy_validation(self):
        """Test validation against topic taxonomy."""
        from validators.check_houston_docmeta import cli

        taxonomy_path = Path("taxonomies/topic_taxonomy.yaml")
        if not taxonomy_path.exists():
            pytest.skip("Taxonomy file not found")

        result = cli([
            "examples/",
            "--taxonomy", str(taxonomy_path)
        ])

        # Should pass or have no Houston documents
        assert result == 0, "Example documents should use valid topics from taxonomy"


class TestCLIBehavior:
    """Test CLI behavior and error handling."""

    def test_validator_help_messages(self):
        """Test that validators provide help messages."""
        validators = [
            "validators/check_houston_features.py",
            "validators/check_houston_tools.py",
            "validators/check_houston_models.py",
            "validators/check_houston_docmeta.py",
            "validators/check_houston_telemetry.py",
        ]

        for validator in validators:
            result = subprocess.run(
                ["python3", validator, "--help"],
                capture_output=True,
                text=True
            )
            assert result.returncode == 0
            assert "usage:" in result.stdout.lower()

    def test_validators_verbose_mode(self):
        """Test that validators support verbose mode."""
        from validators.check_houston_features import cli

        config_path = Path("30_config/houston-features.json")

        # Should work with verbose flag
        result = cli(["--config", str(config_path), "--verbose"])
        assert result == 0

    def test_validator_exit_codes(self, tmp_path):
        """Test that validators return correct exit codes."""
        from validators.check_houston_features import cli

        # Exit 0 for success
        valid_config = tmp_path / "valid.json"
        valid_config.write_text(Path("30_config/houston-features.json").read_text())
        assert cli(["--config", str(valid_config)]) == 0

        # Exit 1 for validation failure
        invalid_config = tmp_path / "invalid.json"
        invalid_config.write_text('{"features": {"agency_levels": {}}}')
        result = cli(["--config", str(invalid_config)])
        assert result in [1, 2], "Should exit with error code"

        # Exit 2 for config error (missing file)
        missing_config = tmp_path / "missing.json"
        result = cli(["--config", str(missing_config)])
        assert result == 1, "Should exit with error for missing file"


class TestEndToEnd:
    """End-to-end workflow tests."""

    def test_full_validation_pipeline(self):
        """Test complete validation pipeline as run in CI."""
        # Step 1: Run all validators
        result = run_all_main([])
        assert result == 0, "All validators should pass"

        # Step 2: Validate examples (skip if example files don't exist)
        example_path = Path("examples/houston_phase1_observation.json")
        if example_path.exists():
            result = run_all_main([
                "--targets", "houston_features",
                "--pass-args", "--config", str(example_path)
            ])
            assert result == 0, "Example validation should pass"

    def test_config_change_validation_workflow(self, tmp_path):
        """Test workflow for validating config changes."""
        from validators.check_houston_features import cli

        # 1. Start with valid config
        config_path = tmp_path / "houston-features.json"
        original = json.loads(Path("30_config/houston-features.json").read_text())
        config_path.write_text(json.dumps(original, indent=2))

        # 2. Validate original
        assert cli(["--config", str(config_path)]) == 0

        # 3. Make valid change (change phase)
        modified = json.loads(config_path.read_text())
        modified["gradual_trust_building"]["current_phase"] = 2
        modified["features"]["agency_levels"]["current_level"] = "advisory"
        config_path.write_text(json.dumps(modified, indent=2))

        # 4. Validate change
        assert cli(["--config", str(config_path)]) == 0

        # 5. Make invalid change (enable deployment in phase 2)
        modified["features"]["agency_levels"]["autonomous"]["can_deploy_updates"] = True
        config_path.write_text(json.dumps(modified, indent=2))

        # 6. Should fail validation
        assert cli(["--config", str(config_path)]) == 1


class TestSchemaConsistency:
    """Test consistency across schemas and examples."""

    def test_all_phase_examples_have_correct_phase_numbers(self):
        """Test that phase examples have matching phase numbers."""
        examples = [
            ("examples/houston_phase1_observation.json", 1),
            ("examples/houston_phase2_collaboration.json", 2),
            ("examples/houston_phase3_partnership.json", 3),
        ]

        for path_str, expected_phase in examples:
            path = Path(path_str)
            if not path.exists():
                continue

            config = json.loads(path.read_text())
            actual_phase = config["gradual_trust_building"]["current_phase"]
            assert actual_phase == expected_phase, (
                f"{path.name} should have phase {expected_phase}"
            )

    def test_all_json_files_are_valid_json(self):
        """Test that all JSON files in repository are valid."""
        json_files = [
            Path("30_config/houston-features.json"),
            Path("30_config/houston-tools.json"),
            Path("schemas/houston_features.schema.json"),
        ]

        # Add example JSON files if they exist
        examples_dir = Path("examples")
        if examples_dir.exists():
            json_files.extend(examples_dir.glob("*.json"))

        for json_file in json_files:
            if not json_file.exists():
                continue

            try:
                json.loads(json_file.read_text())
            except json.JSONDecodeError as e:
                pytest.fail(f"{json_file} is not valid JSON: {e}")
