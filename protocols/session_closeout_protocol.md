# Session Closeout Protocol v1.1

**Source:** `C010_standards/protocols/session_closeout_protocol.md`
**Version:** 1.1
**Last Updated:** 2025-12-27

## Purpose

Ensure every Claude Code session ends with a verifiable clean state. No silent drift, no orphaned changes, no forgotten stashes. This protocol defines the minimum actions required before declaring a session complete.

---

## Quick Reference

| Closeout Level | When to Use | Steps Required |
|----------------|-------------|----------------|
| **Minimum** | Quick task, single-file change | Steps 1-3 |
| **Standard** | Normal development session | Steps 1-5 |
| **Full** | Multi-repo work, major changes | Steps 1-7 |

---

## Protocol Steps

### Step 1: Confirm Location

```bash
pwd
basename $(git rev-parse --show-toplevel 2>/dev/null || pwd)
git branch --show-current
```

**Pass criteria:** You are in the expected repo on the expected branch.

---

### Step 2: Assess Working Tree State

```bash
git status --porcelain=v1
```

**Interpret output:**
| Prefix | Meaning | Action Required |
|--------|---------|-----------------|
| ` M` | Modified, not staged | Review and stage or restore |
| `M ` | Modified, staged | Ready to commit |
| `??` | Untracked | Decide: add, ignore, or delete |
| `!!` | Ignored | Safe noise (no action) |
| `D ` | Deleted, staged | Verify intentional |
| ` D` | Deleted, not staged | Restore or stage deletion |

**Clean state:** Empty output = nothing to commit.

---

### Step 3: Handle Local-Only Artifacts

These files should **never** be committed but may show as modified:

| File Pattern | Expected Behavior |
|--------------|-------------------|
| `.DS_Store` | Should be gitignored; restore if tracked |
| `.claude/settings.local.json` | Machine-specific; must be gitignored |
| `**/node_modules/**` | Rebuild artifact; gitignored |
| `**/.venv/**`, `**/venv/**` | Rebuild artifact; gitignored |
| `**/__pycache__/**` | Ephemeral; gitignored |

**If tracked despite gitignore:**
```bash
git rm --cached <file>
# Then commit the untracking
```

---

### Step 4: Stash Triage (MANDATORY)

**⚠️ Zero-stash default:** Do not use `git stash` for "clean closeout" or to avoid decisions.

**First, always check:**
```bash
git stash list
```

**If stash list is non-empty, you MUST resolve each before declaring clean:**

| Resolution | Command | When to Use |
|------------|---------|-------------|
| Convert to WIP branch | `git stash branch wip/<topic> stash@{N}` | Work worth keeping |
| Apply and commit | `git stash show -p stash@{N}` then `git stash pop` | Ready to finish |
| Drop with receipt | `git stash drop stash@{N}` | Obsolete/superseded work |

**Stash decision tree:**

```
git stash list output?
├── EMPTY: ✅ Proceed to Step 5
└── NON-EMPTY: For each stash:
    ├── Is this work still relevant?
    │   ├── YES: Convert to branch → git stash branch wip/<topic> stash@{N}
    │   └── NO: Is it superseded by committed work?
    │       ├── YES: Drop it → git stash drop stash@{N} (write receipt)
    │       └── NO: Review contents → git stash show -p stash@{N}
    └── Create receipt documenting decision
```

**If you must stash new work (emergency only):**
```bash
# Always name it with context
git stash push -m "<repo> <why> <YYYY-MM-DD>" -u

# Example:
git stash push -m "W001 blocked-by-rebase 2025-12-27" -u
```

**Preferred alternative (instead of stash):**
```bash
git switch -c wip/<topic>
git add -A && git commit -m "WIP: <description> (do not merge)"
```

---

### Step 5: Commit Verification

**Before committing:**
1. Stage intentionally: `git add -p` (interactive) or `git add <specific-files>`
2. Review staged changes: `git diff --cached`
3. Commit with meaningful message

**After committing:**
```bash
# Verify commit exists
git log --oneline -1

# Check remote sync status
git fetch origin
git rev-list --left-right --count origin/$(git branch --show-current)...HEAD
```

**Interpret count output:**
| Output | Meaning |
|--------|---------|
| `0  0` | Fully synced |
| `0  N` | N commits ahead (need to push) |
| `N  0` | N commits behind (need to pull) |
| `N  M` | Diverged (need merge/rebase) |

---

### Step 6: Evidence & Receipt Verification

**Required artifacts (session work):**

| Artifact Type | Location | Purpose |
|---------------|----------|---------|
| Change receipt | `20_receipts/` | Documents what changed and why |
| Test output | Console or `70_evidence/` | Proves changes work |
| Build artifact | `70_evidence/exports/` | Generated outputs (if applicable) |

**Receipt minimum content:**
- Timestamp (ISO 8601)
- What changed (file list or summary)
- Why it changed (ticket, request, or context)
- Verification performed (tests run, manual checks)

---

### Step 7: Multi-Repo Coordination (Full Closeout)

If session touched multiple repos:

```bash
# From workspace root
for repo in C010_standards C017_brain-on-tap; do
  echo "=== $repo ==="
  (cd "$repo" && git status --short && git log --oneline -1)
done
```

**Coordination checklist:**
- [ ] All repos committed
- [ ] Cross-repo references are consistent
- [ ] Shared artifacts (symlinks, configs) are valid
- [ ] Push order respects dependencies (upstream first)

---

## Closeout Report Template

```
SESSION CLOSEOUT REPORT
=======================
Repo:     <repo_name>
Branch:   <branch>
HEAD:     <commit_sha>
Status:   CLEAN | DIRTY (reason)

Changes This Session:
- <summary of commits>

Receipts Created:
- <receipt paths>

Open Items:
- <any deferred work>

Verification:
- Tests: PASS | FAIL | SKIPPED
- Build: PASS | FAIL | N/A
```

---

## Anti-Patterns

**Do NOT:**
- Declare "clean" without running `git status`
- Commit `.claude/settings.local.json` (contains machine-specific paths)
- Leave uncommitted changes without explicit handoff
- Force-push without warning
- Skip receipt creation for non-trivial changes

---

## Provenance

When this protocol is rendered dynamically, include:

```
---
Protocol Source: C010_standards/protocols/session_closeout_protocol.md
Protocol Version: 1.0
Loaded From: <absolute_path>
Standards Commit: <git_sha>
---
```

This enables traceability when protocols are updated.

---

*Protocol owned by C010_standards. Updates require version bump and receipt.*
