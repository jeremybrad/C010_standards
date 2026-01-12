# Validators API Documentation

**Version**: 1.0.0
**Last Updated**: 2026-01-12
**Purpose**: CLI and Python API reference for C010 validators

---

## Overview

C010_standards provides 6 production-ready validators: 5 for Houston agent configuration/metadata, plus a general-purpose repository contract validator. All validators follow consistent CLI and Python interfaces.

---

## Quick Reference

| Validator | Target | CLI |
|-----------|--------|-----|
| `check_houston_docmeta` | DocMeta v1.2 documents | `python validators/check_houston_docmeta.py` |
| `check_houston_features` | Houston features config | `python validators/check_houston_features.py` |
| `check_houston_tools` | Houston tools config | `python validators/check_houston_tools.py` |
| `check_houston_models` | Houston models config | `python validators/check_houston_models.py` |
| `check_houston_telemetry` | Telemetry health | `python validators/check_houston_telemetry.py` |
| `check_repo_contract` | Repository structure | `python validators/check_repo_contract.py` |

---

## Common CLI Interface

All validators share these options:

```bash
python validators/check_houston_<type>.py [OPTIONS] [CONFIG_PATH]
```

### Options

| Flag | Description | Default |
|------|-------------|---------|
| `--verbose`, `-v` | Detailed output | Off |
| `--json-output PATH` | Write results to JSON | None |
| `--strict` | Treat warnings as errors | Off |
| `--help`, `-h` | Show help | - |

### Exit Codes

| Code | Meaning |
|------|---------|
| `0` | All checks passed |
| `1` | Validation failure (errors found) |
| `2` | Configuration/parse error |

---

## run_all.py - Batch Runner

Run all validators in sequence.

### Usage

```bash
# Run all with defaults
python validators/run_all.py

# Run specific validators
python validators/run_all.py --targets houston_docmeta houston_features

# Pass args to validators
python validators/run_all.py --pass-args --verbose

# Run repo_contract only
python validators/run_all.py --targets repo_contract --pass-args --verbose
```

### Options

| Flag | Description |
|------|-------------|
| `--targets` | Space-separated validator names (default: all) |
| `--pass-args` | Pass remaining args to validators |

**Note:** Stops at first failure by design. Unknown targets print available validators to stderr.

### Available Targets

```
houston_docmeta
houston_features
houston_tools
houston_models
houston_telemetry
repo_contract
```

**Note:** `repo_contract` is a general-purpose validator for any git repository. Its verify entrypoint discovery is advisory-only (does not affect exit code).

---

## check_houston_docmeta

Validates document metadata for Houston agent retrieval.

### CLI Usage

```bash
# Validate specific file
python validators/check_houston_docmeta.py path/to/doc.yaml

# Validate with custom taxonomy
python validators/check_houston_docmeta.py --taxonomy taxonomies/topic_taxonomy.yaml doc.yaml

# Verbose output
python validators/check_houston_docmeta.py -v doc.yaml
```

### Validation Rules

| Rule | Description |
|------|-------------|
| `is_houston_document` | Checks for `agent:houston` or `source:mission-control` tags |
| `has_mission_control_project` | Requires "Mission Control" or "P210" in projects |
| `has_agent_houston_tag` | Requires `routing.tags` contains `agent:houston` |
| `has_sensitivity_tag` | Requires sensitivity classification |
| `valid_topics` | Topics must exist in taxonomy |
| `playbook_has_related` | `playbook:success` requires `related_docs` |

### Python API

```python
from validators.check_houston_docmeta import (
    is_houston_document,
    validate_document,
    cli
)

# Check if document targets Houston
doc = {"routing": {"tags": ["agent:houston"]}}
result = is_houston_document(doc)  # True

# Validate document
errors = validate_document(doc, taxonomy_terms=["monitoring", "deployment"])
# Returns list of error strings

# Run CLI programmatically
exit_code = cli(["--verbose", "path/to/doc.yaml"])
```

---

## check_houston_features

Validates Houston agent feature configuration.

### CLI Usage

```bash
# Validate default config
python validators/check_houston_features.py

# Validate custom config path
python validators/check_houston_features.py 30_config/houston-features.json

# With JSON schema validation
python validators/check_houston_features.py --schema schemas/houston_features.schema.json
```

### Validation Rules

| Rule | Description |
|------|-------------|
| `valid_editors` | `ide_integration.supported_editors` contains valid editors |
| `autonomous_safety` | Autonomous mode requires password protection |
| `deploy_phase_permission` | `can_deploy_updates` only in Phase 3+ |
| `phase_consistency` | `current_level` matches phase requirements |

### Python API

```python
from validators.check_houston_features import (
    validate_supported_editors,
    validate_autonomous_safety,
    validate_autonomous_deploy_permission,
    cli
)

config = {
    "ide_integration": {"supported_editors": ["vscode", "cursor"]},
    "agency_levels": {"current_level": "supervisory"},
    "safety_controls": {"destructive_actions": {"require_password": True}},
    "gradual_trust_building": {"current_phase": 1}
}

# Validate specific rules
errors = validate_supported_editors(config)
errors = validate_autonomous_safety(config)
errors = validate_autonomous_deploy_permission(config)
```

---

## check_houston_tools

Validates Houston tool pipeline configuration.

### CLI Usage

```bash
python validators/check_houston_tools.py 30_config/houston-tools.json
python validators/check_houston_tools.py -v
```

### Validation Rules

| Rule | Description |
|------|-------------|
| `phase_consistency` | Tool phases don't exceed feature phase |
| `dangerous_ops_gated` | Destructive tools gated to Phase 3 |
| `pipeline_integrity` | Tool references valid pipelines |
| `endpoint_validation` | No placeholder endpoints in enabled tools |

### Python API

```python
from validators.check_houston_tools import (
    validate_phase_consistency,
    validate_dangerous_operations,
    cli
)

tools_config = {"phase_settings": {"current_phase": 2}}
features_config = {"gradual_trust_building": {"current_phase": 2}}

errors = validate_phase_consistency(tools_config, features_config)
```

---

## check_houston_models

Validates Houston model deployment configuration.

### CLI Usage

```bash
python validators/check_houston_models.py 30_config/houston-models.json
```

### Validation Rules

| Rule | Description |
|------|-------------|
| `deploy_phase_permission` | Deployment only enabled in Phase 3+ |
| `model_availability` | Referenced models exist |
| `fallback_chain` | Fallback models are valid |

### Python API

```python
from validators.check_houston_models import (
    validate_phase_deployment_consistency,
    cli
)

config = {
    "deployment": {"can_deploy": False},
    "phase_settings": {"current_phase": 1}
}

errors = validate_phase_deployment_consistency(config)
```

---

## check_houston_telemetry

Validates Houston telemetry health and freshness.

### CLI Usage

```bash
# Check telemetry with default staleness (300s)
python validators/check_houston_telemetry.py

# Custom staleness threshold
python validators/check_houston_telemetry.py --max-age 600

# Check specific telemetry file
python validators/check_houston_telemetry.py telemetry/latest.json
```

### Validation Rules

| Rule | Description |
|------|-------------|
| `data_freshness` | Telemetry not stale (default: 300s) |
| `latency_thresholds` | Response times within limits |
| `fallback_loops` | No infinite fallback chains |
| `required_metrics` | Core metrics present |

### Python API

```python
from validators.check_houston_telemetry import (
    validate_freshness,
    validate_latency,
    cli
)

telemetry = {
    "timestamp": "2026-01-12T10:00:00Z",
    "metrics": {"response_time_ms": 150}
}

errors = validate_freshness(telemetry, max_age_seconds=300)
errors = validate_latency(telemetry, max_latency_ms=500)
```

---

## check_repo_contract

Validates repository structure compliance for any git repository.

### CLI Usage

```bash
# Validate current repository (auto-discovers git root)
python validators/check_repo_contract.py

# Validate specific repository
python validators/check_repo_contract.py --repo-root /path/to/repo

# Verbose output (shows verify entrypoint discovery)
python validators/check_repo_contract.py -v
```

### Validation Rules

| Rule | Description | Severity |
|------|-------------|----------|
| `is_git_repo` | Must have `.git` directory | Error |
| `required_files` | README.md, .gitignore, 20_receipts/ | Error |
| `recommended_files` | CLAUDE.md, .gitattributes | Tip (advisory) |
| `repo_card_markers` | If `repo_card:start` exists, must have `:end` | Error |
| `verify_entrypoints` | Checks for make verify, 00_run/verify.*, scripts/verify*.py | Tip (advisory) |

### Verify Entrypoint Discovery

Detection priority order (first match wins):
1. `Makefile` with `verify:` target
2. `00_run/verify.*` files (lexicographic first)
3. `scripts/verify*.py` files (lexicographic first)

This check is **advisory only** - missing verify entrypoints produce tips, not errors.

### Python API

```python
from validators.check_repo_contract import (
    check_is_git_repo,
    check_required_files,
    check_recommended_files,
    check_verify_entrypoints,
    cli
)

from pathlib import Path

repo = Path("/path/to/repo")

# Check individual rules
errors = check_is_git_repo(repo, verbose=True)
errors = check_required_files(repo, verbose=True)
warnings = check_recommended_files(repo, verbose=True)
warnings = check_verify_entrypoints(repo, verbose=True)

# Run CLI programmatically
exit_code = cli(["--repo-root", "/path/to/repo", "--verbose"])
```

---

## Common Module (common.py)

Shared utilities for all validators.

### Functions

```python
from validators.common import (
    load_yaml,
    load_json,
    parse_args,
    format_errors,
    write_json_output
)

# Load configuration files
config = load_yaml("path/to/config.yaml")
config = load_json("path/to/config.json")

# Standard argument parsing
args = parse_args(["--verbose", "config.yaml"])

# Format error output
formatted = format_errors(["Error 1", "Error 2"], verbose=True)

# Write JSON results
write_json_output({"errors": [], "passed": True}, "output.json")
```

---

## JSON Output Format

When using `--json-output`, validators produce:

```json
{
  "validator": "check_houston_features",
  "version": "1.0.0",
  "timestamp": "2026-01-12T10:30:00Z",
  "config_path": "30_config/houston-features.json",
  "passed": false,
  "error_count": 2,
  "warning_count": 1,
  "errors": [
    {
      "rule": "autonomous_safety",
      "message": "Autonomous mode requires password protection",
      "severity": "error",
      "remediation": "Set safety_controls.destructive_actions.require_password to true"
    }
  ],
  "warnings": [
    {
      "rule": "deprecated_field",
      "message": "legacy_mode is deprecated",
      "severity": "warning"
    }
  ]
}
```

---

## Integration Examples

### CI/CD Pipeline

```yaml
# .github/workflows/validate.yml
name: Validate Configs

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: pip install pyyaml jsonschema

      - name: Run validators
        run: python validators/run_all.py --pass-args --verbose
```

### Pre-commit Hook

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: validate-houston
        name: Validate Houston configs
        entry: python validators/run_all.py
        language: python
        pass_filenames: false
        files: ^30_config/houston.*\.json$
```

### Python Script

```python
#!/usr/bin/env python
"""Validate all Houston configs before deployment."""

import sys
from validators import run_all

if __name__ == "__main__":
    exit_code = run_all.main([
        "--targets", "houston_features", "houston_tools",
        "--pass-args", "--strict"
    ])
    sys.exit(exit_code)
```

---

## Error Remediation

Each validator provides remediation suggestions:

| Error | Remediation |
|-------|-------------|
| "Missing agent:houston tag" | Add `agent:houston` to `routing.tags` |
| "Autonomous mode without password" | Set `require_password: true` in safety_controls |
| "Deploy enabled in Phase 1" | Set `can_deploy_updates: false` or advance to Phase 3 |
| "Invalid topic: foo" | Use topic from `taxonomies/topic_taxonomy.yaml` |
| "Telemetry stale" | Check telemetry collection service |
| "Missing required file: README.md" | Create README.md at repository root |
| "Missing required dir: 20_receipts" | Run `mkdir -p 20_receipts` |
| "No verify entrypoint found" | Add `make verify` target or `00_run/verify.*` script |

---

## Extending Validators

### Adding New Rules

```python
# In validators/check_houston_<type>.py

def validate_new_rule(config: dict, verbose: bool = False) -> list[str]:
    """Validate new rule.

    Args:
        config: Loaded configuration dict
        verbose: Print detailed output

    Returns:
        List of error messages (empty if valid)
    """
    errors = []

    if some_condition_fails(config):
        errors.append("New rule failed: explanation")
        if verbose:
            print("  Remediation: do this instead")

    return errors
```

### Registering Validators

```python
# In validators/__init__.py

AVAILABLE_VALIDATORS = {
    "houston_docmeta": "check_houston_docmeta",
    "houston_features": "check_houston_features",
    "houston_tools": "check_houston_tools",
    "houston_models": "check_houston_models",
    "houston_telemetry": "check_houston_telemetry",
    "repo_contract": "check_repo_contract",
    # Add new validators here
    "new_validator": "check_new_validator",
}
```

---

## Related Documentation

- [schema_versioning_policy.md](../protocols/schema_versioning_policy.md) - Version rules
- [schema_migration_checklist.md](../protocols/schema_migration_checklist.md) - Migration guide
- [tier3_documentation_spec.md](../protocols/tier3_documentation_spec.md) - Doc standards

---

*Maintained by: Jeremy Bradford & Claude*
