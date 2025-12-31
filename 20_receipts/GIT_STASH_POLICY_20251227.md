# Git Stash Policy Addition

**Date**: 2025-12-27
**Files Edited**:
- `protocols/betty_protocol.md`
- `protocols/session_closeout_protocol.md`

## A1: betty_protocol.md

**Markers added**:
```
<!-- BOT:git_stash_policy:start -->
<!-- BOT:git_stash_policy:end -->
```

**Location**: After "Branching" section, before "Chroma policies"

**Content**: Zero-stash default policy with:
- Approved uses (emergency context switching only)
- Mandatory rules when stash is used (name it, triage immediately)
- Preferred resolution pattern (stash → branch)
- Closeout gate requirement
- Preferred alternative (WIP branch + WIP commit)

## A2: session_closeout_protocol.md

**Version**: 1.0 → 1.1

**Change**: Rewrote "Step 4: Stash vs WIP Commit Decision" to "Step 4: Stash Triage (MANDATORY)"

**New requirements**:
- Always run `git stash list` at closeout
- Non-empty stash list = session NOT clean
- Resolution table with commands
- Decision tree for each stash
- Named stash requirement with example

## Rationale

**Stash is emergency-only; WIP branches are the default.**

Stashes are:
- Easy to forget (silent, no branch visible)
- Hard to audit (no commit message, no receipt trail)
- Context-lossy (no associated branch/PR/issue)

WIP branches are:
- Visible in `git branch`
- Have commit messages
- Can be pushed for backup
- Appear in receipts naturally

## Extraction Pattern

```bash
# Extract stash policy slice
sed -n '/<!-- BOT:git_stash_policy:start -->/,/<!-- BOT:git_stash_policy:end -->/p' \
  protocols/betty_protocol.md
```

## Commit SHA

`6eded11`

---
Generated: 2025-12-27
