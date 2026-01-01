# Receipt: MkDocs Build-Only CI Workflow Rollout

**Date**: 2026-01-01
**Action**: Applied C019's build-only MkDocs CI workflow to all repos with mkdocs.yml
**Status**: COMPLETE

## Scope

Searched all repos in `/Users/jeremybradford/SyncedProjects` for `mkdocs.yml` files.

## Repos Found

| Repo | Status | Action |
|------|--------|--------|
| C019_docs-site | Already has workflow | Skipped (canonical source) |
| C017_brain-on-tap | Missing docs CI | Added `.github/workflows/docs-ci.yml` |

## Workflow Applied

Build-only workflow (no GitHub Pages deployment) with:
- Triggers on push/PR to main for docs/**, mkdocs.yml, requirements.txt
- Python 3.11 with pip caching
- `mkdocs build --strict` validation
- Upload build artifact (7-day retention)
- Manual trigger via workflow_dispatch

## Commits

| Repo | Commit | Message |
|------|--------|---------|
| C017_brain-on-tap | 11500ad | ci(docs): add build-only MkDocs workflow |

## Canonical Source

`C019_docs-site/.github/workflows/deploy-docs.yml` - This is the authoritative workflow that was used as the template.

## Verification

- [ ] C017_brain-on-tap Actions build passes

## Files Changed

| Repo | File | Change |
|------|------|--------|
| C017_brain-on-tap | `.github/workflows/docs-ci.yml` | Created (51 lines) |
