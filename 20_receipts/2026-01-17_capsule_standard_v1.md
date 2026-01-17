# Receipt: Capsule Standard v1 Implementation

**Date**: 2026-01-17
**Author**: Claude Code
**Type**: Feature Implementation

## Summary

Implemented the C010 Capsule Standard v1 (`c010.capsule.v1`), a new workspace-wide metadata standard for atomic, self-contained artifacts such as session handoffs, memory exports, and activity logs.

## Files Created (9)

| File | Purpose |
|------|---------|
| `protocols/capsules/capsule_spec_v1.md` | Protocol specification document |
| `schemas/capsulemeta_v1.0.yaml` | YAML schema template |
| `validators/check_capsulemeta.py` | Validator implementation |
| `10_docs/examples/capsules/README.md` | Examples documentation |
| `10_docs/examples/capsules/handoff_example.md` | Handoff capsule example |
| `10_docs/examples/capsules/memory_export_example.md` | Memory export example |
| `10_docs/examples/capsules/activity_example.md` | Activity log example |
| `tests/test_check_capsulemeta.py` | Comprehensive test suite |
| `20_receipts/2026-01-17_capsule_standard_v1.md` | This receipt |

## Files Modified (3)

| File | Change |
|------|--------|
| `validators/__init__.py` | Added `capsulemeta` to `AVAILABLE_VALIDATORS` |
| `CLAUDE.md` | Added `capsulemeta` to Available Validators list |
| `10_docs/notes/CHANGELOG.md` | Added 2026-01-17 entry |

## Specification

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `capsule_spec` | string | Must equal `"c010.capsule.v1"` |
| `capsule_id` | string | UUID or stable identifier |
| `created_at` | string | ISO 8601 UTC datetime |
| `kind` | enum | `handoff`, `memory_export`, `activity`, `other` |
| `producer.tool` | string | Tool that produced the capsule |

### Optional Fields

`producer.agent`, `title`, `summary`, `tags`, `expires_at`, `related_capsules`, `provenance`, `custom`

### Exit Codes

- **0**: All validations passed
- **1**: Validation failure (missing required field, invalid value, unknown field in strict mode)
- **2**: Parse/config error (invalid YAML, file not found)

## Verification Commands

```bash
# 1. Validate examples pass
python validators/check_capsulemeta.py 10_docs/examples/capsules/ --verbose
# Expected: exit 0

# 2. Run pytest
pytest tests/test_check_capsulemeta.py -v
# Expected: all pass

# 3. Run full validator suite
python validators/run_all.py
# Expected: exit 0 (all validators pass)

# 4. Test strict mode
python validators/check_capsulemeta.py 10_docs/examples/capsules/ --strict --verbose
# Expected: exit 0 (examples have no unknown fields)
```

## Consumer Guidance

### For Producers

When creating capsules, include YAML frontmatter with all required fields:

```yaml
---
capsule_spec: "c010.capsule.v1"
capsule_id: "your-unique-id"
created_at: "2026-01-17T14:30:00Z"
kind: "handoff"
producer:
  tool: "your-tool-name"
---

# Your content here
```

### For Validators in CI

```bash
# Validate capsules in a directory
python validators/check_capsulemeta.py path/to/capsules/

# Strict mode for schema enforcement
python validators/check_capsulemeta.py --strict path/to/capsules/

# JSON output for CI integration
python validators/check_capsulemeta.py --json-output results.json path/to/capsules/
```

### For Consumers

Parse the YAML frontmatter and check `capsule_spec == "c010.capsule.v1"` to identify capsule documents. Use `kind` to route to appropriate handlers.

## Related Documents

- [Capsule Specification v1](../protocols/capsules/capsule_spec_v1.md)
- [Schema Template](../schemas/capsulemeta_v1.0.yaml)
- [Changelog](../10_docs/notes/CHANGELOG.md)
