# Repository Guidelines

## Project Structure & Module Organization
- `schemas/`: Canonical DocMeta and CodeMeta definitions (`*.yaml` templates plus original markdown references). Add new schema versions as `name_vX.Y.yaml` and mirror upstream documentation beside them.
- `taxonomies/`: Consolidated content, emotion, topic, and universal-term taxonomies; each file starts with source attribution comments.
- `protocols/`: Authoritative governance docs such as `betty_protocol.md` and `universal_claude_standards.md`.
- `notes/`: Roadmap, changelog, schema consumer inventory, and future ADRs. Update `notes/CHANGELOG.md` whenever you touch canonical assets.

## Build, Test, and Development Commands
No build tooling ships with this repo yet. When drafting validators, stage CLIs under `validators/` and document their usage here (e.g., ``python validators/docmeta_check.py path/to/file``).

## Coding Style & Naming Conventions
- Store versioned specs as lowercase filenames using underscores (e.g., `docmeta_v1.2.yaml`).
- Keep comments at the top of YAML files noting original source paths and dates.
- Markdown documents should open with a level-1 heading and track provenance in an italicized block.
- Maintain ASCII unless upstream text requires Unicode (e.g., typographic quotes in sourced material).

## Testing Guidelines
There are no automated tests yet. When validators are introduced, colocate unit tests under `validators/tests/` and document invocation commands in this guide and `README.md`. Include sample metadata fixtures under `validators/fixtures/` for reproducibility.

## Commit & Pull Request Guidelines
- Follow conventional summaries such as `docs: sync docmeta schema` or `taxonomies: import emotion updates` observed across workspace repos.
- Reference affected files and upstream sources in the commit body; include bullet lists for multiple changes.
- Pull requests should: describe the consolidation performed, link to original artifact paths, note any deviations or unresolved diffs, and update `notes/CHANGELOG.md`. Attach diff snippets or receipts when migrating large specs.


## Agent Operations
- Houston-specific routing rules live in `notes/HOUSTON_INFERENCE.md`; review before changing `30_config/houston.json`.
- Retrieval workflow, tagging requirements, and feedback loops are in `notes/AGENT_PLAYBOOK.md`. Keep DocMeta tags aligned before adding memories.
- Feature toggles live in `30_config/houston-features.json`; validate changes against `schemas/houston_features.schema.json` before enabling new agency levels.
- Tool pipelines/configuration live in `notes/HOUSTON_TOOLING.md` and `30_config/houston-tools.json`. Keep `phase_settings.current_phase` aligned with `gradual_trust_building.current_phase`.
- Interface plan lives in `notes/HOUSTON_INTERFACE.md`; coordinate UI hotkeys with `houston-features.json` changes.
- Model bootstrap scripts sit in `notes/scripts/MODEL_BOOTSTRAP.md`. Follow the host priority order (cloud → RTX → Mac) and log receipts for each pull.
- Keep `houston-models.json` tags exact (e.g., `qwen2.5-coder:32b-q4_K_M`). Upcoming validators will flag mismatches.

## Security & Configuration Tips
- Do not place raw data dumps or secrets in this repository; store large artifacts in `$SADB_DATA_DIR` per Betty Protocol.
- When copying documents from other repos, scrub tokens and ensure routing/governance fields remain accurate for downstream consumers.
