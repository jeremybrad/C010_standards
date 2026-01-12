# Schema Migration Checklist

**Version**: 1.0.0
**Last Updated**: 2026-01-12
**Purpose**: Step-by-step checklist for repos adopting C010 schemas

---

## Overview

This checklist guides projects through adopting C010_standards schemas (DocMeta, CodeMeta, Houston configs). Use it when:
- Onboarding a new repo to workspace standards
- Upgrading an existing repo to a new schema version
- Auditing schema compliance across the workspace

---

## Pre-Migration Assessment

### 1. Identify Current State

- [ ] Run folder audit: `bash 00_run/audit_syncedprojects.command`
- [ ] Check if repo has Betty Protocol structure (`00_admin/`, `10_docs/`, `20_receipts/`, etc.)
- [ ] Identify existing metadata files (YAML frontmatter, META.yaml, etc.)
- [ ] Note any custom schemas that may conflict

### 2. Determine Target Tier

| Tier | Requirements | Use When |
|------|--------------|----------|
| **Tier 1** | README.md, CHANGELOG.md, META.yaml | All repos |
| **Tier 2** | + CLAUDE.md, 10_docs/, 20_receipts/ | Active development |
| **Tier 3** | + 7 NotebookLM docs | Complex/kitted repos |

- [ ] Select target tier based on project complexity
- [ ] Verify repo meets prerequisites for target tier

---

## Tier 1 Migration (Required)

### README.md

- [ ] Verify README.md exists at repo root
- [ ] Add repo card markers if using NotebookLM sync:
  ```markdown
  <!-- BOT:repo_card:start -->
  ...content...
  <!-- BOT:repo_card:end -->
  ```
- [ ] Run README validator: `python scripts/validate_readme_repo_card.py <repo_path>`

### CHANGELOG.md

- [ ] Create CHANGELOG.md if missing
- [ ] Use semantic versioning format:
  ```markdown
  ## [1.0.0] - 2026-01-12
  ### Added
  - Initial release
  ```
- [ ] Include dates for all entries

### META.yaml

- [ ] Create META.yaml at repo root
- [ ] Include required fields:
  ```yaml
  project:
    last_reviewed: 2026-01-12
    summary: "Brief project description"
    status: active  # active|maintenance|archived
    series: P  # P|C|W|U
  ```
- [ ] Validate against spec: `protocols/META_YAML_SPEC.md`

---

## Tier 2 Migration (Recommended)

### CLAUDE.md

- [ ] Create CLAUDE.md at repo root
- [ ] Follow cross-platform format: `protocols/cross_platform_claude_md.md`
- [ ] Include sections:
  - Overview
  - Platform Compatibility (if cross-platform)
  - Common Commands
  - Key Files
  - Troubleshooting

### Folder Structure

- [ ] Create `10_docs/` for documentation
- [ ] Create `20_receipts/` for change receipts
- [ ] Create `00_admin/` for admin files (if applicable)
- [ ] Add to `audit_exceptions.yaml` if custom folders needed

### .gitignore Baseline

- [ ] Ensure .gitignore includes:
  ```
  .DS_Store
  .venv/
  venv/
  node_modules/
  data/
  .env
  ```

---

## Tier 3 Migration (Advanced)

### Documentation Suite

Create 7 docs in `docs/{repo_name}/`:

- [ ] OVERVIEW.md - System overview, ecosystem fit
- [ ] QUICKSTART.md - Install, run, verify in 5 minutes
- [ ] ARCHITECTURE.md - Component diagram, data flow
- [ ] CODE_TOUR.md - File map, key functions
- [ ] OPERATIONS.md - Run modes, day-to-day workflows
- [ ] SECURITY_AND_PRIVACY.md - What stays local, security model
- [ ] OPEN_QUESTIONS.md - Unresolved decisions, known limitations

### Content Validation

- [ ] Each doc has metadata header (Version, Last Updated)
- [ ] File paths and line numbers are accurate
- [ ] Internal links resolve correctly
- [ ] Code examples are tested/working

### NotebookLM Sync

- [ ] Create/identify NotebookLM notebook for repo
- [ ] Add all Tier 3 docs as sources
- [ ] Generate standard artifacts:
  - [ ] Mind Map
  - [ ] Briefing Doc
  - [ ] Study Guide
  - [ ] Audio Overview
  - [ ] Infographic
  - [ ] Flashcards
  - [ ] Quiz

---

## Houston Config Migration (If Applicable)

For repos using Houston agent integration:

### Features Config

- [ ] Create/update `houston-features.json`
- [ ] Validate: `python validators/check_houston_features.py`
- [ ] Verify phase alignment with trust building

### Tools Config

- [ ] Create/update `houston-tools.json`
- [ ] Validate: `python validators/check_houston_tools.py`
- [ ] Ensure phase gating is correct

### Document Metadata

- [ ] Add Houston routing tags to relevant docs:
  ```yaml
  routing:
    tags:
      - "agent:houston"
      - "sensitivity:internal"
  ```
- [ ] Validate: `python validators/check_houston_docmeta.py`

---

## Post-Migration Validation

### Run All Validators

```bash
python validators/run_all.py --pass-args --verbose
```

- [ ] All validators pass (exit code 0)
- [ ] No warnings in output

### Compliance Check

- [ ] Run folder audit again
- [ ] Verify repo shows as compliant
- [ ] Update exception file if needed

### Documentation Update

- [ ] Update repo README if needed
- [ ] Create migration receipt in `20_receipts/`
- [ ] Update CHANGELOG.md

---

## Common Issues

| Issue | Solution |
|-------|----------|
| YAML syntax errors | Validate with `python -c "import yaml; yaml.safe_load(open('file.yaml'))"` |
| Missing required fields | Check schema spec for required vs optional fields |
| Path resolution failures | Use absolute paths in doc references |
| Validator import errors | Run from repo root directory |
| Coverage false positives | Check `.coveragerc` source configuration |

---

## Receipt Template

After migration, create receipt:

```markdown
# Schema Migration Receipt

**Date**: YYYY-MM-DD
**Repo**: {repo_name}
**Target Tier**: {1|2|3}
**Outcome**: Completed/Partial

## Changes Made

- [ ] Tier 1: README, CHANGELOG, META.yaml
- [ ] Tier 2: CLAUDE.md, folder structure
- [ ] Tier 3: 7 NotebookLM docs + artifacts

## Validation Results

- Folder audit: PASS/FAIL
- Validators: PASS/FAIL
- NotebookLM sync: PASS/FAIL/N/A

## Notes

{Any issues, exceptions, or follow-ups}
```

---

## Related Documentation

- [betty_protocol.md](betty_protocol.md) - Folder structure requirements
- [schema_versioning_policy.md](schema_versioning_policy.md) - Version change rules
- [tier3_documentation_spec.md](tier3_documentation_spec.md) - Tier 3 content specs
- [META_YAML_SPEC.md](META_YAML_SPEC.md) - META.yaml contract

---

*Maintained by: Jeremy Bradford & Claude*
