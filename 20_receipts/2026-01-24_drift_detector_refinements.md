# Session Receipt: Drift Detector Refinements

**Date**: 2026-01-24
**Repo**: C010_standards
**Branch**: main

## Commits Made

1. `c52d8b9` - chore(drift): treat 1-commit primer SHA lag as expected
2. `b3c34d9` - fix: exclude macOS Icon files from windows_filename validator
3. `f7174ce` - fix(test): correct coverage config for non-package repo

## What Was Done

### Drift Detector
- Added `allowed_sha_lag_commits: 1` to `30_config/drift_rules.yaml`
- Updated `scripts/drift/level2.py` with `_get_commit_lag()` helper
- PROJECT_PRIMER.md being 1 commit behind HEAD now INFO instead of MAJOR

### Icon File Handling
- Added `/Icon` to default excludes in `validators/check_windows_filename.py`
- Created `.stignore` for Syncthing (Icon*, .DS_Store, __pycache__, etc.)

### Test Coverage Fix
- Changed `pytest.ini` from `--cov=C010_standards` to `--cov=validators`
- Coverage now 73% (passing 70% threshold)

### Claude Code Hooks (outside C010)
- Updated `~/.local/bin/c018-hook-wrapper.py`:
  - Injects C018 repo path into sys.path
  - Maps `pre_tool_use` → `handle_pre_tool_use`
  - Outputs valid JSON for hook runner
- Removed `Bash` from hook matcher in `~/.claude/settings.json`

## Current State

- Tests: 183 passed, 5 skipped, 73% coverage
- Drift Level 2: CRITICAL=0, MAJOR=0, MINOR=27, INFO=31
- Working tree clean, pushed to origin/main

## Potential Follow-ups

- Address 27 MINOR findings (stale path patterns)
- Address 11 misplaced `*.meta.yaml` files in validators/
- Fix C018 LaunchAgent plist (~ expansion issue)
