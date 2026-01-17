# Capsule Examples

This directory contains example capsule documents conforming to the `c010.capsule.v1` specification.

## Files

| File | Kind | Description |
|------|------|-------------|
| `handoff_example.md` | handoff | Session handoff between agents |
| `memory_export_example.md` | memory_export | Context/memory export |
| `activity_example.md` | activity | Activity log with custom fields |

## Validation

Validate all examples using:

```bash
python validators/check_capsulemeta.py 10_docs/examples/capsules/ --verbose
```

## Specification

See [Capsule Specification v1](../../../protocols/capsules/capsule_spec_v1.md) for complete documentation.

## Schema

The YAML template is at: `schemas/capsulemeta_v1.0.yaml`
