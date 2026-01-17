# Capsule Specification v1

**Version**: 1.0
**Status**: Active
**Effective Date**: 2026-01-17

## Purpose

Capsules are atomic, self-contained metadata artifacts designed for agent-to-agent handoffs, memory exports, activity logs, and other structured data exchange. Each capsule carries YAML frontmatter that enables discovery, provenance tracking, and lifecycle management.

This specification defines the structure, required fields, and validation rules for capsule documents conforming to `c010.capsule.v1`.

## Terminology

| Term | Definition |
|------|------------|
| **Capsule** | A document with YAML frontmatter conforming to this spec |
| **Producer** | The tool or agent that created the capsule |
| **Kind** | The category of capsule content (handoff, memory_export, activity, other) |
| **Provenance** | Optional chain-of-custody metadata for traceability |

## Document Structure

Capsules are markdown files with YAML frontmatter delimited by `---`:

```markdown
---
capsule_spec: "c010.capsule.v1"
capsule_id: "550e8400-e29b-41d4-a716-446655440000"
created_at: "2026-01-17T14:30:00Z"
kind: "handoff"
producer:
  tool: "claude-code"
  agent: "session-manager"
title: "Session handoff from task-123"
summary: "Context for continuing database migration work"
tags:
  - "migration"
  - "database"
---

# Session Handoff

[Markdown content follows...]
```

## Required Fields

| Field | Type | Description | Validation |
|-------|------|-------------|------------|
| `capsule_spec` | string | Specification version identifier | Must equal `"c010.capsule.v1"` |
| `capsule_id` | string | Unique identifier for this capsule | Non-empty string; UUID recommended |
| `created_at` | string | Creation timestamp | Valid ISO 8601 datetime (UTC recommended) |
| `kind` | enum | Capsule category | One of: `handoff`, `memory_export`, `activity`, `other` |
| `producer.tool` | string | Tool that created the capsule | Non-empty string |

## Optional Fields

| Field | Type | Description |
|-------|------|-------------|
| `producer.agent` | string | Specific agent or component within the tool |
| `title` | string | Human-readable title for the capsule |
| `summary` | string | Brief description of capsule contents |
| `tags` | list[string] | Freeform tags for categorization |
| `expires_at` | string | ISO 8601 datetime when capsule becomes stale |
| `related_capsules` | list[string] | IDs of related capsules |
| `provenance` | object | Chain-of-custody tracking (see below) |
| `custom` | object | Extension point for tool-specific metadata |

### Provenance Object

The optional `provenance` field tracks the capsule's origin and derivation:

| Subfield | Type | Description |
|----------|------|-------------|
| `provenance.source_session` | string | ID of originating session |
| `provenance.parent_capsule` | string | ID of capsule this was derived from |
| `provenance.workflow` | string | Name of workflow that generated this capsule |
| `provenance.version` | string | Version of the producing tool |

## Validation Rules

### Standard Mode (Default)

1. **Spec Check**: `capsule_spec` must exactly equal `"c010.capsule.v1"`
2. **Required Fields**: All required fields must be present and non-empty
3. **ISO 8601 Datetime**: `created_at` must be valid ISO 8601 format
4. **Kind Enum**: `kind` must be one of the allowed values
5. **Unknown Fields**: Unknown top-level fields generate **warnings** but do not cause validation failure

### Strict Mode (`--strict`)

All standard mode rules apply, plus:

6. **Unknown Fields**: Unknown top-level fields cause validation **failure** (exit 1)

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | All validations passed |
| 1 | Validation failure (missing required field, invalid value, unknown field in strict mode) |
| 2 | Parse/config error (invalid YAML, file not found, unreadable file) |

## Kind Values

| Value | Use Case |
|-------|----------|
| `handoff` | Session handoff between agents or sessions |
| `memory_export` | Exported context, memory, or learned information |
| `activity` | Activity log, audit trail, or event record |
| `other` | Catch-all for capsules that don't fit other categories |

## Versioning Policy

### What Constitutes a Breaking Change (v1 → v2)

- Adding a new **required** field
- Removing or renaming an existing required field
- Changing the type of a required field
- Changing allowed enum values in a breaking way (removing values)
- Changing the `capsule_spec` identifier format

### Non-Breaking Changes (patch versions)

- Adding new **optional** fields
- Adding new enum values to `kind`
- Relaxing validation rules
- Clarifying documentation

## Unknown Field Handling

Per the Betty Protocol's extensibility principle:

> "Ignore unknown fields unless explicitly disallowed"

By default, unknown top-level fields in capsule frontmatter are:
- **Logged as warnings** in verbose mode
- **Ignored** for validation purposes (exit 0)

In `--strict` mode, unknown fields cause validation failure (exit 1) to enforce schema compliance.

## Examples

See `10_docs/examples/capsules/` for working examples:

- `handoff_example.md` - Session handoff between agents
- `memory_export_example.md` - Context/memory export
- `activity_example.md` - Activity log with custom fields

## Schema Reference

The YAML schema template is located at: `schemas/capsulemeta_v1.0.yaml`

## Validator

Validate capsule documents using:

```bash
# Validate specific files
python validators/check_capsulemeta.py path/to/capsule.md

# Validate directory recursively
python validators/check_capsulemeta.py 10_docs/examples/capsules/ --verbose

# Strict mode (unknown fields cause failure)
python validators/check_capsulemeta.py --strict path/to/capsule.md

# JSON output for CI
python validators/check_capsulemeta.py --json-output results.json path/to/capsule.md
```

## Integration Points

### Consumers

- **Mission Control**: Ingests handoff capsules for session continuity
- **Memory systems**: Exports and imports context via memory_export capsules
- **Audit systems**: Processes activity capsules for compliance tracking

### Producers

- **Claude Code**: Generates handoff capsules on session end
- **Agent orchestrators**: Create activity logs as capsules
- **Export utilities**: Package context as memory_export capsules

## Related Documents

- [DocMeta Schema v1.2](../../schemas/docmeta_v1.2.yaml) - Document metadata standard
- [Betty Protocol](../betty_protocol.md) - Workspace governance standards
