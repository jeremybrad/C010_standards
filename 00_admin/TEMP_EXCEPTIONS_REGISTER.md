# Temporary Exceptions Register

**Created:** 2026-01-01
**Last Updated:** 2026-01-01
**Review Cadence:** Quarterly
**Next Review:** 2026-03-31

## Purpose

This register tracks repos with **temporary exceptions** to the Betty Protocol folder structure. These repos have declared exceptions with explicit remediation gates and planned destinations.

Unlike permanent exceptions (e.g., C010_standards which defines the standards), temporary exceptions are meant to be reduced over time.

---

## Active Temporary Exceptions

### C002_sadb

**Status:** COMPLIANT (as of 2026-01-01)
**Previous:** Temporary Exception (space-containing directories)
**Resolution:** Archived legacy directories to `90_archive/`:
- `docs 2/` → `90_archive/docs_2/` (v1.2A orders/checklists)
- `docs 3/` → `90_archive/docs_3/` (v1.2B orders/checklists)
- `n8n and Sad Bees/` → `90_archive/n8n_and_sad_bees/` (roadmap)

**Exception File:** `00_admin/audit_exceptions.yaml` (still has 24 allowed dirs for legacy pipeline code)
**Note:** Remaining non-standard dirs (`pipeline/`, `library/`, `scripts/`, etc.) are tolerated via exception file due to import dependencies. These are flagged for future migration but are not blocking compliance.

---

### C003_sadb_canonical

**Status:** COMPLIANT (as of 2026-01-01)
**Previous:** Temporary Exception (3 violations)
**Resolution:** `Betty Audit Files/` renamed to `70_evidence/betty_audit_files`

The directory rename was completed with:
- All Python CLI scripts updated with new path
- Documentation references updated
- Exception file cleaned up

**Remaining non-standard dirs:** Still has `20_schemas`, `50_cli`, `60_mcp`, etc. but these are now handled by the exception file and don't cause audit failures.

---

### C019_docs-site

**Status:** COMPLIANT (as of 2026-01-01)
**Previous:** Temporary Exception (`tools/` at repo root)
**Resolution:** Moved `tools/` to `40_src/tools/`
- Single file: `generate_site.py` (Projects Directory generator)
- References updated in Makefile and docstrings
- Receipt: `20_receipts/receipt_tools_dir_migration_2026-01-01.md`

---

### U01_comfyUI

**Status:** Excluded (External Tool)
**Compliance:** 22 violations
**Exception File:** None (external tool, not maintained)
**Owner:** External (ComfyUI project)

**Justification:**
This is an external tool (ComfyUI) that is configured but not developed by this workspace. Its structure follows upstream conventions and should not be modified.

**Recommendation:** Mark as `excluded` in audit, skip from compliance checks.

---

## Permanent Exceptions

### C010_standards

**Status:** Permanent Exception (Standards Repository)
**Exception File:** `00_admin/audit_exceptions.yaml`
**Justification:** Defines the Betty Protocol folder structure. Its top-level dirs (`schemas/`, `taxonomies/`, `protocols/`, `validators/`) exist for discoverability and import compatibility.

---

## Script Enhancement (COMPLETED)

~~The audit script (`scripts/audit_folder_structure.sh`) had a parsing bug with directory names containing spaces.~~

**Fixed:** 2026-01-01 (commit `8cf9de8`)
- Replaced word-splitting enumeration (`ls` + unquoted var) with space-safe `find -print0` + bash array approach
- Directory names with spaces now correctly appear as single entries in CSV output
- Example: `"docs 3;docs 2;n8n and Sad Bees"` instead of `"2;3;n8n;and;Sad;Bees"`

---

## Remediation Priority

| Priority | Repo | Quick Win | Effort | Status |
|----------|------|-----------|--------|--------|
| 1 | C017_brain-on-tap | Add `venv` to exceptions | Low | ✅ DONE |
| 2 | C003_sadb_canonical | Rename `Betty Audit Files` | Low | ✅ DONE |
| 3 | C002_sadb | Archive `docs 2/3/n8n` | Low | ✅ DONE |
| 4 | Audit script | Fix space handling | Medium | ✅ DONE |
| 5 | C019_docs-site | Move `tools/` to `40_src/` | Low | ✅ DONE |
| 6 | C002_sadb | Migrate `tmp/` to gitignore | Low | Pending |
| 7 | C003_sadb_canonical | Merge `90_launchers` to `00_run` | Medium | Pending |
