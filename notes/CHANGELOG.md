# Metadata Governance Changelog

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
