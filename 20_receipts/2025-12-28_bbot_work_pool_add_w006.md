# BBOT Work Pool: Add W006_Abandoned_Cart

**Date**: 2025-12-28
**Author**: Claude Code
**Status**: Complete

## Summary

Added W006_Abandoned_Cart to BBOT Work Pool v1 as the second work pool repo alongside W005_BigQuery.

## Changes

### C010_standards

1. **Registry** (`registry/repos.yaml`):
   - Added W006_Abandoned_Cart entry with `pool: work`
   - Fixed duplicate `story:` field from prior session (W005 content was accidentally appended)
   - Added full entry with story, contracts, interfaces, commands

2. **Validator Evidence** (`70_evidence/exports/Brain_on_Tap_Work_Pool.md`):
   - Updated report showing 2/2 repos ELIGIBLE

### W006_Abandoned_Cart

1. **README.md**: Added BOT:repo_card markers with 10 required headings
2. **DATA_SOURCES.md**: Created with BigQuery tables and sensitivity classifications
3. **.gitignore**: Updated with export hygiene patterns and evidence directory exceptions
4. **00_run/verify.command**: Created verify entry point
5. **Tracked exports removed**: 270 CSV/XLSX files removed from git index (local files preserved)

## Validation Results

```
============================================================
BRAIN ON TAP WORK POOL REPORT
============================================================

W005_BigQuery: PASS

W006_Abandoned_Cart: PASS

------------------------------------------------------------
Result: 2/2 repos ELIGIBLE for work pool
```

## Export Cleanup

W006 had 270 tracked export files outside evidence directories:
- `00_admin/master_docs/` - 1 XLSX
- `40_src/abandoned_cart_abtest/` - 25 CSVs
- `40_src/analysis/` - 5 CSVs
- `40_src/reports/` - 3 CSVs
- `50_data/raw/` - 180+ CSVs
- `70_evidence/` - 56 CSVs

All removed from git index with `git rm --cached`. Local files preserved.

## Commits

1. **W006_Abandoned_Cart**:
   - `8ab0816 feat: Add W006 to BBOT Work Pool v1`
   - Pushed to `main`

2. **C010_standards**:
   - `14285f5 feat(registry): Add W006_Abandoned_Cart to work pool`
   - Pushed to `main`

## Design Decisions

1. **Evidence directory exception**: Files in `20_receipts/` and `80_evidence_packages/` are exempt from export hygiene (same as W005)
2. **70_evidence/ not exempted**: Unlike 20_receipts, 70_evidence is for working data, not final evidence packages
3. **.gitignore strategy**: Added universal patterns at end with explicit exceptions for evidence directories

## Next Steps

- Consider adding more W-series repos to work pool as needed
- Run periodic validator audits to catch drift
