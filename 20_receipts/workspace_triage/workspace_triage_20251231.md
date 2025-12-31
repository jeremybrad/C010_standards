# Workspace Triage Receipt

**Timestamp:** 20251231_094713
**Workspace:** /Users/jeremybradford/SyncedProjects
**Python version:** 3.14.2
**Script:** scripts/workspace_triage.py

## Git Status

| Field | Value |
|-------|-------|
| Branch | `fix/folder-structure-remediation-20251230` |
| Commit | `b3d6fb7` |
| Push | ✅ Pushed to `origin` |
| Remote | `https://github.com/jeremybrad/C010_standards.git` |

## Command

```bash
python3 scripts/workspace_triage.py /Users/jeremybradford/SyncedProjects
```

## Output Files

| File | Path | SHA256 |
|------|------|--------|
| CSV | `10_docs/notes/workspace_triage/workspace_triage_20251231.csv` | `eca9e3b3723c9da4...` |
| Receipt | `C010_standards/20_receipts/workspace_triage/workspace_triage_20251231.md` | (this file) |

## Summary

| Metric | Value |
|--------|-------|
| Repos scanned | 61 |
| Compliant | 10 |
| Safe autofix | 0 |
| Needs exception | 25 |
| Manual migration | 26 |

## By Series

| Series | Count |
|--------|-------|
| C (Core) | 17 |
| P (Projects) | 32 |
| W (Work) | 11 |
| U (Utility) | 1 |
| Other | 0 |

## Recommended Route Breakdown

| Route | Count | Description |
|-------|-------|-------------|
| compliant | 10 | Already compliant, no action needed |
| safe_autofix | 0 | Only missing files, can use --autofix-safe |
| needs_exception | 25 | Has Python imports or submodule refs, needs exception file |
| manual_migration | 26 | Invalid dirs need manual moves |

## Top 10 Repos by Non-Compliant Size

| Rank | Repo | Size (MB) | File Count | Route |
|------|------|-----------|------------|-------|
| - | (none with non-compliant content) | - | - | - |

## Repos Needing Exception (Detail)

### C001_mission-control
- **Reason:** Python repo with 2 sibling-dir import patterns
- **Invalid dirs:** 50_profiles;70_entities;backups;data;dist;docs;examples;external;logs;mcp-ops-agents;notes;scripts;tests;tools;workspace
- **Import risk hits:** 2
- **Examples:** `external/standards/validators/run_all.py:17:    sys.path.insert(0, str(REPO_R... | external/standard`

### C002_sadb
- **Reason:** Python repo with 5 sibling-dir import patterns
- **Invalid dirs:** all_in_one_v1_2;approvals;artifacts;assets;benchmarks;dashboard;data;docs;docs 2;docs 3;extractions;heartbeat;ingest;intake;library;logs;n8n and Sad Bees;pipeline;receipts;reports;reviews;sadb_orders_1_2C;scripts;src;test_data;tests;tmp
- **Import risk hits:** 5
- **Examples:** `pipeline/scripts/claude_extractor_v2.py:10:sys.path.insert(0, os.path.dirname... | pipeline/ai/triag`

### C003_sadb_canonical
- **Reason:** Python repo with 5 sibling-dir import patterns
- **Invalid dirs:** 20_schemas;50_cli;60_artifacts;60_mcp;70_entities;70_runs;90_launchers;90_tests;99_kst;Betty Audit Files;SADB_DATA;__pycache__;docs;env;pipelines;requirements;scripts;tests
- **Import risk hits:** 5
- **Examples:** `tests/test_policy_enforcement.py:27:sys.path.insert(0, str(Path(__file__).par... | kst_cli.py:34:sys`

### C004_star-extraction
- **Reason:** Python repo with 4 sibling-dir import patterns
- **Invalid dirs:** docs;examples;out;prompts;run;schema;scripts;src;tests
- **Import risk hits:** 4
- **Examples:** `src/test_framework.py:10:sys.path.insert(0, str(Path(__file__).parent)) | EXTRACT_NOW.py:9:sys.path.`

### C007_the_cavern_club
- **Reason:** Python repo with 5 sibling-dir import patterns
- **Invalid dirs:** SADB_DATA;agent_configs;agora;atlas;backups;custom;data;docs;fsapi;houston;logs;mcp;openapi-servers;openapi-specs;resolver;sadb-mem-writer;sadb-rag-api;streamdeck-voices;tests;tools
- **Import risk hits:** 5
- **Examples:** `betty_voice_server.py:25:    sys.path.insert(0, betty_path) | tests/test_voice_manager.py:11:sys.pat`

### C008_CBFS
- **Reason:** Python repo with 5 sibling-dir import patterns
- **Invalid dirs:** 40_review;40_tools;50_canonical;50_cli;50_exports;60_review;90_tests;data;docs;extraction;fact_review_batches;forensics;integration;metrics;schema;scripts;training;validation;verification
- **Import risk hits:** 5
- **Examples:** `90_tests/test_review_queue.py:16:sys.path.insert(0, str(Path(__file__).parent... | 90_tests/test_exp`

### C010_standards
- **Reason:** Python repo with 5 sibling-dir import patterns
- **Invalid dirs:** prompts;protocols;registry;schemas;scripts;taxonomies;tests;tools;validators;workspace
- **Import risk hits:** 5
- **Examples:** `tests/test_common.py:10:from validators.common import ( | tests/test_check_houston_tools.py:9:sys.pa`

### C017_brain-on-tap
- **Reason:** Python repo with 3 sibling-dir import patterns
- **Invalid dirs:** _disabled_apps;brain_on_tap;brain_on_tap.egg-info;build;dist;docs;legacy;out;site;tests
- **Import risk hits:** 3
- **Examples:** `brain_on_tap/memory_lab/adapter.py:204:        sys.path.insert(0, cli_path) | brain_on_tap/gui_app.p`

### C018_terminal-insights
- **Reason:** Python repo with 5 sibling-dir import patterns
- **Invalid dirs:** __pycache__;data;docs;logs;p181;reports;scripts
- **Import risk hits:** 5
- **Examples:** `test_turbo.py:11:sys.path.insert(0, str(Path(__file__).parent / "40_src")) | p181/rehydrator_adapter`

### C019_docs-site
- **Reason:** Python repo with 5 sibling-dir import patterns
- **Invalid dirs:** _audits;data;docs;evals;lora_adapters;rag;scripts;site;ui
- **Import risk hits:** 5
- **Examples:** `test_search_raw.py:5:sys.path.insert(0, str(Path(__file__).parent)) | test_rag.py:5:sys.path.insert(`

### C020_pavlok
- **Reason:** Python repo with 1 sibling-dir import patterns
- **Invalid dirs:** docs;scripts
- **Import risk hits:** 1
- **Examples:** `40_src/tests/conftest.py:10:sys.path.insert(0, str(Path(__file__).parent.pare...`

### P030_ai-services
- **Reason:** Python repo with 4 sibling-dir import patterns
- **Invalid dirs:** __pycache__;betty-venv;cognitive-venv
- **Import risk hits:** 4
- **Examples:** `memory-api-server.py:8:sys.path.append(os.path.expanduser('~/SyncedProjects/W... | memory-api-server`

### P050_ableton-mcp
- **Reason:** Python repo with 5 sibling-dir import patterns
- **Invalid dirs:** ableton_remote_scripts;config;docs;examples;receipts;scripts;src;tests
- **Import risk hits:** 5
- **Examples:** `examples/sample_management_demo.py:22:sys.path.insert(0, str(Path(__file__).p... | examples/automati`

### P052_n8n-mcp-setup
- **Reason:** Python repo with 1 sibling-dir import patterns
- **Invalid dirs:** caddy;n8n-data;n8n-mcp-setup;redis-data;workflows
- **Import risk hits:** 1
- **Examples:** `dewey-dual-scanner.py:221:    sys.path.append(os.path.dirname(os.path.abspath...`

### P090_relay
- **Reason:** Python repo with 5 sibling-dir import patterns
- **Invalid dirs:** __pycache__;agents;bookmarklets;broadcasted_messages;council_logs;extracted_wisdom;logs;messages;scraped_messages;scripts;ui_components
- **Import risk hits:** 5
- **Examples:** `debug_relay.py:14:sys.path.append('/Users/jeremybradford/SyncedProjects/relay... | start-roundtable-`

### P092_mirrorlab
- **Reason:** Python repo with 5 sibling-dir import patterns
- **Invalid dirs:** forensics;research
- **Import risk hits:** 5
- **Examples:** `40_src/test_few_conversations.py:8:sys.path.insert(0, str(Path(__file__).pare... | 40_src/debug_grok`

### P110_knowledge-synthesis-tool
- **Reason:** Python repo with 5 sibling-dir import patterns
- **Invalid dirs:** Active-Projects;Betty-Source-Tracker;Codify;For Claude;WOW-Lead-Attribution-Infrastructure;__pycache__;_seeds;agents;betty-memory-cathedral;config;context-templates;data;dewey-notes;docs;examples;frontend-templates;frontmatter_cleanups;kst_modules;memory-system;n8n-workflows;pc-setup-package;scripts;sources;templates;tests;utils
- **Import risk hits:** 5
- **Examples:** `tests/unit/test_modular.py:10:sys.path.insert(0, os.path.dirname(os.path.absp... | tests/qa/qa_test_`

### P151_clouddriveinventory
- **Reason:** Python repo with 5 sibling-dir import patterns
- **Invalid dirs:** __pycache__;api;asyncq;data;dataset;docs;migrations;repositories;scripts;tests;tools
- **Import risk hits:** 5
- **Examples:** `verify_phase8_hardening.py:22:sys.path.insert(0, str(Path(__file__).parent)) | test_phase8_smoke.py:`

### P159_memory-system
- **Reason:** Python repo with 1 sibling-dir import patterns
- **Invalid dirs:** __pycache__;configs;receipts;scripts
- **Import risk hits:** 1
- **Examples:** `test_rotate_claude_memory.py:16:sys.path.append('scripts')`

### P160_open-webui-ollama-setup
- **Reason:** Python repo with 2 sibling-dir import patterns
- **Invalid dirs:** SADB_DATA;agent_configs;agora;atlas;backups;custom;data;fsapi;houston;logs;openapi-servers;openapi-specs;resolver;sadb-mem-writer;sadb-rag-api;streamdeck-voices;tools
- **Import risk hits:** 2
- **Examples:** `betty_voice_server.py:25:    sys.path.insert(0, betty_path) | custom/betty_voice_integration.py:15: `

### P169_workflow-harvest
- **Reason:** Python repo with 1 sibling-dir import patterns
- **Invalid dirs:** docs;examples;open-webui-betty;src
- **Import risk hits:** 1
- **Examples:** `cli.py:15:sys.path.insert(0, str(Path(__file__).parent / "src"))`

### P171_elevenlabs-music-mcp
- **Reason:** Python repo with 1 sibling-dir import patterns
- **Invalid dirs:** config;examples;src;tests
- **Import risk hits:** 1
- **Examples:** `test_phase2_live.py:18:sys.path.insert(0, str(Path(__file__).parent / "src"))`

### P190_conversation-exports-web
- **Reason:** Python repo with 4 sibling-dir import patterns
- **Invalid dirs:** QA_REPORTS;Super Events Pack;TAGGING_PROMPTS;analysis;arcs;chroma_db;config;conversation_tags;conversation_tags_v2;data;docs;entity_registry;facts;facts_v2;logs;m1_emotional;m2_enriched;metadata;metadata_arcs;metadata_full;out_jude;prompts;qa_enriched;qa_tools;scripts;temp_m2;temp_m2_analyses;temp_m2_batch;temp_m2_results;training_data
- **Import risk hits:** 4
- **Examples:** `temp_m2_conv2.py:6:sys.path.insert(0, '/home/user/P190_conversation-exports-w... | scripts/d021_proc`

### P212_band-in-a-box-ai
- **Reason:** Python repo with 3 sibling-dir import patterns
- **Invalid dirs:** __pycache__;datasets;docs;experiments;models;outputs;scripts
- **Import risk hits:** 3
- **Examples:** `scripts/scan_biab_files.py:14:sys.path.append(str(Path(__file__).parent.parent)) | scripts/search_sa`

### U01_comfyUI
- **Reason:** Python repo with 5 sibling-dir import patterns
- **Invalid dirs:** __pycache__;alembic_db;api_server;app;comfy;comfy_api;comfy_api_nodes;comfy_config;comfy_execution;comfy_extras;custom_nodes;input;middleware;models;output;script_examples;temp;tests;tests-unit;user;utils;workflows
- **Import risk hits:** 5
- **Examples:** `nodes.py:22:sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(... | tests-unit/comfy_`


---
*Generated by workspace_triage.py at 20251231_094713*
