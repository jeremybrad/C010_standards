# Brain on Tap Work Pool Standard

**Version:** 1.0.0
**Date:** 2025-12-28
**Status:** Active

## Purpose

Define an opt-in "work pool" for repositories that require additional rigor for business analytics and stakeholder-facing work. Work pool repos have stricter evidence, data source, and isolation requirements beyond basic BBOT eligibility.

## Pool System Overview

Repositories can belong to one of three pools:

| Pool | Description | Default |
|------|-------------|---------|
| `personal` | Personal projects, infrastructure, experimental work | Yes |
| `work` | Business analytics, stakeholder deliverables, evidence-backed claims | No |
| `archive` | Deprecated or inactive repos | No |

**Key principle:** Work pool is opt-in. Existing BBOT behavior remains unchanged. Repos without a `pool` field default to `personal`.

## Work Pool Requirements

Work pool repos (`pool: work`) MUST meet all basic BBOT eligibility requirements PLUS:

### MUST (Blocking)

| # | Requirement | Validation |
|---|-------------|------------|
| 1 | README repo card present | BOT:repo_card markers in README.md |
| 2 | DATA_SOURCES.md present | File exists with sensitivity classification |
| 3 | `20_receipts/` directory exists | Evidence trail for non-trivial work |
| 4 | `80_evidence_packages/` directory exists | Claim backing for stakeholder delivery |
| 5 | Verify entry point exists | `make verify` OR `00_run/verify.command` OR `scripts/verify_claims.py` |
| 6 | Export hygiene | Required .gitignore patterns, no tracked exports |

### SHOULD (Advisory)

| # | Requirement | Purpose |
|---|-------------|---------|
| 1 | DATA_SOURCES.md has sensitivity classification | Clear data handling guidance |
| 2 | Pool isolation respected | No direct path dependencies to personal repos |
| 3 | Evidence packages have hash verification | Tamper-evident claims |

## DATA_SOURCES.md Format

Work pool repos MUST have a DATA_SOURCES.md file documenting data sources with sensitivity:

```markdown
# Data Sources

## BigQuery Tables

| Table | Sensitivity | Purpose | Refresh |
|-------|-------------|---------|---------|
| `project.dataset.table` | INTERNAL | Description | Daily |

## Sensitivity Classifications

- **PUBLIC**: Can be shared externally
- **INTERNAL**: Internal use only, not PII
- **CONFIDENTIAL**: Contains PII or sensitive business data
- **RESTRICTED**: Highly sensitive, need-to-know basis

## Export Hygiene

Exports from this repo MUST NOT be committed to git. Use:
- `$SADB_DATA_DIR/exports/` for persistent exports
- `/tmp/` for ephemeral exports
```

### Starter Template

For repos missing DATA_SOURCES.md, use this template:

```markdown
# Data Sources

## Overview

This document tracks all data sources used by this project and their sensitivity classifications.

## Data Sources

| Source | Type | Sensitivity | Purpose |
|--------|------|-------------|---------|
| TBD | TBD | INTERNAL | TBD |

## Sensitivity Classifications

- **PUBLIC**: Can be shared externally
- **INTERNAL**: Internal use only, not PII
- **CONFIDENTIAL**: Contains PII or sensitive business data
- **RESTRICTED**: Highly sensitive, need-to-know basis

## Export Policy

All exports MUST:
1. Be written to `$SADB_DATA_DIR/exports/` or `/tmp/`
2. Never be committed to git
3. Follow the .gitignore patterns in this repo
```

## Export Hygiene Requirements

Work pool repos MUST have .gitignore patterns preventing export commits:

```gitignore
# Export hygiene (work pool requirement)
*.csv
*.xlsx
*.parquet
exports/
data/
!.gitkeep
```

The validator checks:
1. These patterns exist in .gitignore
2. No tracked files match export patterns (`git ls-files` check)

**Exception**: Files in `20_receipts/` and `80_evidence_packages/` are allowed as they serve as evidence/documentation. Only exports outside these directories are flagged.

## Verify Entry Point

Work pool repos MUST have at least one of these verify entry points:

1. **Makefile target**: `make verify`
2. **00_run script**: `00_run/verify.command` (macOS) or `00_run/verify.sh`
3. **Python script**: `scripts/verify_claims.py`

The verify entry point should validate claims made in reports/evidence packages.

## Pool Isolation

Work pool repos should avoid direct path dependencies to personal pool repos. This prevents:
- Accidental data leakage between pools
- Broken references when pools are deployed separately

**Allowed exceptions:**
- C010_standards (shared governance)
- C001_mission-control (credential vault)
- C017_brain-on-tap (context generation)
- Symlinks within $SADB_DATA_DIR

**Validation:** Check imports, config files, and scripts for hardcoded paths to non-work repos.

## Registry Schema Extension

Add optional `pool` field to registry entries:

```yaml
repos:
  - repo_id: W005_BigQuery
    name: BigQuery Infrastructure
    pool: work                    # NEW: work | personal | archive
    bot_active: true
    path_rel: W005_BigQuery
    # ... other fields
```

**Default:** If `pool` is missing, the repo defaults to `personal` pool.

## Validation

### Using the Validator

```bash
# Validate all work pool repos
python scripts/validate_brain_on_tap_work_pool.py

# Validate specific repo
python scripts/validate_brain_on_tap_work_pool.py --repo W005_BigQuery

# Verbose output
python scripts/validate_brain_on_tap_work_pool.py --verbose
```

### Validation Checks

| Check | Severity | Description |
|-------|----------|-------------|
| Basic BBOT eligibility | ERROR | Must pass base eligibility first |
| README repo card | ERROR | BOT:repo_card markers present |
| DATA_SOURCES.md exists | ERROR | File must exist |
| DATA_SOURCES.md has sensitivity | WARNING | Classifications should be present |
| 20_receipts/ exists | ERROR | Directory must exist |
| 80_evidence_packages/ exists | ERROR | Directory must exist |
| Verify entry point | ERROR | At least one verify mechanism |
| Export hygiene | ERROR | .gitignore patterns + no tracked exports |
| Pool isolation | WARNING | Advisory check for cross-pool dependencies |

### Exit Codes

- `0`: All MUST requirements pass
- `1`: One or more MUST requirements fail
- `2`: Configuration or file error

## Reports

The validator produces two report files:

1. **Markdown**: `70_evidence/exports/Brain_on_Tap_Work_Pool.md`
2. **CSV**: `70_evidence/exports/Brain_on_Tap_Work_Pool.csv`

### CSV Format

```csv
repo_id,pool,bot_active,pass,fail_reasons
W005_BigQuery,work,true,PASS,
W006_Abandoned_Cart,work,true,FAIL,"Missing DATA_SOURCES.md"
```

## Migration Guide

### Adding Existing Repo to Work Pool

1. **Add pool field to registry**:
   ```yaml
   - repo_id: W005_BigQuery
     pool: work        # Add this
     bot_active: true
     # ...
   ```

2. **Create DATA_SOURCES.md** (use starter template above)

3. **Create 80_evidence_packages/** if missing:
   ```bash
   mkdir -p 80_evidence_packages
   touch 80_evidence_packages/.gitkeep
   ```

4. **Add export hygiene to .gitignore**

5. **Create verify entry point**:
   ```bash
   mkdir -p 00_run
   echo '#!/bin/bash\necho "Verify not implemented"' > 00_run/verify.command
   chmod +x 00_run/verify.command
   ```

6. **Run validator**:
   ```bash
   python scripts/validate_brain_on_tap_work_pool.py --repo W005_BigQuery --verbose
   ```

## Related Standards

- `brain_on_tap_repo_eligibility_v1.md` - Base BBOT eligibility requirements
- `betty_protocol.md` - Evidence-driven development requirements
- `readme_repo_card.md` - README repo card format
- `registry/schema.md` - Full registry schema

## Changelog

- **1.0.0** (2025-12-28): Initial release - opt-in work pool with stricter requirements
