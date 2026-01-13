# Receipt: PROJECT_PRIMER Rollout - C010_standards

**Date**: 2026-01-12
**Operator**: Claude Code (Opus 4.5)
**Session**: PROJECT_PRIMER harness rollout

## Summary

Generated PROJECT_PRIMER.md for C010_standards as part of the core repos rollout. Created v2 RELATIONS.yaml with ownership boundaries. Updated notebook_map.yaml tracking.

## Documents Modified

| File | Action | Description |
|------|--------|-------------|
| `RELATIONS.yaml` | Created | v2 format with owns/must_not_own/depends_on |
| `PROJECT_PRIMER.md` | Generated | Single-file documentation bundle |

## RELATIONS.yaml v2 Content

```yaml
version: 2
repo: C010_standards

owns:
  - "Workspace protocols and governance rules (Betty Protocol, README repo card standard)"
  - "Data schemas (DocMeta, CodeMeta, Houston configs)"
  - "Classification taxonomies (topics, emotions, metadata)"
  - "Validation tools (Houston validators, README repo card checker)"
  - "Project registry and workspace inventory (KNOWN_PROJECTS.md)"
  - "Bootstrap scripts for bulk repo upgrades (Ruff, testing, Claude support)"
  - "Agent onboarding documentation (AGENT_START_HERE.md)"

must_not_own:
  - "Runtime services or deployable applications (belongs to individual project repos)"
  - "Data storage, embeddings, or artifacts (belongs to $SADB_DATA_DIR and C003)"
  - "Memory infrastructure pipelines (belongs to C002/C003 SADB repos)"
  - "Project-specific configuration or code (stays in respective repos)"
  - "Health monitoring or service dashboards (belongs to C001_mission-control)"

depends_on:
  # C010 is the foundation - no upstream dependencies
```

## Primer Generation Output

```
Primer generated: /Users/jeremybradford/SyncedProjects/C010_standards/PROJECT_PRIMER.md
Tier: kitted
Repo SHA: 6eff996
Primer hash: sha256:e448a5911ac9
```

## Verification

- [x] README repo card exists (BOT markers present)
- [x] META.yaml exists with required fields
- [x] RELATIONS.yaml v2 format with owns/must_not_own/depends_on
- [x] PROJECT_PRIMER.md generated with populated boundaries
- [x] Integration Map populated (no upstream dependencies - foundation repo)
- [x] Quick Routing table present
- [x] Provenance block with SHA and timestamp
- [x] notebook_map.yaml updated with primer entry

## notebook_map.yaml Entry

```yaml
C010_standards:
  enabled: true
  tier: kitted
  repo_sha: 6eff996
  generated_at: '2026-01-12T19:19:59Z'
  primer_path: PROJECT_PRIMER.md
  primer_hash: 'sha256:e448a5911ac9'
  platforms:
    chatgpt: { status: pending }
    claude_projects: { status: pending }
    gemini: { status: not_started }
```

## Known Issues

None identified.

## Next Steps

1. Upload PROJECT_PRIMER.md to ChatGPT/Claude Projects
2. Test with deep dive kickoff prompt
3. Verify Betty respects ownership boundaries
