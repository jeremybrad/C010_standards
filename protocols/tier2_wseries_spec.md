# Tier 2 W-Series Documentation Specification

**Version**: 1.0.0
**Last Updated**: 2026-01-15
**Purpose**: Documentation requirements for W-series (Work) repositories

---

## Overview

This specification defines Tier 2 documentation requirements for W-series repositories. W-series repos are client-focused work projects that require consistent documentation for onboarding, knowledge transfer, and operational clarity.

---

## Required Documents

| Document | Purpose | Template |
|----------|---------|----------|
| **README.md** | Project overview and quick start | Existing (do not overwrite) |
| **CLAUDE.md** | Claude Code session guidance | Existing (do not overwrite) |
| **META.yaml** | Project metadata with client info | `meta_yaml_wseries.template.yaml` |
| **CHANGELOG.md** | Change history and versioning | `changelog.template.md` |
| **glossary.yaml** | Domain-specific terminology | `glossary.template.yaml` |

## Required Folders

| Folder | Purpose |
|--------|---------|
| **10_docs/** | Documentation, guides, architecture decisions |
| **20_receipts/** | Change receipts and evidence (Betty Protocol) |

---

## W-Series Specific Requirements

### META.yaml

W-series repos **must** include the `client` field:

```yaml
project:
  last_reviewed: 2026-01-15
  summary: "One-line description under 100 chars"
  status: active
  series: W
  client: "ClientName"  # REQUIRED for W-series
```

### Client Field Values

Common client values:
- `Wowway` - Wowway/CMO reporting projects
- `Internal` - Internal tooling and automation
- `Research` - Research and analysis projects

---

## Compliance Checklist

A W-series repo is **Tier 2 compliant** when:

- [ ] README.md exists with project overview
- [ ] CLAUDE.md exists with session guidance
- [ ] META.yaml exists with all required fields including `client`
- [ ] CHANGELOG.md exists with at least one entry
- [ ] glossary.yaml exists in 10_docs/ (can be minimal)
- [ ] 10_docs/ directory exists
- [ ] 20_receipts/ directory exists
- [ ] `project.last_reviewed` is within 30 days

---

## Bootstrap Process

### 1. Run Bootstrap Script

```bash
# Dry-run to preview changes
bash scripts/bootstrap_tier2_wseries.sh --dry-run W001 W003 W008 W009 W011

# Apply changes
bash scripts/bootstrap_tier2_wseries.sh W001 W003 W008 W009 W011
```

### 2. Populate Content

After scaffolding, populate content using the playbook:

```bash
bbot tier2-docs-playbook --repo W001_cmo-weekly-reporting
```

Or manually:

1. **META.yaml**: Fill in `summary`, `client`, `folders`, `files`
2. **CHANGELOG.md**: Add current state and recent changes
3. **glossary.yaml**: Add 3+ domain-specific terms

### 3. Validate Compliance

```bash
python scripts/validate_tier2_compliance.py ~/SyncedProjects/W001_cmo-weekly-reporting
```

### 4. Generate PROJECT_PRIMER

After Tier 2 compliance, repos are eligible for PROJECT_PRIMER generation:

```bash
generate-project-primer W001_cmo-weekly-reporting
```

---

## Quality Gates

### Gate 1: Structure
- All required files exist
- All required folders exist

### Gate 2: Content
- META.yaml has all required fields populated
- CHANGELOG.md has at least one entry with date
- glossary.yaml has at least 1 term (3+ recommended)

### Gate 3: Freshness
- `project.last_reviewed` is within 30 days
- CHANGELOG.md reflects recent changes

---

## Validation Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Fully compliant |
| 1 | Missing required files/folders |
| 2 | Files exist but content incomplete |

---

## Comparison with Other Tiers

| Requirement | Tier 1 | Tier 2 (W-Series) | Tier 3 |
|-------------|--------|-------------------|--------|
| README.md | Yes | Yes | Yes |
| CHANGELOG.md | Yes | Yes | Yes |
| META.yaml | Yes | Yes (+ client) | Yes |
| CLAUDE.md | No | Yes | Yes |
| glossary.yaml | No | Yes | Yes |
| 10_docs/ | No | Yes | Yes |
| 20_receipts/ | No | Yes | Yes |
| 7 NotebookLM docs | No | No | Yes |

---

## Related Standards

- [tier3_documentation_spec.md](tier3_documentation_spec.md) - Full Tier 3 requirements
- [META_YAML_SPEC.md](META_YAML_SPEC.md) - META.yaml contract
- [betty_protocol.md](betty_protocol.md) - Folder structure and receipts
- [cross_platform_claude_md.md](cross_platform_claude_md.md) - CLAUDE.md format

---

*Maintained by: Jeremy Bradford & Claude*
