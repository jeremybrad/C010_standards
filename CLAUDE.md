# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

C010_standards is the canonical source of truth for workspace-wide metadata standards, YAML schemas, taxonomies, and protocol definitions. It anchors the Betty Protocol, DocMeta/CodeMeta schemas, Houston configuration, and validation tooling used across Mission Control, SADB, and infrastructure projects.

**Location**: `~/SyncedProjects/C010_standards`
**Consumed by**: C001_mission-control (as git submodule at `external/standards`)

## Architecture

### Core Components

**Schemas (`schemas/`)** - Versioned metadata templates:
- `docmeta_v1.2.yaml` - Document metadata schema with routing, governance, and entity tracking
- `codemeta_v1.0.yaml` - Code artifact metadata (repos, scripts, libraries)
- `houston_features.schema.json` - JSON schema for Houston feature toggles and trust phases

**Taxonomies (`taxonomies/`)** - Controlled vocabularies:
- `topic_taxonomy.yaml` - Technical topics (monitoring, deployment, infra, etc.)
- `content_taxonomy.yaml` - Document types and categorization
- `emotion_taxonomy.yaml` - Emotional context tagging
- `universal_terms.yaml` - Canonical terminology and synonyms

**Validators (`validators/`)** - Phase 2 production tooling (COMPLETE):
- `check_houston_docmeta.py` - Enforce routing tags and taxonomy alignment (YAML/MD parsing)
- `check_houston_features.py` - Validate feature config against JSON schema and trust phases
- `check_houston_tools.py` - Verify tool pipeline consistency and dangerous ops gating
- `check_houston_models.py` - Check deployment permissions against trust phases
- `check_houston_telemetry.py` - Ensure telemetry freshness, latency, and fallback loops
- `run_all.py` - Orchestration harness (stops on first failure)

**Houston Config (`30_config/`)** - Mission Control agent configuration:
- `houston-features.json` - Feature toggles, agency levels, trust building phases
- `houston-tools.json` - Tool pipelines, capability flags, phase gating

## Common Commands

### Running Validators

```bash
# Run all validators
python validators/run_all.py

# Run specific validators
python validators/run_all.py --targets houston_docmeta houston_features

# Individual validator with verbose output
python validators/check_houston_features.py --verbose

# Output to JSON for CI integration
python validators/check_houston_docmeta.py --json-output 70_evidence/docmeta_results.json

# Telemetry with custom staleness threshold
python validators/check_houston_telemetry.py --max-age 600  # 10 minutes
```

**Current State**: All 5 validators are fully implemented (Phase 2 complete). They exit 0 on pass, 1 on validation failure, 2 on config errors. Include verbose mode, JSON output, and remediation suggestions.

### Schema Validation

Houston features config is validated against `schemas/houston_features.schema.json` using jsonschema library:
```bash
python validators/check_houston_features.py --schema schemas/houston_features.schema.json
```

Install dependencies: `pip install pyyaml jsonschema` (optional - validators warn if missing)

### Testing Taxonomy Changes

When modifying taxonomies:
1. Verify YAML syntax: `python -c "import yaml; yaml.safe_load(open('taxonomies/topic_taxonomy.yaml'))"`
2. Run DocMeta validator to check Houston documents against updated taxonomy:
   ```bash
   python validators/check_houston_docmeta.py --taxonomy taxonomies/topic_taxonomy.yaml --verbose
   ```
3. Update consuming projects (Mission Control, SADB) if terms change

### Ruff Bootstrap Tooling

C010_standards provides workspace-wide Python linting standards:

```bash
# Bootstrap Ruff config to all repos in workspace
bash scripts/bootstrap_ruff.sh

# Bootstrap to specific directory
bash scripts/bootstrap_ruff.sh /path/to/workspace
```

**Template location**: `policy/python/pyproject.ruff.template.toml`
**What it does**: Adds Ruff configuration to any git repo in SyncedProjects that doesn't already have `[tool.ruff]` section
**Receipt tracking**: Creates timestamped receipt in `00_admin/RECEIPTS/ruff_*.txt`

**Note**: Assumes Ruff is already installed (`brew install ruff` or `pipx install ruff`)

## Houston Configuration Guidelines

### Feature Toggles (`30_config/houston-features.json`)

**Trust Building Phases** - Houston operates in gradual phases:
- **Phase 1 (Observation)**: `supervisory` agency level, basic monitoring only
- **Phase 2 (Collaboration)**: `advisory` level, IDE integration, proactive alerts
- **Phase 3 (Partnership)**: `autonomous` level, full agency with emergency protocols

**Critical Rules**:
- `agency_levels.current_level` must match the phase's `agency_level`
- `autonomous.can_deploy_updates` requires `current_phase >= 3`
- `safety_controls.destructive_actions.require_password` must be `true` when `current_level` is `autonomous`
- `gradual_trust_building.auto_advance` is `false` by default - phases advance manually
- Phase advancement requires receipt entry in `notes/CHANGELOG.md` with pattern `Phase <n> activated`

**Audio/Visual Theme**: Mission Control retro console aesthetic with radio static effects, CRT scanlines, LED indicators. TTS engine is local with southern ops personality.

### Tool Pipelines (`30_config/houston-tools.json`)

- `phase_settings.current_phase` must be ≤ `gradual_trust_building.current_phase` from `houston-features.json`
- Phase 3 operations (`kill_processes`, `system_shutdown`) should not appear in Phase 1/2 overrides
- VPS tools require real endpoint (not placeholder `example.com`) before enabling

## Metadata Standards

### DocMeta v1.2 Tagging for Houston

Documents targeting Houston agent retrieval must include:

```yaml
doc:
  projects:
    - "Mission Control"
    - "P210"
  topics:
    - "monitoring"  # from taxonomies/topic_taxonomy.yaml
routing:
  tags:
    - "agent:houston"
    - "sensitivity:internal"
connections:
  related_docs:  # required when routing.tags contains playbook:success
    - "<sha256 or path>"
```

**Topic Validation**: All `doc.topics` values must exist in `taxonomies/topic_taxonomy.yaml`. Common Houston topics: monitoring, deployment, infra, automation, orchestration.

### CodeMeta v1.0 Usage

For code artifacts (scripts, repos, libraries):

```yaml
code:
  repo: "https://github.com/..."
  language: "python"
  dependencies:
    - name: "yaml"
      version: "6.0"
```

See `schemas/codemeta_v1.0.yaml` for full template.

## File Conventions

### Naming
- Versioned schemas: lowercase with underscores (`docmeta_v1.2.yaml`)
- Keep source attribution comments at top of YAML files
- Markdown docs start with level-1 heading

### YAML Comments
All imported YAML files include provenance:
```yaml
# Source: ../P002_sadb/10_docs/SADB_DocMeta_Schema_v1.2.md
# Attribution: SADB knowledge base metadata schema maintained by Jeremy Bradford.
```

### Updates
- Update `notes/CHANGELOG.md` when touching canonical schemas or taxonomies
- Reference affected files and upstream sources in commit body
- Include diff snippets for schema changes

## Validator Architecture

All validators follow a consistent pattern:

**CLI Contract**:
- Accept paths/configs as arguments with sensible defaults
- Exit 0 on pass, 1 on validation failure, 2 on config/parse errors
- Support `--verbose` for detailed output
- Support `--json-output` for CI integration
- Provide actionable remediation suggestions on failure

**Common Structure**:
```python
def cli(argv: List[str] | None = None) -> int:
    args = parse_args(argv or [])
    config = load_config(args.config)

    all_errors = []
    all_errors.extend(validate_rule_1(config, args.verbose))
    all_errors.extend(validate_rule_2(config, args.verbose))

    if all_errors:
        print(f"❌ Validation FAILED ({len(all_errors)} issues)")
        # Print remediation suggestions
        return 1
    else:
        print("✅ Validation passed")
        return 0
```

**Registry**: Update `validators/__init__.py` `AVAILABLE_VALIDATORS` when adding new validators

## Integration Points

### Consuming Projects
- **Mission Control** (`C001_mission-control`): Consumes via git submodule at `external/standards`
- **SADB** (`P002_sadb`): DocMeta/CodeMeta templates, taxonomy lookups
- **Betty Mirror** (`P001_bettymirror`): Protocol enforcement, lint rules
- **Infrastructure** (various): Standard taxonomies for tagging via Ruff bootstrap

### Schema Consumers
See `notes/SCHEMA_CONSUMERS.md` for complete inventory of which projects depend on each schema version.

### Houston Integration
- Interface blueprint: `notes/HOUSTON_INTERFACE.md`
- Inference routing: `notes/HOUSTON_INFERENCE.md`
- Agent playbook: `notes/AGENT_PLAYBOOK.md`
- Tooling plan: `notes/HOUSTON_TOOLING.md`
- Model bootstrap: `notes/scripts/MODEL_BOOTSTRAP.md`

## Roadmap

**Phase 1 (Complete)**: Consolidation of schemas, taxonomies, protocols from SADB and Betty Mirror

**Phase 2 (Complete)**: All 5 validators implemented, Ruff baseline deployed, C001 integration via submodule

**Phase 3 (In Progress)**: Adoption across repos, Houston interface prototyping, schema versioning policy

See `notes/ROADMAP.md` for detailed task breakdown.

## Important Notes

- **No build system**: Pure schema/config repository, no compilation required
- **Python 3.13+**: Validators use modern type hints (`List[str] | None`)
- **YAML as source of truth**: Markdown schema docs are reference only
- **Houston is not a chatbot**: It's a Mission Control operations agent with gradual trust phases
- **Taxonomy changes are breaking**: Update consuming projects when modifying controlled vocabularies
- **Validators are production-ready**: Exit 0 on pass, 1 on fail - use in CI workflows
- **Dependencies optional**: Validators warn if PyYAML/jsonschema missing but still function

## Betty Protocol Compliance

All work follows Betty Protocol evidence-driven development:
1. Document non-trivial changes in `20_receipts/` (when applicable)
2. Update `notes/CHANGELOG.md` for schema modifications
3. Never auto-commit - only when explicitly requested
4. Report blockers transparently in validator output
5. Keep README and CHANGELOG accurate when behavior changes
6. Run validators before committing Houston config changes
