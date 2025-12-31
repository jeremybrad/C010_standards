# Schema Versioning Policy

## Overview

This document defines the versioning policy for all schemas managed in C010_standards. Following these guidelines ensures backward compatibility, predictable migrations, and clear communication with consuming projects.

## Scope

This policy applies to:
- **DocMeta schema** (`schemas/docmeta_v*.yaml`)
- **CodeMeta schema** (`schemas/codemeta_v*.yaml`)
- **Houston features schema** (`schemas/houston_features.schema.json`)
- **Future schemas** added to the repository

## Versioning Scheme

### Format: `MAJOR.MINOR`

We use semantic versioning with two components:

- **MAJOR**: Breaking changes that require migration
- **MINOR**: Backward-compatible additions or clarifications

Examples:
- `v1.0` → First stable release
- `v1.1` → Added optional fields (backward compatible)
- `v1.2` → Added more optional fields (backward compatible)
- `v2.0` → Changed required fields or removed fields (breaking)

### File Naming

Schema files MUST include the version number:

```
schemas/
├── docmeta_v1.2.yaml          # Current DocMeta version
├── docmeta_v1.2.md            # Documentation for v1.2
├── codemeta_v1.0.yaml         # Current CodeMeta version
├── houston_features.schema.json  # JSON schemas use package versioning
```

## Version Increments

### MAJOR Version (Breaking Changes)

Increment MAJOR version when making changes that require existing documents to be updated:

**Breaking changes include:**
- Removing fields
- Renaming fields
- Changing field types (e.g., string → array)
- Making optional fields required
- Changing field semantics (e.g., `created` from date to datetime)

**Example:**
```yaml
# docmeta_v1.2.yaml
doc:
  created: "2025-11-08"  # Date format

# docmeta_v2.0.yaml (BREAKING)
doc:
  created_at: "2025-11-08T10:30:00Z"  # Field renamed + datetime format
```

**When making MAJOR changes:**
1. Create new schema file with incremented MAJOR version
2. Keep old schema file for reference (mark as deprecated)
3. Write migration guide in `notes/migrations/`
4. Update CHANGELOG.md with migration instructions
5. Notify all consuming projects (see SCHEMA_CONSUMERS.md)
6. Set deprecation timeline (minimum 3 months)

### MINOR Version (Non-Breaking Changes)

Increment MINOR version for backward-compatible changes:

**Non-breaking changes include:**
- Adding optional fields
- Adding new enum values
- Clarifying documentation
- Adding examples
- Relaxing validation rules (e.g., making required field optional)

**Example:**
```yaml
# docmeta_v1.2.yaml
doc:
  title: "<required>"
  description: "<required>"

# docmeta_v1.3.yaml (non-breaking)
doc:
  title: "<required>"
  description: "<required>"
  summary: "<optional short description>"  # New optional field
```

**When making MINOR changes:**
1. Update existing schema file with new version number
2. Add comments explaining new fields
3. Update documentation (.md file)
4. Update CHANGELOG.md
5. Run validators to ensure existing docs still pass
6. Inform consuming projects (optional but recommended)

## Schema Lifecycle

### States

1. **Draft** - Under development, not used in production
2. **Stable** - Used in production, subject to this versioning policy
3. **Deprecated** - Old version, migration guide available, will be removed
4. **Archived** - Removed from active use, kept for reference only

### Deprecation Process

When a MAJOR version supersedes an older version:

1. **Announcement** (Month 0):
   - Update CHANGELOG.md with deprecation notice
   - Add deprecation warning to old schema file
   - Post announcement in team communication channels

2. **Grace Period** (Months 1-3):
   - Both versions supported
   - Migration guide available
   - Validators accept both versions
   - Consuming projects encouraged to migrate

3. **Sunset** (Month 4+):
   - Old version moved to Archive/
   - Validators only accept new version
   - Migration guide remains available

**Example deprecation notice:**
```yaml
# DocMeta v1.2 (DEPRECATED)
# Source: ../C002_sadb/10_docs/SADB_DocMeta_Schema_v1.2.md
# DEPRECATED: 2025-12-01 - Please migrate to v2.0
# Migration guide: notes/migrations/docmeta_v1.2_to_v2.0.md
# Sunset date: 2026-03-01
```

## Validation

### Schema Validation

All schema changes MUST pass validation before release:

```bash
# For JSON schemas
python validators/check_houston_features.py --schema schemas/houston_features.schema.json --verbose

# For YAML schemas (validate examples)
python validators/check_houston_docmeta.py examples/ --verbose
```

### Backward Compatibility Testing

Before releasing a MINOR version:

1. Run validators on existing documents
2. Verify all tests pass
3. Test in integration environment
4. Review with 1-2 consuming projects

Before releasing a MAJOR version:

1. Create migration guide
2. Test migration on sample documents
3. Validate migrated documents against new schema
4. Get approval from project leads
5. Coordinate release with consuming projects

## Documentation Requirements

### For Each Schema Version

Every schema version MUST have:

1. **YAML Schema File** (`schemas/name_vX.Y.yaml`)
   - Complete template with all fields
   - Inline comments explaining each field
   - Examples for complex fields
   - Source attribution comments

2. **Markdown Documentation** (`schemas/name_vX.Y.md`)
   - Purpose and use cases
   - Field descriptions
   - Validation rules
   - Examples (valid and invalid)
   - Changelog from previous version

3. **CHANGELOG Entry** (`notes/CHANGELOG.md`)
   - Date of release
   - Version number
   - Summary of changes
   - Breaking vs. non-breaking designation
   - Migration guide link (if breaking)

### Migration Guides

For MAJOR version changes, create `notes/migrations/name_vOLD_to_vNEW.md`:

```markdown
# Migration Guide: DocMeta v1.2 → v2.0

## Summary
Brief description of breaking changes

## Breaking Changes

### 1. Field Renamed: `created` → `created_at`
**Old (v1.2):**
```yaml
doc:
  created: "2025-11-08"
```

**New (v2.0):**
```yaml
doc:
  created_at: "2025-11-08T10:30:00Z"
```

**Migration steps:**
1. Rename field
2. Convert to ISO 8601 datetime format
3. Add timezone (default to UTC if unknown)

## Automated Migration

```bash
# Migration script available
python scripts/migrate_docmeta_v1_to_v2.py input.yaml
```

## Validation

After migration, validate with:
```bash
python validators/check_houston_docmeta.py --verbose migrated_file.yaml
```
```

## Consuming Projects

### Schema Consumer Registry

Maintain `notes/SCHEMA_CONSUMERS.md` with:
- Project name
- Schema(s) consumed
- Current version in use
- Contact person
- Last updated date

### Communication Protocol

When releasing schema changes:

1. **MINOR versions:**
   - Update CHANGELOG.md
   - Post in #dev-updates Slack channel
   - Email optional

2. **MAJOR versions:**
   - Create RFC document
   - Present in team meeting
   - Post in #dev-updates with migration timeline
   - Email all project contacts
   - Schedule office hours for migration support
   - Update submodules in consuming projects

## Version Locking

### Git Submodules

Projects consuming C010_standards via git submodule:

1. Lock to specific commit or tag
2. Test new versions before updating submodule
3. Update submodule in dedicated PR
4. Run validation after submodule update

**Example:**
```bash
# In consuming project
cd external/standards
git fetch
git checkout v2.0.0  # Tagged release
cd ../..
git add external/standards
git commit -m "chore: update C010_standards to v2.0.0"
```

### Version Tagging

C010_standards uses git tags for schema releases:

**Tag format:** `schema/<name>/v<MAJOR>.<MINOR>`

Examples:
- `schema/docmeta/v1.2`
- `schema/docmeta/v2.0`
- `schema/codemeta/v1.0`

**Creating a tag:**
```bash
git tag -a schema/docmeta/v1.3 -m "DocMeta v1.3: Added summary field"
git push origin schema/docmeta/v1.3
```

## Testing Requirements

### Before Release

All schema changes MUST include:

1. **Unit tests** for new validation rules
   ```python
   def test_new_optional_field():
       """Test that new optional field is validated correctly."""
       ...
   ```

2. **Example documents** showing new fields
   ```yaml
   # examples/docmeta_v1.3_example.yaml
   ```

3. **Integration tests** with real documents
   ```bash
   python validators/run_all.py --pass-args --verbose
   ```

### Continuous Validation

CI pipeline runs validators on:
- Every commit
- Every PR
- Nightly against all example documents

## Edge Cases

### Schema Splits

If a schema becomes too complex, consider splitting:

**Before:**
```
docmeta_v1.2.yaml  # 200 lines, complex
```

**After:**
```
docmeta_v2.0.yaml           # Core fields only
docmeta_extended_v2.0.yaml  # Advanced features
```

This is considered a MAJOR change requiring migration.

### Schema Merges

If two schemas overlap significantly, consider merging in a new MAJOR version.

### Field Reuse

When adding fields, check if similar fields exist in other schemas. Consider:
- Using the same field name for consistency
- Creating a shared schema fragment
- Adding cross-references in documentation

## Review Process

### For MINOR Changes

1. Create PR with schema update
2. Run `make ci` locally
3. Get approval from 1 maintainer
4. Merge and update CHANGELOG

### For MAJOR Changes

1. Write RFC (Request for Comments) document
2. Present in team meeting
3. Collect feedback (1 week minimum)
4. Create PR with schema + migration guide
5. Get approval from 2+ maintainers
6. Coordinate release with affected projects
7. Merge and tag release

## Examples

### Example 1: Adding Optional Field (MINOR)

```yaml
# Before: docmeta_v1.2.yaml
doc:
  title: "Required title"
  description: "Required description"

# After: docmeta_v1.3.yaml
doc:
  title: "Required title"
  description: "Required description"
  summary: "Optional 1-line summary"  # NEW in v1.3
```

**CHANGELOG entry:**
```markdown
## 2025-11-08 - DocMeta v1.3
- **Non-breaking**: Added optional `doc.summary` field for short summaries
- Backward compatible with v1.2
- No migration required
```

### Example 2: Making Field Required (MAJOR)

```yaml
# Before: docmeta_v1.2.yaml
doc:
  sha256: "<optional>"

# After: docmeta_v2.0.yaml
doc:
  sha256: "<required>"  # NOW REQUIRED
```

**CHANGELOG entry:**
```markdown
## 2025-12-01 - DocMeta v2.0
- **BREAKING**: Field `doc.sha256` is now required
- Migration guide: notes/migrations/docmeta_v1_to_v2.md
- Deprecation timeline:
  - v1.2 deprecated 2025-12-01
  - v1.2 sunset 2026-03-01
- All documents must include sha256 hash
```

## Questions & Support

For questions about schema versioning:
1. Check this document first
2. Review existing schemas for patterns
3. Ask in #dev-standards Slack channel
4. Open issue in C010_standards repository

---

**Last updated:** 2025-11-08
**Next review:** 2026-02-08 (quarterly)
