# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

C010_standards is the canonical source of truth for workspace-wide metadata standards, YAML schemas, taxonomies, and protocol definitions. It anchors the Betty Protocol, DocMeta/CodeMeta schemas, Houston configuration, and validation tooling used across Mission Control, SADB, and infrastructure projects.

**Location**: `~/SyncedProjects/C010_standards`
**Consumed by**: C001_mission-control (as git submodule at `external/standards`)

## Platform Compatibility

This workspace syncs between macOS and Windows via Syncthing. Commands are provided in cross-platform format where possible.

**Environment**:
- **macOS/Linux**: `~/SyncedProjects` paths, bash/zsh shells
- **Windows**: `C:\Users\jerem\SyncedProjects` paths, PowerShell (primary) or Git Bash

**Path Conventions**:
- Python and most modern tools accept forward slashes (`/`) on all platforms
- Examples use forward slashes by default - works on Windows PowerShell and macOS/Linux
- Backslash (`\`) alternatives noted only when specifically required

**Command Compatibility**:
- Use `python` (not `python3`) - works cross-platform
- Prefer `python -m module.command` for tool execution
- Shell scripts (`.sh`) require bash - native on macOS/Linux, needs Git Bash on Windows
- PowerShell scripts (`.ps1`) are Windows-only

**Virtual Environments**:
```bash
# Create (cross-platform)
python -m venv venv

# Activate (platform-specific)
source venv/bin/activate              # macOS/Linux/Git Bash
venv\Scripts\Activate.ps1             # Windows PowerShell
```

**Common Paths**:
```bash
# Project root (absolute)
~/SyncedProjects/C010_standards           # macOS/Linux/Git Bash
C:\Users\jerem\SyncedProjects\C010_standards  # Windows PowerShell

# Prefer relative paths when already in workspace:
cd C010_standards                     # Works everywhere from workspace root
```

**Tool Preferences**:
- File operations: Use Claude Code built-in tools (Read/Edit/Write) rather than shell commands (cat/sed/echo)
- Search: Use Grep tool rather than grep/rg commands
- Find files: Use Glob tool rather than find command

**Service Management**:
```bash
# Docker (cross-platform)
docker ps
docker start service-name

# Process inspection (platform-specific)
ps aux | grep name                    # macOS/Linux
Get-Process | Where-Object {$_.Name -like "*name*"}  # PowerShell
```

---
**Note**: This project follows the [Cross-Platform CLAUDE.md Standard](protocols/cross_platform_claude_md.md) from C010_standards.

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

**Available Validators** (registered in `validators/__init__.py`):
- `houston_docmeta` - Document metadata validation
- `houston_features` - Feature configuration validation
- `houston_tools` - Tool pipeline validation
- `houston_models` - Model deployment validation
- `houston_telemetry` - Telemetry health validation

**Houston Config (`30_config/`)** - Mission Control agent configuration:
- `houston-features.json` - Feature toggles, agency levels, trust building phases
- `houston-tools.json` - Tool pipelines, capability flags, phase gating

**Governance (`00-Governance/`)** - Historical backups and migration tooling:
- `YAML Official/` - Official taxonomy versions
- `YAML_Backup_20250713/` - Backup snapshots from July 2025
- `Scripts/` - Canvas migration and sorting utilities for Notion migration

## Common Commands

### Running Validators

```bash
# Run all validators (platform-agnostic - recommended)
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

**Platform Notes**:
- Commands work on Windows (PowerShell/cmd), macOS, and Linux
- Use forward slashes (`validators/run_all.py`) - Python handles path conversion
- On Windows with backslash preference: `python validators\run_all.py` also works

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
# Bootstrap Ruff config to all repos in workspace (Unix/macOS)
bash scripts/bootstrap_ruff.sh

# Bootstrap to specific directory (Unix/macOS)
bash scripts/bootstrap_ruff.sh /path/to/workspace

# Windows (Git Bash recommended)
bash scripts/bootstrap_ruff.sh
# Or specify Windows path
bash scripts/bootstrap_ruff.sh C:/Users/username/SyncedProjects
```

**Template location**: `policy/python/pyproject.ruff.template.toml`
**What it does**: Adds Ruff configuration to any git repo in SyncedProjects that doesn't already have `[tool.ruff]` section
**Receipt tracking**: Creates timestamped receipt in `00_admin/RECEIPTS/ruff_*.txt`

**Note**: Assumes Ruff is already installed (`brew install ruff` on macOS, `pipx install ruff` cross-platform)

### Submodule Management

C010_standards is consumed by Mission Control as a git submodule. When making changes to schemas or validators:

```bash
# In Mission Control repository
cd ~/SyncedProjects/C001_mission-control           # macOS/Linux
cd C:\Users\jerem\SyncedProjects\C001_mission-control  # Windows

# Update submodule to latest C010_standards
git submodule update --remote --merge

# Commit the submodule pointer update
git add external/standards
git commit -m "chore: update standards submodule"
```

**CI Integration**: Mission Control's `.github/workflows/standards.yml` automatically runs C010 validators on PRs

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
- **SADB** (`C002_sadb`): DocMeta/CodeMeta templates, taxonomy lookups
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
- **Python 3.11+**: Validators use modern type hints (`list[str] | None`)
- **YAML as source of truth**: Markdown schema docs are reference only
- **Houston is not a chatbot**: It's a Mission Control operations agent with gradual trust phases
- **Taxonomy changes are breaking**: Update consuming projects when modifying controlled vocabularies
- **Validators are production-ready**: Exit 0 on pass, 1 on fail - use in CI workflows
- **Dependencies optional**: Validators warn if PyYAML/jsonschema missing but still function

## Troubleshooting

### Import Errors When Running Validators

**Symptom**: `ModuleNotFoundError` or import failures

**Solution**: Ensure you're running validators from the repository root:

```bash
# Navigate to repo root first
cd ~/SyncedProjects/C010_standards           # macOS/Linux
cd C:\Users\jerem\SyncedProjects\C010_standards  # Windows

# Then run validators
python validators/run_all.py
```

Validators automatically add the repo root to `sys.path`, but must be run from the correct directory.

### Missing Dependencies

**Symptom**: Warnings about missing `pyyaml` or `jsonschema`

**Solution**: Install optional dependencies:

```bash
pip install pyyaml jsonschema
```

Note: Validators will still run without these (with warnings), but validation will be limited.

### YAML Syntax Errors

**Symptom**: `yaml.scanner.ScannerError` when modifying taxonomies

**Solution**: Validate YAML syntax before running validators:

```bash
# Quick syntax check
python -c "import yaml; yaml.safe_load(open('taxonomies/topic_taxonomy.yaml'))"

# If successful, no output = valid YAML
```

Common YAML issues:
- Inconsistent indentation (use spaces, not tabs)
- Missing quotes around values with special characters
- Trailing spaces on lines

### Validator Exit Codes

- **0**: All checks passed
- **1**: Validation failure (check output for specific errors)
- **2**: Configuration/parse error (file not found, invalid JSON/YAML)

### Path Issues on Windows

**Symptom**: File not found errors on Windows

**Solution**: Python accepts forward slashes on Windows:

```bash
# These both work on Windows
python validators/run_all.py          # Recommended (cross-platform)
python validators\run_all.py          # Also valid
```

### Schema Version Mismatches

**Symptom**: Documents fail validation after schema updates

**Solution**: Check which schema version is in use:

```bash
# View schema consumers and versions
cat notes/SCHEMA_CONSUMERS.md

# Update consuming projects to match new schema version
```

See "Integration Points > Schema Consumers" for affected projects.

## Betty Protocol Compliance

All work follows Betty Protocol evidence-driven development:
1. Document non-trivial changes in `20_receipts/` (when applicable)
2. Update `notes/CHANGELOG.md` for schema modifications
3. Never auto-commit - only when explicitly requested
4. Report blockers transparently in validator output
5. Keep README and CHANGELOG accurate when behavior changes
6. Run validators before committing Houston config changes

## META.yaml Contract

This repo uses META.yaml for project metadata. See `~/SyncedProjects/C010_standards/protocols/META_YAML_SPEC.md` for full spec.

**Agent responsibility:** Update META.yaml when adding/removing folders or key files, and set `last_reviewed` to today's date.
