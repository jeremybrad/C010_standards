# Houston Agent Playbook

## Purpose
Defines how Houston (Mission Control agent) retrieves, filters, and updates workspace memory while respecting metadata governance. Pair this with `notes/HOUSTON_INFERENCE.md` for inference routing specifics.

## Memory Tagging Convention
Every DocMeta/CodeMeta record destined for Houston must include:
- `doc.projects: ["Mission Control", "P210"]`
- `doc.topics`: include at least one of `monitoring`, `deployment`, `api-status`, `infra` for operational memories, or `coding-pattern`, `playbook` for technical lore.
- `routing.tags`: append `agent:houston` and `sensitivity:internal`.

Example DocMeta snippet:
```yaml
schema: "DocMeta.v1.2"
doc:
  projects: ["Mission Control", "P210"]
  topics: ["monitoring", "playbook"]
  routing:
    tags: ["source:mission-control", "agent:houston", "sensitivity:internal"]
```

## Retrieval Layers
1. **Recent Dialogue Window** – last five conversational turns stored via MCP memory.
2. **Agent-Scoped Knowledge Base** – query SADB where `projects` contains `Mission Control` and `routing.tags` contains `agent:houston`.
3. **Code Context (conditional)** – when `is_coding_related(query)` is true, pull CodeMeta docs with `doc.filetype: source` and `doc.routing.tags` that include `schema:codemeta`.
4. **System State Snapshots** – latest telemetry entries ingested from `70_evidence/mission-control/*.jsonl` with tag `state:live`.

Combine results using weighted recency + semantic score. Suggested weights: recent (0.3), knowledge base (0.4), code (0.2), system state (0.1).

### Pseudocode
```python
def smart_retrieve(query, agent="houston"):
    window = pull_recent_conversation(limit=5)
    knowledge = search_memories(query, tags={"agent": agent})
    code = search_codex(query) if is_coding_related(query) else []
    system = fetch_system_state(limit=3)
    return rank_results([
        (window, 0.3),
        (knowledge, 0.4),
        (code, 0.2),
        (system, 0.1)
    ])
```

## Feedback Loop
After successful remediation, write a DocMeta receipt with `routing.tags` including `agent:houston`, `playbook:success`, and link the relevant telemetry ID in `connections.related_docs`. This builds actionable troubleshooting patterns for future sessions.

## Access Controls
- Houston should ignore memories tagged `sensitivity:personal` or `domain:creative`.
- For escalations requiring personal context, delegate to the appropriate agent rather than re-tagging data.

## Validator Notes
Upcoming validators should confirm:
1. `30_config/houston-features.json` conforms to `schemas/houston_features.schema.json` and matches the current trust phase.
2. All Houston-tagged DocMeta entries include required routing tags/projects.
3. Retrieval templates reference existing taxonomy values (see `taxonomies/` for canonical spellings).
4. System-state records older than 30 days are archived (prevent stale data from dominating scores).
