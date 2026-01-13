# C010_standards

**🗺️ Your Workspace Orientation & Standards Hub**

Welcome to the information center for Jeremy Bradford's development workspace. Before working with ANY repository in SyncedProjects, start here.

<!-- BOT:repo_card:start -->

## What this repo is

C010_standards is the **canonical source of truth** for workspace organization, standards, and governance across Jeremy Bradford's 66+ project ecosystem. It serves as the "info center" or "visitor center" for the workspace. It provides:

- **Protocols & Standards**: Betty Protocol (workspace governance), README repo card standard, cross-platform CLAUDE.md format
- **Schemas**: DocMeta v1.2, CodeMeta v1.0, Houston features/tools/telemetry JSON schemas
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
| Learning data flow architecture | `workspace/PROJECT_RELATIONSHIPS.md` |
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
| `schemas/` | YAML/JSON schema definitions (docmeta, codemeta, houston_*) |
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
│   └── cross_platform_claude_md.md
├── schemas/                      # Data contracts
│   ├── docmeta_v1.2.yaml        # Document metadata
│   ├── codemeta_v1.0.yaml       # Code metadata
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
| `Betty Protocol` | Markdown | Folder structure + governance rules |
| `README Repo Card` | Markdown + BOT markers | Deterministic README extraction |

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
| All P/C/W repos | Must follow Betty Protocol and folder structure |

## Provenance

- **Version**: 1.0.0
- **Last Updated**: 2025-12-28
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
- Memory systems are COMPLEX - read [workspace/PROJECT_RELATIONSHIPS.md](workspace/PROJECT_RELATIONSHIPS.md)
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

2. **[workspace/PROJECT_RELATIONSHIPS.md](workspace/PROJECT_RELATIONSHIPS.md)** (15 min)
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
├── workspace/                    # 📊 Workspace-level organization
│   ├── KNOWN_PROJECTS.md        # Auto-generated project inventory
│   ├── PROJECT_RELATIONSHIPS.md # Data flow & system architecture
│   ├── scripts/                 # Project registry generation
│   └── pr-execution/            # PR modernization tracking
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
cat workspace/PROJECT_RELATIONSHIPS.md

# Or open in your browser/editor
open workspace/PROJECT_RELATIONSHIPS.md
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

### Houston Validators (Production-Ready)

Five validators ensure compliance with Houston agent protocols:

```bash
# Run individual validators
python validators/check_houston_docmeta.py <file.yaml>
python validators/check_houston_features.py <file.json>
python validators/check_houston_models.py <file.json>
python validators/check_houston_telemetry.py <file.json>
python validators/check_houston_tools.py <file.json>

# Run all validators
python validators/run_all.py
```

**What They Check:**
- Schema compliance (required fields, types)
- Semantic validation (logical consistency)
- Houston-specific rules (phase transitions, tool pipelines)
- Cross-file references (imported configs)

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
| [workspace/PROJECT_RELATIONSHIPS.md](workspace/PROJECT_RELATIONSHIPS.md) | System architecture | As needed |
| [protocols/betty_protocol.md](protocols/betty_protocol.md) | Governance rules | Quarterly |
| [AGENT_START_HERE.md](AGENT_START_HERE.md) | AI agent guide | As needed |

### When Things Go Wrong

**Problem:** Can't find the right file/version
**Solution:** Read [workspace/PROJECT_RELATIONSHIPS.md](workspace/PROJECT_RELATIONSHIPS.md) section "For LLMs: Finding Canonical Versions"

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

**For Humans:** Check [workspace/PROJECT_RELATIONSHIPS.md](workspace/PROJECT_RELATIONSHIPS.md) or ask Jeremy.

**For Validators:** Run with `--verbose` flag for detailed error messages.

---

*Last Updated: 2026-01-13*
*Maintained by: Jeremy Bradford & Claude*

_All downstream repositories should treat this repo as the authoritative metadata spec. Updates here require versioning, changelog, and communication across projects._
