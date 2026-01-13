# PROJECT_PRIMER.md Protocol

**Version**: 1.0.0
**Last Updated**: 2026-01-12
**Purpose**: Specification for single-file LLM Project context documents

---

## Overview

This protocol defines `PROJECT_PRIMER.md` - a consolidated, LLM-ready document generated per repository. The primer bundles canonical documentation into a single file optimized for manual upload to LLM Projects (ChatGPT Projects, Claude Projects, Gemini context).

**Key Principle**: The primer is a **derived artifact**. Canonical truth remains in source documents (README, META.yaml, CLAUDE.md, Tier 3 docs). If conflicts exist, source documents override.

---

## Problem Addressed

1. **Context drift** - Starting repo conversations without context leads to redundant build plans
2. **Accidental duplication** - Repos rebuild components that exist elsewhere
3. **Upload friction** - LLM Projects require file uploads; many files = high friction
4. **Missing boundaries** - No clear "this repo OWNS X, does NOT own Y" documentation

---

## Document Structure

### Required Sections (All Tiers)

| Section | Purpose |
|---------|---------|
| **Provenance** | Generation metadata (SHA, timestamp, source list) |
| **Quick Facts** | Status, owner, entry points at a glance |
| **What This Repo IS** | One paragraph purpose statement |
| **What This Repo IS NOT** | Explicit deferrals to other repos |
| **Responsibility Boundaries** | OWNS / MUST NOT own lists |
| **Integration Map** | Dependencies and interfaces |
| **Quick Routing** | Intent-to-section navigation table |
| **Standards Snapshot** | C010 rules reference |

### Tier-Based Sections

| Tier | Additional Sections |
|------|---------------------|
| **simple** | README content (repo card if present) |
| **extended** | + META.yaml + CLAUDE.md extracts |
| **kitted** | + Full Tier 3 7-pack (OVERVIEW through OPEN_QUESTIONS) |

Tier definitions align with Tier 3 Documentation Specification.

---

## Section Specifications

### Provenance (Required)

```markdown
## Provenance

- **Generated**: YYYY-MM-DD HH:MM (local)
- **Repo SHA**: <first 7 characters>
- **Generator**: generate-project-primer v<version>
- **Source Docs**:
  - README.md
  - META.yaml
  - CLAUDE.md
  - docs/{repo}/OVERVIEW.md
  - ...

> **Derived document.** If conflicts exist, source docs override this primer.
```

### Quick Facts (Required)

```markdown
## Quick Facts

| Field | Value |
|-------|-------|
| **Repo ID** | C017_brain-on-tap |
| **Status** | active |
| **Owner** | <maintainer> |
| **Series** | C (Core) |
| **Entry Point** | `python -m brain_on_tap` |
| **Port** | 8821 (if applicable) |
```

### Responsibility Boundaries (Required)

```markdown
## Responsibility Boundaries

### This Repo OWNS
- Profile resolution and rendering
- Session context injection
- Template system for prompts

### This Repo MUST NOT Own
- Credential storage (defer to C001_mission-control)
- Document sync to NotebookLM (defer to C021_notebooklm-mcp)
- Workspace standards (defer to C010_standards)
```

### Integration Map (Required)

```markdown
## Integration Map

| External System | Direction | Interface | Status |
|-----------------|-----------|-----------|--------|
| C001_mission-control | depends on | HTTP API :8820 | active |
| C010_standards | follows | protocols/* | active |
| C021_notebooklm-mcp | consumed by | notebook_map.yaml | active |
```

### Quick Routing (Required)

```markdown
## Quick Routing

| If you want to... | Read this section |
|-------------------|-------------------|
| Understand what this repo does | What This Repo IS |
| Run locally | Quickstart |
| Debug issues | Operations |
| Find specific code | Code Tour |
| Understand architecture | Architecture |
| Know security rules | Security & Privacy |
| See current roadmap | Open Questions |
```

### Standards Snapshot (Required)

```markdown
## Standards Snapshot (C010)

This repo follows workspace standards from C010_standards:
- **Betty Protocol**: Evidence in 20_receipts/, no self-certification
- **META.yaml**: Keep `last_reviewed` current
- **Cross-platform**: Commands work on macOS, Windows, Linux
- **Closeout**: Git status clean, stash triaged, receipts written

Full standards are canonical in C010_standards.
```

---

## Authority & Precedence

When resolving conflicts:

1. **C010_standards** (workspace governance)
2. **Repo-level contracts** (README repo card, META.yaml, CLAUDE.md)
3. **Tier 3 docs** (OVERVIEW through OPEN_QUESTIONS)
4. **Receipts / ADRs** (20_receipts/, 10_docs/ADRs/)
5. **Source code** (behavioral truth)
6. **PROJECT_PRIMER.md** (derived, lowest precedence)

---

## File Naming & Location

| Location | Purpose |
|----------|---------|
| `<repo_root>/PROJECT_PRIMER.md` | In-repo (primary) |
| `~/.claude/primers/<repo_id>_PROJECT_PRIMER.md` | Export location (optional) |

The primer is **gitignored by default** since it's derived. Regenerate rather than commit stale versions.

---

## Generation

### Command

```bash
generate-project-primer <repo_id>
```

### Output

```
Primer generated: /path/to/PROJECT_PRIMER.md
Hash: sha256:abc123...
Source SHA: 337cf4b
Upload status: pending (ChatGPT, Claude Projects, Gemini)
```

### Regeneration Triggers

Regenerate when:
- Any Tier 3 doc changes
- README repo card changes
- META.yaml changes
- CLAUDE.md changes
- New integration or entry point is added

---

## Tracking

Primer metadata is stored in `notebook_map.yaml` under a `primers:` section:

```yaml
primers:
  C017_brain-on-tap:
    enabled: true
    tier: kitted
    repo_sha: "04653d7"
    generated_at: "2026-01-12T18:22:11Z"
    primer_path: "PROJECT_PRIMER.md"
    primer_hash: "sha256:abc123..."
    platforms:
      chatgpt:
        status: uploaded
        uploaded_at: "2026-01-12"
      claude_projects:
        status: pending
      gemini:
        status: not_started
```

### Platform Status Values

| Status | Meaning |
|--------|---------|
| `not_started` | No upload attempted |
| `pending` | Primer exists but not uploaded |
| `uploaded` | Uploaded, hash matches |
| `stale` | Uploaded hash != current primer hash |

---

## Validation Rules

Primers must pass these checks:

| Rule | Check |
|------|-------|
| `has_provenance` | Provenance section with SHA + timestamp |
| `has_routing` | Quick Routing table present |
| `has_boundaries` | Responsibility Boundaries section present |
| `tier_complete` | All required sections for repo tier present |
| `no_absolute_paths` | Commands use relative paths or variables |
| `source_docs_exist` | All listed source docs actually exist |

---

## LLM Project Setup

### Project Instructions (paste into ChatGPT/Claude Project settings)

```
You are working inside a Project containing documentation for ONE repository.

Mission:
- PROJECT_PRIMER.md is your primary context. Read it first.
- Before proposing work, consult the primer to avoid duplicating existing components.

Rules:
1. Read Provenance + Quick Facts + Responsibility Boundaries first
2. Use Quick Routing table to navigate to relevant sections
3. If knowledge gaps remain, ask questions BEFORE proposing steps
4. Respect "MUST NOT own" boundaries - defer to listed repos
5. Reference document sections when making claims

Output:
- Be explicit about what you read vs inferred
- Include "Existing components I'm reusing" in build plans
```

### Deep Dive Kickoff Message

First message in a new Project conversation:

```
Deep dive kickoff.

1. Read PROJECT_PRIMER.md completely
2. DO NOT propose steps yet

Return:
A) Summary: what this repo IS, IS NOT, and OWNS
B) Knowledge gaps (what you cannot conclude from the primer)
C) 10-20 clarifying questions grouped by:
   - Purpose & users
   - Current state & completed work
   - Interfaces/contracts
   - Integration with other repos
   - Roadmap & priorities
D) Doc drift issues noticed (contradictions, stale refs)

After I answer: provide roadmap + integration plan + maintenance notes.
```

---

## Template

Full template for reference:

```markdown
# PROJECT PRIMER — <repo_id> <repo_name>

## Provenance

- **Generated**: YYYY-MM-DD HH:MM
- **Repo SHA**: <sha>
- **Generator**: generate-project-primer v1.0.0
- **Source Docs**:
  - README.md
  - META.yaml
  - CLAUDE.md
  - docs/<repo>/OVERVIEW.md
  - docs/<repo>/QUICKSTART.md
  - docs/<repo>/ARCHITECTURE.md
  - docs/<repo>/CODE_TOUR.md
  - docs/<repo>/OPERATIONS.md
  - docs/<repo>/SECURITY_AND_PRIVACY.md
  - docs/<repo>/OPEN_QUESTIONS.md

> **Derived document.** If conflicts exist, source docs override this primer.

---

## Quick Facts

| Field | Value |
|-------|-------|
| **Repo ID** | <repo_id> |
| **Status** | active / experimental / archived |
| **Owner** | <maintainer> |
| **Series** | P / C / W / U |
| **Entry Point** | `<command>` |
| **Port** | <port> |

---

## What This Repo IS

<One paragraph describing the repo's purpose and primary function>

---

## What This Repo IS NOT

- Does NOT <function> (that's <other_repo>'s job)
- Does NOT <function> (defer to <other_repo>)
- Does NOT <function>

---

## Responsibility Boundaries

### This Repo OWNS
- <responsibility 1>
- <responsibility 2>
- <responsibility 3>

### This Repo MUST NOT Own
- <responsibility> (defer to <repo_id>)
- <responsibility> (defer to <repo_id>)

---

## Integration Map

| External System | Direction | Interface | Status |
|-----------------|-----------|-----------|--------|
| <repo/system> | depends on / provides / consumed by | <interface> | active / planned |

---

## Quick Routing

| If you want to... | Read this section |
|-------------------|-------------------|
| Understand purpose | What This Repo IS |
| Run locally | Quickstart |
| Debug issues | Operations |
| Find code | Code Tour |
| Understand architecture | Architecture |
| Security rules | Security & Privacy |
| Current roadmap | Open Questions |

---

## README (Repo Card)

<verbatim README content or extracted repo card block>

---

## META.yaml

```yaml
<verbatim META.yaml content>
```

---

## CLAUDE.md

<key sections from CLAUDE.md>

---

## Overview

<OVERVIEW.md content>

---

## Quickstart

<QUICKSTART.md content>

---

## Architecture

<ARCHITECTURE.md content>

---

## Code Tour

<CODE_TOUR.md content>

---

## Operations

<OPERATIONS.md content>

---

## Security & Privacy

<SECURITY_AND_PRIVACY.md content>

---

## Open Questions

<OPEN_QUESTIONS.md content>

---

## Standards Snapshot (C010)

This repo follows workspace standards from C010_standards:
- **Betty Protocol**: Evidence in 20_receipts/, no self-certification
- **META.yaml**: Keep `last_reviewed` current
- **Cross-platform**: Commands work on macOS, Windows, Linux
- **Closeout**: Git status clean, stash triaged, receipts written

Full standards are canonical in C010_standards.
```

---

## Related Protocols

- **tier3_documentation_spec.md** - Source doc content specifications
- **readme_repo_card.md** - README structure for repo card extraction
- **META_YAML_SPEC.md** - META.yaml field definitions
- **cross_platform_claude_md.md** - CLAUDE.md conventions
- **betty_protocol.md** - Evidence and receipt requirements
