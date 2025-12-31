# Metadata Governance Roadmap

## Phase 1 – Consolidation
- [x] Copy/normalize DocMeta v1.2 and CodeMeta v1.0 schemas into `schemas/`
- [x] Move taxonomies (content, topic, emotion) into `taxonomies/`
- [x] Capture Betty Protocol + Universal Claude Standards under `protocols/`
- [x] Document schema consumers (versions noted in canonical files)

## Phase 2 – Tooling (COMPLETE)
- [x] Build `validators/docmeta_check.js` (or Python) for schema validation
- [x] Add validator ensuring Houston model tags/fallback chains match installed models
- [x] Add validator checking DocMeta routing tags for Houston memories align with taxonomy (`agent:houston`, `sensitivity:internal`)
- [x] Add validator confirming `houston-tools` phase settings match enabled pipelines and permissions
- [x] Implement all 5 Houston validators with full validation logic
- [x] Add verbose mode, JSON output, and remediation suggestions to all validators
- [x] Rename to C010_standards and integrate with C001_mission-control as submodule
- [x] Add Ruff baseline and workspace-wide bootstrap script
- [ ] Prototype Houston interface component (text/voice bar) after validator implementations complete
- [ ] Integrate with Mission Control headless service (optional API endpoint)
- [ ] Provide npm/CLI package so other repos can `npm install metadata-governance`

## Phase 3 – Adoption
- [ ] Update SADB, Mission Control, Infrastructure READMEs to reference C010_standards
- [x] Add CI checks in C001_mission-control to validate metadata (non-blocking)
- [ ] Add CI checks in other major repos to validate metadata
- [ ] Publish changelog and versioning policy

## Parking Lot
- Investigate existing lint rules (`P001_bettymirror/40_src/bettylint/rules.yaml`)
- Consolidate duplicate taxonomies (30_config vs 30_taxonomy)
- Design a schema registry (DocMeta v1.2, v1.3, etc.) with migration guidelines
- Explore bundling standard prompts and best practices
