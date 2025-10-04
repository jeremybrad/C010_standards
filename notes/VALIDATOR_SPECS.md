# Validator Specifications

Blueprint for Phase 2 tooling that keeps Houston’s metadata, inference config, and telemetry aligned. Each section defines required inputs, validation steps, and failure handling.

## 1. DocMeta Tag Validator (`validators/check_houston_docmeta.py`)
**Goal:** Ensure Houston-targeted documents follow tagging conventions so retrieval filters remain precise.

- **Scope:** Files in `schemas/`, `notes/`, or imported SADB YAML with `routing.tags` containing `agent:houston` or `source:mission-control`.
- **Checks:**
  1. `doc.projects` includes both `Mission Control` and `P210`.
  2. `routing.tags` contains `agent:houston` and `sensitivity:internal`.
  3. `doc.topics` values exist in `taxonomies/topic_taxonomy.yaml` (`monitoring`, `deployment`, `infra`, etc.).
  4. `connections.related_docs` present when `routing.tags` contains `playbook:success`.
- **Output:** JSON summary (pass/fail per file) plus optional fix hints (`--fix` flag can append missing tags). Log results to `70_evidence/validator_docmeta.json`.

## 2. Model Inventory Validator (`validators/check_houston_models.py`)
**Goal:** Confirm `30_config/houston.json` + `houston-features.json` reference models that are installed and match fallback chains.

- **Inputs:**
  - `30_config/houston.json` (host endpoints, model list).
  - `~/models/config/houston-models.json` (use-case priorities).
  - Optional cache from `ollama list` (passed via `--models-file`).
- **Checks:**
  1. Primary cloud model `qwen-coder:480b` present in both configs.
  2. Each fallback chain contains at least one local tag (`qwen2.5-coder:32b-q4_K_M`, `qwen2.5-coder:14b-q4_K_M`, etc.).
  3. No unrecognized model names (cross-check with canonical taxonomy `taxonomies/universal_terms.yaml` for synonyms).
  4. `houston-features.json.features.agency_levels.autonomous.can_deploy_updates` is `true` only if `gradual_trust_building.current_phase >= 3`.
- **Output:** Markdown/JSON report plus exit code >0 on mismatch.

## 3. Telemetry Freshness Validator (`validators/check_houston_telemetry.py`)
**Goal:** Ensure health monitoring data feeding Houston is current.

- **Scope:** Files under `70_evidence/houston_telemetry.jsonl` (and mission-control telemetry directory).
- **Checks:**
  1. Most recent entry timestamp within 5 minutes of current time (configurable `--max-age`).
  2. Required fields present: `host`, `model`, `latency_ms`, `fallback_chain`, `manual_override`.
  3. Latency thresholds: warn if `latency_ms > 10000` (10s) and escalate if average exceeds `5000` over last 20 entries.
  4. Fallback loops flagged when chain length > 3.
- **Output:** stdout summary + JSON artifact `70_evidence/validator_telemetry.json`. Include `--watch` mode for CI to poll.

## 4. Feature Toggle Validator (`validators/check_houston_features.py`)
**Goal:** Ensure `30_config/houston-features.json` meets schema and phase requirements.

- **Checks:**
  1. Validate against JSON schema (to be stored in `schemas/houston_features.schema.json`).
  2. `features.ide_integration.supported_editors` subset of allowed values (`cursor`, `vscode`, `jetbrains`).
  3. If `agency_levels.current_level` is `autonomous`, assert `safety_controls.destructive_actions.require_password` is true.
  4. `gradual_trust_building.current_phase` ≤ length of `phases`; when `auto_advance` is false, require manual receipt entry in `notes/CHANGELOG.md` (pattern `Phase <n> activated`).
- **Output:** Structured diff for invalid settings plus suggestion of remediation steps.

## 5. Tool Pipeline Validator (`validators/check_houston_tools.py`)
**Goal:** Verify `30_config/houston-tools.json` aligns pipelines, capability flags, and phase gating with documented expectations.

- **Checks:**
  1. Ensure every pipeline step maps to a known tool capability (cross-check against `notes/HOUSTON_TOOLING.md`).
  2. Confirm `phase_settings.current_phase` is ≤ `gradual_trust_building.current_phase` from `houston-features.json` (if available via flag `--features-config`).
  3. Validate `tool_access.local_tools.phase_overrides` includes entries for phases declared in `phase_settings.phases` and excludes phase 3 operations (e.g., `kill_processes`, `system_shutdown`).
  4. Warn if `vps_tools.enabled` is true while `endpoint` is placeholder (`example.com`).
- **Output:** JSON diagnostics plus CLI warnings guiding next steps (e.g., “Enable VPS tools after remote MCP is provisioned”).

## Execution Harness
- Provide `validators/run_all.py` to orchestrate these checks with a shared CLI (e.g., `python validators/run_all.py --targets docmeta models`).
- Integrate into roadmap Phase 2; initial placeholder scripts can raise `NotImplementedError` but enforce contract & tests.
