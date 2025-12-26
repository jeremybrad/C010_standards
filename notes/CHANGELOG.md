# Metadata Governance Changelog

## 2025-12-26
- **Folder Structure Standard Update**: Updated Betty Protocol Canon to include `00_run` and `50_data` as allowed top-level directories
- **Easy Buttons Standard**: Added `00_run/` folder convention for double-clickable launchers (`.command` for macOS, `.ps1` for Windows)
- **Folder Structure Audit Script**: Created `scripts/audit_folder_structure.sh` with:
  - Checks for non-compliant numbered directories
  - Required files validation (README.md, rules_now.md, RELATIONS.yaml)
  - Per-repo exceptions via `00_admin/audit_exceptions.yaml`
  - Receipt generation in `20_receipts/`
- **Standards Pulse Generator**: Created `00_run/` easy buttons and `tools/export_standards_pulse.py`:
  - Generates `70_evidence/exports/Standards_Pulse.xlsx` (multi-sheet workbook)
  - Generates `70_evidence/exports/Standards_Inventory.csv` (flat inventory)
  - Creates receipts in `20_receipts/`
  - Cross-platform launchers (macOS .command, Windows .ps1)
- **Standards Guide**: Created `10_docs/STANDARDS_GUIDE.md` documenting:
  - Where standards live (protocols/, schemas/, taxonomies/)
  - The process for adding new standards
  - How to confirm standards are in place
  - The Define → Document → Bootstrap → Validate lifecycle

## 2025-10-18
- **Cross-Platform CLAUDE.md Standard**: Created comprehensive protocol (`protocols/cross_platform_claude_md.md`) for writing CLAUDE.md files that work seamlessly across macOS and Windows
- **Cross-Platform Template**: Added reusable template snippet (`policy/templates/claude_md_crossplatform.template.md`) for inclusion in CLAUDE.md files
- **Bootstrap Script**: Created `scripts/bootstrap_claude_crossplatform.sh` to automatically add cross-platform awareness to existing CLAUDE.md files across workspace
- **C010 CLAUDE.md Updated**: Added Platform Compatibility section demonstrating cross-platform best practices
- **Workspace Sync Support**: Addressed Syncthing-based workspace synchronization between macOS (bash/zsh) and Windows (PowerShell/Git Bash) environments
- Bootstrap script supports dry-run mode and creates receipts in `00_admin/RECEIPTS/`
- Protocol includes path conventions, command patterns, virtual environment handling, and shell detection guidance
- Updated README with cross-platform bootstrap instructions and protocol reference

## 2025-10-11
- **P002 → C002 Migration**: Promoted P002_sadb to C002_sadb as core infrastructure project - knowledge extraction system consumed by Mission Control, validators, and infrastructure projects
- **P160 → C004 Migration**: Promoted P160 (Open Web UI) to C004_open-web-ui as core infrastructure project
- **ADR 001 Created**: Documented modularity architecture decision and migration rationale in `notes/ADR/001-modularity-architecture.md`
- **C005 Proposed**: Proposed C005_mcp-tools as new core project for Model Context Protocol tooling
- **Repository Organization Updated**: Added comprehensive section on project promotion criteria and git submodule patterns
- **Division of Responsibilities**: Clarified governance (C010) vs operations (C001) responsibilities
- Updated PROJECT_MAP.md to reflect C002 and C004 migrations and C005 proposal
- Updated Quick Stats to reflect 7 active core projects + 1 proposed

## 2025-10-04
- **Phase 2 Complete**: Implemented all 5 Houston validators with full validation logic (exit 0/1 instead of stub 99)
- Implemented `check_houston_features.py`: JSON schema validation, phase consistency, safety controls, autonomous deployment permissions
- Implemented `check_houston_docmeta.py`: routing tag validation, taxonomy alignment, project tags, playbook requirements
- Implemented `check_houston_models.py`: deployment permission validation against trust phases
- Implemented `check_houston_tools.py`: phase alignment, dangerous operations gating, VPS endpoint validation
- Implemented `check_houston_telemetry.py`: freshness checks, required fields, latency thresholds, fallback loop detection
- All validators include verbose mode, JSON output options, and actionable remediation suggestions
- Renamed repository from P210_metadata-governance to C010_standards
- Added Ruff baseline config (`pyproject.toml`, policy templates, `scripts/bootstrap_ruff.sh`)
- Integrated C010_standards into C001_mission-control as git submodule at `external/standards`
- Added CI workflow (`.github/workflows/standards.yml`) in C001 for non-blocking validation
- Successfully bootstrapped Ruff config across ~20 workspace repositories

## 2025-09-21
- Added Houston chat/voice interface blueprint (`notes/HOUSTON_INTERFACE.md`) and referenced it across contributor guides/roadmap for future UI work.
- Scaffolded Houston validator harness (`validators/run_all.py`) and stub modules for DocMeta, features, tools, models, and telemetry checks.
- Documented Houston tooling architecture (`notes/HOUSTON_TOOLING.md`) and added staged tool configuration (`30_config/houston-tools.json`); expanded validator specs/roadmap accordingly.
- Authored validator specifications (`notes/VALIDATOR_SPECS.md`), introduced Houston feature config (`30_config/houston-features.json`) with schema guard (`schemas/houston_features.schema.json`), and cross-linked guidance in contributor docs.
- Added Houston retrieval playbook (`notes/AGENT_PLAYBOOK.md`) and linked guidance from contributor docs/roadmap for future validation tasks.
- Documented Houston inference routing (`notes/HOUSTON_INFERENCE.md`) and model bootstrap workflow (`notes/scripts/MODEL_BOOTSTRAP.md`); updated contributor guidance and roadmap validator tasks.
- Added canonical DocMeta v1.2 and CodeMeta v1.0 assets under `schemas/`, preserving original Markdown guidance alongside new YAML templates with source attribution.
- Consolidated taxonomies from `P002_sadb` into `taxonomies/` (content, emotion, topic, metadata classifications, universal terms, disambiguation rules, stoplist) with header notes pointing to upstream paths.
- Archived the unimplemented cross-corpus taxonomy expansion (`taxonomy_additions_cross_corpus.yaml`) for review; upstream fixtures in `30_taxonomy/` remain excluded pending validation.
- Captured workspace governance standards in `protocols/betty_protocol.md` and `protocols/universal_claude_standards.md`, documenting upstream versions/dates.
- Updated repository README and roadmap to record Phase 1 consolidation progress; schema consumer catalog remains a follow-up item.
