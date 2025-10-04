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
- Allowed top level: 00_admin, 10_docs, 20_receipts, 30_config, 40_src, 70_evidence, 90_archive
- Single canonical README at repo root. Secondary READMEs are stubs that point to root.
- Required files: README.md, rules_now.md, RELATIONS.yaml
- Data policy: no data or artifacts in repo. Use $SADB_DATA_DIR with optional `50_data -> ../.links/SADB_Data` symlink for compatibility.
- RELATIONS.yaml links the repo to P002_sadb as the truth source.

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
*Protocol validated 2025-09-07: 6.6GB recovered from 8.0GB test cleanup*