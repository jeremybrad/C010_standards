# Schema Consumers

Inventory of repositories currently using the canonical DocMeta and CodeMeta schemas. Each entry lists the version enforced and the code paths or prompts that depend on it.

## DocMeta v1.2
- `../C003_sadb_canonical` (formerly P002/C002)
  - `40_src/kv/kv_meta_load.py` — loads DocMeta YAML into Postgres, defaulting to `DocMeta.v1.2` when recording `schema_version`.
  - `40_src/kv/kv_meta_generate.py` — orchestrates LLM generation of DocMeta files and validates `schema` equals `DocMeta.v1.2`.
  - `40_src/kv/prompts/docmeta_v12.txt` — LLM prompt that embeds the schema definition verbatim.
  - `40_src/kv/debug_turbo.py` — Turbo debugging script hard-codes a DocMeta v1.2 stub for validation requests.
  - `40_src/kv/kv_terms_universal.py` & `build_universal_terms.sh` — reference DocMeta topics/keywords when syncing the universal term index.
  - `20_receipts/docmeta/*.docmeta.yaml` — generated metadata artifacts stamped with `schema: DocMeta.v1.2`.

## CodeMeta v1.0
- `../C003_sadb_canonical` (formerly P002/C002)
  - `40_src/kv/prompts/codemeta_v10.txt` — LLM prompt defining the CodeMeta v1.0 structure.
  - Operational receipts (`20_receipts/*`) describe current usage for code-library curation and reference the v1.0 specification.

## Observations & Next Actions
- No other repositories currently pin to DocMeta or CodeMeta schemas. Mission Control and Infrastructure references are aspirational pending adoption work.
- When additional consumers appear, update this inventory and capture their schema version requirements to manage migrations.
