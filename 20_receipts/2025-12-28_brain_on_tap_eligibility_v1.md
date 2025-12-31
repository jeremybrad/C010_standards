# Receipt: Brain on Tap Repo Eligibility Standard v1

**Date**: 2025-12-28
**Session**: BBOT eligibility standard implementation

## Summary

Implemented the Brain on Tap (BBOT) repo eligibility standard v1 in C010_standards. This defines the requirements for a repository to be eligible for BBOT primer injection.

## Files Changed

| File | Action | Description |
|------|--------|-------------|
| `protocols/brain_on_tap_repo_eligibility_v1.md` | Created | Protocol spec with MUST/SHOULD requirements |
| `scripts/validate_brain_on_tap_eligibility.py` | Created | Validator script |
| `registry/repos.yaml` | Modified | Added `bot_active` and `path_rel` to all entries |

## Key Design Decisions

1. **MUST fields for eligibility**: `repo_id`, `name`, `bot_active`, `path_rel`
2. **README repo card required**: Reuses existing `validate_readme_repo_card.py` logic
3. **`bot_active` boolean semantics**: `true` = include in primers, `false` = exclude
4. **`path_rel` must be relative**: No absolute paths, no drive letters, no `~`

## How to Run the Validator

```bash
# Single repo
python scripts/validate_brain_on_tap_eligibility.py C010_standards

# Multiple repos with verbose output
python scripts/validate_brain_on_tap_eligibility.py C010_standards C017_brain-on-tap --verbose
```

## Example Output

```
============================================================
BRAIN ON TAP ELIGIBILITY REPORT
============================================================

C010_standards: PASS

C017_brain-on-tap: PASS

------------------------------------------------------------
Result: 2/2 repos ELIGIBLE
```

## Validation Results

Tested on C010_standards and C017_brain-on-tap - both pass eligibility.

## Exit Codes

- `0`: All repos pass
- `1`: Validation errors
- `2`: Configuration/file error

## Related

- `protocols/readme_repo_card.md` - README repo card standard
- `registry/schema.md` - Registry schema v1.2
