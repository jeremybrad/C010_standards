# Betty Protocol — Workspace Edition (v2025-09-07)

**Source:** `/Users/jeremybradford/SyncedProjects/WORKSPACE_BETTY_PROTOCOL.md`
**Consolidated into P210:** 2025-09-21
**Notes:** Text below mirrors the workspace canonical version without modification.


## Purpose
Keep every repo workable and drift-free. All artifacts live outside git. Every change leaves receipts.

## Workspace Cleanup Protocol (NEW)

### Three-Wave Cleanup System
Successfully tested 2025-09-07: 8.0GB → 1.4GB (82.5% reduction)

#### Wave 1: Containment
- Quarantine secrets to `$SADB_DATA_DIR/secure/` (chmod 600)
- Archive git-bundles, snapshots, To-Classify folders
- Update `.stignore` to prevent re-sync
- Create receipt in `_receipts/workspace_wave1_*.txt`

#### Wave 2: Classification & Cleanup
- Remove virtual environments (node_modules, *-env, .venv)
- Move conversation exports to `$SADB_DATA_DIR/conversation-exports/`
- Move ChromaDB stores to `$SADB_DATA_DIR/chromadb-archives/`
- Quarantine large binaries to `Archive/trash_*/`
- Generate manifests and duplicate reports

#### Wave 3: Finish & Lock
- Compress and deduplicate exports (gzip + SHA-1)
- Move data extractions to `$SADB_DATA_DIR/extractions/`
- Archive work data to labeled locations
- Create final manifest for manual review

### Nightly Autocontainment (Cron)
```bash
# Runs at 2:10 AM - sweeps strays to dated Archive/cleanup_*/to-classify/
10 2 * * * ROOT=$HOME/SyncedProjects bash -lc 'workspace_autocontain.sh'
```

## Canon (per repo)

> **Quick Reference:** See [`protocols/CANONICAL_STRUCTURE.md`](CANONICAL_STRUCTURE.md) for a consolidated structure reference with decision tables and validation commands.

- Allowed top level: 00_admin, 00_run, 10_docs, 20_receipts, 30_config, 40_src, 50_data, 50_reference_reports, 60_tests, 70_evidence, 80_reports, 90_archive
- Single canonical README at repo root. Secondary READMEs are stubs that point to root.
- Required files: README.md, rules_now.md, RELATIONS.yaml
- Data policy: no data or artifacts in repo. Use $SADB_DATA_DIR with optional `50_data -> ../.links/SADB_Data` symlink for compatibility.
- Easy buttons: `00_run/` contains double-clickable launchers (`.command` for macOS, `.ps1` for Windows) for common operations.
- **Series-aware enforcement**: `00_run/` is **mandatory** for C-series (Core) and W-series (Work) repos; **optional** for P-series (Projects) and U-series (Utility) repos.
- RELATIONS.yaml links the repo to C002_sadb as the truth source.

## Guardrails
- Pre-commit hook blocks: new top-level dirs, files > 10 MB (allowlist .sqlite|.db)
- Pre-commit warns: artifacts (extractions/, tmp/, *.ndjson, *.jsonl, *.wav, run_*.py)
- .gitignore baseline: .DS_Store, .venv/, data/, pipeline/logs/, chroma_data/, api.log, api.pid, .env, node_modules/, *-env/

## Space Management Rules
- **Delete Immediately**: Virtual environments (rebuildable)
- **Compress**: Conversation exports (60-70% reduction with gzip)
- **Externalize**: ChromaDB stores, large data files
- **Deduplicate**: Files >1MB by SHA-1 hash
- **Quarantine**: Unidentified files to `Archive/trash_*/` for 30 days

## Receipts & Snapshots
- `repo_snapshot.sh` writes `00_admin/SNAPSHOT_*/` with git_status, tree_L4, readme_paths, baseline counts
- Every stabilization step writes `00_admin/RECEIPTS/<step>_<ts>.txt`
- Workspace cleanup writes `_receipts/workspace_wave{1,2,3}_*.txt`
- Review packets land in `$SADB_DATA_DIR/review_packets/<ts>/`

## Branching
- Protect `main`
- Work on short-lived branches: stabilize/*, feat/*, fix/*
- Tag rollback points before structure changes

<!-- BOT:git_stash_policy:start -->
## Git Stash Policy (Zero-stash default)

**Default:** Do not use `git stash` for "clean closeout" or to avoid decisions.

### Approved uses (rare)
Use stash only for immediate context switching when Git blocks you (checkout/pull/rebase) and you must switch tasks now.

### Mandatory rules when stash is used
1) **Name it.** Always: `git stash push -m "<repo> <why> <date>" -u` (use `-u` only if needed).
2) **Triage immediately.** Same session or next session, no exceptions.
3) **Preferred resolution: stash → branch.**
   - `git stash branch wip/<topic> stash@{N}`
4) **Never let stashes age silently.**
   - If a stash exists, create a receipt that includes:
     - stash id (stash@{N})
     - summary of contents (files)
     - decision: branch/apply/drop
     - commands executed

### Closeout gate
If `git stash list` is non-empty at closeout, the session is **not "clean"** until:
- stashes are converted to WIP branches, or
- explicitly dropped with a receipt explaining why.

### Preferred alternative (instead of stash)
Use a WIP branch with a WIP commit:
- `git switch -c wip/<topic>`
- `git add -A && git commit -m "WIP: <what this is> (do not merge)"`
<!-- BOT:git_stash_policy:end -->

## Chroma policies (optional)
- Seed a minimal `sadb_policies` collection stored under `$SADB_DATA_DIR/chroma_policies`
- Include only: root README, rules_now.md, and optional Do_Dont.md, RELATIONS.yaml

## Betty Beat (private journal)
- Private entries under `$SADB_DATA_DIR/betty_beat/<repo>/<YYYY>/<YYYY-MM-DD>.md`
- In-repo stub `10_docs/BettyBeat_INDEX.md` points to the private location
- Beat entries capture what/why/decisions/risks/next + last commit summary and diffstat

## Session prelude for agents
- Load: root README, rules_now.md, RELATIONS.yaml (or pull via Chroma policies)
- Check WORKSPACE_BETTY_PROTOCOL.md for latest cleanup procedures
- Never create new top-level dirs
- Propose a change plan before file writes
- Create receipts for all operations
- Treat "baby protocol" as alias for Betty Protocol

## Verification Commands
```bash
# Check space usage
du -sh Archive/cleanup_*/to-classify/

# Find large files
find . -size +50M -type f

# Check for duplicates
find . -type f -size +1M -exec shasum {} \; | sort | uniq -d

# Review receipts
ls -la _receipts/workspace_wave*
```

---

<!-- BOT:operator_standards_brief:start -->
## Operator Standards Brief

**Purpose**: Queryable slice for dynamic injection into operator primers and closeouts.

### Folder structure (top-level)
Allowed only:
`00_admin`, `00_run`, `10_docs`, `20_receipts`, `20_approvals`, `20_inbox`, `30_config`, `40_src`, `50_data`, `50_reference_reports`, `60_tests`, `70_evidence`, `80_evidence_packages`, `80_reports`, `90_archive`

### Local-only artifacts (never commit)
- `.claude/settings.local.json`
- `.DS_Store`
- `exports/`, `logs/`, temp outputs unless explicitly routed to `70_evidence/`

### Move discipline
- Use `git mv` for tracked files (preserves history)
- Use `mv`/`rm` for untracked artifacts
- If bypassing a guardrail, leave a receipt in `20_receipts/`

### Session hygiene expectation
- Before declaring done: `git status` is empty (or acceptably clean)
- Receipts written for non-trivial operations
- Pushes synced where upstream exists
- Stash or document any WIP explicitly
<!-- BOT:operator_standards_brief:end -->

---

<!-- BOT:repo_registry_usage:start -->
## Repo Registry

**Location**: `C010_standards/registry/repos.yaml`

The canonical Repo Registry provides structured metadata about repos in the workspace. Consuming tools (e.g., C017_brain-on-tap primers) read this file to render repo context.

### Usage
- Read `repos.yaml` at runtime—do not duplicate content elsewhere
- Filter by `repo_id` to get relevant entry
- Render: purpose, contracts, interfaces, status

### Schema (required fields)
- `repo_id`: Unique identifier (e.g., `C017_brain-on-tap`)
- `name`: Human-readable name
- `purpose`: One-sentence purpose statement
- `authoritative_sources`: Paths to canonical content
- `contracts`: Commitments (APIs, formats, protocols)
- `status`: `active` | `deprecated` | `archived`

See `registry/README.md` for full schema documentation.
<!-- BOT:repo_registry_usage:end -->

---

<!-- BOT:command_discoverability:start -->
## Command Discoverability

**Policy**: CLI commands and "cheat sheet" guidance must be written to persistent locations.

### Requirements
- New CLI commands go in `docs/COMMANDS.md` (or equivalent)
- Commands must be renderable via BBOT help/commands profile
- Avoid leaving commands only in chat—they will be lost

### Persistent Locations
- Registry: `C010_standards/registry/repos.yaml` → `commands` field
- Per-repo: `docs/COMMANDS.md` or equivalent
- BBOT: Playbooks that query command documentation

### Anti-pattern
```
# BAD: Command exists only in chat history
"Run `python scripts/special_tool.py --flag` to do the thing"

# GOOD: Command documented in registry or docs
commands:
  - "python scripts/special_tool.py --flag"
```
<!-- BOT:command_discoverability:end -->

---
*Protocol validated 2025-09-07: 6.6GB recovered from 8.0GB test cleanup*
