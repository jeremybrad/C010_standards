# Folder Structure Remediation Analysis

**Date:** 2025-12-30
**Branch:** `fix/folder-structure-remediation-20251230`
**Status:** ANALYSIS COMPLETE - AWAITING DECISION

## Executive Summary

C010_standards has **16 non-compliant top-level directories**. However, C010 is a special case:
- It's the repo that **defines** the folder structure standard
- Its `validators/` directory is a Python package with internal imports
- Moving directories would break imports across 30+ Python files

**Two approaches are available:**

| Approach | Effort | Risk | Recommendation |
|----------|--------|------|----------------|
| A: Exception Declaration | Low | Low | **Recommended for Python code dirs** |
| B: Full Migration | High | Medium | Better for documentation dirs |

## Current Violations (16 directories)

| Directory | Type | Migration Target | Risk |
|-----------|------|------------------|------|
| `00-Governance/` | Archive/Historical | `90_archive/00-Governance/` | Low |
| `Archive/` | Archive | `90_archive/` (merge) | Low |
| `docs/` | Documentation | `10_docs/` (merge) | Low |
| `examples/` | Samples | `10_docs/examples/` | Low |
| `notes/` | Internal docs | `10_docs/notes/` | Low |
| `policy/` | Policy docs | `10_docs/policy/` | Low |
| `prompts/` | Code assets | `40_src/prompts/` | Low |
| `protocols/` | **Core content** | `10_docs/protocols/` OR Exception | Medium |
| `registry/` | Config data | `30_config/registry/` | Low |
| `schemas/` | **Core content** | Exception recommended | High |
| `scripts/` | Code | `40_src/scripts/` | Medium |
| `taxonomies/` | **Core content** | Exception recommended | High |
| `tests/` | Python tests | `40_src/tests/` | High (imports) |
| `tools/` | Code | `40_src/tools/` | Low |
| `validators/` | **Python package** | Exception recommended | **Critical** |
| `workspace/` | Mixed | `70_evidence/workspace/` | Low |

## Impact Analysis

### Python Import Dependencies
```
validators/ imported by:
  - 6 validator modules (internal)
  - 8 test files
  - CONTRIBUTING.md examples
  - run_all.py orchestrator
```

Moving `validators/` to `40_src/validators/` would require:
1. Update all 30+ import statements
2. Add `40_src` to PYTHONPATH in pytest.ini, scripts, and CI
3. Update CLAUDE.md examples
4. Update CONTRIBUTING.md examples

### Core Content Directories
`schemas/`, `taxonomies/`, `protocols/` are the **primary deliverables** of C010_standards. They exist at top-level for discoverability - consumers expect to find standards content at obvious paths.

## Recommended Approach: Hybrid

### Phase 1: Easy Migrations (Low Risk)
Move documentation and archive dirs that don't have import dependencies:

```bash
# Documentation consolidation
git mv docs/* 10_docs/ 2>/dev/null || true
git mv examples 10_docs/examples
git mv notes 10_docs/notes
git mv policy 10_docs/policy
rmdir docs 2>/dev/null || true

# Archive consolidation
git mv Archive 90_archive/Archive
git mv 00-Governance 90_archive/00-Governance
mkdir -p 90_archive
```

### Phase 2: Exception Declaration (Core Content)
Create formal exception for C010's special nature:

```yaml
# 00_admin/audit_exceptions.yaml
# C010_standards exception declaration
#
# C010 is the standards repository that DEFINES folder structure rules.
# Its structure is intentionally different for these reasons:
# 1. Core content (schemas/, taxonomies/, protocols/) must be discoverable
# 2. validators/ is a Python package with internal imports
# 3. Consumers depend on current paths (submodule references)

exception_type: standards_repository
reason: |
  C010_standards defines the Betty Protocol folder structure.
  Its content directories exist at top-level for discoverability
  and to serve as canonical reference paths.

allowed_additional_dirs:
  - schemas      # Core deliverable: metadata schema definitions
  - taxonomies   # Core deliverable: controlled vocabularies
  - protocols    # Core deliverable: protocol documents
  - validators   # Python package: auditing tools
  - tests        # Python tests for validators
  - registry     # Configuration registry
  - tools        # Supporting tools
  - scripts      # Operational scripts (referenced from 00_run/)

required_files:
  - README.md
  # rules_now.md and RELATIONS.yaml exist at root
```

### Phase 3: Script Path Updates
After moving `scripts/`:
- Update `00_run/audit_syncedprojects.command` line 28
- Update `00_run/audit_syncedprojects.ps1` equivalent

## Verification Commands

```bash
# After Phase 1 migrations
git status  # Should show clean renames

# After Phase 2 exception
bash scripts/audit_folder_structure.sh ~/SyncedProjects
# C010 should now show as "exception" not "migrate"

# Test validators still work
python validators/run_all.py
```

## Decision Required

Choose approach for C010_standards:

**Option A: Minimal migration + exception** (Recommended)
- Move docs/examples/notes/policy to 10_docs/
- Move Archive/00-Governance to 90_archive/
- Declare exception for schemas/taxonomies/protocols/validators/tests

**Option B: Full migration**
- Move everything to compliant folders
- Update all Python imports (30+ files)
- Update PYTHONPATH in pytest.ini, CI, scripts
- Update documentation examples

**Option C: Pure exception** (Least effort)
- Keep current structure
- Declare exception for entire repo as "standards repository"
- Document rationale

---
**Next Action:** Jeremy to choose approach (A/B/C), then continue remediation.
