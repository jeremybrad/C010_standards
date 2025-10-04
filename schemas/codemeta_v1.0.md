# CodeMeta Schema v1.0 (Canonical Copy)

_Source: `/Users/jeremybradford/SyncedProjects/P002_sadb/10_docs/CodeMeta_Schema_v1.0.md` • Retrieved for consolidation into P210 metadata governance repo._

Purpose: capture retrieval-ready metadata for source files so we can search by intent, understand purpose, and curate a gold-standard code library later. Output is YAML stored as a sidecar and loaded into `doc_meta` (with `schema_version: CodeMeta.v1.0` and `doc.type: code`).

## YAML shape

```yaml
schema: "CodeMeta.v1.0"
doc:
  sha256: "<sha256_bytes>"
  path: "<absolute or repo-relative path>"
  repo: "<top-level project or repo name>"
  language: "<python|javascript|typescript|go|rust|java|kotlin|ruby|php|c|cpp|csharp|swift|bash|sql|r|julia|lua|other>"
  runtime: "<e.g., python 3.11, node 20, go 1.22>"        # optional
  framework: "<e.g., fastapi, flask, react, nextjs>"       # optional
  filetype: "<source|config|schema|script|test|notebook>"
  sloc: <int>                                              # lines of code (approx)
  summary: |
    <2–5 sentences: what this file/module does and why it exists>
  entrypoints:
    - "<function or CLI command users call>"
  functions:
    - name: "<fn name>"
      summary: "<what it does in one line>"
      params: ["<name:type=default>", "..."]               # optional
      returns: "<type or description>"                      # optional
  classes:
    - name: "<class name>"
      summary: "<role>"
      methods: ["<method name>", "..."]                    # optional
  cli:
    commands:
      - name: "<command>"
        usage: "<example invocation>"
        summary: "<what the command achieves>"
  dependencies:
    imports: ["<pkg or module>", "..."]
    external_services: ["<api/db/queue>", "..."]           # optional
    config_files: ["<path>", "..."]                         # optional
  tests:
    present: <true|false>
    hints: ["<files or patterns detected>", "..."]
  examples:
    - "<very short example of usage>"                       # optional
  quality:
    lints: ["<ruff|eslint|pylint>", "..."]                 # optional
    complexity_hint: "<low|medium|high>"                    # optional
    smells: ["<duplicate logic|tight coupling|no tests>", "..."]  # optional
  security:
    secrets_suspected: <true|false>
    notes: ["<BEGIN PRIVATE KEY detected>", "..."]         # optional
    license: "<MIT|Apache-2.0|Proprietary|Unknown>"
  provenance:
    conversations: ["<conv_id:message_id>", "..."]         # optional
    commit: "<short sha or unknown>"                        # optional
  relationships:
    related_docs: ["<sha256 or path>", "..."]              # optional
    projects: ["<SADB|CloudMD|ParallelLLMs|...>"]
    topics: ["<tags helpful for search>", "..."]
    keywords: ["<free-text search terms>", "..."]
  routing:
    canonical: <true|false>
    live: <true|false>
    tags: ["source:code", "priority:normal"]
  notes: |
    <optional curatorial notes for future you>
```

## Rules
- Prefer facts from code over guesses. If uncertain, omit the field.
- Summaries should be short, specific, and retrieval-friendly.
- Do not include full code. Do not echo secrets. If a secret pattern is detected, set `security.secrets_suspected: true` and describe only at a high level.
- Keep `doc.type: code`. `schema: CodeMeta.v1.0`.
