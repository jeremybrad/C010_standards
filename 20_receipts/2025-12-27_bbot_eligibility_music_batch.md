# Receipt: Brain on Tap Eligibility - Music Batch

**Date**: 2025-12-27
**Operator**: Claude Code
**Task**: Enable P050, P091, P167, P212 for Brain on Tap (music-themed batch)

## Summary

Expanded BBOT eligibility from 18 repos to 22 repos with music/audio focus:
1. **P050_ableton-mcp** - MCP server for Ableton Live (17 tools, Orpheus integration)
2. **P091_voice-notes-pipeline** - SuperWhisper → Betty AI voice notes pipeline
3. **P167_dj-claude-mcp** - Intelligent Spotify playlist generation via Claude MCP
4. **P212_band-in-a-box-ai** - 214K+ sample library with semantic search

## Changes Made

### Registry Updates (`registry/repos.yaml`)

Added 4 new entries with `bot_active: true`:
- `P050_ableton-mcp` (status: incubating)
- `P091_voice-notes-pipeline` (status: incubating)
- `P167_dj-claude-mcp` (status: active)
- `P212_band-in-a-box-ai` (status: incubating)

### README Repo Cards Added

| Repo | Commit | Push Status |
|------|--------|-------------|
| P050_ableton-mcp | `16ffc8a` | Pushed to main (rebased) |
| P091_voice-notes-pipeline | `364e706` | Pushed to branch (modernize/sprint2-mining) |
| P167_dj-claude-mcp | `b61bfed` | Pushed to main |
| P212_band-in-a-box-ai | `a9f2c65` | Pushed to main |

Note: P091 committed to feature branch, not main.

## Validation Results

| Status | Before | After |
|--------|--------|-------|
| PASS | 18 | 22 |
| FAIL | 0 | 0 |
| N/A | 1 | 1 |

## Evidence

- Eligibility report: `70_evidence/exports/Brain_on_Tap_Eligibility.md`

## Eligible Repos (22 total)

### C-Series (Core Infrastructure)
1. C001_mission-control
2. C002_sadb
3. C003_sadb_canonical
4. C004_star-extraction
5. C005_mybuddy
6. C006_revelator
7. C007_the_cavern_club
8. C008_CBFS
9. C009_mcp-memory-http
10. C010_standards
11. C011_agents
12. C015_local-tts
13. C016_prompt-engine (archived)
14. C017_brain-on-tap
15. C018_terminal-insights
16. C019_docs-site
17. C020_pavlok (experimental)

### P-Series (Projects)
18. P050_ableton-mcp (NEW)
19. P091_voice-notes-pipeline (NEW)
20. P110_knowledge-synthesis-tool
21. P167_dj-claude-mcp (NEW)
22. P212_band-in-a-box-ai (NEW)
