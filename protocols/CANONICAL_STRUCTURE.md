# Canonical Repository Structure Reference

**Purpose**: Single source of truth for repository folder structure during cleanup and organization tasks.

**Use this when**: Deciding where a file belongs, validating repo structure, or performing "Project Everything in Its Right Place" cleanup.

---

## Quick Reference: Allowed Top-Level Folders

| Folder | Purpose | When to Use |
|--------|---------|-------------|
| `00_admin` | Administrative files, snapshots, receipts | Always valid - compliance snapshots, admin notes |
| `00_run` | Easy button launchers | **Mandatory** for C/W series; optional for P/U |
| `10_docs` | Documentation and guides | Always valid - READMEs, guides, specs |
| `20_approvals` | Approval documentation | When tracking sign-offs and approvals |
| `20_inbox` | Incoming items to process | Temporary holding for items needing triage |
| `20_receipts` | Change receipts and evidence | Always valid - audit trail for changes |
| `30_config` | Configuration files | Always valid - JSON, YAML, TOML configs |
| `40_src` | Source code | Always valid - **production code lives here** |
| `50_data` | Data files or symlink | Symlink to `$SADB_DATA_DIR` when needed |
| `60_tests` | Test files and fixtures | When tests need separation from `40_src` |
| `70_evidence` | Evidence and artifacts | Always valid - test outputs, audit evidence |
| `80_evidence_packages` | Packaged evidence bundles | Bundled evidence for review/delivery |
| `80_reports` | Generated reports | Output from analysis or reporting tools |
| `90_archive` | Archived items | Old/deprecated code, historical content |

### Core vs Extended Folders

**Core folders (always valid in any repo):**
- `00_admin`, `00_run`, `10_docs`, `20_receipts`, `30_config`, `40_src`, `60_tests`, `70_evidence`, `90_archive`

**Extended folders (use when needed):**
- `20_approvals`, `20_inbox`, `50_data`, `80_evidence_packages`, `80_reports`

---

## Series-Specific Rules

| Series | Description | `00_run/` Requirement |
|--------|-------------|----------------------|
| **C-series** | Core Infrastructure | **MANDATORY** |
| **W-series** | Work Projects | **MANDATORY** |
| **P-series** | Personal Projects | Optional |
| **U-series** | Utility/External Tools | Optional (minimal structure) |

### Series Characteristics

**C-series (Core)** `C001`-`C099`:
- Foundational infrastructure used across multiple projects
- Changes affect downstream projects
- Often used as git submodules
- Require governance and documentation

**W-series (Work)** `W001`-`W099`:
- Work-related projects
- May have different backup/security requirements
- Clearly separated from personal projects

**P-series (Personal)** `P001`-`P999`:
- Personal experiments and tools
- May depend on C-projects
- Can be experimental or production-grade

**U-series (Utility)** `U01`-`U99`:
- External tools (not Jeremy's original code)
- NO GitHub remote
- Excluded from workspace audits

---

## Required Files

### Mandatory (Betty Protocol)
| File | Purpose |
|------|---------|
| `README.md` | Project overview (single canonical at root) |
| `rules_now.md` | Current working rules |
| `RELATIONS.yaml` | Links to C002_sadb as truth source |

### Recommended (Agent Guidance)
| File | Purpose |
|------|---------|
| `CLAUDE.md` | AI agent guidance - **read first** |
| `META.yaml` | Project metadata for compliance |
| `WHY_I_CARE.md` | Purpose and motivation |
| `ROADMAP.md` | Plans and next steps |

---

## Naming Conventions

### Projects
```
X###_kebab-case-name
```
- `X` = Series prefix (C, P, W, U)
- `###` = Number (001-999 for C/P/W, 01-99 for U)
- Name in kebab-case

**Examples:** `C001_mission-control`, `P110_knowledge-synthesis-tool`, `W002_analytics`, `U01_comfyUI`

### Folders
- Lowercase with number prefix: `00_`, `10_`, `20_`, `30_`, `40_`, `50_`, `60_`, `70_`, `80_`, `90_`
- Never create new top-level folders outside this list

### Files
- **Protocols/Standards:** `SCREAMING_SNAKE_CASE.md` (e.g., `CANONICAL_STRUCTURE.md`)
- **Documentation:** `kebab-case.md` or `Title_Case.md` depending on context
- **Source code:** Follow language conventions (snake_case for Python, camelCase for JS)

---

## Quick Decision Table: "Where Does This Go?"

| I have... | Put it in... | Notes |
|-----------|--------------|-------|
| A Python/JS source file | `40_src/` | Production code only |
| A config file (JSON, YAML) | `30_config/` | Or root if framework requires |
| A documentation file | `10_docs/` | Or root for README |
| Test outputs or artifacts | `70_evidence/` | Never commit to git |
| Old/deprecated code | `90_archive/` | Keep for reference |
| Test files/fixtures | `60_tests/` | Or `40_src/tests/` |
| Change evidence/receipts | `20_receipts/` | Audit trail |
| A launcher script | `00_run/` | `.command` (Mac), `.ps1` (Win) |
| Generated reports | `80_reports/` | Analysis outputs |
| Packaged evidence | `80_evidence_packages/` | Bundled for delivery |
| Items needing triage | `20_inbox/` | Temporary only |
| Approval documentation | `20_approvals/` | Sign-offs, confirmations |
| Data files | **EXTERNAL** | Use `$SADB_DATA_DIR`, symlink via `50_data/` |

---

## Anti-Patterns (Don't Do These)

### Structure Anti-Patterns
- **Don't nest projects** - Projects belong at root of SyncedProjects
- **Don't create new top-level folders** - Pre-commit hook will block this
- **Don't commit data to git** - Use `$SADB_DATA_DIR` with optional `50_data/` symlink
- **Don't use folders not in the allowed list** - Violates Betty Protocol

### File Anti-Patterns
- **Don't use test_/draft_/sample_ prefixes for production code** - These indicate non-production files
- **Don't assume the largest file is main** - Check `CLAUDE.md` for canonical entrypoints
- **Don't create secondary READMEs** - Single canonical README at root (stubs point to root)
- **Don't commit `.env`, `node_modules/`, `.venv/`** - Listed in `.gitignore`

### Process Anti-Patterns
- **Don't bypass guardrails without receipt** - Document in `20_receipts/` if you must
- **Don't move tracked files with `mv`** - Use `git mv` to preserve history
- **Don't leave stashes without receipt** - Convert to WIP branch or document

---

## Guardrails (Pre-commit Enforcement)

**Blocked:**
- New top-level directories
- Files > 10 MB (allowlist: `.sqlite`, `.db`)

**Warned:**
- Artifacts: `extractions/`, `tmp/`, `*.ndjson`, `*.jsonl`, `*.wav`, `run_*.py`

**Ignored (`.gitignore` baseline):**
- `.DS_Store`, `.venv/`, `data/`, `pipeline/logs/`, `chroma_data/`, `api.log`, `api.pid`, `.env`, `node_modules/`, `*-env/`

---

## Cross-References

For deeper reading on specific topics:

| Topic | Document |
|-------|----------|
| Full Betty Protocol | `protocols/betty_protocol.md` |
| Project naming & promotion | `REPOSITORY_ORGANIZATION.md` |
| Agent onboarding | `AGENT_START_HERE.md` |
| META.yaml specification | `protocols/META_YAML_SPEC.md` |
| Workspace cleanup | Betty Protocol § Workspace Cleanup Protocol |
| Git stash policy | Betty Protocol § Git Stash Policy |
| Session hygiene | Betty Protocol § Operator Standards Brief |

---

## Validation Commands

```bash
# Check for disallowed top-level folders
ls -d */ | grep -vE '^(00_|10_|20_|30_|40_|50_|60_|70_|80_|90_)'

# Find files in wrong locations (production code outside 40_src)
find . -name "*.py" -path "*/90_archive/*" -o -name "*.py" -path "*/70_evidence/*"

# Verify required files exist
for f in README.md rules_now.md RELATIONS.yaml; do [ -f "$f" ] && echo "✓ $f" || echo "✗ $f missing"; done

# Check for data files that shouldn't be committed
find . -name "*.ndjson" -o -name "*.jsonl" -o -name "*.sqlite" 2>/dev/null
```

---

*Last Updated: 2025-01-16*
*Source: Consolidated from betty_protocol.md, AGENT_START_HERE.md, REPOSITORY_ORGANIZATION.md*
*Location: C010_standards/protocols/CANONICAL_STRUCTURE.md*
