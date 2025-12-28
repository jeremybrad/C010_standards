# Receipt: Brain on Tap Eligibility - Core Two-Pack

**Date**: 2025-12-27
**Operator**: Claude Code
**Task**: Enable C018_terminal-insights and C005_mybuddy for Brain on Tap

## Summary

Expanded BBOT eligibility from 10 repos to 12 repos by adding the "core two-pack":
1. **C018_terminal-insights** - Terminal notes, command patterns, troubleshooting receipts
2. **C005_mybuddy** - Personal buddy system with ChromaDB semantic search

## Rationale

- **C018_terminal-insights**: High-leverage for Brain on Tap - surfaces CLI patterns, gotchas, and canonical commands already learned
- **C005_mybuddy**: One of the oldest "synthetic self / buddy" tracks - enables querying design decisions and artifacts

Both repos are "folder-structure messy" in the audit, but BBOT Eligibility v1 doesn't care about that. Track A (eligibility) vs Track B (folder structure migration) are separate timelines.

## Changes Made

### Registry Updates (`registry/repos.yaml`)

Added 2 new entries with `bot_active: true` and `path_rel`:
- `C018_terminal-insights`
- `C005_mybuddy`

### README Repo Cards Added

| Repo | Commit | Branch |
|------|--------|--------|
| C018_terminal-insights | `98397be` | main |
| C005_mybuddy | `3a53133` | main |

## Validation Results

| Status | Before | After |
|--------|--------|-------|
| PASS | 10 | 12 |
| FAIL | 0 | 0 |
| N/A | 1 | 1 |

## Evidence

- Eligibility report: `70_evidence/exports/Brain_on_Tap_Eligibility.md`
- CSV export: `70_evidence/exports/Brain_on_Tap_Eligibility.csv`

## Eligible Repos (12 total)

1. C001_mission-control
2. C002_sadb
3. C003_sadb_canonical
4. C004_star-extraction
5. C005_mybuddy (NEW)
6. C006_revelator
7. C007_the_cavern_club
8. C009_mcp-memory-http
9. C010_standards
10. C017_brain-on-tap
11. C018_terminal-insights (NEW)
12. P110_knowledge-synthesis-tool
