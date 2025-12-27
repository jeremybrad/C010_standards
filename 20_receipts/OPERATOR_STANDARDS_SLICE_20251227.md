# Operator Standards Slice Addition

**Date**: 2025-12-27
**File Edited**: `protocols/betty_protocol.md`

## Change Summary

Added queryable slice for dynamic injection into operator primers and closeouts.

## Markers Added

```
<!-- BOT:operator_standards_brief:start -->
...content...
<!-- BOT:operator_standards_brief:end -->
```

## Intent

Enable zero-duplication operator standards injection:
- Operator primers can extract content between BOT markers at render time
- Operator closeouts can validate against the same canonical source
- No copied MD briefs in profiles; single source of truth in C010_standards

## Content Included

1. **Folder structure (top-level)** - Complete ALLOWED_DIRS list
2. **Local-only artifacts** - Files that should never be committed
3. **Move discipline** - `git mv` vs `mv` rules
4. **Session hygiene expectation** - Clean shutdown requirements

## Extraction Pattern

```bash
# Extract slice from canonical source
sed -n '/<!-- BOT:operator_standards_brief:start -->/,/<!-- BOT:operator_standards_brief:end -->/p' \
  protocols/betty_protocol.md
```

## Commit SHA

`1ddf6e5`

---
Generated: 2025-12-27
