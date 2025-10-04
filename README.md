# P210 Metadata Governance

Canonical home for workspace-wide metadata standards, YAML schemas, taxonomies, and protocol definitions. Anchors the Betty Protocol, DocMeta/CodeMeta schemas, and the tooling used by Mission Control, SADB, and other projects.

## Purpose
- Provide a single source of truth for metadata/front-matter schemas (DocMeta, CodeMeta, etc.)
- Maintain taxonomies (topics, content types, emotions) used across documentation and tooling
- Host governance documents (Betty Protocol, Universal Claude Standards) with version tracking
- Deliver validation tooling (linters, schema checkers) for consistent application in all repositories

## Directory Layout
```
schemas/      # YAML/JSON schemas (DocMeta, CodeMeta, future variants)
taxonomies/   # Topic, content, emotion taxonomies (consolidated)
protocols/    # Governance docs (Betty Protocol, Universal Claude Standards)
prompts/      # LLM prompts for metadata generation
validators/   # CLI/CI tools for schema enforcement (TODO)
notes/        # Planning notes (ROADMAP, CHANGELOG, ADRs)
```

## Initial Tasks
- [x] Consolidate DocMeta/CodeMeta schemas from `P002_sadb/10_docs/`
- [x] Move taxonomy files from `P002_sadb/30_config` and `30_taxonomy` into `taxonomies/`
- [x] Link/import Betty Protocol (`WORKSPACE_BETTY_PROTOCOL.md`, `P001_bettymirror/CLAUDE.md`)
- [ ] Create initial validator placeholder (e.g., `validators/docmeta_check.js`)
- [ ] Update consuming projects (Mission Control, SADB, Infrastructure) to reference this repo

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

## Next Steps
1. Import existing standards with attribution (no duplication—use symlinks or include notes pointing to original sources until migration complete)
2. Draft a migration checklist for repositories adopting the canonical schemas
3. Set up CI/Git hooks to validate metadata using these schemas
4. Coordinate with Mission Control to expose this repository in its docs and UI

---

_All downstream repositories should treat this repo as the authoritative metadata spec. Updates here require versioning, changelog, and communication across projects._
