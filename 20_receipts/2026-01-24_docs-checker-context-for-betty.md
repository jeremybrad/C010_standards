# Documentation Ecosystem Context for Betty

> **Purpose**: One-off context document to help Betty understand the existing documentation infrastructure so she can help improve the docs-checker skill.
>
> **Created**: 2026-01-24
> **For**: Betty (Claude session working on docs-checker improvements)

---

## Quick Reference: Where Everything Lives

| Component | Location | Purpose |
|-----------|----------|---------|
| **docs-checker skill** | `~/.claude/skills/docs-checker/SKILL.md` (symlink) | Claude Code slash command definition |
| **Actual skill file** | `C017_brain-on-tap/.claude/skills/docs-checker/SKILL.md` | The real file (symlinked) |
| **docs.freshness.v1 profile** | `C017_brain-on-tap/brain_on_tap/profiles/docs.freshness.v1.yaml` | bbot profile that powers the audit |
| **docs_freshness source** | `C017_brain-on-tap/brain_on_tap/sources/docs_freshness.py` | Python implementation (436 lines) |
| **Tier definitions** | `C010_standards/protocols/tier3_documentation_spec.md` | Authoritative tier 1/2/3 definitions |
| **PROJECT_PRIMER protocol** | `C010_standards/protocols/project_primer_protocol.md` | How primers are built |
| **README repo card standard** | `C010_standards/protocols/readme_repo_card.md` | Extractable README blocks |
| **generate-project-primer tool** | `C021_notebooklm-mcp/src/notebooklm_mcp/primer_gen/` | Primer generation code |
| **Betty Protocol** | `C010_standards/protocols/betty_protocol.md` | Folder structure & governance |

---

## Documentation Tier System

### Tier 1: Required (Every Repo)
**Files**: `README.md`, `CHANGELOG.md`, `META.yaml`

These are non-negotiable. Every repository must have them.

### Tier 2: Extended (Active/Complex Repos)
**Files**: `CLAUDE.md`, `glossary.yaml` (in 10_docs/)
**Folders**: `10_docs/`, `20_receipts/`

Required for active development repos and W-series (client work).

### Tier 3: Deep Reference (Kitted Repos)
**Location**: `docs/{repo_name}/` or `docs/standards/`
**Required 7 Documents**:
1. `OVERVIEW.md` - System overview, ecosystem fit
2. `QUICKSTART.md` - Install, run, verify in 5 minutes
3. `ARCHITECTURE.md` - Component diagram, data flow
4. `CODE_TOUR.md` - File map, key functions
5. `OPERATIONS.md` - Run modes, workflows, troubleshooting
6. `SECURITY_AND_PRIVACY.md` - Security model, local data handling
7. `OPEN_QUESTIONS.md` - Unresolved decisions, roadmap

### Tier Classifications

| Classification | Composition | Example |
|----------------|-------------|---------|
| **simple** | Tier 1 only | Utility scripts, archived repos |
| **extended** | Tier 1 + Tier 2 | Active development repos |
| **kitted** | Tier 1 + 2 + 3 | Complex systems with full docs |

---

## How Documents Are Built

### PROJECT_PRIMER.md (Derived Artifact)

**What it is**: A single-file LLM-ready context document generated per repository.

**How it's built**: The `generate-project-primer` tool (from C021_notebooklm-mcp) gathers source documents and assembles them:

```
SOURCE DOCUMENTS                    PRIMER SECTIONS
───────────────────────────────────────────────────
META.yaml ──────────────────────► Quick Facts table
README.md (repo card) ──────────► What This Repo IS/IS NOT
CLAUDE.md ──────────────────────► Session guidance extracts
docs/{repo}/*.md (Tier 3) ──────► Full deep reference content
Git metadata ───────────────────► Provenance (SHA, timestamp)
```

**Required sections (all tiers)**:
1. Provenance - Generation metadata
2. Quick Facts - Status, owner, entry points
3. What This Repo IS - Purpose statement
4. What This Repo IS NOT - Scope boundaries
5. Responsibility Boundaries - OWNS / MUST NOT own
6. Integration Map - Dependencies table
7. Quick Routing - Intent-to-section navigation
8. Standards Snapshot - C010 rules reference

**Tier-based additions**:
- Tier 1: + README content (repo card if present)
- Tier 2: + META.yaml + CLAUDE.md extracts
- Tier 3: + All 7 deep reference docs

**Command**: `generate-project-primer <repo_id>`

### README.md Repo Card

**What it is**: An extractable block in README.md marked with BOT markers.

**Format**:
```markdown
<!-- BOT:repo_card:start -->
## What this repo is
...
## What it is not
...
(8 more required sections)
<!-- BOT:repo_card:end -->
```

**Required 10 headings**:
1. What this repo is
2. What it is not
3. When to use it
4. Entry points
5. Core architecture
6. Interfaces and contracts
7. Common workflows
8. Footguns and gotchas
9. Related repos
10. Provenance

**Validator**: `python scripts/validate_readme_repo_card.py <repo_path>`

---

## Current docs-checker Implementation

### The Skill File (`SKILL.md`)

Located at: `C017_brain-on-tap/.claude/skills/docs-checker/SKILL.md`

The skill:
1. Invokes `bbot render docs.freshness.v1`
2. Interprets the results (FRESH/STALE/MISSING)
3. Guides updates for stale docs
4. Handles PROJECT_PRIMER.md specially (regenerate, don't edit)

### The bbot Profile (`docs.freshness.v1.yaml`)

```yaml
id: docs.freshness.v1
label: "Documentation Freshness Audit"
kind: audit
agent_type: operator
status: active

sections:
  - name: freshness_report
    source: docs_freshness
    days_threshold: 30
    include_tier3: true
```

### The Source Implementation (`docs_freshness.py`)

**Key functions**:
- `fetch_docs_freshness()` - Main entry point
- `analyze_doc_freshness()` - Analyzes single document
- `get_doc_last_modified()` - Gets last mod date from git
- `get_related_commits()` - Finds commits since last update
- `suggest_updates()` - Generates update suggestions

**Freshness logic**:
- **FRESH**: No related commits AND doc is recent
- **STALE**: Related commits detected OR doc > threshold days old
- **MISSING**: Document doesn't exist
- **UNKNOWN**: File not tracked by git

**Current tier handling**:
- Tier 1: README.md, CLAUDE.md
- Tier 2: PROJECT_PRIMER.md (special SHA-based freshness check)
- Tier 3: docs/{repo_name}/*.md, docs/*.md, 10_docs/*.md

---

## What's Missing / Improvement Opportunities

### Current Gaps

1. **Tier definitions not fully aligned**: The source hardcodes tier membership rather than reading from C010 protocols

2. **No receipt guidance**: Doesn't check or suggest 20_receipts/ updates

3. **No commit hygiene**: Doesn't guide commit message format or git workflow

4. **No META.yaml freshness**: Tier 1 includes META.yaml but it's not checked

5. **No CHANGELOG.md tracking**: Another Tier 1 doc not currently audited

6. **No cross-repo awareness**: Can't audit workspace-wide documentation state

7. **Single threshold**: Same 30-day rule for all tiers (Tier 1 might need stricter)

### Potential Enhancements

1. **Tier-aware thresholds**: Different freshness rules per tier
2. **Receipt integration**: Check for recent receipts, suggest creating them
3. **Commit guidance**: Include commit message templates in output
4. **Dependency awareness**: Know that PROJECT_PRIMER depends on README, CLAUDE.md, Tier 3 docs
5. **Validation integration**: Run validators as part of freshness check
6. **Workspace mode**: Audit all repos in SyncedProjects

---

## Authority Hierarchy

When resolving conflicts about documentation requirements:

1. **C010_standards** (highest) - Workspace governance
2. **Repo-level contracts** - README repo card, META.yaml, CLAUDE.md
3. **Tier 3 docs** - The 7-doc deep reference
4. **Receipts / ADRs** - 20_receipts/, 10_docs/ADRs/
5. **Source code** - Behavioral truth
6. **PROJECT_PRIMER.md** (lowest) - Derived artifact

---

## Key Protocols to Reference

| Protocol | Path | What It Defines |
|----------|------|-----------------|
| Tier 3 Documentation Spec | `protocols/tier3_documentation_spec.md` | All tier definitions |
| Project Primer Protocol | `protocols/project_primer_protocol.md` | How primers are built |
| README Repo Card | `protocols/readme_repo_card.md` | Extractable README format |
| Tier 2 W-Series Spec | `protocols/tier2_wseries_spec.md` | W-series requirements |
| Betty Protocol | `protocols/betty_protocol.md` | Folder structure, receipts |
| Brain on Tap Eligibility | `protocols/brain_on_tap_repo_eligibility_v1.md` | Repo readiness criteria |

---

## Related Validators

| Validator | What It Checks |
|-----------|----------------|
| `validate_readme_repo_card.py` | README repo card compliance |
| `validate_tier2_compliance.py` | W-series Tier 2 requirements |
| `check_repo_contract.py` | Betty Protocol structure |
| `check_capsulemeta.py` | Capsule frontmatter |

---

## Repos Involved

| Repo | Role |
|------|------|
| **C010_standards** | Protocol definitions, validators, authority |
| **C017_brain-on-tap** | bbot engine, profiles, sources, skill files |
| **C021_notebooklm-mcp** | generate-project-primer tool |

---

## Next Steps for Improvement

1. **Read the protocols**: Start with `tier3_documentation_spec.md` and `project_primer_protocol.md`
2. **Understand the source**: Review `docs_freshness.py` implementation
3. **Identify gaps**: Compare protocol requirements vs. current implementation
4. **Design enhancements**: Decide which improvements to prioritize
5. **Update in layers**: Profile YAML → Source Python → Skill MD

---

*This document is a receipt for context-sharing. It lives in C010_standards/20_receipts/ and can be deleted after the docs-checker improvement work is complete.*
