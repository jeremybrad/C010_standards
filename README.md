# C010_standards

Canonical home for workspace-wide metadata standards, YAML schemas, taxonomies, and protocol definitions. Anchors the Betty Protocol, DocMeta/CodeMeta schemas, and the tooling used by Mission Control, SADB, and other projects.

**Status**: Integrated into C001_mission-control as git submodule (`external/standards`)
**Ruff**: Baseline config + workspace bootstrap script included

## Purpose
- Provide a single source of truth for metadata/front-matter schemas (DocMeta, CodeMeta, etc.)
- Maintain taxonomies (topics, content types, emotions) used across documentation and tooling
- Host governance documents (Betty Protocol, Universal Claude Standards) with version tracking
- Deliver validation tooling (linters, schema checkers) for consistent application in all repositories
- Define and enforce SyncedProjects repository organization standards (C/P/W naming conventions)

## Organization Documentation
- **[REPOSITORY_ORGANIZATION.md](REPOSITORY_ORGANIZATION.md)** - Naming conventions, folder structure, cleanup procedures
- **[PROJECT_MAP.md](PROJECT_MAP.md)** - Current project inventory with status and migration needs

## Directory Layout
```
schemas/      # YAML/JSON schemas (DocMeta, CodeMeta, future variants)
taxonomies/   # Topic, content, emotion taxonomies (consolidated)
protocols/    # Governance docs (Betty Protocol, Universal Claude Standards)
prompts/      # LLM prompts for metadata generation
validators/   # CLI/CI tools for schema enforcement (Phase 2 stubs)
notes/        # Planning notes (ROADMAP, CHANGELOG, ADRs)
policy/       # Ruff templates and Python standards
scripts/      # Bootstrap scripts (bootstrap_ruff.sh)
30_config/    # Houston features and tool pipeline config
```

## Completed Setup
- [x] Consolidate DocMeta/CodeMeta schemas from `P002_sadb/10_docs/`
- [x] Move taxonomy files from `P002_sadb/30_config` and `30_taxonomy` into `taxonomies/`
- [x] Link/import Betty Protocol (`WORKSPACE_BETTY_PROTOCOL.md`, `P001_bettymirror/CLAUDE.md`)
- [x] Create validator scaffolds (5 Houston validators + orchestration harness)
- [x] Rename P210 → C010_standards
- [x] Add Ruff baseline config + workspace bootstrap script
- [x] Wire into C001_mission-control as git submodule
- [x] Add CI guardrails to C001 (`.github/workflows/standards.yml`)

## References
- Workspace protocol: `/Users/jeremybradford/SyncedProjects/WORKSPACE_BETTY_PROTOCOL.md`
- Enforcement repo: `/Users/jeremybradford/SyncedProjects/P001_bettymirror`
- Document schemas & taxonomies: `/Users/jeremybradford/SyncedProjects/P002_sadb`
- Schema consumer inventory: `notes/SCHEMA_CONSUMERS.md`
- Houston inference plan: `notes/HOUSTON_INFERENCE.md`
- Houston retrieval playbook: `notes/AGENT_PLAYBOOK.md`
- Houston features config: `30_config/houston-features.json` (schema: `schemas/houston_features.schema.json`)
- Houston tooling plan: `notes/HOUSTON_TOOLING.md`
- Houston tool pipelines config: `30_config/houston-tools.json`
- Houston interface blueprint: `notes/HOUSTON_INTERFACE.md`

## Quick Start

### Run Validators
```bash
cd ~/SyncedProjects/C010_standards
python validators/run_all.py
```
**Expected**: Exit status 99 (not implemented) - Phase 2 stubs signal unimplemented logic

### Bootstrap Ruff Across Workspace
```bash
bash ~/SyncedProjects/C010_standards/scripts/bootstrap_ruff.sh
```
Adds Ruff config to all git repos in `SyncedProjects/` that don't already have it

### Update Submodule in C001
```bash
cd ~/SyncedProjects/C001_mission-control
git submodule update --remote --merge
```

## Next Steps
1. Phase 2: Implement validator logic (replace exit 99 with real checks)
2. Draft migration checklist for repositories adopting canonical schemas
3. Expose standards in Mission Control UI/docs
4. Add schema versioning policy (v1.3, v2.0, etc.)

---

_All downstream repositories should treat this repo as the authoritative metadata spec. Updates here require versioning, changelog, and communication across projects._
