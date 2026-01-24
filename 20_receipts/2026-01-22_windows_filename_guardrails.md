# Receipt: Windows Filename Compatibility Guardrails

**Date**: 2026-01-22
**Session**: SyncThing sync failures from Windows-incompatible filenames

## Problem

SyncThing sync between macOS and Windows was failing due to filenames containing:
- Colons in ISO 8601 timestamps (`T05:19:05`)
- Reserved Windows name `nul`
- Asterisks in Obsidian-Vault files
- macOS Icon files with control character (`\r`)

## What Was Done

### 1. Fixed Existing Issues

| Issue | Count | Fix |
|-------|-------|-----|
| Colons in timestamps | 23 | Renamed `T05:19:05` → `T05-19-05` |
| Reserved name `nul` | 4+ | Deleted (kept `nul_placeholder` versions) |
| Asterisks in Obsidian | 2 | Renamed/deleted |
| macOS Icon files | 19 | Added to `.stignore` |

### 2. Updated .stignore (Workspace Root)

Added patterns to prevent future sync issues:
```
Icon?
nul
**/.venv_*/**
```

### 3. Created Validator

**File**: `validators/check_windows_filename.py`

Checks for:
- Reserved characters: `\ / : * ? " < > |`
- Reserved names: CON, PRN, AUX, NUL, COM1-9, LPT1-9
- Trailing dots/spaces
- Control characters

Usage:
```bash
python validators/check_windows_filename.py /path/to/scan
python validators/check_windows_filename.py --fix  # Auto-fix
```

Registered in `validators/__init__.py` as `windows_filename`.

### 4. Created Workspace Scanner

**File**: `_scripts/scan_windows_filenames.py`

Standalone script for scanning any directory:
```bash
python _scripts/scan_windows_filenames.py              # Scan SyncedProjects
python _scripts/scan_windows_filenames.py --all        # Scan all sync locations
python _scripts/scan_windows_filenames.py --fix        # Auto-fix issues
```

Generates timestamped reports in `_scripts/20_receipts/`.

### 5. Updated CLAUDE.md

Added "Windows Filename Compatibility (CRITICAL)" section to C010_standards/CLAUDE.md with:
- Forbidden characters and names
- Common mistakes (ISO timestamps with colons)
- Validation commands
- Correct timestamp format for receipts

## Lessons Learned

1. **Investigate before deleting** - When user reports "still seeing issues," ask what specifically before taking destructive action
2. **macOS Icon files are custom folder icons** - They have value; use `.stignore` to exclude from sync rather than deleting
3. **ISO 8601 timestamps need modification for Windows** - Replace colons with dashes in the time portion
4. **SyncThing .stignore patterns** - `Icon?` matches Icon files with control characters; patterns apply immediately

## Key Files

| File | Purpose |
|------|---------|
| `validators/check_windows_filename.py` | Validator for CI/pre-commit |
| `_scripts/scan_windows_filenames.py` | Workspace-wide scanner |
| `.stignore` | SyncThing ignore patterns (workspace root) |
| `CLAUDE.md` | Updated with filename rules for future agents |

## Verification

```bash
# Confirm no Windows-incompatible files remain
python validators/check_windows_filename.py ~/SyncedProjects
# Expected: "[OK] Windows filename validation passed"
```
