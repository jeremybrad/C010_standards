# Schema Versioning Policy

**Version**: 1.0.0
**Last Updated**: 2026-01-12
**Purpose**: Rules for versioning schemas and managing breaking changes

---

## Overview

This policy governs how C010_standards schemas are versioned, when version bumps are required, and how breaking changes are communicated to consuming projects.

---

## Versioning Format

All schemas use **Semantic Versioning** (SemVer):

```
MAJOR.MINOR.PATCH
  │     │     └── Bug fixes, documentation updates
  │     └──────── New features (backward compatible)
  └────────────── Breaking changes
```

### Examples

| Change | Version Bump | Example |
|--------|--------------|---------|
| Fix typo in docs | 1.0.0 → 1.0.1 | Corrected field description |
| Add optional field | 1.0.1 → 1.1.0 | Added `metadata.custom` |
| Rename required field | 1.1.0 → 2.0.0 | `doc.topics` → `doc.tags` |
| Remove deprecated field | 1.1.0 → 2.0.0 | Removed `legacy_field` |

---

## Version Bump Rules

### PATCH (x.x.X)

No action required by consumers.

- Documentation fixes
- Validator bug fixes
- Adding examples
- Clarifying existing behavior

### MINOR (x.X.0)

Consumers should review but no code changes required.

- Adding new **optional** fields
- Adding new **optional** sections
- New validation rules that don't reject previously valid docs
- Deprecation warnings (not removals)

### MAJOR (X.0.0)

Consumers MUST update their implementations.

- Removing fields or sections
- Renaming required fields
- Changing field types
- Changing field semantics
- New required fields
- Stricter validation that rejects previously valid docs

---

## Breaking Change Process

### Step 1: Announce Deprecation (Minor Version)

```yaml
# In schema
fields:
  old_field_name:
    deprecated: true
    deprecated_in: "1.2.0"
    removal_version: "2.0.0"
    replacement: "new_field_name"
```

### Step 2: Document in CHANGELOG

```markdown
## [1.2.0] - 2026-01-12

### Deprecated
- `old_field_name` is deprecated, use `new_field_name` instead
  - Will be removed in v2.0.0
```

### Step 3: Update Validators

- Emit warnings for deprecated usage
- Accept both old and new during transition

### Step 4: Notify Consumers

Update `SCHEMA_CONSUMERS.md` with migration notice:

```markdown
## Migration Notices

### DocMeta 1.2 → 2.0 (Planned: 2026-Q2)
- `old_field_name` → `new_field_name`
- Affected repos: C001, C003, P110
```

### Step 5: Execute Major Version

- Remove deprecated fields
- Update validators to reject old format
- Bump to major version
- Update all consumer references

---

## Schema Files

### Naming Convention

```
{schema_name}_v{MAJOR}.{MINOR}.yaml
```

Examples:
- `docmeta_v1.2.yaml`
- `codemeta_v1.0.yaml`
- `houston_features.schema.json` (JSON Schema uses separate versioning)

### File Retention

| Version Status | Retention |
|---------------|-----------|
| Current | Active in `schemas/` |
| Previous major | Archive in `schemas/archive/` |
| Older | Delete (available in git history) |

---

## Compatibility Matrix

Track which projects use which schema versions:

```markdown
## SCHEMA_CONSUMERS.md

| Schema | Version | Consumers |
|--------|---------|-----------|
| DocMeta | 1.2 | C001, C003, C017, P110 |
| DocMeta | 1.1 | C002 (legacy) |
| CodeMeta | 1.0 | All |
| Houston Features | 1.0 | C001 |
```

---

## Validator Versioning

Validators follow their target schema version:

| Validator | Schema Target | Notes |
|-----------|--------------|-------|
| `check_houston_docmeta.py` | DocMeta 1.2 | Warns on 1.1 usage |
| `check_houston_features.py` | Houston Features 1.0 | JSON Schema validated |

### Version Flag

Validators should support version detection:

```bash
# Check validator version
python validators/check_houston_docmeta.py --version
# Output: check_houston_docmeta 1.2.0 (targeting DocMeta v1.2)
```

---

## JSON Schema Versioning

For JSON schemas (Houston configs):

### $schema and $id

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://standards.jeremybradford.dev/schemas/houston_features/v1.0",
  "title": "Houston Features Configuration",
  "version": "1.0.0"
}
```

### Version in Schema

Always include version in the schema itself:

```json
{
  "properties": {
    "$schema_version": {
      "const": "1.0.0",
      "description": "Schema version this config targets"
    }
  }
}
```

---

## Transition Periods

### Deprecation Window

| Change Type | Minimum Window |
|-------------|---------------|
| Optional field removal | 1 minor version |
| Required field change | 2 minor versions |
| Major structural change | 3 months |

### Enforcement Timeline

```
v1.1.0: Deprecation announced (warnings)
v1.2.0: Warning intensity increased
v1.3.0: Error mode available (--strict)
v2.0.0: Deprecated items removed
```

---

## Communication Channels

### When to Notify

| Event | Channel |
|-------|---------|
| PATCH release | CHANGELOG only |
| MINOR release | CHANGELOG + README |
| Deprecation | CHANGELOG + consumer notification |
| MAJOR release | All channels + migration guide |

### Consumer Notification Template

```markdown
## Schema Update Notice

**Schema**: DocMeta
**Current**: v1.2
**Planned**: v2.0 (Target: 2026-Q2)

### Breaking Changes

1. `old_field` renamed to `new_field`
2. `legacy_section` removed

### Migration Steps

1. Update YAML frontmatter: `old_field` → `new_field`
2. Remove `legacy_section` if present
3. Run validator: `python validators/check_houston_docmeta.py --strict`

### Affected Repos

- C001_mission-control
- C003_sadb_canonical

### Timeline

- 2026-01-15: Deprecation warnings enabled
- 2026-03-01: --strict mode available
- 2026-04-01: v2.0 released
```

---

## Exception Process

### Requesting Version Exception

If a consumer cannot upgrade immediately:

1. Open issue in C010_standards
2. Specify:
   - Repo name
   - Current schema version
   - Reason for delay
   - Target upgrade date
3. Add to exceptions list in `SCHEMA_CONSUMERS.md`

### Exception Format

```markdown
## Version Exceptions

| Repo | Schema | Stuck At | Reason | Target Date |
|------|--------|----------|--------|-------------|
| C002_sadb | DocMeta | 1.1 | Legacy migration | 2026-Q3 |
```

---

## Audit Trail

### Schema Change Log

Every schema change must include:

```markdown
## CHANGELOG.md entry

### [1.2.0] - 2026-01-12

#### Changed (DocMeta)
- Added optional `metadata.custom` field (#123)

#### Deprecated (DocMeta)
- `legacy_field` - use `new_field` instead

#### Migration
- No action required (backward compatible)
```

### Git Tags

Tag releases for schema versions:

```bash
git tag -a docmeta-v1.2.0 -m "DocMeta schema v1.2.0"
git push origin docmeta-v1.2.0
```

---

## Quick Reference

### Do I Need a Version Bump?

| Change | Bump? |
|--------|-------|
| Fixed typo | PATCH |
| Added optional field | MINOR |
| Added required field | MAJOR |
| Renamed field | MAJOR |
| Changed field type | MAJOR |
| Deprecated field | MINOR |
| Removed deprecated field | MAJOR |
| Updated docs only | PATCH |
| New example file | PATCH |

---

## Related Documentation

- [schema_migration_checklist.md](schema_migration_checklist.md) - Repo migration guide
- [tier3_documentation_spec.md](tier3_documentation_spec.md) - Documentation standards
- [betty_protocol.md](betty_protocol.md) - Governance rules

---

*Maintained by: Jeremy Bradford & Claude*
