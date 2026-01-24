# PROJECT PRIMER — C010_standards

## Provenance

- **Generated**: 2026-01-24 11:09
- **Repo SHA**: 9243928
- **Generator**: generate-project-primer v1.0.0
- **Source Docs**:
  - README.md
  - META.yaml
  - CLAUDE.md
  - docs/standards/OVERVIEW.md
  - docs/standards/QUICKSTART.md
  - docs/standards/ARCHITECTURE.md
  - docs/standards/CODE_TOUR.md
  - docs/standards/OPERATIONS.md
  - docs/standards/SECURITY_AND_PRIVACY.md
  - docs/standards/OPEN_QUESTIONS.md
  - RELATIONS.yaml

> **Derived document.** If conflicts exist, source docs override this primer.

---

## Quick Facts

| Field | Value |
|-------|-------|
| **Repo ID** | C010_standards |
| **Status** | active |
| **Owner** | Jeremy Bradford |
| **Series** | C (Core) |
| **Tier** | kitted |
| **Entry Point** | See Quickstart |
| **Port** | none |

---

## What This Repo IS

Standards, governance, and project templates for workspace

---

## What This Repo IS NOT

- **Not an application**: No runtime services, APIs, or deployable code
- **Not project-specific**: Standards here apply workspace-wide, not to one project
- **Not data storage**: No conversation exports, embeddings, or artifacts (those live in `$SADB_DATA_DIR`)
- **Not memory infrastructure**: SADB, CBFS, MyBuddy are separate repos (C002, C008, C005)
- **Not executable pipelines**: Validators are standalone tools, not part of a data pipeline

---

## Responsibility Boundaries

### This Repo OWNS
- Workspace protocols and governance rules (Betty Protocol, README repo card standard)
- Data schemas (DocMeta, CodeMeta, Houston configs)
- Classification taxonomies (topics, emotions, metadata)
- Validation tools (Houston validators, README repo card checker)
- Project registry: registry/repos.yaml (source of truth) and 70_evidence/workspace/KNOWN_PROJECTS.md (derived output)
- Bootstrap scripts for bulk repo upgrades (Ruff, testing, Claude support)
- Agent onboarding documentation (AGENT_START_HERE.md)

### This Repo MUST NOT Own
- Runtime services or deployable applications (belongs to individual project repos)
- Data storage, embeddings, or artifacts (belongs to $SADB_DATA_DIR and C003)
- Memory infrastructure pipelines (belongs to C002/C003 SADB repos)
- Project-specific configuration or code (stays in respective repos)
- Health monitoring or service dashboards (belongs to C001_mission-control)

---

## Integration Map

| External System | Direction | Interface | Status |
|-----------------|-----------|-----------|--------|
| C001_mission-control | relates to | Consumes as git submodule at external/standards/ | active |
| C017_brain-on-tap | relates to | Profile extraction uses DocMeta schema | active |
| C019_docs-site | relates to | Publishes/searches workspace docs (MkDocs + Docs RAG) | active |
| all_repos | relates to | CI validators enforce compliance workspace-wide | active |
| all | relates to | Defines standards for entire workspace | active |

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

## README

# C010_standards

**🗺️ Your Workspace Orientation & Standards Hub**

Welcome to the information center for Jeremy Bradford's development workspace. Before working with ANY repository in SyncedProjects, start here.

<!-- BOT:repo_card:start -->

## What this repo is

C010_standards is the **canonical source of truth** for workspace organization, standards, and governance across Jeremy Bradford's 66+ project ecosystem. It serves as the "info center" or "visitor center" for the workspace. It provides:

- **Protocols & Standards**: Betty Protocol (workspace governance), README repo card standard, cross-platform CLAUDE.md format
- **Schemas**: DocMeta v1.2, CodeMeta v1.0, CapsuleMeta v1.0, Houston features/tools/telemetry JSON schemas
- **Taxonomies**: Topic, emotion, and metadata classification systems
- **Validators**: Python scripts to check compliance with schemas and protocols
- **Project Registry**: Machine-readable repo metadata (`registry/repos.yaml` is source of truth; `70_evidence/workspace/KNOWN_PROJECTS.md` is auto-generated)
- **Bootstrap Scripts**: Add Ruff, testing, Claude support to repos in bulk
- **Agent Guidance**: AGENT_START_HERE.md for LLM onboarding

This is the "visitor center" that orients both humans and AI agents before they work in any other repo.

## What it is not

- **Not an application**: No runtime services, APIs, or deployable code
- **Not project-specific**: Standards here apply workspace-wide, not to one project
- **Not data storage**: No conversation exports, embeddings, or artifacts (those live in `$SADB_DATA_DIR`)
- **Not memory infrastructure**: SADB, CBFS, MyBuddy are separate repos (C002, C008, C005)
- **Not executable pipelines**: Validators are standalone tools, not part of a data pipeline

## When to use it

| Use Case | Entry Point |
|----------|-------------|
| Starting work in ANY repo | Read `AGENT_START_HERE.md` first |
| Understanding workspace structure | `70_evidence/workspace/KNOWN_PROJECTS.md` |
| Learning data flow architecture | `70_evidence/workspace/PROJECT_RELATIONSHIPS.md` |
| Checking folder structure compliance | `protocols/betty_protocol.md` |
| Validating Houston configs | `python validators/run_all.py` |
| Validating README repo cards | `python scripts/validate_readme_repo_card.py <repo>` |
| Adding cross-platform Claude support | `bash scripts/bootstrap_claude_crossplatform.sh` |
| Adding Ruff linting to repos | `bash scripts/bootstrap_ruff.sh` |
| Creating a new project | `PROJECT_TEMPLATE.md` |
| Systematic repo upgrades | `COMPREHENSIVE_PR_TEMPLATE.md` |

## Entry points

| Path | Purpose |
|------|---------|
| `AGENT_START_HERE.md` | **Required reading** for AI agents before any work |
| `protocols/` | Governance docs (betty_protocol, readme_repo_card, universal_claude_standards) |
| `protocols/capsules/` | Capsule metadata standard for handoffs and memory exports |
| `schemas/` | YAML/JSON schema definitions (docmeta, codemeta, capsulemeta, houston_*) |
| `validators/` | Python compliance checkers for Houston configs |
| `scripts/` | Bootstrap utilities + `validate_readme_repo_card.py` |
| `workspace/` | Project inventory, relationships, PR tracking |
| `taxonomies/` | Classification systems (topics, emotions, metadata) |
| `00_run/` | Double-click launchers (standards_pulse, folder_audit) |
| `examples/` | Reference implementations of schemas |
| `policy/` | Python (Ruff) and testing (pytest/jest) configs |

## Core architecture

```
C010_standards/
├── AGENT_START_HERE.md          # LLM pre-flight checklist
├── protocols/                    # Standards documents
│   ├── betty_protocol.md        # Workspace governance (non-negotiable)
│   ├── readme_repo_card.md      # README repo card standard
│   ├── universal_claude_standards.md
│   ├── cross_platform_claude_md.md
│   └── capsules/                # Capsule metadata standard
│       └── capsule_spec_v1.md
├── schemas/                      # Data contracts
│   ├── docmeta_v1.2.yaml        # Document metadata
│   ├── codemeta_v1.0.yaml       # Code metadata
│   ├── capsulemeta_v1.0.yaml    # Capsule metadata
│   └── houston_*.schema.json    # Houston agent configs
├── validators/                   # Compliance checkers
│   ├── check_houston_*.py       # 5 Houston validators
│   ├── run_all.py               # Batch runner
│   └── common.py                # Shared utilities
├── scripts/                      # Bootstrap + validation
│   ├── validate_readme_repo_card.py  # README repo card checker
│   ├── bootstrap_ruff.sh
│   └── bootstrap_claude_crossplatform.sh
├── workspace/                    # Inventory & architecture
│   ├── KNOWN_PROJECTS.md        # Auto-generated nightly
│   └── PROJECT_RELATIONSHIPS.md # Data flow diagrams
└── 00_run/                       # Easy buttons
    ├── standards_pulse.command  # macOS launcher
    └── audit_syncedprojects.command
```

**Key Integration**: This repo is a git submodule in C001_mission-control at `external/standards/`.

## Interfaces and contracts

| Interface | Format | Description |
|-----------|--------|-------------|
| `DocMeta v1.2` | YAML | Document metadata schema (required frontmatter) |
| `CodeMeta v1.0` | YAML | Code file metadata schema |
| `Houston Features` | JSON Schema | AI agent capability configuration |
| `Houston Tools` | JSON Schema | Tool pipeline definitions |
| `Houston Telemetry` | JSON Schema | Agent telemetry format |
| `CapsuleMeta v1.0` | YAML | Capsule metadata for handoffs, memory exports, activity logs |
| `Epoch v1.0` | YAML | Repo state snapshot with git HEAD and derived artifact checksums |
| `Betty Protocol` | Markdown | Folder structure + governance rules |
| `README Repo Card` | Markdown + BOT markers | Deterministic README extraction |
| `Docs Publishing` | C019 integration | Standards authored in C010; publishing/search served by C019 |

**Validator Exit Codes**:
- `0`: All checks pass
- `1`: Validation failure (one or more errors)
- `2`: Config/parse error (cannot complete validation)

## Common workflows

```bash
# 1. Validate Houston configs
python validators/run_all.py
python validators/run_all.py --pass-args --verbose

# 2. Validate README repo card
python scripts/validate_readme_repo_card.py ~/SyncedProjects/C017_brain-on-tap --strict

# 3. Run folder structure audit (double-click or CLI)
bash 00_run/audit_syncedprojects.command
# Output: 70_evidence/exports/folder_structure_audit_latest.csv

# 4. Generate standards pulse report
bash 00_run/standards_pulse.command
# Output: 70_evidence/exports/Standards_Pulse.xlsx

# 5. Bootstrap repos with Ruff linting
bash scripts/bootstrap_ruff.sh

# 6. Add cross-platform CLAUDE.md to repos
bash scripts/bootstrap_claude_crossplatform.sh --dry-run  # Preview
bash scripts/bootstrap_claude_crossplatform.sh            # Apply

# 7. Update project registry (runs nightly at 2:45 AM)
python workspace/scripts/generate_project_registry.py

# 8. Validate capsule documents
python validators/check_capsulemeta.py path/to/capsule.md
python validators/check_capsulemeta.py --strict 10_docs/examples/capsules/

# 9. Validate EPOCH.yaml (repo state snapshot)
python validators/check_epoch.py                    # Warn if missing, exit 0
python validators/check_epoch.py --require          # Exit 1 if missing
python validators/check_epoch.py --strict           # Verify repo_head matches git HEAD
```

## Footguns and gotchas

| Issue | Impact | Mitigation |
|-------|--------|------------|
| Editing KNOWN_PROJECTS.md manually | Overwritten nightly by auto-generation | Edit `generate_project_registry.py` or wait for regen |
| Ignoring AGENT_START_HERE.md | LLMs pick wrong files, create duplicates | Always read it first in any session |
| Changing schemas without version bump | Downstream validators break silently | Update version, changelog, notify affected repos |
| Running bootstrap scripts without `--dry-run` | Bulk changes across all repos | Always preview first |
| Missing `$SADB_DATA_DIR` env var | Scripts fail to find data artifacts | Set in shell profile: `export SADB_DATA_DIR="$HOME/SADB_Data"` |
| Editing registry/repos.yaml incorrectly | Registry is source of truth | Follow schema, validate before commit |

## Related repos

| Repo | Relationship |
|------|--------------|
| `C001_mission-control` | Embeds C010 as git submodule at `external/standards/` |
| `C002_sadb` | Uses Betty Protocol; source of conversation data |
| `C017_brain-on-tap` | Extracts README repo cards for LLM context |
| `C019_docs-site` | Canonical docs publishing/search surface (MkDocs + Docs RAG) |
| All P/C/W repos | Must follow Betty Protocol and folder structure |

## Provenance

- **Version**: 1.0.0
- **Last Updated**: 2026-01-17
- **Git SHA**: (run `git rev-parse --short HEAD` for current)
- **Receipts**: `20_receipts/`
- **Standard**: Self-hosting - this README passes `scripts/validate_readme_repo_card.py`

<!-- BOT:repo_card:end -->

---

## What This Is

This is the canonical source of truth for workspace organization, standards, and navigation. Think of it as the visitor center at a national park - you get your map, learn the rules, and understand where everything is before you start exploring.

**Key Resources:**
- **Workspace Standards** (Betty Protocol, repo organization)
- **Project Inventory** (KNOWN_PROJECTS.md - auto-updated nightly)
- **Memory System Architecture** (how SADB → CBFS → MyBuddy flows)
- **Schemas & Taxonomies** (DocMeta, CodeMeta, topics, emotions)
- **Validation Tools** (linters, checkers for compliance)
- **Templates** (project structure, PRs, documentation)

---

## 🤖 For AI Agents

**⚠️ STOP AND READ THIS FIRST: [AGENT_START_HERE.md](AGENT_START_HERE.md)**

This is your required pre-flight checklist. It explains:
- How to find canonical files (not test/draft/old versions)
- Common mistakes LLMs make (and how to avoid them)
- The memory system architecture (SADB vs CBFS vs MyBuddy)
- Decision trees for file selection
- When to ask instead of guess

**Quick Context for Agents:**
- 66 total projects (C### = Core, P### = Personal, W### = Work)
- Memory systems are COMPLEX - read [70_evidence/workspace/PROJECT_RELATIONSHIPS.md](70_evidence/workspace/PROJECT_RELATIONSHIPS.md)
- Data lives OUTSIDE git in `$SADB_DATA_DIR` - never commit data files
- Betty Protocol is non-negotiable - read [protocols/betty_protocol.md](protocols/betty_protocol.md)

---

## 👤 For Humans

### New to This Workspace?

Read these in order:

1. **[70_evidence/workspace/KNOWN_PROJECTS.md](70_evidence/workspace/KNOWN_PROJECTS.md)** (5 min)
   - Auto-generated nightly inventory of all 66 projects
   - Shows status, last modified, and brief description
   - Your map of what exists and where it lives

2. **[70_evidence/workspace/PROJECT_RELATIONSHIPS.md](70_evidence/workspace/PROJECT_RELATIONSHIPS.md)** (15 min)
   - How data flows between systems
   - Memory pipeline architecture (SADB → CBFS → MyBuddy)
   - Critical dependencies and execution order
   - For LLMs: How to find canonical versions

3. **[protocols/betty_protocol.md](protocols/betty_protocol.md)** (15 min)
   - Workspace governance and cleanup rules
   - Required folder structure (00_, 10_, 20_, 30_, 40_, 70_, 90_)
   - Data policy: artifacts stay outside git
   - Receipt generation requirements

4. **[REPOSITORY_ORGANIZATION.md](REPOSITORY_ORGANIZATION.md)** (10 min)
   - C/P/W series naming conventions
   - Project lifecycle (Active → Maintenance → Archived)
   - Migration procedures and standards

### Working with LLMs?

Essential documents:
- **[protocols/universal_claude_standards.md](protocols/universal_claude_standards.md)** - Standards for Claude interactions
- **[protocols/cross_platform_claude_md.md](protocols/cross_platform_claude_md.md)** - Cross-platform CLAUDE.md format
- **[PROJECT_TEMPLATE.md](PROJECT_TEMPLATE.md)** - Template for new projects
- **[COMPREHENSIVE_PR_TEMPLATE.md](COMPREHENSIVE_PR_TEMPLATE.md)** - For systematic repo upgrades

---

## Directory Layout

```
C010_standards/
├── AGENT_START_HERE.md          # ⭐ Required reading for AI agents
├── README.md                     # This file - your starting point
│
├── 00_run/                       # 🖱️ Easy Buttons (double-click launchers)
│   ├── standards_pulse.command  # macOS: Generate standards inventory
│   ├── standards_pulse.ps1      # Windows: Generate standards inventory
│   ├── audit_syncedprojects.command  # macOS: Audit folder structure
│   └── audit_syncedprojects.ps1      # Windows: Audit folder structure
│
├── 70_evidence/                  # 📊 Evidence & generated artifacts
│   └── workspace/
│       └── KNOWN_PROJECTS.md    # Auto-generated project inventory
│
├── protocols/                    # 📜 Governance & standards
│   ├── betty_protocol.md        # Workspace rules & cleanup
│   ├── universal_claude_standards.md
│   └── cross_platform_claude_md.md
│
├── schemas/                      # 📋 YAML/JSON schemas
│   ├── docmeta_v1.2.yaml        # Document metadata schema
│   ├── codemeta_v1.0.yaml       # Code metadata schema
│   └── houston_features.schema.json
│
├── taxonomies/                   # 🏷️ Classification systems
│   ├── topic_taxonomy.yaml      # Content topics
│   ├── emotion_taxonomy.yaml    # Emotional states
│   └── metadata_taxonomy.yaml   # General metadata
│
├── validators/                   # ✅ Validation tools
│   ├── check_houston_docmeta.py
│   ├── check_houston_features.py
│   └── run_all.py               # Run all validators
│
├── examples/                     # 📚 Reference implementations
│   ├── docmeta_example.yaml
│   ├── codemeta_example.yaml
│   └── houston_*_example.json
│
├── scripts/                      # 🛠️ Bootstrap & utilities
│   ├── bootstrap_ruff.sh        # Add Ruff to all repos
│   ├── bootstrap_testing.sh     # Add test standards to repos
│   └── bootstrap_claude_crossplatform.sh
│
├── tests/                        # 🧪 Validator tests
├── policy/                       # Standards & templates
│   ├── python/                  # Ruff configuration
│   └── testing/                 # Test infrastructure templates
├── 30_config/                    # Houston configuration
├── notes/                        # Planning & ADRs
└── Archive/                      # Archived legacy files
```

---

## Common Tasks

### Easy Buttons (00_run/)

The `00_run/` directory contains double-click launchers for common operations. No terminal required.

**Standards Pulse** - Generate a complete inventory of all standards:
- **macOS**: Double-click `00_run/standards_pulse.command`
- **Windows**: Right-click `00_run/standards_pulse.ps1` → Run with PowerShell
- **Output**: `70_evidence/exports/Standards_Pulse.xlsx`, `Standards_Inventory.csv`

**Folder Structure Audit** - Check all repos for Betty Protocol compliance:
- **macOS**: Double-click `00_run/audit_syncedprojects.command`
- **Windows**: Right-click `00_run/audit_syncedprojects.ps1` → Run with PowerShell
- **Output**: `70_evidence/exports/folder_structure_audit_latest.csv`

The CSV includes columns for pivoting: `repo_name`, `repo_series`, `compliant`, `missing_required_files`, `invalid_top_level_dirs`, `has_00_run`, `exceptions_applied`.

**Note**: Generated files are gitignored. Regenerate on-demand with the launchers above.

---

### 1. Find a Project

```bash
# View all projects with status
cat 70_evidence/workspace/KNOWN_PROJECTS.md

# Search for a specific project
grep -i "sadb" 70_evidence/workspace/KNOWN_PROJECTS.md
```

### 2. Understand System Dependencies

```bash
# Read the architecture document
cat 70_evidence/workspace/PROJECT_RELATIONSHIPS.md

# Or open in your browser/editor
open 70_evidence/workspace/PROJECT_RELATIONSHIPS.md
```

### 3. Validate Your Changes

```bash
# Install dependencies (first time only)
pip install -r requirements.txt

# Run all validators
python validators/run_all.py

# Run with verbose output
python validators/run_all.py --pass-args --verbose
```

### 4. Bootstrap a New Repo

```bash
# Add Ruff linting to all repos
bash scripts/bootstrap_ruff.sh

# Add cross-platform Claude support
bash scripts/bootstrap_claude_crossplatform.sh

# Preview changes (dry-run)
bash scripts/bootstrap_claude_crossplatform.sh --dry-run
```

### 5. Check Your Work Against Standards

```bash
# Does your CLAUDE.md follow the protocol?
# Check: protocols/cross_platform_claude_md.md

# Does your folder structure match Betty Protocol?
# Check: protocols/betty_protocol.md

# Does your metadata follow the schema?
python validators/check_houston_docmeta.py path/to/your/file.yaml
```

---

## Standards Hierarchy

This repo defines standards used across all projects:

### 1. Governance (Must Follow)
- **[protocols/betty_protocol.md](protocols/betty_protocol.md)** - Non-negotiable workspace rules
- **[REPOSITORY_ORGANIZATION.md](REPOSITORY_ORGANIZATION.md)** - Naming and structure
- Pre-commit hooks, guardrails, receipt generation

### 2. Documentation Standards
- **[protocols/universal_claude_standards.md](protocols/universal_claude_standards.md)** - AI agent guidance format
- **[protocols/cross_platform_claude_md.md](protocols/cross_platform_claude_md.md)** - Cross-platform CLAUDE.md
- YAML frontmatter requirements (DocMeta schema)

### 3. Metadata Schemas
- **DocMeta v1.2** - Document metadata (schemas/docmeta_v1.2.yaml)
- **CodeMeta v1.0** - Code metadata (schemas/codemeta_v1.0.yaml)
- **CapsuleMeta v1.0** - Capsule metadata for handoffs/exports (schemas/capsulemeta_v1.0.yaml)
- **Houston Features** - AI agent capabilities (schemas/houston_features.schema.json)

### 4. Taxonomies
- **Topics** - Content classification (taxonomies/topic_taxonomy.yaml)
- **Emotions** - Emotional state tracking (taxonomies/emotion_taxonomy.yaml)
- **Metadata** - General metadata terms (taxonomies/metadata_taxonomy.yaml)

### 5. Python Standards
- **Ruff** - Linting configuration (policy/python/)
- Code style enforcement across all Python projects
- Bootstrap script: `scripts/bootstrap_ruff.sh`

### 6. Testing Standards
- **pytest.ini** - Python test configuration (policy/testing/)
- **jest.config.js** - Node.js test configuration (policy/testing/)
- **70% coverage minimum** - Workspace standard threshold
- **Standard markers**: `unit`, `integration`, `slow`, `network`, `smoke`
- Bootstrap script: `scripts/bootstrap_testing.sh`

See [policy/testing/README.md](policy/testing/README.md) for full documentation.

---

## Validation Tools

### Validators (Production-Ready)

Eight validators ensure compliance with Houston configs, metadata schemas, and repository contracts:

```bash
# Run individual validators
python validators/check_houston_docmeta.py <file.yaml>
python validators/check_houston_features.py <file.json>
python validators/check_houston_models.py <file.json>
python validators/check_houston_telemetry.py <file.json>
python validators/check_houston_tools.py <file.json>
python validators/check_repo_contract.py
python validators/check_capsulemeta.py <file.md>
python validators/check_epoch.py [--require|--strict]

# Run all validators
python validators/run_all.py
```

**What They Check:**
- Schema compliance (required fields, types)
- Semantic validation (logical consistency)
- Houston-specific rules (phase transitions, tool pipelines)
- Capsule frontmatter (c010.capsule.v1)
- Repository structure (README, receipts, markers)
- Epoch state snapshots (git HEAD, primer SHA256 sync)

**Execution Contexts:** Validators fall into two categories:
- **Portable** (`repo_contract`, `capsulemeta`, `constitution`, `epoch`): Work in any repo
- **C010-context** (`houston_*`): Require `30_config/` files present in C010

Consumer repos using C010 as a submodule should use `--targets` to run only portable validators. See [validators/README.md](validators/README.md) for details.

**Testing:**
- 22 comprehensive tests with pytest
- GitHub Actions CI/CD pipeline
- Type checking with mypy
- Code coverage reporting

---

## Integration

### Submodule in C001_mission-control

This repo is integrated into Mission Control as a git submodule:

```bash
# Location in C001_mission-control
external/standards/

# Update to latest standards
cd ~/SyncedProjects/C001_mission-control
git submodule update --remote --merge
```

**Purpose:** Mission Control uses these schemas and validators to enforce consistency across all projects.

---

## Quick Reference

### Essential Files (Bookmark These)

| File | Purpose | Update Frequency |
|------|---------|------------------|
| [70_evidence/workspace/KNOWN_PROJECTS.md](70_evidence/workspace/KNOWN_PROJECTS.md) | Project inventory | Nightly (auto) |
| [70_evidence/workspace/PROJECT_RELATIONSHIPS.md](70_evidence/workspace/PROJECT_RELATIONSHIPS.md) | System architecture | As needed |
| [protocols/betty_protocol.md](protocols/betty_protocol.md) | Governance rules | Quarterly |
| [AGENT_START_HERE.md](AGENT_START_HERE.md) | AI agent guide | As needed |

### When Things Go Wrong

**Problem:** Can't find the right file/version
**Solution:** Read [70_evidence/workspace/PROJECT_RELATIONSHIPS.md](70_evidence/workspace/PROJECT_RELATIONSHIPS.md) section "For LLMs: Finding Canonical Versions"

**Problem:** Validator fails but you don't know why
**Solution:** Run with verbose: `python validators/run_all.py --pass-args --verbose`

**Problem:** Project structure doesn't match Betty Protocol
**Solution:** Read [protocols/betty_protocol.md](protocols/betty_protocol.md) and compare folder layout

**Problem:** AI is using old/test files
**Solution:** Make sure it read [AGENT_START_HERE.md](AGENT_START_HERE.md) first

---

## Contributing

### Before Making Changes

1. Create a branch: `git checkout -b feat/descriptive-name`
2. Make changes following Betty Protocol
3. Run validators: `python validators/run_all.py`
4. Update relevant documentation (README, protocols, etc.)
5. Create a PR (don't merge directly to main)

### Standards Updates

Changes to schemas, protocols, or taxonomies require:
- [ ] Version bump (if breaking change)
- [ ] Update CHANGELOG.md
- [ ] Test validators still pass
- [ ] Notify affected projects (if breaking)
- [ ] Update examples to match new schema

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

---

## Maintenance

### Auto-Generated Content

**70_evidence/workspace/KNOWN_PROJECTS.md** is generated nightly by:
```bash
python workspace/scripts/generate_project_registry.py
```

Runs via cron at 2:45 AM daily. Manual trigger:
```bash
bash workspace/scripts/update-registry.sh
```

### Status Indicators

- ✅ **Active** - In current use, well-maintained
- 🔄 **Maintenance** - Stable, infrequent updates
- 📦 **Archived** - Historical, read-only
- 🚧 **In Development** - Under active construction

---

## Philosophy: "No Belief Without Receipts"

Everything in this workspace follows a core principle:

> **Every change leaves evidence. Every decision is documented. Every artifact has provenance.**

This isn't bureaucracy - it's how we stay sane managing 66 projects and thousands of files. When you follow these standards, you're helping:
- **Future you** understand why decisions were made
- **Other AI agents** find the right files without guessing
- **The workspace** stay organized as it grows

Leave breadcrumbs. Document your reasoning. Create receipts.

---

## Additional Resources

### Quick Start Guides
- [QUICK_START_GUIDE.md](QUICK_START_GUIDE.md) - Common workflows
- [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - Command cheat sheet
- [PROJECT_TEMPLATE.md](PROJECT_TEMPLATE.md) - New project structure

### Templates & Examples
- [COMPREHENSIVE_PR_TEMPLATE.md](COMPREHENSIVE_PR_TEMPLATE.md) - Systematic repo upgrades
- [examples/](examples/) - Schema examples and reference implementations

### Planning & History
- [notes/ROADMAP.md](notes/ROADMAP.md) - Future plans
- [notes/CHANGELOG.md](notes/CHANGELOG.md) - Version history
- [notes/ADR/](notes/ADR/) - Architecture decision records

### Advanced Topics
- [notes/HOUSTON_INFERENCE.md](notes/HOUSTON_INFERENCE.md) - AI agent inference plans
- [notes/HOUSTON_TOOLING.md](notes/HOUSTON_TOOLING.md) - Tool pipeline design
- [notes/AGENT_PLAYBOOK.md](notes/AGENT_PLAYBOOK.md) - Houston retrieval strategies

---

## Next Steps

### Phase 3 (In Progress)
1. [x] Draft migration checklist for schema adoption - [protocols/schema_migration_checklist.md](protocols/schema_migration_checklist.md)
2. [ ] Expose standards in Mission Control UI/docs
3. [x] Add schema versioning policy - [protocols/schema_versioning_policy.md](protocols/schema_versioning_policy.md)
4. [x] Complete validator test coverage (96 tests passing)
5. [x] Generate API documentation for validators - [validators/API.md](validators/API.md)

### Phase 4 (Future)
1. [ ] Consolidate SADB ecosystem (address sprawl documented in PROJECT_RELATIONSHIPS.md)
2. [ ] Implement M2/M3 pipeline stages (memory consolidation/validation)
3. [ ] Integrate P190 metadata extraction into canonical pipeline
4. [ ] Automated compliance checking (pre-commit hooks for all repos)

---

## Questions?

**For AI Agents:** Re-read [AGENT_START_HERE.md](AGENT_START_HERE.md) - the answer is probably there.

**For Humans:** Check [70_evidence/workspace/PROJECT_RELATIONSHIPS.md](70_evidence/workspace/PROJECT_RELATIONSHIPS.md) or ask Jeremy.

**For Validators:** Run with `--verbose` flag for detailed error messages.

---

*Last Updated: 2026-01-17*
*Maintained by: Jeremy Bradford & Claude*

_All downstream repositories should treat this repo as the authoritative metadata spec. Updates here require versioning, changelog, and communication across projects._


---

## META.yaml

```yaml
# Project metadata for C010_standards
# Auto-generated by Claude - agents should keep this current

project:
  repo_id: C010_standards
  owner: Jeremy Bradford
  last_reviewed: 2026-01-17
  summary: "Standards, governance, and project templates for workspace"
  status: active
  series: C
  port: none  # No runtime service - pure standards/config repo

folders:
  00_admin: "Administrative files and snapshots"
  00_run: "Double-click launchers"
  10_docs: "Documentation"
  20_receipts: "Change receipts"
  30_config: "Configuration"
  Archive: "Archived items"
  docs: "Additional documentation"
  examples: "Template examples"
  notes: "Development notes"
  policy: "Policy documents"
  prompts: "Prompt templates"
  protocols: "Protocol definitions"
  schemas: "Data schemas"
  scripts: "Utility scripts"
  taxonomies: "Classification taxonomies"
  tests: "Test suite"
  validators: "Validation tools"
  workspace: "Workspace utilities"

files:
  Makefile: "Build automation"
  CLAUDE.md: "Claude Code guidance"
  README.md: "Project documentation"
  AGENT_START_HERE.md: "Agent onboarding"
  AGENTS.md: "Agent documentation"
  CONTRIBUTING.md: "Contribution guidelines"
  PROJECT_TEMPLATE.md: "New project template"
  QUICK_START_GUIDE.md: "Quick start guide"
  AUDIT_CHECKLIST.md: "Audit checklist"
  pyproject.toml: "Python project config"
  protocols/capsules/capsule_spec_v1.md: "Capsule standard v1 specification"
  schemas/capsulemeta_v1.0.yaml: "Capsule metadata schema template"
  validators/check_capsulemeta.py: "Capsule frontmatter validator"

relates_to:
  - C001_mission-control: "Consumes as git submodule at external/standards/"
  - C017_brain-on-tap: "Profile extraction uses DocMeta schema"
  - C019_docs-site: "Publishes/searches workspace docs (MkDocs + Docs RAG)"
  - all_repos: "CI validators enforce compliance workspace-wide"
  - all: "Defines standards for entire workspace"

maintainer_notes:
  - "Central source of truth for workspace conventions"
  - "Templates used when creating new P/C/W projects"

```

---

## CLAUDE.md

# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

C010_standards is the canonical source of truth for workspace-wide metadata standards, YAML schemas, taxonomies, and protocol definitions. It anchors the Betty Protocol, DocMeta/CodeMeta schemas, Houston configuration, and validation tooling used across Mission Control, SADB, and infrastructure projects.

**Location**: `~/SyncedProjects/C010_standards`
**Consumed by**: C001_mission-control (as git submodule at `external/standards`)

## Platform Compatibility

This workspace syncs between macOS and Windows via Syncthing. Commands are provided in cross-platform format where possible.

**Environment**:
- **macOS/Linux**: `~/SyncedProjects` paths, bash/zsh shells
- **Windows**: `C:\Users\jerem\SyncedProjects` paths, PowerShell (primary) or Git Bash

**Path Conventions**:
- Python and most modern tools accept forward slashes (`/`) on all platforms
- Examples use forward slashes by default - works on Windows PowerShell and macOS/Linux
- Backslash (`\`) alternatives noted only when specifically required

**Command Compatibility**:
- Use `python` (not `python3`) - works cross-platform
- Prefer `python -m module.command` for tool execution
- Shell scripts (`.sh`) require bash - native on macOS/Linux, needs Git Bash on Windows
- PowerShell scripts (`.ps1`) are Windows-only

**Virtual Environments**:
```bash
# Create (cross-platform)
python -m venv venv

# Activate (platform-specific)
source venv/bin/activate              # macOS/Linux/Git Bash
venv\Scripts\Activate.ps1             # Windows PowerShell
```

**Common Paths**:
```bash
# Project root (absolute)
~/SyncedProjects/C010_standards           # macOS/Linux/Git Bash
C:\Users\jerem\SyncedProjects\C010_standards  # Windows PowerShell

# Prefer relative paths when already in workspace:
cd C010_standards                     # Works everywhere from workspace root
```

**Tool Preferences**:
- File operations: Use Claude Code built-in tools (Read/Edit/Write) rather than shell commands (cat/sed/echo)
- Search: Use Grep tool rather than grep/rg commands
- Find files: Use Glob tool rather than find command

**Service Management**:
```bash
# Docker (cross-platform)
docker ps
docker start service-name

# Process inspection (platform-specific)
ps aux | grep name                    # macOS/Linux
Get-Process | Where-Object {$_.Name -like "*name*"}  # PowerShell
```

### Windows Filename Compatibility (CRITICAL)

**This workspace syncs to Windows via SyncThing. NEVER create files or directories with Windows-incompatible names.**

**Forbidden in filenames:**
- Reserved characters: `: * ? " < > | \ /`
- Reserved names: `CON`, `PRN`, `AUX`, `NUL`, `COM1-9`, `LPT1-9`
- Trailing dots or spaces
- Control characters (including `\r` in macOS Icon files)

**Common mistakes to avoid:**
- ISO 8601 timestamps with colons: `2025-10-28T05:19:05Z` - Use dashes instead: `2025-10-28T05-19-05Z`
- Files named `nul` (Windows reserved name)
- macOS folder Icon files (contain `\r`) - these are handled by `.stignore`

**Validation:**
```bash
# Check a directory for Windows-incompatible names
python validators/check_windows_filename.py /path/to/scan

# Workspace-wide scan (from _scripts/)
python _scripts/scan_windows_filenames.py --all
```

**If you create a receipt or artifact with a timestamp, use this format:**
- Good: `receipt_2025-10-28T05-19-05Z.md`
- Bad: `receipt_2025-10-28T05:19:05Z.md`

---
**Note**: This project follows the [Cross-Platform CLAUDE.md Standard](protocols/cross_platform_claude_md.md) from C010_standards.

## Architecture

### Core Components

**Schemas (`schemas/`)** - Versioned metadata templates:
- `docmeta_v1.2.yaml` - Document metadata schema with routing, governance, and entity tracking
- `codemeta_v1.0.yaml` - Code artifact metadata (repos, scripts, libraries)
- `houston_features.schema.json` - JSON schema for Houston feature toggles and trust phases

**Taxonomies (`taxonomies/`)** - Controlled vocabularies:
- `topic_taxonomy.yaml` - Technical topics (monitoring, deployment, infra, etc.)
- `content_taxonomy.yaml` - Document types and categorization
- `emotion_taxonomy.yaml` - Emotional context tagging
- `universal_terms.yaml` - Canonical terminology and synonyms

**Validators (`validators/`)** - Phase 2 production tooling (COMPLETE):
- `check_houston_docmeta.py` - Enforce routing tags and taxonomy alignment (YAML/MD parsing)
- `check_houston_features.py` - Validate feature config against JSON schema and trust phases
- `check_houston_tools.py` - Verify tool pipeline consistency and dangerous ops gating
- `check_houston_models.py` - Check deployment permissions against trust phases
- `check_houston_telemetry.py` - Ensure telemetry freshness, latency, and fallback loops
- `run_all.py` - Orchestration harness (stops on first failure)

**Available Validators** (registered in `validators/__init__.py`):
- `houston_docmeta` - Document metadata validation
- `houston_features` - Feature configuration validation
- `houston_tools` - Tool pipeline validation
- `houston_models` - Model deployment validation
- `houston_telemetry` - Telemetry health validation
- `capsulemeta` - Capsule frontmatter validation (c010.capsule.v1)

**Houston Config (`30_config/`)** - Mission Control agent configuration:
- `houston-features.json` - Feature toggles, agency levels, trust building phases
- `houston-tools.json` - Tool pipelines, capability flags, phase gating

**Governance (`00-Governance/`)** - Historical backups and migration tooling:
- `YAML Official/` - Official taxonomy versions
- `YAML_Backup_20250713/` - Backup snapshots from July 2025
- `Scripts/` - Canvas migration and sorting utilities for Notion migration

## Common Commands

### Running Validators

```bash
# Run all validators (platform-agnostic - recommended)
python validators/run_all.py

# Run specific validators
python validators/run_all.py --targets houston_docmeta houston_features

# Individual validator with verbose output
python validators/check_houston_features.py --verbose

# Output to JSON for CI integration
python validators/check_houston_docmeta.py --json-output 70_evidence/docmeta_results.json

# Telemetry with custom staleness threshold
python validators/check_houston_telemetry.py --max-age 600  # 10 minutes
```

**Platform Notes**:
- Commands work on Windows (PowerShell/cmd), macOS, and Linux
- Use forward slashes (`validators/run_all.py`) - Python handles path conversion
- On Windows with backslash preference: `python validators\run_all.py` also works

**Current State**: All 5 validators are fully implemented (Phase 2 complete). They exit 0 on pass, 1 on validation failure, 2 on config errors. Include verbose mode, JSON output, and remediation suggestions.

### Schema Validation

Houston features config is validated against `schemas/houston_features.schema.json` using jsonschema library:
```bash
python validators/check_houston_features.py --schema schemas/houston_features.schema.json
```

Install dependencies: `pip install pyyaml jsonschema` (optional - validators warn if missing)

### Testing Taxonomy Changes

When modifying taxonomies:
1. Verify YAML syntax: `python -c "import yaml; yaml.safe_load(open('taxonomies/topic_taxonomy.yaml'))"`
2. Run DocMeta validator to check Houston documents against updated taxonomy:
   ```bash
   python validators/check_houston_docmeta.py --taxonomy taxonomies/topic_taxonomy.yaml --verbose
   ```
3. Update consuming projects (Mission Control, SADB) if terms change

### Ruff Bootstrap Tooling

C010_standards provides workspace-wide Python linting standards:

```bash
# Bootstrap Ruff config to all repos in workspace (Unix/macOS)
bash scripts/bootstrap_ruff.sh

# Bootstrap to specific directory (Unix/macOS)
bash scripts/bootstrap_ruff.sh /path/to/workspace

# Windows (Git Bash recommended)
bash scripts/bootstrap_ruff.sh
# Or specify Windows path
bash scripts/bootstrap_ruff.sh C:/Users/username/SyncedProjects
```

**Template location**: `policy/python/pyproject.ruff.template.toml`
**What it does**: Adds Ruff configuration to any git repo in SyncedProjects that doesn't already have `[tool.ruff]` section
**Receipt tracking**: Creates timestamped receipt in `00_admin/RECEIPTS/ruff_*.txt`

**Note**: Assumes Ruff is already installed (`brew install ruff` on macOS, `pipx install ruff` cross-platform)

### Submodule Management

C010_standards is consumed by Mission Control as a git submodule. When making changes to schemas or validators:

```bash
# In Mission Control repository
cd ~/SyncedProjects/C001_mission-control           # macOS/Linux
cd C:\Users\jerem\SyncedProjects\C001_mission-control  # Windows

# Update submodule to latest C010_standards
git submodule update --remote --merge

# Commit the submodule pointer update
git add external/standards
git commit -m "chore: update standards submodule"
```

**CI Integration**: Mission Control's `.github/workflows/standards.yml` automatically runs C010 validators on PRs

## Houston Configuration Guidelines

### Feature Toggles (`30_config/houston-features.json`)

**Trust Building Phases** - Houston operates in gradual phases:
- **Phase 1 (Observation)**: `supervisory` agency level, basic monitoring only
- **Phase 2 (Collaboration)**: `advisory` level, IDE integration, proactive alerts
- **Phase 3 (Partnership)**: `autonomous` level, full agency with emergency protocols

**Critical Rules**:
- `agency_levels.current_level` must match the phase's `agency_level`
- `autonomous.can_deploy_updates` requires `current_phase >= 3`
- `safety_controls.destructive_actions.require_password` must be `true` when `current_level` is `autonomous`
- `gradual_trust_building.auto_advance` is `false` by default - phases advance manually
- Phase advancement requires receipt entry in `notes/CHANGELOG.md` with pattern `Phase <n> activated`

**Audio/Visual Theme**: Mission Control retro console aesthetic with radio static effects, CRT scanlines, LED indicators. TTS engine is local with southern ops personality.

### Tool Pipelines (`30_config/houston-tools.json`)

- `phase_settings.current_phase` must be ≤ `gradual_trust_building.current_phase` from `houston-features.json`
- Phase 3 operations (`kill_processes`, `system_shutdown`) should not appear in Phase 1/2 overrides
- VPS tools require real endpoint (not placeholder `example.com`) before enabling

## Metadata Standards

### DocMeta v1.2 Tagging for Houston

Documents targeting Houston agent retrieval must include:

```yaml
doc:
  projects:
    - "Mission Control"
    - "P210"
  topics:
    - "monitoring"  # from taxonomies/topic_taxonomy.yaml
routing:
  tags:
    - "agent:houston"
    - "sensitivity:internal"
connections:
  related_docs:  # required when routing.tags contains playbook:success
    - "<sha256 or path>"
```

**Topic Validation**: All `doc.topics` values must exist in `taxonomies/topic_taxonomy.yaml`. Common Houston topics: monitoring, deployment, infra, automation, orchestration.

### CodeMeta v1.0 Usage

For code artifacts (scripts, repos, libraries):

```yaml
code:
  repo: "https://github.com/..."
  language: "python"
  dependencies:
    - name: "yaml"
      version: "6.0"
```

See `schemas/codemeta_v1.0.yaml` for full template.

## File Conventions

### Naming
- Versioned schemas: lowercase with underscores (`docmeta_v1.2.yaml`)
- Keep source attribution comments at top of YAML files
- Markdown docs start with level-1 heading

### YAML Comments
All imported YAML files include provenance:
```yaml
# Source: ../P002_sadb/10_docs/SADB_DocMeta_Schema_v1.2.md
# Attribution: SADB knowledge base metadata schema maintained by Jeremy Bradford.
```

### Updates
- Update `notes/CHANGELOG.md` when touching canonical schemas or taxonomies
- Reference affected files and upstream sources in commit body
- Include diff snippets for schema changes

## Validator Architecture

All validators follow a consistent pattern:

**CLI Contract**:
- Accept paths/configs as arguments with sensible defaults
- Exit 0 on pass, 1 on validation failure, 2 on config/parse errors
- Support `--verbose` for detailed output
- Support `--json-output` for CI integration
- Provide actionable remediation suggestions on failure

**Common Structure**:
```python
def cli(argv: List[str] | None = None) -> int:
    args = parse_args(argv or [])
    config = load_config(args.config)

    all_errors = []
    all_errors.extend(validate_rule_1(config, args.verbose))
    all_errors.extend(validate_rule_2(config, args.verbose))

    if all_errors:
        print(f"❌ Validation FAILED ({len(all_errors)} issues)")
        # Print remediation suggestions
        return 1
    else:
        print("✅ Validation passed")
        return 0
```

**Registry**: Update `validators/__init__.py` `AVAILABLE_VALIDATORS` when adding new validators

## Integration Points

### Consuming Projects
- **Mission Control** (`C001_mission-control`): Consumes via git submodule at `external/standards`
- **SADB** (`C002_sadb`): DocMeta/CodeMeta templates, taxonomy lookups
- **Betty Mirror** (`P001_bettymirror`): Protocol enforcement, lint rules
- **Infrastructure** (various): Standard taxonomies for tagging via Ruff bootstrap

### Schema Consumers
See `notes/SCHEMA_CONSUMERS.md` for complete inventory of which projects depend on each schema version.

### Houston Integration
- Interface blueprint: `notes/HOUSTON_INTERFACE.md`
- Inference routing: `notes/HOUSTON_INFERENCE.md`
- Agent playbook: `notes/AGENT_PLAYBOOK.md`
- Tooling plan: `notes/HOUSTON_TOOLING.md`
- Model bootstrap: `notes/scripts/MODEL_BOOTSTRAP.md`

## Roadmap

**Phase 1 (Complete)**: Consolidation of schemas, taxonomies, protocols from SADB and Betty Mirror

**Phase 2 (Complete)**: All 5 validators implemented, Ruff baseline deployed, C001 integration via submodule

**Phase 3 (In Progress)**: Adoption across repos, Houston interface prototyping, schema versioning policy

See `notes/ROADMAP.md` for detailed task breakdown.

## Important Notes

- **No build system**: Pure schema/config repository, no compilation required
- **Python 3.11+**: Validators use modern type hints (`list[str] | None`)
- **YAML as source of truth**: Markdown schema docs are reference only
- **Houston is not a chatbot**: It's a Mission Control operations agent with gradual trust phases
- **Taxonomy changes are breaking**: Update consuming projects when modifying controlled vocabularies
- **Validators are production-ready**: Exit 0 on pass, 1 on fail, 2 on config/parse error - use in CI workflows
- **Dependencies optional**: Validators warn if PyYAML/jsonschema missing but still function

## Troubleshooting

### Import Errors When Running Validators

**Symptom**: `ModuleNotFoundError` or import failures

**Solution**: Ensure you're running validators from the repository root:

```bash
# Navigate to repo root first
cd ~/SyncedProjects/C010_standards           # macOS/Linux
cd C:\Users\jerem\SyncedProjects\C010_standards  # Windows

# Then run validators
python validators/run_all.py
```

Validators automatically add the repo root to `sys.path`, but must be run from the correct directory.

### Missing Dependencies

**Symptom**: Warnings about missing `pyyaml` or `jsonschema`

**Solution**: Install optional dependencies:

```bash
pip install pyyaml jsonschema
```

Note: Validators will still run without these (with warnings), but validation will be limited.

### YAML Syntax Errors

**Symptom**: `yaml.scanner.ScannerError` when modifying taxonomies

**Solution**: Validate YAML syntax before running validators:

```bash
# Quick syntax check
python -c "import yaml; yaml.safe_load(open('taxonomies/topic_taxonomy.yaml'))"

# If successful, no output = valid YAML
```

Common YAML issues:
- Inconsistent indentation (use spaces, not tabs)
- Missing quotes around values with special characters
- Trailing spaces on lines

### Validator Exit Codes

- **0**: All checks passed
- **1**: Validation failure (check output for specific errors)
- **2**: Configuration/parse error (file not found, invalid JSON/YAML)

### Path Issues on Windows

**Symptom**: File not found errors on Windows

**Solution**: Python accepts forward slashes on Windows:

```bash
# These both work on Windows
python validators/run_all.py          # Recommended (cross-platform)
python validators\run_all.py          # Also valid
```

### Schema Version Mismatches

**Symptom**: Documents fail validation after schema updates

**Solution**: Check which schema version is in use:

```bash
# View schema consumers and versions
cat notes/SCHEMA_CONSUMERS.md

# Update consuming projects to match new schema version
```

See "Integration Points > Schema Consumers" for affected projects.

## Betty Protocol Compliance

All work follows Betty Protocol evidence-driven development:
1. Document non-trivial changes in `20_receipts/` (when applicable)
2. Update `notes/CHANGELOG.md` for schema modifications
3. Never auto-commit - only when explicitly requested
4. Report blockers transparently in validator output
5. Keep README and CHANGELOG accurate when behavior changes
6. Run validators before committing Houston config changes

## META.yaml Contract

This repo uses META.yaml for project metadata. See `~/SyncedProjects/C010_standards/protocols/META_YAML_SPEC.md` for full spec.

**Agent responsibility:** Update META.yaml when adding/removing folders or key files, and set `last_reviewed` to today's date.


---

## Overview

**Last Updated**: 2026-01-12
**Version**: 1.0.0

## What Is C010_standards?

C010_standards is the canonical source of truth for workspace-wide standards, governance, and organization across the 66+ project ecosystem. It defines protocols, schemas, taxonomies, and validation tooling that ensure consistency and quality across all repositories.

## Ecosystem Position

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          SyncedProjects Ecosystem                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                      C010_standards (This Repo)                       │   │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────────┐  │   │
│  │  │ Protocols  │  │  Schemas   │  │ Taxonomies │  │   Validators   │  │   │
│  │  │ (11 docs)  │  │ (3 specs)  │  │ (8 files)  │  │  (6 checkers)  │  │   │
│  │  └────────────┘  └────────────┘  └────────────┘  └────────────────┘  │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                    │                                         │
│                    ┌───────────────┼───────────────┐                        │
│                    ▼               ▼               ▼                        │
│  ┌─────────────────────┐ ┌─────────────────┐ ┌─────────────────────────┐   │
│  │   C001_mission-     │ │ C017_brain-on-  │ │    All P/C/W Repos      │   │
│  │      control        │ │      tap        │ │  (Betty Compliance)     │   │
│  │  (Embeds as git     │ │ (Extracts repo  │ │                         │   │
│  │    submodule)       │ │    cards)       │ │  66+ repositories       │   │
│  └─────────────────────┘ └─────────────────┘ └─────────────────────────┘   │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Core Components

| Component | Purpose | Location |
|-----------|---------|----------|
| **Protocols** | Governance rules and standards definitions | `protocols/` |
| **Schemas** | Data contracts for metadata and configuration | `schemas/` |
| **Taxonomies** | Controlled vocabularies for classification | `taxonomies/` |
| **Validators** | Compliance checking tools | `validators/` |
| **Registry** | Project metadata and relationships | `registry/` |
| **Houston Config** | Agent feature toggles and trust phases | `30_config/` |

## Key Capabilities

### 1. Betty Protocol Governance
- Non-negotiable folder structure requirements (00_, 10_, 20_, etc.)
- Receipt-driven evidence documentation
- Data policy enforcement (artifacts outside git)
- Pre-commit hooks and guardrails

### 2. Metadata Standards
- DocMeta v1.2 for document metadata with routing and governance
- CodeMeta v1.0 for code artifact tracking
- Houston configuration schemas for agent behavior

### 3. Taxonomy Management
- Topic taxonomy for technical classification
- Content taxonomy for document types
- Emotion taxonomy for context tagging
- Universal terms with synonym disambiguation

### 4. Validation Suite
- Houston validators (docmeta, features, tools, models, telemetry)
- Repository contract compliance checking
- README repo card validation
- Orchestrated validation harness

### 5. Project Registry
- Structured metadata for all 66+ projects
- Lifecycle tracking (Active → Maintenance → Archived)
- Relationship mapping between repos

## Operating Modes

| Mode | Description | Use Case |
|------|-------------|----------|
| **Reference** | Consult standards and schemas | Starting new projects, understanding requirements |
| **Validation** | Run compliance checks | Pre-commit, CI/CD, periodic audits |
| **Bootstrap** | Apply standards to repos | New repo setup, standardization campaigns |
| **Governance** | Update protocols and schemas | Standards evolution, version bumps |

## Integration Points

| System | Integration Type | Status |
|--------|-----------------|--------|
| C001_mission-control | Git submodule at `external/standards/` | Active |
| C017_brain-on-tap | README repo card extraction | Active |
| C019_docs-site | Docs publishing/search (MkDocs + Docs RAG) | Active |
| All P/C/W repos | Betty Protocol compliance | Active |
| CI/CD workflows | Validator execution | Active |
| NotebookLM | Documentation sync | Active |

## Docs Publishing Model

Standards documentation follows a clear separation of concerns:

| Layer | Repo | Responsibility |
|-------|------|----------------|
| **Authoring** | C010_standards | Source of truth for protocols, schemas, taxonomies |
| **Publishing** | C019_docs-site | MkDocs site build, static hosting |
| **Search** | C019_docs-site | Docs RAG API (FAISS index, semantic retrieval) |
| **UI Client** | C001_mission-control | Optional `/docs` endpoint consuming C019 |

### How Updates Propagate

1. **Source Change**: Edit protocols/schemas/docs in C010_standards
2. **Export Trigger**: C019's `DOCS_GLOBS` patterns detect changes
3. **Build**: `mkdocs build` regenerates static site
4. **Index**: `rag-export` + `rag-index` updates FAISS vectors
5. **Serve**: RAG API (port 8123) and MkDocs site (port 8085) reflect changes

### Do Not

- Build ad-hoc docs sites in random repos
- Duplicate MkDocs config or FAISS indexing inside C010
- Move docs authoring out of C010 into C019

## Why C010_standards?

- **Single Source of Truth** - One place for all workspace governance
- **Evidence-Driven** - "No belief without receipts" philosophy
- **AI-Ready** - Standards optimized for both human and AI agent consumption
- **Scalable** - Supports 66+ repos with consistent structure
- **Validated** - Automated compliance checking prevents drift

## Related Documentation

- [QUICKSTART.md](QUICKSTART.md) - Get started with standards
- [ARCHITECTURE.md](ARCHITECTURE.md) - System design details
- [OPERATIONS.md](OPERATIONS.md) - Day-to-day workflows


---

## Quickstart

**Last Updated**: 2026-01-12
**Version**: 1.0.0

Get oriented with workspace standards in 5 minutes.

## Prerequisites

- Git
- Python 3.11+ (for validators)
- Access to SyncedProjects workspace

## Quick Start

### 1. Clone or Navigate

```bash
cd ~/SyncedProjects/C010_standards
```

### 2. Read Agent Pre-Flight (Required for AI Agents)

```bash
cat AGENT_START_HERE.md
```

This document contains the mandatory checklist before operating in any repo.

### 3. Understand Betty Protocol

```bash
cat protocols/betty_protocol.md
```

Core governance rules:
- Folder structure: `00_admin/`, `10_docs/`, `20_receipts/`, `30_config/`, `40_src/`, `70_evidence/`, `90_archive/`
- Every change produces documented evidence
- Artifacts stay outside git repos
- Receipts required for non-trivial work

## Configuration

### For Mission Control Integration

C001_mission-control embeds standards as a git submodule:

```bash
cd ~/SyncedProjects/C001_mission-control
git submodule update --init external/standards
```

### For New Projects

Use the project template to ensure compliance:

```bash
# Copy template structure
cp -r ~/SyncedProjects/C010_standards/PROJECT_TEMPLATE.md ./
```

## First Operations

### Run All Validators

```bash
# Run from repo root
cd ~/SyncedProjects/C010_standards
python validators/run_all.py
```

Exit codes:
- `0` - All checks pass
- `1` - Validation failure
- `2` - Config/parse error

### Validate a Single Aspect

```bash
# Check Houston features
python validators/check_houston_features.py --config 30_config/houston-features.json

# Check repository contract
python validators/check_repo_contract.py --repo ~/SyncedProjects/P050_ableton-mcp
```

### Check README Repo Card

```bash
python scripts/validate_readme_repo_card.py ~/SyncedProjects/C001_mission-control/README.md
```

## Key Documents to Read

| Document | Purpose | When to Read |
|----------|---------|--------------|
| `AGENT_START_HERE.md` | Agent pre-flight checklist | Before any AI agent work |
| `protocols/betty_protocol.md` | Core governance rules | Starting any project |
| `protocols/tier3_documentation_spec.md` | Documentation standards | Creating docs |
| `schemas/docmeta_v1.2.yaml` | Document metadata schema | Tagging documents |
| `taxonomies/topic_taxonomy.yaml` | Topic classification | Categorizing content |

## Troubleshooting

### Validator Fails with Import Error

```bash
# Run from repo root (not validators directory)
cd ~/SyncedProjects/C010_standards
python -c "import yaml, jsonschema"  # Check dependencies
```

### Missing Betty Protocol Folders

```bash
# Create required structure
mkdir -p 00_admin 10_docs 20_receipts 30_config 40_src 70_evidence 90_archive
```

### Unknown Taxonomy Term

```bash
# Check universal terms for synonyms
grep -i "your_term" taxonomies/universal_terms.yaml
```

## Next Steps

- [OPERATIONS.md](OPERATIONS.md) - Day-to-day workflows
- [ARCHITECTURE.md](ARCHITECTURE.md) - System design
- [CODE_TOUR.md](CODE_TOUR.md) - Navigate the codebase


---

## Architecture

**Last Updated**: 2026-01-12
**Version**: 1.0.0

## System Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           C010_standards                                     │
│                    Workspace Standards & Governance Hub                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                        PROTOCOLS LAYER                               │    │
│  │  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌────────────┐  │    │
│  │  │    Betty     │ │   Tier 3     │ │   Session    │ │   Cross-   │  │    │
│  │  │   Protocol   │ │    Docs      │ │  Closeout    │ │  Platform  │  │    │
│  │  │  (core gov)  │ │   (specs)    │ │  (handoff)   │ │  (compat)  │  │    │
│  │  └──────────────┘ └──────────────┘ └──────────────┘ └────────────┘  │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                    │                                         │
│  ┌─────────────────────────────────┼─────────────────────────────────┐      │
│  │                        SCHEMAS LAYER                               │      │
│  │  ┌──────────────┐ ┌──────────────┐ ┌──────────────────────────┐   │      │
│  │  │   DocMeta    │ │   CodeMeta   │ │    Houston Features      │   │      │
│  │  │    v1.2      │ │    v1.0      │ │    (JSON Schema)         │   │      │
│  │  │  (routing,   │ │  (repos,     │ │  (trust phases, agency,  │   │      │
│  │  │  governance) │ │   scripts)   │ │   feature toggles)       │   │      │
│  │  └──────────────┘ └──────────────┘ └──────────────────────────┘   │      │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                    │                                         │
│  ┌─────────────────────────────────┼─────────────────────────────────┐      │
│  │                      TAXONOMIES LAYER                              │      │
│  │  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────────────┐   │      │
│  │  │ Topic  │ │Content │ │Emotion │ │Metadata│ │ Universal Terms│   │      │
│  │  │  Tax   │ │  Tax   │ │  Tax   │ │  Tax   │ │ (synonyms,     │   │      │
│  │  │        │ │        │ │        │ │        │ │  disambig)     │   │      │
│  │  └────────┘ └────────┘ └────────┘ └────────┘ └────────────────┘   │      │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                    │                                         │
│  ┌─────────────────────────────────┼─────────────────────────────────┐      │
│  │                      VALIDATORS LAYER                              │      │
│  │  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────────┐  │      │
│  │  │  Houston   │ │  Houston   │ │  Houston   │ │    Repo        │  │      │
│  │  │  DocMeta   │ │  Features  │ │Tools/Models│ │   Contract     │  │      │
│  │  │  Checker   │ │  Checker   │ │  Checkers  │ │   Checker      │  │      │
│  │  └────────────┘ └────────────┘ └────────────┘ └────────────────┘  │      │
│  │                         │                                          │      │
│  │                  ┌──────┴──────┐                                   │      │
│  │                  │  run_all.py │                                   │      │
│  │                  │ (orchestrate)│                                   │      │
│  │                  └─────────────┘                                   │      │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                    │                                         │
│  ┌─────────────────────────────────┼─────────────────────────────────┐      │
│  │                       REGISTRY LAYER                               │      │
│  │  ┌──────────────────────────────────────────────────────────────┐ │      │
│  │  │                      repos.yaml                               │ │      │
│  │  │  - 66+ project metadata entries                               │ │      │
│  │  │  - Lifecycle tracking (active/maintenance/archived)          │ │      │
│  │  │  - Relationship mapping                                       │ │      │
│  │  └──────────────────────────────────────────────────────────────┘ │      │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Core Principles

1. **Single Source of Truth** - All workspace standards originate here
2. **Evidence-Driven** - "No belief without receipts" philosophy
3. **Layered Architecture** - Protocols → Schemas → Taxonomies → Validators
4. **Composable Validation** - Individual checkers can run standalone or orchestrated
5. **Version Control** - Schemas are versioned (DocMeta v1.2, CodeMeta v1.0)

## Component Details

### Protocols (`protocols/`)

Core governance documents that define how the workspace operates.

**Key Files:**
- `betty_protocol.md` - Non-negotiable governance rules
- `tier3_documentation_spec.md` - Canonical documentation structure
- `session_closeout_protocol.md` - Session handoff procedures
- `cross_platform_claude_md.md` - CLAUDE.md format spec
- `META_YAML_SPEC.md` - Project metadata contract

### Schemas (`schemas/`)

Data contracts that define metadata structures.

**DocMeta v1.2** (`docmeta_v1.2.yaml`):
```yaml
# Document metadata with routing and governance
routing:
  primary_audience: [internal, external, all]
  visibility: [public, private, restricted]
governance:
  owner: string
  review_cycle: duration
entities:
  mentions: [entity_ids]
```

**Houston Features** (`houston_features.schema.json`):
```json
{
  "trust_phases": ["supervised", "advisory", "autonomous"],
  "agency_level": "advisory",
  "features": {
    "auto_commit": false,
    "dangerous_ops": ["delete", "force_push"]
  }
}
```

### Taxonomies (`taxonomies/`)

Controlled vocabularies for consistent classification.

| Taxonomy | Purpose | Entry Count |
|----------|---------|-------------|
| `topic_taxonomy.yaml` | Technical topics | ~50 terms |
| `content_taxonomy.yaml` | Document types | ~20 types |
| `emotion_taxonomy.yaml` | Emotional context | ~15 emotions |
| `universal_terms.yaml` | Synonym registry | ~100 terms |
| `disambiguation_rules.yaml` | Context resolution | ~30 rules |

### Validators (`validators/`)

Python-based compliance checkers with standard exit codes.

**Validator Pattern:**
```python
def validate(config_path: str) -> int:
    """
    Returns:
        0 - Validation passed
        1 - Validation failed
        2 - Config/parse error
    """
```

**Available Validators:**
- `check_houston_docmeta.py` - DocMeta routing and taxonomy
- `check_houston_features.py` - Feature configuration
- `check_houston_tools.py` - Tool pipeline consistency
- `check_houston_models.py` - Model deployment permissions
- `check_houston_telemetry.py` - Telemetry freshness
- `check_repo_contract.py` - Repository structure

## Data Flow

### Validation Flow

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  Config File │────▶│   Validator  │────▶│  Exit Code   │
│  (JSON/YAML) │     │   (Python)   │     │  (0/1/2)     │
└──────────────┘     └──────────────┘     └──────────────┘
                            │
                            ▼
                     ┌──────────────┐
                     │   Console    │
                     │   Output     │
                     │  (details)   │
                     └──────────────┘
```

### Standards Consumption Flow

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  C010_standards │────▶│  Consumer Repo  │────▶│   Compliance    │
│   (protocols,   │     │  (applies       │     │   Check         │
│    schemas)     │     │   standards)    │     │  (pass/fail)    │
└─────────────────┘     └─────────────────┘     └─────────────────┘
        │
        ▼
┌─────────────────┐
│   Git Submodule │
│   (embedded in  │
│    C001)        │
└─────────────────┘
```

### Registry Update Flow

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Nightly Job   │────▶│  Scan Repos     │────▶│  Update         │
│   (cron)        │     │  (META.yaml)    │     │  repos.yaml     │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                                                        │
                                                        ▼
                                                ┌─────────────────┐
                                                │ KNOWN_PROJECTS  │
                                                │     .md         │
                                                └─────────────────┘
```

## Integration Points

| Component | Integration Method | Purpose |
|-----------|--------------------|---------|
| C001_mission-control | Git submodule | Embedded standards reference |
| C017_brain-on-tap | README repo card | Project metadata extraction |
| CI/CD pipelines | Validator execution | Automated compliance |
| Pre-commit hooks | Script invocation | Local validation |
| NotebookLM | Doc sync | AI knowledge ingestion |

## Related Documentation

- [CODE_TOUR.md](CODE_TOUR.md) - Navigate the codebase
- [OPERATIONS.md](OPERATIONS.md) - Day-to-day operation
- [OVERVIEW.md](OVERVIEW.md) - System overview


---

## Code Tour

**Last Updated**: 2026-01-12
**Version**: 1.0.0

Navigate the C010_standards codebase efficiently.

## Quick Reference

| I want to... | Look at... |
|--------------|------------|
| Understand workspace governance | `protocols/betty_protocol.md` |
| Create Tier 3 documentation | `protocols/tier3_documentation_spec.md` |
| Define document metadata | `schemas/docmeta_v1.2.yaml` |
| Classify content by topic | `taxonomies/topic_taxonomy.yaml` |
| Run compliance checks | `validators/run_all.py` |
| Find a project's metadata | `registry/repos.yaml` |
| Configure agent behavior | `30_config/houston-features.json` |
| Set up a new repo | `PROJECT_TEMPLATE.md` |
| Understand agent pre-flight | `AGENT_START_HERE.md` |

## Directory Map

```
C010_standards/
├── 00_admin/                    # Governance policies
├── 10_docs/                     # Documentation artifacts
├── 20_receipts/                 # Change receipts (148+ entries)
│   └── YYYY-MM-DD_description.md
├── 30_config/                   # Configuration files
│   ├── houston-features.json    # Feature toggles and trust phases
│   └── houston-tools.json       # Tool pipeline configuration
├── docs/                        # Tier 3 documentation
│   └── standards/               # This folder
├── protocols/                   # Standards definitions (11 docs)
│   ├── betty_protocol.md        # Core governance rules
│   ├── tier3_documentation_spec.md  # Doc standards
│   ├── session_closeout_protocol.md # Session handoff
│   ├── cross_platform_claude_md.md  # CLAUDE.md format
│   ├── META_YAML_SPEC.md        # Metadata contract
│   └── ...
├── registry/                    # Project registry
│   ├── repos.yaml               # All project metadata
│   ├── schema.md                # Registry data model
│   └── README.md                # Usage guide
├── schemas/                     # Data contracts
│   ├── docmeta_v1.2.yaml        # Document metadata
│   ├── codemeta_v1.0.yaml       # Code metadata
│   └── houston_features.schema.json
├── scripts/                     # Utilities
│   ├── bootstrap_ruff.sh        # Add Ruff to repos
│   ├── bootstrap_claude_crossplatform.sh
│   └── validate_readme_repo_card.py
├── taxonomies/                  # Controlled vocabularies
│   ├── topic_taxonomy.yaml      # Technical topics
│   ├── content_taxonomy.yaml    # Document types
│   ├── emotion_taxonomy.yaml    # Emotional context
│   ├── universal_terms.yaml     # Synonyms
│   └── disambiguation_rules.yaml
├── validators/                  # Compliance checkers
│   ├── run_all.py               # Orchestration harness
│   ├── check_houston_docmeta.py
│   ├── check_houston_features.py
│   ├── check_houston_tools.py
│   ├── check_houston_models.py
│   ├── check_houston_telemetry.py
│   └── check_repo_contract.py
├── workspace/                   # Workspace-level docs
│   ├── KNOWN_PROJECTS.md        # Auto-generated nightly
│   └── PROJECT_RELATIONSHIPS.md # System architecture
├── AGENT_START_HERE.md          # Required pre-flight
├── CLAUDE.md                    # Claude Code guidance
├── CONTRIBUTING.md              # Contribution guide
├── META.yaml                    # Project metadata
├── PROJECT_TEMPLATE.md          # New repo template
└── README.md                    # Main entry point
```

## Key Entry Points

### Validator Orchestrator (`validators/run_all.py`)

```python
# Runs all validators in sequence, stops on first failure
def main():
    validators = [
        "check_houston_features.py",
        "check_houston_tools.py",
        "check_houston_models.py",
        "check_houston_telemetry.py",
        "check_houston_docmeta.py",
    ]
    for validator in validators:
        exit_code = run_validator(validator)
        if exit_code != 0:
            sys.exit(exit_code)
    sys.exit(0)
```

### README Repo Card Validator (`scripts/validate_readme_repo_card.py`)

```python
# Extracts and validates repo card from README
def validate_repo_card(readme_path: str) -> bool:
    """
    Checks for BOT markers and required fields:
    - Project ID (C###, P###, W###)
    - Status (active, maintenance, archived)
    - Purpose (1-2 sentence description)
    """
```

## Configuration

### Houston Features (`30_config/houston-features.json`)

```json
{
  "trust_phase": "advisory",
  "agency_level": "advisory",
  "features": {
    "auto_commit": false,
    "auto_push": false,
    "dangerous_operations": {
      "enabled": false,
      "allowed": ["soft_reset"]
    }
  },
  "phase_gates": {
    "supervised": ["all"],
    "advisory": ["delete", "force_push"],
    "autonomous": []
  }
}
```

### Project Registry (`registry/repos.yaml`)

```yaml
repositories:
  C001_mission-control:
    id: C001
    name: mission-control
    status: active
    tier: kitted
    path: ~/SyncedProjects/C001_mission-control
    relationships:
      - embeds: C010_standards
```

## Common Patterns

### Validator Pattern

```python
#!/usr/bin/env python3
"""Houston validator for [aspect]."""

import sys
import yaml
import argparse

def validate(config: dict) -> list[str]:
    """Returns list of validation errors."""
    errors = []
    # ... validation logic
    return errors

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    args = parser.parse_args()

    with open(args.config) as f:
        config = yaml.safe_load(f)

    errors = validate(config)
    if errors:
        for e in errors:
            print(f"ERROR: {e}")
        sys.exit(1)

    print("OK: All checks passed")
    sys.exit(0)

if __name__ == "__main__":
    main()
```

### Receipt Pattern

```markdown
# Receipt: [Description]

**Date**: YYYY-MM-DD
**Agent**: Claude [Model]
**Project**: C010_standards

## Summary

[What was done]

## Changes

- [Change 1]
- [Change 2]

## Verification

[How to verify]
```

## Development Commands

```bash
# Run all validators (from repo root)
python validators/run_all.py

# Validate single aspect
python validators/check_houston_features.py --config 30_config/houston-features.json

# Bootstrap Ruff on a repo
bash scripts/bootstrap_ruff.sh ~/SyncedProjects/P050_ableton-mcp

# Validate README repo card
python scripts/validate_readme_repo_card.py ~/SyncedProjects/C001_mission-control/README.md
```

## Test Files

| Test Area | Location | Description |
|-----------|----------|-------------|
| Validators | `validators/*.py` | Each validator is self-testing |
| Schemas | `schemas/*.yaml` | Validated by jsonschema |
| Repo Card | `scripts/validate_readme_repo_card.py` | README extraction test |

## Related Documentation

- [ARCHITECTURE.md](ARCHITECTURE.md) - System design
- [OPERATIONS.md](OPERATIONS.md) - Day-to-day operation
- [OVERVIEW.md](OVERVIEW.md) - System overview


---

## Operations

**Last Updated**: 2026-01-12
**Version**: 1.0.0

Day-to-day operation of C010_standards.

## Operating Modes

### Reference Mode (Primary)

```bash
# Consult standards before starting work
cat protocols/betty_protocol.md
cat protocols/tier3_documentation_spec.md
```

Use when starting new projects or reviewing requirements.

### Validation Mode

```bash
# Run all Houston validators (from repo root)
python validators/run_all.py
```

Use for pre-commit checks, CI/CD, and periodic audits.

### Bootstrap Mode

```bash
# Apply Ruff config to a repo
bash scripts/bootstrap_ruff.sh ~/SyncedProjects/P050_ableton-mcp

# Add cross-platform Claude support
bash scripts/bootstrap_claude_crossplatform.sh ~/SyncedProjects/P050_ableton-mcp
```

Use when standardizing repos or setting up new projects.

### Governance Mode

```bash
# Update a protocol
vi protocols/betty_protocol.md

# Bump schema version
vi schemas/docmeta_v1.3.yaml  # Create new version
```

Use when evolving standards (requires careful review).

## Daily Workflows

### Session Startup (AI Agents)

1. Read `AGENT_START_HERE.md` (mandatory pre-flight)
2. Check `protocols/betty_protocol.md` for current governance
3. Verify Houston trust phase in `30_config/houston-features.json`

### Health Check

```bash
# Run validator suite
python validators/run_all.py --config 30_config/houston-features.json
```

| Result | Status |
|--------|--------|
| Exit 0 | All checks pass |
| Exit 1 | Validation failure - review output |
| Exit 2 | Config/parse error - check file syntax |

### Adding a New Protocol

1. Create protocol document in `protocols/`
2. Add reference in `README.md`
3. Create receipt in `20_receipts/`
4. Update CHANGELOG.md

```bash
# Example
vi protocols/new_protocol.md
echo "- Added new_protocol.md" >> CHANGELOG.md
```

### Updating a Taxonomy

1. Edit taxonomy file in `taxonomies/`
2. Validate against schema (if applicable)
3. Create change receipt

```bash
# Add term to topic taxonomy
vi taxonomies/topic_taxonomy.yaml
# Verify format
python -c "import yaml; yaml.safe_load(open('taxonomies/topic_taxonomy.yaml'))"
```

### Recovery from Validation Failure

When validator fails:

```bash
# 1. Read error output
python validators/check_houston_features.py --config 30_config/houston-features.json

# 2. Fix configuration
vi 30_config/houston-features.json

# 3. Re-run validation
python validators/check_houston_features.py --config 30_config/houston-features.json
```

## Common Operations

**Check repo compliance:**
```bash
python validators/check_repo_contract.py --repo ~/SyncedProjects/P050_ableton-mcp
```

**Validate README repo card:**
```bash
python scripts/validate_readme_repo_card.py ~/SyncedProjects/C001_mission-control/README.md
```

**List all projects:**
```bash
cat 70_evidence/workspace/KNOWN_PROJECTS.md
```

**Check project relationships:**
```bash
cat workspace/PROJECT_RELATIONSHIPS.md
```

**Find a taxonomy term:**
```bash
grep -i "term" taxonomies/universal_terms.yaml
```

## Resource Management

### File Counts

| Category | Approximate Count |
|----------|-------------------|
| Protocols | 11 documents |
| Schemas | 3 versioned specs |
| Taxonomies | 8 files |
| Validators | 6 checkers |
| Receipts | 148+ entries |
| Registry entries | 66+ repos |

### Storage

- Repository size: ~5MB (excluding receipts archive)
- No external data dependencies
- No runtime services

## Troubleshooting Quick Reference

### Validation Issues

| Symptom | Fix |
|---------|-----|
| `ImportError: yaml` | Install PyYAML: `pip install pyyaml` |
| `ImportError: jsonschema` | Install: `pip install jsonschema` |
| Exit code 2 | Check YAML/JSON syntax in config file |
| Exit code 1 | Review validation errors in output |

### Schema Issues

| Symptom | Fix |
|---------|-----|
| Unknown field in DocMeta | Check `schemas/docmeta_v1.2.yaml` for valid fields |
| Invalid routing value | Must be: `internal`, `external`, or `all` |
| Missing required field | Check schema for required properties |

### Taxonomy Issues

| Symptom | Fix |
|---------|-----|
| Term not recognized | Check `taxonomies/universal_terms.yaml` for synonyms |
| Disambiguation needed | Consult `taxonomies/disambiguation_rules.yaml` |
| New term needed | Add to appropriate taxonomy file |

## Tool Categories

### Read-Only
- `cat protocols/*.md` - Read protocols
- `cat schemas/*.yaml` - Read schemas
- `python validators/*.py` - Run validators (no file changes)
- `grep` through taxonomies

### Modification
- Edit protocols (governance changes)
- Update schemas (version bumps)
- Add taxonomy terms
- Create receipts

### Administrative (Require Care)
- Schema version changes (affects all consumers)
- Protocol amendments (workspace-wide impact)
- Registry updates (project tracking)

## Log Locations

| Log | Location | Purpose |
|-----|----------|---------|
| Change receipts | `20_receipts/` | Audit trail |
| Validator output | stdout | Validation results |
| Nightly registry | `70_evidence/workspace/KNOWN_PROJECTS.md` | Project list |

## Upgrading Standards

### Minor Update (patch)

```bash
# 1. Make changes
vi protocols/betty_protocol.md

# 2. Update version in META.yaml
vi META.yaml  # version: 1.0.1

# 3. Create receipt
vi 20_receipts/$(date +%Y-%m-%d)_update_description.md

# 4. Commit
git add -A && git commit -m "chore: update betty protocol"
```

### Schema Version Bump

```bash
# 1. Create new version file
cp schemas/docmeta_v1.2.yaml schemas/docmeta_v1.3.yaml

# 2. Update version in new file
vi schemas/docmeta_v1.3.yaml

# 3. Update consumers (notify via CHANGELOG)
vi CHANGELOG.md

# 4. Create receipt documenting changes
```

## Related Documentation

- [QUICKSTART.md](QUICKSTART.md) - Initial setup
- [ARCHITECTURE.md](ARCHITECTURE.md) - System design
- [SECURITY_AND_PRIVACY.md](SECURITY_AND_PRIVACY.md) - Security model


---

## Security & Privacy

**Last Updated**: 2026-01-12
**Version**: 1.0.0

Security model and data protection for C010_standards.

## Security Principles

1. **No Secrets Stored** - Standards repo contains no credentials or sensitive data
2. **Public by Design** - All protocols and schemas are meant to be shared
3. **Audit Trail** - All changes documented in receipts
4. **Controlled Vocabularies** - Taxonomies prevent ambiguity and injection
5. **Validation Before Trust** - Houston validators enforce compliance

## Repository Security

### What This Repo Contains

| Content Type | Sensitivity | Notes |
|--------------|-------------|-------|
| Protocols | Public | Governance documentation |
| Schemas | Public | Data contracts |
| Taxonomies | Public | Controlled vocabularies |
| Validators | Public | Python compliance checkers |
| Registry | Internal | Project metadata (no secrets) |
| Configuration | Internal | Feature toggles (no credentials) |

### What This Repo Does NOT Contain

| Content Type | Where It Lives |
|--------------|----------------|
| API keys | C001_mission-control vault |
| Passwords | Never in any repo |
| Personal data | Not stored |
| Private credentials | Environment variables only |

## Houston Configuration Security

### Trust Phases

```json
{
  "trust_phases": ["supervised", "advisory", "autonomous"],
  "current_phase": "advisory"
}
```

| Phase | Description | Dangerous Ops |
|-------|-------------|---------------|
| **Supervised** | Human approves all actions | All blocked |
| **Advisory** | Agent suggests, human executes | Most blocked |
| **Autonomous** | Agent executes with limits | Minimal blocking |

### Phase Gates

Operations gated by trust phase:

| Operation | Supervised | Advisory | Autonomous |
|-----------|------------|----------|------------|
| File read | Allowed | Allowed | Allowed |
| File write | Approval | Allowed | Allowed |
| Git commit | Approval | Allowed | Allowed |
| Git push | Blocked | Approval | Allowed |
| Force push | Blocked | Blocked | Approval |
| Delete files | Blocked | Approval | Approval |

### Feature Toggles

```json
{
  "features": {
    "auto_commit": false,
    "auto_push": false,
    "dangerous_operations": {
      "enabled": false
    }
  }
}
```

## Data Privacy

### What Data is Processed

| Data Type | Processing |
|-----------|------------|
| Project metadata | Aggregated in registry |
| Document routing | Classification only |
| Taxonomy terms | Lookup and validation |
| Validation results | Console output only |

### What Data is NOT Collected

- Personal information
- Usage analytics
- Telemetry (beyond local Houston metrics)
- External service calls

## Validation Security

### Validator Behavior

All validators:
- Read configuration files (no network)
- Output to stdout only
- Return exit codes (0/1/2)
- Make no file modifications

### Input Validation

```python
# Validators use safe YAML loading
config = yaml.safe_load(file)  # Not yaml.load()

# JSON schema validation
jsonschema.validate(config, schema)
```

## Threat Model

### Mitigated Threats

| Threat | Mitigation |
|--------|------------|
| Malicious protocol injection | Git history + review |
| Invalid taxonomy terms | Schema validation |
| Configuration tampering | Houston validators |
| Unauthorized standards changes | Protected branches + receipts |
| Schema version confusion | Explicit versioning (v1.2, v1.3) |

### Accepted Risks

| Risk | Acceptance Rationale |
|------|---------------------|
| Standards publicly visible | Intentionally public for transparency |
| Validator bypass | Enforcement at CI/CD level |
| Local config modification | User's machine, user's choice |

### Out of Scope

| Risk | Notes |
|------|-------|
| Code execution vulnerabilities | Validators are read-only |
| Network attacks | No network connections |
| Authentication bypass | No authentication system |

## Security Checklist

### Initial Setup

- [ ] Verify no secrets in commit history
- [ ] Confirm Houston features are conservative
- [ ] Enable protected branches on main

### Ongoing

- [ ] Review protocol changes before merge
- [ ] Validate schema changes against consumers
- [ ] Audit receipts periodically
- [ ] Keep validator dependencies updated

## Incident Response

### Accidental Secret Commit

1. **Immediately**: Remove from HEAD
   ```bash
   git reset HEAD~1
   git push --force-with-lease  # Only if not yet pushed
   ```

2. **If pushed**: Rotate the credential immediately

3. **Document**: Create receipt documenting incident

4. **Prevent**: Add to `.gitignore`

### Invalid Standard Published

1. **Identify**: Which protocol/schema affected
2. **Assess**: Impact on consuming repos
3. **Fix**: Create corrected version
4. **Notify**: Update CHANGELOG with notice
5. **Document**: Receipt with timeline and fix

### Validator Producing False Positives

1. **Verify**: Reproduce the issue
2. **Analyze**: Check validator logic
3. **Fix**: Update validator code
4. **Test**: Verify against known good configs
5. **Document**: Receipt with fix details

## Audit Trail

All changes to standards tracked in:
- Git commit history
- `20_receipts/` directory (148+ entries)
- CHANGELOG.md

Receipt format ensures:
- Date and agent identification
- Summary of changes
- Verification steps
- Cross-references to related work

## Related Documentation

- [ARCHITECTURE.md](ARCHITECTURE.md) - System design
- [OPERATIONS.md](OPERATIONS.md) - Day-to-day operation
- [OPEN_QUESTIONS.md](OPEN_QUESTIONS.md) - Unresolved decisions


---

## Open Questions

**Last Updated**: 2026-01-12
**Version**: 1.0.0

Unresolved decisions, known limitations, and future considerations.

## Architecture Questions

### Schema Versioning Strategy

**Current State**: Schemas use simple version suffixes (docmeta_v1.2.yaml, codemeta_v1.0.yaml)

**Question**: Should we adopt semantic versioning with breaking change indicators?

| Option | Pros | Cons |
|--------|------|------|
| Keep current (v1.2) | Simple, familiar | No breaking change signal |
| SemVer (1.2.0) | Industry standard | More complex filenames |
| Date-based (2026-01) | Clear timeline | Less intuitive |

**Resolution**: Pending - current approach works for now

### Validator Orchestration

**Current State**: `run_all.py` stops on first failure

**Question**: Should validators continue and report all failures?

| Option | Pros | Cons |
|--------|------|------|
| Stop on first | Fast feedback | May hide other issues |
| Run all, report all | Complete picture | Slower, more output |
| Configurable | Flexible | More complex |

**Resolution**: Pending - may add `--continue-on-error` flag

## Known Limitations

### Protocol Limitations

| Limitation | Impact | Workaround |
|------------|--------|------------|
| No protocol inheritance | Each protocol standalone | Copy shared sections |
| Manual sync to consumers | Standards drift possible | CI/CD checks |
| No protocol deprecation process | Old protocols linger | Manual cleanup |

### Taxonomy Limitations

| Limitation | Impact | Workaround |
|------------|--------|------------|
| Flat hierarchy only | No nested topics | Use compound terms |
| No multilingual support | English only | N/A |
| No versioned taxonomies | Breaking changes risky | Careful additions |

### Validator Limitations

| Limitation | Impact | Workaround |
|------------|--------|------------|
| Python 3.11+ required | Older environments fail | Specify version |
| No parallel execution | Slower for many repos | Run selectively |
| Console output only | No structured reports | Pipe to file |

## Security Considerations

### Houston Trust Phase Automation

**Question**: Should trust phase advancement be automated based on metrics?

**Current Approach**: Manual phase changes only

**Potential Improvements**:
- Auto-advance after N successful operations
- Auto-demote on validation failures
- Configurable thresholds

**Resolution**: Manual preferred for safety

### Taxonomy Injection Prevention

**Question**: How to prevent malicious taxonomy entries?

**Current Approach**: Git review + protected branches

**Potential Improvements**:
- Automated term validation
- Blocklist for dangerous patterns
- Schema-based constraints

**Resolution**: Current approach sufficient for internal use

## Feature Roadmap Questions

### Multi-Workspace Support

**Current State**: Single workspace (SyncedProjects) assumed

**Question**: Should standards support multiple independent workspaces?

**Considerations**:
- Paths currently hardcoded to `~/SyncedProjects`
- Registry assumes single workspace
- Would require configuration layer

**Resolution**: Not planned - single workspace sufficient

### Protocol Testing Framework

**Current State**: No automated protocol testing

**Question**: Should we add tests that verify protocol compliance?

**Considerations**:
- Protocols are documentation, not code
- Validators partially cover this
- Would need example repos

**Resolution**: Partial coverage via validators; full framework not planned

### Taxonomy API

**Current State**: Taxonomies are static YAML files

**Question**: Should we provide a lookup API?

**Considerations**:
- Would enable runtime validation
- Adds service dependency
- Current grep-based lookup works

**Resolution**: Not planned - YAML files sufficient

## Integration Questions

### NotebookLM Sync Frequency

**Current State**: Manual sync via MCP tools

**Question**: Should Tier 3 docs auto-sync on commit?

**Considerations**:
- Requires webhook or CI/CD integration
- NotebookLM API rate limits apply
- Manual control preferred for now

**Resolution**: Manual sync preferred

### Cross-Repo Validation

**Current State**: Validators run per-repo

**Question**: Should we validate cross-repo relationships?

**Considerations**:
- Registry contains relationship data
- Would catch broken references
- Requires workspace-wide scan

**Resolution**: Partial - registry validates relationships

## Performance Questions

### Large Registry Performance

**Current State**: 66+ repos in single repos.yaml

**Question**: Will performance degrade at 200+ repos?

**Current Approach**: Simple YAML load

**Potential Improvements**:
- Index by project ID
- Split by series (C/P/W)
- Database backend

**Resolution**: Not yet an issue - monitor as workspace grows

### Validator Parallelization

**Current State**: Sequential validator execution

**Question**: Should validators run in parallel?

**Considerations**:
- Python GIL limits threading benefit
- Multiprocessing adds complexity
- Current runtime acceptable (~5s)

**Resolution**: Not planned unless runtime becomes problematic

## Resolved Questions

| Question | Resolution | Date |
|----------|------------|------|
| DocMeta version | v1.2 adopted as standard | 2025-12 |
| Houston validator suite | All 5 validators complete | 2025-12 |
| Tier 3 doc structure | 7 docs standard adopted | 2026-01 |
| Receipt format | Markdown with standard headers | 2025-10 |
| Taxonomy format | YAML with flat structure | 2025-09 |

## Contributing Questions

If you encounter an unresolved question:

1. Check existing issues on GitHub
2. Add question to this document with context
3. Propose options if you have ideas
4. Reference related code or protocol behavior

## Related Documentation

- [ARCHITECTURE.md](ARCHITECTURE.md) - System design context
- [SECURITY_AND_PRIVACY.md](SECURITY_AND_PRIVACY.md) - Security decisions
- [OPERATIONS.md](OPERATIONS.md) - Operational context


---

## Standards Snapshot (C010)

This repo follows workspace standards from C010_standards:

- **Betty Protocol**: Evidence in 20_receipts/, no self-certification
- **META.yaml**: Keep `last_reviewed` current
- **Cross-platform**: Commands work on macOS, Windows, Linux
- **Closeout**: Git status clean, stash triaged, receipts written

Full standards are canonical in C010_standards.
