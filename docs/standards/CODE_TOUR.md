# C010_standards Code Tour

**Last Updated**: 2026-01-12
**Version**: 1.0.0

Navigate the C010_standards codebase efficiently.

## Quick Reference

| I want to... | Look at... |
|--------------|------------|
| Understand workspace governance | `protocols/betty_protocol.md` |
| Create Tier 3 documentation | `protocols/tier3_documentation_spec.md` |
| Define document metadata | `schemas/docmeta_v1.2.yaml` |
| Classify content by topic | `taxonomies/topic_taxonomy.yaml` |
| Run compliance checks | `validators/run_all.py` |
| Find a project's metadata | `registry/repos.yaml` |
| Configure agent behavior | `30_config/houston-features.json` |
| Set up a new repo | `PROJECT_TEMPLATE.md` |
| Understand agent pre-flight | `AGENT_START_HERE.md` |

## Directory Map

```
C010_standards/
├── 00_admin/                    # Governance policies
├── 10_docs/                     # Documentation artifacts
├── 20_receipts/                 # Change receipts (148+ entries)
│   └── YYYY-MM-DD_description.md
├── 30_config/                   # Configuration files
│   ├── houston-features.json    # Feature toggles and trust phases
│   └── houston-tools.json       # Tool pipeline configuration
├── docs/                        # Tier 3 documentation
│   └── standards/               # This folder
├── protocols/                   # Standards definitions (11 docs)
│   ├── betty_protocol.md        # Core governance rules
│   ├── tier3_documentation_spec.md  # Doc standards
│   ├── session_closeout_protocol.md # Session handoff
│   ├── cross_platform_claude_md.md  # CLAUDE.md format
│   ├── META_YAML_SPEC.md        # Metadata contract
│   └── ...
├── registry/                    # Project registry
│   ├── repos.yaml               # All project metadata
│   ├── schema.md                # Registry data model
│   └── README.md                # Usage guide
├── schemas/                     # Data contracts
│   ├── docmeta_v1.2.yaml        # Document metadata
│   ├── codemeta_v1.0.yaml       # Code metadata
│   └── houston_features.schema.json
├── scripts/                     # Utilities
│   ├── bootstrap_ruff.sh        # Add Ruff to repos
│   ├── bootstrap_claude_crossplatform.sh
│   └── validate_readme_repo_card.py
├── taxonomies/                  # Controlled vocabularies
│   ├── topic_taxonomy.yaml      # Technical topics
│   ├── content_taxonomy.yaml    # Document types
│   ├── emotion_taxonomy.yaml    # Emotional context
│   ├── universal_terms.yaml     # Synonyms
│   └── disambiguation_rules.yaml
├── validators/                  # Compliance checkers
│   ├── run_all.py               # Orchestration harness
│   ├── check_houston_docmeta.py
│   ├── check_houston_features.py
│   ├── check_houston_tools.py
│   ├── check_houston_models.py
│   ├── check_houston_telemetry.py
│   └── check_repo_contract.py
├── workspace/                   # Workspace-level docs
│   ├── KNOWN_PROJECTS.md        # Auto-generated nightly
│   └── PROJECT_RELATIONSHIPS.md # System architecture
├── AGENT_START_HERE.md          # Required pre-flight
├── CLAUDE.md                    # Claude Code guidance
├── CONTRIBUTING.md              # Contribution guide
├── META.yaml                    # Project metadata
├── PROJECT_TEMPLATE.md          # New repo template
└── README.md                    # Main entry point
```

## Key Entry Points

### Validator Orchestrator (`validators/run_all.py`)

```python
# Runs all validators in sequence, stops on first failure
def main():
    validators = [
        "check_houston_features.py",
        "check_houston_tools.py",
        "check_houston_models.py",
        "check_houston_telemetry.py",
        "check_houston_docmeta.py",
    ]
    for validator in validators:
        exit_code = run_validator(validator)
        if exit_code != 0:
            sys.exit(exit_code)
    sys.exit(0)
```

### README Repo Card Validator (`scripts/validate_readme_repo_card.py`)

```python
# Extracts and validates repo card from README
def validate_repo_card(readme_path: str) -> bool:
    """
    Checks for BOT markers and required fields:
    - Project ID (C###, P###, W###)
    - Status (active, maintenance, archived)
    - Purpose (1-2 sentence description)
    """
```

## Configuration

### Houston Features (`30_config/houston-features.json`)

```json
{
  "trust_phase": "advisory",
  "agency_level": "advisory",
  "features": {
    "auto_commit": false,
    "auto_push": false,
    "dangerous_operations": {
      "enabled": false,
      "allowed": ["soft_reset"]
    }
  },
  "phase_gates": {
    "supervised": ["all"],
    "advisory": ["delete", "force_push"],
    "autonomous": []
  }
}
```

### Project Registry (`registry/repos.yaml`)

```yaml
repositories:
  C001_mission-control:
    id: C001
    name: mission-control
    status: active
    tier: kitted
    path: ~/SyncedProjects/C001_mission-control
    relationships:
      - embeds: C010_standards
```

## Common Patterns

### Validator Pattern

```python
#!/usr/bin/env python3
"""Houston validator for [aspect]."""

import sys
import yaml
import argparse

def validate(config: dict) -> list[str]:
    """Returns list of validation errors."""
    errors = []
    # ... validation logic
    return errors

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    args = parser.parse_args()

    with open(args.config) as f:
        config = yaml.safe_load(f)

    errors = validate(config)
    if errors:
        for e in errors:
            print(f"ERROR: {e}")
        sys.exit(1)

    print("OK: All checks passed")
    sys.exit(0)

if __name__ == "__main__":
    main()
```

### Receipt Pattern

```markdown
# Receipt: [Description]

**Date**: YYYY-MM-DD
**Agent**: Claude [Model]
**Project**: C010_standards

## Summary

[What was done]

## Changes

- [Change 1]
- [Change 2]

## Verification

[How to verify]
```

## Development Commands

```bash
# Run all validators
cd validators && python run_all.py --config ../30_config/houston-features.json

# Validate single aspect
python validators/check_houston_features.py --config 30_config/houston-features.json

# Bootstrap Ruff on a repo
./scripts/bootstrap_ruff.sh ~/SyncedProjects/P050_ableton-mcp

# Validate README repo card
python scripts/validate_readme_repo_card.py ~/SyncedProjects/C001_mission-control/README.md
```

## Test Files

| Test Area | Location | Description |
|-----------|----------|-------------|
| Validators | `validators/*.py` | Each validator is self-testing |
| Schemas | `schemas/*.yaml` | Validated by jsonschema |
| Repo Card | `scripts/validate_readme_repo_card.py` | README extraction test |

## Related Documentation

- [ARCHITECTURE.md](ARCHITECTURE.md) - System design
- [OPERATIONS.md](OPERATIONS.md) - Day-to-day operation
- [OVERVIEW.md](OVERVIEW.md) - System overview
