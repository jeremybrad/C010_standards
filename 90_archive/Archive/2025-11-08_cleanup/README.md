# Archive: 2025-11-08 Cleanup

## Contents

This archive contains legacy files removed during the Week 3 repository cleanup as part of the comprehensive repository review.

### YAML_Backup_20250713/

**Date**: July 13, 2025
**Purpose**: Backup of taxonomy files before consolidation
**Archived because**: Taxonomies have been consolidated into `taxonomies/` directory. This backup is no longer needed as:
- Current taxonomies are maintained in `taxonomies/`
- Changes are tracked in git history
- No need for separate backup copies

**Files**:
- `content_taxonomy.yaml`
- `emotion_taxonomy.yaml`
- `master_taxonomy.yaml`
- `privacy_taxonomy.yaml`
- `taxonomy_governance.yaml`

### Scripts/

**Purpose**: Notion Canvas migration scripts
**Archived because**: Notion to Obsidian migration completed months ago. Scripts served their purpose:
- `canvas-batch-migrate.sh` - First migration batch
- `canvas-batch-migrate-round2.sh` - Second migration batch
- `canvas-migration-script.py` - Python migration logic
- `canvas-sort-and-migrate.py` - Canvas sorting and migration

**Note**: These scripts were one-time migration tools and are no longer actively used.

## Retention Policy

**Recommendation**: Keep this archive for 6 months (until May 2026), then delete if:
- No need to reference old migration logic
- No need to rollback taxonomy changes
- Git history provides sufficient audit trail

## Restoration

If you need to restore any of these files:

```bash
# From repository root
cp Archive/2025-11-08_cleanup/Scripts/* 00-Governance/Scripts/
```

## See Also

- Git commit for this cleanup: See commit message referencing "Week 3 cleanup"
- Current taxonomies: `taxonomies/` directory
- Change history: `notes/CHANGELOG.md`
