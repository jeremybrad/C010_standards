# C010_standards Quickstart

**Last Updated**: 2026-01-12
**Version**: 1.0.0

Get oriented with workspace standards in 5 minutes.

## Prerequisites

- Git
- Python 3.11+ (for validators)
- Access to SyncedProjects workspace

## Quick Start

### 1. Clone or Navigate

```bash
cd ~/SyncedProjects/C010_standards
```

### 2. Read Agent Pre-Flight (Required for AI Agents)

```bash
cat AGENT_START_HERE.md
```

This document contains the mandatory checklist before operating in any repo.

### 3. Understand Betty Protocol

```bash
cat protocols/betty_protocol.md
```

Core governance rules:
- Folder structure: `00_admin/`, `10_docs/`, `20_receipts/`, `30_config/`, `40_src/`, `70_evidence/`, `90_archive/`
- Every change produces documented evidence
- Artifacts stay outside git repos
- Receipts required for non-trivial work

## Configuration

### For Mission Control Integration

C001_mission-control embeds standards as a git submodule:

```bash
cd ~/SyncedProjects/C001_mission-control
git submodule update --init external/standards
```

### For New Projects

Use the project template to ensure compliance:

```bash
# Copy template structure
cp -r ~/SyncedProjects/C010_standards/PROJECT_TEMPLATE.md ./
```

## First Operations

### Run All Validators

```bash
# Run from repo root
cd ~/SyncedProjects/C010_standards
python validators/run_all.py
```

Exit codes:
- `0` - All checks pass
- `1` - Validation failure
- `2` - Config/parse error

### Validate a Single Aspect

```bash
# Check Houston features
python validators/check_houston_features.py --config 30_config/houston-features.json

# Check repository contract
python validators/check_repo_contract.py --repo ~/SyncedProjects/P050_ableton-mcp
```

### Check README Repo Card

```bash
python scripts/validate_readme_repo_card.py ~/SyncedProjects/C001_mission-control/README.md
```

## Key Documents to Read

| Document | Purpose | When to Read |
|----------|---------|--------------|
| `AGENT_START_HERE.md` | Agent pre-flight checklist | Before any AI agent work |
| `protocols/betty_protocol.md` | Core governance rules | Starting any project |
| `protocols/tier3_documentation_spec.md` | Documentation standards | Creating docs |
| `schemas/docmeta_v1.2.yaml` | Document metadata schema | Tagging documents |
| `taxonomies/topic_taxonomy.yaml` | Topic classification | Categorizing content |

## Troubleshooting

### Validator Fails with Import Error

```bash
# Ensure you're in the validators directory
cd ~/SyncedProjects/C010_standards/validators
python -c "import yaml, jsonschema"  # Check dependencies
```

### Missing Betty Protocol Folders

```bash
# Create required structure
mkdir -p 00_admin 10_docs 20_receipts 30_config 40_src 70_evidence 90_archive
```

### Unknown Taxonomy Term

```bash
# Check universal terms for synonyms
grep -i "your_term" taxonomies/universal_terms.yaml
```

## Next Steps

- [OPERATIONS.md](OPERATIONS.md) - Day-to-day workflows
- [ARCHITECTURE.md](ARCHITECTURE.md) - System design
- [CODE_TOUR.md](CODE_TOUR.md) - Navigate the codebase
