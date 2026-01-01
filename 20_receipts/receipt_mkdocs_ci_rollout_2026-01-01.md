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
| C017_brain-on-tap | 567c5a2 | fix(ci): add mkdocstrings plugin for docs build |

## Canonical Source

`C019_docs-site/.github/workflows/deploy-docs.yml` - This is the authoritative workflow that was used as the template.

## Verification

- [x] C019_docs-site Actions build passes (pre-existing)
- [ ] C017_brain-on-tap Actions build passes

**Note**: C017's build fails with 18 warnings in strict mode. These are pre-existing broken links in docs (similar to what was fixed in C019 earlier today). The workflow itself is correctly installed. Fixing C017's docs is a separate task.

Broken links in C017 include:
- `DOCS_INDEX.md` → multiple `../` links to files outside docs_dir
- `memory_lab.md` → links to `../10_docs/` files
- `playbooks.md` → link to `../10_docs/PLAYBOOKS_SCHEMA.md`

## Follow-up Required

C017_brain-on-tap needs its docs fixed (same pattern as C019's earlier fix today):
- Remove or fix `../` relative links in docs/*.md
- Or remove `--strict` flag if warnings are acceptable

## Files Changed

| Repo | File | Change |
|------|------|--------|
| C017_brain-on-tap | `.github/workflows/docs-ci.yml` | Created (52 lines, includes mkdocstrings) |
