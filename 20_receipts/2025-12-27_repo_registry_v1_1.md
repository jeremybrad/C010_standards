# Repo Registry v1.1 Receipt

**Date**: 2025-12-27
**Agent**: Claude Code (Opus 4.5)
**Task**: Strengthen registry schema and add validator

## Summary

Upgraded Repo Registry from v1.0 to v1.1:
- Fixed YAML parsing issue where `- CLI: value` was parsed as dict instead of string
- Added explicit schema guidance for `interfaces` field format
- Added validator script to catch type errors

## Changes

### registry/schema.md
- Version bumped to 1.1
- Added "Interface Format (Important)" section explaining string-only requirement
- Added correct/wrong examples for interfaces field

### registry/repos.yaml
- Fixed 7 interface entries that were parsing as dicts:
  - C017_brain-on-tap: 3 entries quoted
  - C002_sadb: 3 entries quoted
  - C001_mission-control: 3 entries quoted

### registry/validate_registry.py (NEW)
- Validates required fields exist
- Validates `status` is `active` or `deprecated`
- Validates all list fields contain strings (not dicts)
- Checks for duplicate repo_ids
- Exit codes: 0=valid, 1=errors, 2=file/parse error

## Issue Found and Fixed

YAML parses unquoted `- key: value` as a single-key dict:
```yaml
# Parsed as: {"CLI": "bbot render"}
- CLI: bbot render

# Parsed as string: "CLI: bbot render"
- "CLI: bbot render"
```

The validator caught 7 entries using the wrong format.

## Verification Output

```
$ python3 registry/validate_registry.py --verbose
Validated 5 entries: ['C010_standards', 'C017_brain-on-tap', 'C002_sadb', 'C001_mission-control', 'W-series']
✅ Registry valid: 5 entries
```

## Skipped

- Marker slices (`repo_cards.md`) - C017 already renders from YAML, no need to duplicate
