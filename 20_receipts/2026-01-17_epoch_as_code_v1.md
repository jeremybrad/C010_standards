# Epoch-as-Code v1 Implementation Receipt

**Date**: 2026-01-17
**Session**: Claude Code Implementation
**Status**: Complete

## Summary

Implemented the Epoch-as-Code v1 standard - a machine-readable repo state snapshot format (`00_admin/EPOCH.yaml`) that tracks git HEAD, derived artifact checksums, and optional standards submodule state.

## Deliverables

### Protocol Document
- **File**: `protocols/ops/epoch_as_code_v1.md`
- **Schema ID**: `c010.epoch.v1`
- **Key features**:
  - Required fields: `epoch_schema`, `repo_id`, `repo_head`, `generated_at_utc`
  - Conditional primer block (required if PROJECT_PRIMER.md exists)
  - Optional standards submodule tracking
  - Unknown field handling (warn by default, error in strict mode)

### Validator
- **File**: `validators/check_epoch.py`
- **Exit codes**: 0 (pass), 1 (validation failure), 2 (parse error)
- **Modes**:
  - Default: Warn if EPOCH.yaml missing, exit 0
  - `--require`: Exit 1 if EPOCH.yaml missing
  - `--strict`: Implies --require, verifies repo_head matches current git HEAD
- **Features**:
  - Required field validation (schema, repo_id, git hash format, ISO 8601 timestamp)
  - Primer SHA256 sync verification
  - Git HEAD freshness check (strict mode)
  - Unknown field detection
  - JSON output for CI integration
  - Verbose mode

### Test Suite
- **File**: `tests/test_check_epoch.py`
- **Coverage**: 40+ test cases covering:
  - YAML loading and parsing
  - Required field validation
  - Git hash pattern validation
  - ISO 8601 timestamp validation
  - Primer synchronization
  - Strict mode behavior
  - Missing EPOCH.yaml behavior
  - CLI exit codes
  - JSON output

### Documentation Updates
- `validators/README.md`: Added epoch validator to table and portable validators list
- `README.md`: Added Epoch v1.0 to interfaces table, validator examples, and execution contexts

### Registration
- `validators/__init__.py`: Added `"epoch": "check_epoch"` to AVAILABLE_VALIDATORS

## Validation Rules

| Rule | Mode | Description |
|------|------|-------------|
| R1 | Required | `epoch_schema == "c010.epoch.v1"` |
| R2 | Required | `repo_id` non-empty string |
| R3 | Required | `repo_head` matches `^[a-f0-9]{7,40}$` |
| R4 | Required | `generated_at_utc` valid ISO 8601 |
| R5 | Conditional | If PROJECT_PRIMER.md exists, primer block required |
| R6 | Conditional | `primer.sha256` must match actual file content |
| R7 | Strict | `repo_head` must equal current git HEAD |
| R8 | Default | Unknown fields generate warnings |
| R9 | Strict | Unknown fields cause validation failure |
| R10 | Require/Strict | Missing EPOCH.yaml causes exit 1 |

## Files Created/Modified

| File | Action |
|------|--------|
| `protocols/ops/epoch_as_code_v1.md` | Created |
| `validators/check_epoch.py` | Created |
| `validators/__init__.py` | Modified (added registration) |
| `tests/test_check_epoch.py` | Created |
| `validators/README.md` | Modified (added to tables) |
| `README.md` | Modified (added to interfaces, validators, contexts) |
| `20_receipts/2026-01-17_epoch_as_code_v1.md` | Created (this file) |
| `10_docs/notes/CHANGELOG.md` | Modified (added entry) |

## Verification Commands

```bash
# Run new validator (should warn + exit 0 - no EPOCH.yaml yet)
python validators/check_epoch.py

# With --require (should exit 1 - no EPOCH.yaml)
python validators/check_epoch.py --require && echo "unexpected pass" || echo "expected fail"

# Run tests
pytest tests/test_check_epoch.py -v

# Run full suite to ensure no regressions
python validators/run_all.py --targets epoch repo_contract capsulemeta
```

## Notes

- Epoch validator is portable (works in any repo)
- Not included by default in run_all.py since EPOCH.yaml is optional
- Gradual adoption supported via warn-and-exit-0 default behavior
- Strict mode suitable for CI enforcement once repos adopt EPOCH.yaml
