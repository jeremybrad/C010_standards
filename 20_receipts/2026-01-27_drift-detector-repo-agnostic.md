# Receipt: Drift Detector Repo-Agnostic + /repo-health Skill

**Date**: 2026-01-27
**Scope**: `scripts/drift/`, `scripts/repo_drift_detector.py`, `skills/repo-health/`

## Changes

### RepoProfile auto-detection (`scripts/drift/models.py`)

Added `RepoProfile` dataclass that auto-detects repo capabilities:

| Flag | Detection logic |
|------|----------------|
| `has_validators` | `validators/` with `__init__.py` |
| `has_schemas` | `schemas/` directory exists |
| `has_taxonomies` | `taxonomies/` directory exists |
| `has_meta_yaml` | `META.yaml` at root |
| `has_project_primer` | `PROJECT_PRIMER.md` at root |
| `has_drift_rules` | `30_config/drift_rules.yaml` exists |

### Universal defaults + rules resolution (`scripts/drift/defaults.py`, new)

- `universal_rules()`: Minimal rules for any Betty Protocol repo (canonical scope = README/CLAUDE/META/CHANGELOG/PRIMER, standard excludes, no validator/schema expectations)
- `resolve_rules()`: Precedence chain: `--rules` CLI flag > repo's `30_config/drift_rules.yaml` > universal defaults
- Logs which file was loaded and which top-level keys were consumed
- Warns on unknown fields (doesn't fail)

### Gated checks

| Check | Gated on |
|-------|----------|
| L1 `_check_validator_inventory` | `profile.has_validators` |
| L1 `_check_schema_inventory` (schemas) | `profile.has_schemas` |
| L1 `_check_schema_inventory` (taxonomies) | `profile.has_taxonomies` |
| L2 `_check_validator_consistency` | `profile.has_validators` |
| L2 `_check_generator_drift` (validator comparison) | `profile.has_validators` |
| L3 `_find_misplaced_artifacts` (validators/) | `profile.has_validators` |

### Entry point changes (`scripts/repo_drift_detector.py`)

- Auto-detects `RepoProfile` before running checks
- Uses `resolve_rules()` instead of local `load_rules()` / `_default_rules()`
- Console-only output when target repo has no `70_evidence/` directory
- Passes `profile` to all level functions
- Gates inventory extraction on `profile.has_validators`

### /repo-health skill (`skills/repo-health/SKILL.md`, new)

Thin wrapper documenting invocation, output, exit codes, and profiling behavior. Symlinked to `~/.claude/skills/repo-health`.

## Acceptance test results

### C010_standards (Level 2)
- CRITICAL: 0, MAJOR: 0, MINOR: 14, INFO: 31
- Same or better than pre-change baseline

### C017_brain-on-tap (Level 2)
- CRITICAL: 0, MAJOR: 1 (stale primer SHA - legitimate), MINOR: 12, INFO: 0
- No validator/schema/taxonomy false positives
- Correctly loaded repo's own `30_config/drift_rules.yaml`

### C001_mission-control (Level 2)
- CRITICAL: 8 (broken links - legitimate), MAJOR: 1 (stale primer), MINOR: 10, INFO: 0
- No validator/schema/taxonomy false positives
- Correctly detected `has_validators=False`

## Files changed

| File | Action |
|------|--------|
| `scripts/drift/models.py` | Added `RepoProfile` dataclass |
| `scripts/drift/defaults.py` | **New** - universal rules + resolution |
| `scripts/drift/level1.py` | Gated 2 checks on profile |
| `scripts/drift/level2.py` | Gated 2 checks on profile |
| `scripts/drift/level3.py` | Gated 1 check on profile |
| `scripts/repo_drift_detector.py` | Profile detection, rules resolution, console-only output |
| `scripts/drift/__init__.py` | Exported `RepoProfile`, `resolve_rules`, `universal_rules` |
| `skills/repo-health/SKILL.md` | **New** - thin skill wrapper |
