# C010 Standards Schema Reference

**Last Updated**: 2026-01-24
**Version**: 1.0.0

Schema definitions for workspace-wide metadata standards.

## Quick Reference

| Schema | Version | Purpose |
|--------|---------|---------|
| DocMeta | v1.2 | Document metadata with routing and governance |
| CodeMeta | v1.0 | Code artifact metadata (repos, scripts, libraries) |
| CapsuleMeta | v1.0 | Atomic, self-contained artifact metadata |
| Houston Features | JSON Schema | Feature toggles and trust phases |

## Schema Directory

All schemas are located in `schemas/`:

```
schemas/
├── docmeta_v1.2.yaml           # Document metadata schema
├── docmeta_v1.2.md             # DocMeta reference documentation
├── codemeta_v1.0.yaml          # Code artifact metadata schema
├── codemeta_v1.0.md            # CodeMeta reference documentation
├── capsulemeta_v1.0.yaml       # Capsule metadata schema
└── houston_features.schema.json # Houston feature config JSON schema
```

## DocMeta v1.2

Document metadata schema for routing, governance, and entity tracking.

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `doc.id` | string | Unique document identifier |
| `doc.title` | string | Document title |
| `doc.projects` | list | Associated project IDs |
| `doc.topics` | list | Topics from `taxonomies/topic_taxonomy.yaml` |

### Houston Routing

Documents targeting Houston agent retrieval must include:

```yaml
doc:
  projects:
    - "Mission Control"
    - "P210"
  topics:
    - "monitoring"
routing:
  tags:
    - "agent:houston"
    - "sensitivity:internal"
connections:
  related_docs:
    - "<sha256 or path>"
```

### Validation

```bash
python validators/check_houston_docmeta.py --verbose
```

## CodeMeta v1.0

Metadata schema for code artifacts (repositories, scripts, libraries).

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `code.repo` | string | Repository URL |
| `code.language` | string | Primary programming language |

### Example

```yaml
code:
  repo: "https://github.com/..."
  language: "python"
  dependencies:
    - name: "pyyaml"
      version: "6.0"
```

## CapsuleMeta v1.0

Metadata schema for atomic, self-contained artifacts (handoffs, exports, activities).

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `capsule_spec` | string | Must be `c010.capsule.v1` |
| `capsule_id` | string | Unique capsule identifier |
| `created_at` | datetime | ISO 8601 creation timestamp |
| `kind` | string | Capsule type (handoff, memory_export, activity, etc.) |
| `producer.tool` | string | Tool that generated the capsule |

### Optional Fields

| Field | Type | Description |
|-------|------|-------------|
| `title` | string | Human-readable title |
| `summary` | string | Brief description |
| `tags` | list | Classification tags |
| `provenance` | object | Source tracking |
| `expires_at` | datetime | Expiration timestamp |
| `related_capsules` | list | Related capsule IDs |
| `custom` | object | Extension fields |

### Validation

```bash
python validators/check_capsulemeta.py --verbose
python validators/check_capsulemeta.py --strict  # Reject unknown fields
```

## Houston Features Schema

JSON Schema for Houston agent feature configuration.

### Location

`schemas/houston_features.schema.json`

### Key Sections

| Section | Purpose |
|---------|---------|
| `agency_levels` | Current agency level (supervisory, advisory, autonomous) |
| `gradual_trust_building` | Trust phases and advancement criteria |
| `safety_controls` | Destructive action guards |
| `monitoring` | Telemetry and health check settings |

### Trust Building Phases

| Phase | Agency Level | Description |
|-------|--------------|-------------|
| 1 | Observation | `supervisory` - Basic monitoring only |
| 2 | Collaboration | `advisory` - IDE integration, proactive alerts |
| 3 | Partnership | `autonomous` - Full agency with emergency protocols |

### Validation

```bash
python validators/check_houston_features.py --schema schemas/houston_features.schema.json
```

## Schema Consumers

Projects consuming these schemas:

| Project | Schemas Used | Integration |
|---------|--------------|-------------|
| C001_mission-control | All | Git submodule at `external/standards` |
| C002_sadb | DocMeta, CodeMeta | Taxonomy lookups |
| P001_bettymirror | DocMeta | Protocol enforcement |

See `notes/SCHEMA_CONSUMERS.md` for complete inventory.

## Taxonomy Integration

Schemas reference controlled vocabularies in `taxonomies/`:

| Taxonomy | Schema Field |
|----------|--------------|
| `topic_taxonomy.yaml` | `doc.topics` |
| `content_taxonomy.yaml` | Document types |
| `universal_terms.yaml` | Canonical terminology |

## Related Documentation

- [ARCHITECTURE.md](ARCHITECTURE.md) - System design
- [CLI.md](CLI.md) - Validator commands
- [OPERATIONS.md](OPERATIONS.md) - Day-to-day workflows
