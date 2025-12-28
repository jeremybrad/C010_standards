# BBOT Work Pool v1 Implementation

**Date**: 2025-12-28
**Author**: Claude Code
**Status**: Complete (with known findings)

## Summary

Implemented BBOT Work Pool v1 as an opt-in pool system extending existing BBOT eligibility. Work pool repos have stricter requirements for business analytics and stakeholder-facing deliverables.

## Changes

### C010_standards (this repo)

1. **Protocol**: Created `protocols/brain_on_tap_work_pool_v1.md`
   - Defines pool system (personal/work/archive)
   - Work pool requirements: README repo card, DATA_SOURCES.md, receipts, evidence packages, verify entry point, export hygiene
   - Pool isolation guidelines

2. **Registry**: Extended `registry/repos.yaml`
   - Added `pool` field (optional, defaults to `personal`)
   - Added W005_BigQuery entry with `pool: work`

3. **Validator**: Created `scripts/validate_brain_on_tap_work_pool.py`
   - Validates work pool repos against all requirements
   - Writes reports to `70_evidence/exports/`
   - Exit codes: 0=pass, 1=fail, 2=config error

### W005_BigQuery

1. **README**: Added repo card block with required sections
2. **DATA_SOURCES.md**: Created with sensitivity classifications
3. **80_evidence_packages/**: Created directory with .gitkeep
4. **.gitignore**: Added export hygiene patterns
5. **00_run/verify.command**: Created verify entry point

## Validation Results

```
W005_BigQuery: FAIL (1 errors)
  ERROR: Tracked export files: 40_src/ingestion/connects/...
```

**Finding**: W005_BigQuery has pre-existing tracked CSV files in `40_src/ingestion/`. These need to be removed from git tracking to fully comply with work pool requirements.

**Remediation needed in W005_BigQuery**:
```bash
git rm --cached 40_src/ingestion/connects/*.csv
git rm --cached 40_src/ingestion/sms/dropbox/*.csv
git commit -m "chore: remove tracked CSV exports for work pool compliance"
```

## Design Decisions

1. **Opt-in by default**: Existing BBOT behavior unchanged. Pool field defaults to `personal`.
2. **Evidence directory exception**: Files in `20_receipts/` and `80_evidence_packages/` excluded from export hygiene check since they serve as evidence.
3. **Verify entry point flexibility**: Supports `make verify`, `00_run/verify.*`, or `scripts/verify_claims.py`.

## Files Changed

```
C010_standards:
  protocols/brain_on_tap_work_pool_v1.md  (created)
  registry/repos.yaml                      (modified)
  scripts/validate_brain_on_tap_work_pool.py (created)
  20_receipts/2025-12-28_bbot_work_pool_v1.md (this receipt)

W005_BigQuery:
  README.md                                (modified)
  DATA_SOURCES.md                          (created)
  .gitignore                               (modified)
  00_run/verify.command                    (created)
  80_evidence_packages/.gitkeep            (created)
```

## Next Steps

1. Clean up tracked CSV files in W005_BigQuery
2. Re-run validator to confirm PASS
3. Consider adding more W-series repos to work pool as needed
