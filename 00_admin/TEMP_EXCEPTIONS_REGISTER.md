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

**Status:** Temporary Exception
**Compliance:** 6 violations (directories with spaces cause parsing issues)
**Exception File:** `00_admin/audit_exceptions.yaml`
**Owner:** Jeremy (Al) Bradford
**Review Cadence:** Quarterly (next: 2026-03-31)

**Key Issues:**
- 30+ non-standard top-level directories
- Import dependencies between directories (HIGH RISK to move)
- Directories with spaces (`docs 2`, `docs 3`, `n8n and Sad Bees`) cause audit parsing issues

**Remediation Gates:**
| Directory | Destination | Blocker |
|-----------|-------------|---------|
| `pipeline/` | `40_src/pipeline` | 5+ sibling imports |
| `library/` | `40_src/library` | Heavily imported |
| `src/` | `40_src/` | Merge with existing |
| `docs/` | `10_docs/` | Merge with existing |

**Recommended Next Action:**
1. Fix audit script to handle spaces in directory names
2. Delete empty/redundant directories (`docs 2`, `docs 3` if duplicate)
3. Add `tmp/` and transient dirs to `.gitignore`

---

### C003_sadb_canonical

**Status:** Temporary Exception
**Compliance:** 3 violations (directory with spaces)
**Exception File:** `00_admin/audit_exceptions.yaml`
**Owner:** Jeremy (Al) Bradford
**Review Cadence:** Quarterly (next: 2026-03-31)

**Key Issues:**
- Non-standard numbered prefixes (20_schemas, 50_cli, 60_mcp, etc.)
- `Betty Audit Files/` directory with spaces causes parsing issues
- `pipelines/` has path-sensitive imports (HIGH RISK)

**Remediation Gates:**
| Directory | Destination | Blocker |
|-----------|-------------|---------|
| `pipelines/` | `40_src/pipelines` | Path-sensitive imports |
| `__pycache__/` | gitignored | Add to `.gitignore` |
| `env/` | gitignored | Add to `.gitignore` |
| `Betty Audit Files/` | `70_evidence/betty_audit` | Rename needed |

**Recommended Next Action:**
1. Rename `Betty Audit Files/` to `70_evidence/betty_audit`
2. Add `__pycache__/` and `env/` to `.gitignore`
3. Consolidate 90_launchers → 00_run

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

## Script Enhancement Needed

The audit script (`scripts/audit_folder_structure.sh`) has a parsing bug with directory names containing spaces:

**Issue:** `load_additional_allowed_dirs()` strips quotes but regex comparison fails for multi-word names.

**Example:**
- Exception declares: `"docs 2"`
- Parsed as: `docs 2` (no quotes)
- Regex match: `^(docs 2|...)$` fails due to spaces

**Fix Required:** Escape spaces in regex or use exact string matching.

---

## Remediation Priority

| Priority | Repo | Quick Win | Effort |
|----------|------|-----------|--------|
| 1 | C017_brain-on-tap | Add `venv` to exceptions | DONE |
| 2 | C003_sadb_canonical | Rename `Betty Audit Files` | Low |
| 3 | C002_sadb | Delete redundant `docs 2/3` | Low |
| 4 | Audit script | Fix space handling | Medium |
| 5 | C002_sadb | Migrate `tmp/` to gitignore | Low |
| 6 | C003_sadb_canonical | Merge `90_launchers` to `00_run` | Medium |
