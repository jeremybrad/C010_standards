# PROJECT PRIMER — C010_standards

## Provenance

- **Generated**: 2026-01-17
- **Repo SHA**: 2217ce4
- **Generator**: claude-code (manual regeneration)
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
- Data schemas (DocMeta, CodeMeta, Houston configs, CapsuleMeta)
- Classification taxonomies (topics, emotions, metadata)
- Validation tools (Houston validators, README repo card checker, capsule validator)
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
| C017_brain-on-tap | relates to | Profile extraction uses DocMeta schema; emits c010.capsule.v1 capsules | active |
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

**Your Workspace Orientation & Standards Hub**

Welcome to the information center for Jeremy Bradford's development workspace. Before working with ANY repository in SyncedProjects, start here.

## What this repo is

C010_standards is the **canonical source of truth** for workspace organization, standards, and governance across Jeremy Bradford's 66+ project ecosystem. It serves as the "info center" or "visitor center" for the workspace. It provides:

- **Protocols & Standards**: Betty Protocol (workspace governance), README repo card standard, cross-platform CLAUDE.md format, Capsule Standard v1
- **Schemas**: DocMeta v1.2, CodeMeta v1.0, CapsuleMeta v1.0, Houston features/tools/telemetry JSON schemas
- **Taxonomies**: Topic, emotion, and metadata classification systems
- **Validators**: Python scripts to check compliance with schemas and protocols (8 validators)
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
| Validating capsule frontmatter | `python validators/check_capsulemeta.py <path>` |
| Validating README repo cards | `python scripts/validate_readme_repo_card.py <repo>` |
| Adding cross-platform Claude support | `bash scripts/bootstrap_claude_crossplatform.sh` |
| Adding Ruff linting to repos | `bash scripts/bootstrap_ruff.sh` |
| Creating a new project | `PROJECT_TEMPLATE.md` |
| Systematic repo upgrades | `COMPREHENSIVE_PR_TEMPLATE.md` |

## Entry points

| Path | Purpose |
|------|---------|
| `AGENT_START_HERE.md` | **Required reading** for AI agents before any work |
| `protocols/` | Governance docs (betty_protocol, readme_repo_card, capsule_spec_v1) |
| `schemas/` | YAML/JSON schema definitions (docmeta, codemeta, capsulemeta, houston_*) |
| `validators/` | Python compliance checkers for Houston configs and capsules |
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
│   ├── capsules/                # Capsule standards
│   │   └── capsule_spec_v1.md   # c010.capsule.v1 specification
│   ├── universal_claude_standards.md
│   └── cross_platform_claude_md.md
├── schemas/                      # Data contracts
│   ├── docmeta_v1.2.yaml        # Document metadata
│   ├── codemeta_v1.0.yaml       # Code metadata
│   ├── capsulemeta_v1.0.yaml    # Capsule metadata template
│   └── houston_*.schema.json    # Houston agent configs
├── validators/                   # Compliance checkers
│   ├── check_houston_*.py       # 5 Houston validators
│   ├── check_repo_contract.py   # Repository structure validator
│   ├── check_capsulemeta.py     # Capsule frontmatter validator
│   ├── run_all.py               # Batch runner
│   └── common.py                # Shared utilities
├── scripts/                      # Bootstrap + validation
│   ├── validate_readme_repo_card.py  # README repo card checker
│   ├── bootstrap_ruff.sh
│   └── bootstrap_claude_crossplatform.sh
├── workspace/                    # Inventory & architecture
│   ├── KNOWN_PROJECTS.md        # Auto-generated nightly
│   └── PROJECT_RELATIONSHIPS.md # Data flow diagrams
├── 10_docs/examples/capsules/   # Capsule examples
│   ├── handoff_example.md
│   ├── memory_export_example.md
│   └── activity_example.md
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
| `CapsuleMeta v1.0` | YAML | Capsule frontmatter (c010.capsule.v1) |
| `Houston Features` | JSON Schema | AI agent capability configuration |
| `Houston Tools` | JSON Schema | Tool pipeline definitions |
| `Houston Telemetry` | JSON Schema | Agent telemetry format |
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

# 2. Validate capsule frontmatter
python validators/check_capsulemeta.py 10_docs/examples/capsules/ --verbose

# 3. Validate README repo card
python scripts/validate_readme_repo_card.py ~/SyncedProjects/C017_brain-on-tap --strict

# 4. Run folder structure audit (double-click or CLI)
bash 00_run/audit_syncedprojects.command
# Output: 70_evidence/exports/folder_structure_audit_latest.csv

# 5. Generate standards pulse report
bash 00_run/standards_pulse.command
# Output: 70_evidence/exports/Standards_Pulse.xlsx

# 6. Bootstrap repos with Ruff linting
bash scripts/bootstrap_ruff.sh

# 7. Add cross-platform CLAUDE.md to repos
bash scripts/bootstrap_claude_crossplatform.sh --dry-run  # Preview
bash scripts/bootstrap_claude_crossplatform.sh            # Apply

# 8. Update project registry (runs nightly at 2:45 AM)
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
| Running run_all.py from consumer repos | Houston validators fail (missing 30_config/) | Use `--targets repo_contract capsulemeta` |

## Related repos

| Repo | Relationship |
|------|--------------|
| `C001_mission-control` | Embeds C010 as git submodule at `external/standards/` |
| `C002_sadb` | Uses Betty Protocol; source of conversation data |
| `C017_brain-on-tap` | Extracts README repo cards for LLM context; emits c010.capsule.v1 capsules |
| `C019_docs-site` | Canonical docs publishing/search surface (MkDocs + Docs RAG) |
| All P/C/W repos | Must follow Betty Protocol and folder structure |

## Provenance

- **Version**: 1.0.0
- **Last Updated**: 2026-01-17
- **Git SHA**: 2217ce4
- **Receipts**: `20_receipts/`
- **Standard**: Self-hosting - this README passes `scripts/validate_readme_repo_card.py`

---

## Overview

### What Is C010_standards?

C010_standards is the canonical source of truth for workspace-wide standards, governance, and organization across the 66+ project ecosystem. It defines protocols, schemas, taxonomies, and validation tooling that ensure consistency and quality across all repositories.

### Ecosystem Position

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          SyncedProjects Ecosystem                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                      C010_standards (This Repo)                       │   │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────────┐  │   │
│  │  │ Protocols  │  │  Schemas   │  │ Taxonomies │  │   Validators   │  │   │
│  │  │ (12 docs)  │  │ (4 specs)  │  │ (8 files)  │  │  (8 checkers)  │  │   │
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

### Core Components

| Component | Purpose | Location |
|-----------|---------|----------|
| **Protocols** | Governance rules and standards definitions | `protocols/` |
| **Schemas** | Data contracts for metadata and configuration | `schemas/` |
| **Taxonomies** | Controlled vocabularies for classification | `taxonomies/` |
| **Validators** | Compliance checking tools | `validators/` |
| **Registry** | Project metadata and relationships | `registry/` |
| **Houston Config** | Agent feature toggles and trust phases | `30_config/` |

### Key Capabilities

#### 1. Betty Protocol Governance
- Non-negotiable folder structure requirements (00_, 10_, 20_, etc.)
- Receipt-driven evidence documentation
- Data policy enforcement (artifacts outside git)
- Pre-commit hooks and guardrails

#### 2. Metadata Standards
- DocMeta v1.2 for document metadata with routing and governance
- CodeMeta v1.0 for code artifact tracking
- CapsuleMeta v1.0 for atomic artifact frontmatter (handoffs, exports, activities)
- Houston configuration schemas for agent behavior

#### 3. Taxonomy Management
- Topic taxonomy for technical classification
- Content taxonomy for document types
- Emotion taxonomy for context tagging
- Universal terms with synonym disambiguation

#### 4. Validation Suite
- Houston validators (docmeta, features, tools, models, telemetry)
- Repository contract compliance checking
- Capsule frontmatter validation
- README repo card validation
- Orchestrated validation harness

#### 5. Project Registry
- Structured metadata for all 66+ projects
- Lifecycle tracking (Active → Maintenance → Archived)
- Relationship mapping between repos

### Operating Modes

| Mode | Description | Use Case |
|------|-------------|----------|
| **Reference** | Consult standards and schemas | Starting new projects, understanding requirements |
| **Validation** | Run compliance checks | Pre-commit, CI/CD, periodic audits |
| **Bootstrap** | Apply standards to repos | New repo setup, standardization campaigns |
| **Governance** | Update protocols and schemas | Standards evolution, version bumps |

### Integration Points

| System | Integration Type | Status |
|--------|-----------------|--------|
| C001_mission-control | Git submodule at `external/standards/` | Active |
| C017_brain-on-tap | README repo card extraction + capsule emission | Active |
| C019_docs-site | Docs publishing/search (MkDocs + Docs RAG) | Active |
| All P/C/W repos | Betty Protocol compliance | Active |
| CI/CD workflows | Validator execution | Active |
| NotebookLM | Documentation sync | Active |

### Docs Publishing Model

Standards documentation follows a clear separation of concerns:

| Layer | Repo | Responsibility |
|-------|------|----------------|
| **Authoring** | C010_standards | Source of truth for protocols, schemas, taxonomies |
| **Publishing** | C019_docs-site | MkDocs site build, static hosting |
| **Search** | C019_docs-site | Docs RAG API (FAISS index, semantic retrieval) |
| **UI Client** | C001_mission-control | Optional `/docs` endpoint consuming C019 |

---

## Quickstart

Get oriented with workspace standards in 5 minutes.

### Prerequisites

- Git
- Python 3.11+ (for validators)
- Access to SyncedProjects workspace

### Quick Start

#### 1. Clone or Navigate

```bash
cd ~/SyncedProjects/C010_standards
```

#### 2. Read Agent Pre-Flight (Required for AI Agents)

```bash
cat AGENT_START_HERE.md
```

This document contains the mandatory checklist before operating in any repo.

#### 3. Understand Betty Protocol

```bash
cat protocols/betty_protocol.md
```

Core governance rules:
- Folder structure: `00_admin/`, `10_docs/`, `20_receipts/`, `30_config/`, `40_src/`, `70_evidence/`, `90_archive/`
- Every change produces documented evidence
- Artifacts stay outside git repos
- Receipts required for non-trivial work

### Configuration

#### For Mission Control Integration

C001_mission-control embeds standards as a git submodule:

```bash
cd ~/SyncedProjects/C001_mission-control
git submodule update --init external/standards
```

#### For New Projects

Use the project template to ensure compliance:

```bash
# Copy template structure
cp -r ~/SyncedProjects/C010_standards/PROJECT_TEMPLATE.md ./
```

### First Operations

#### Run All Validators

```bash
# Run from repo root
cd ~/SyncedProjects/C010_standards
python validators/run_all.py
```

Exit codes:
- `0` - All checks pass
- `1` - Validation failure
- `2` - Config/parse error

#### Validate a Single Aspect

```bash
# Check Houston features
python validators/check_houston_features.py --config 30_config/houston-features.json

# Check repository contract
python validators/check_repo_contract.py --repo ~/SyncedProjects/P050_ableton-mcp

# Check capsule frontmatter
python validators/check_capsulemeta.py 20_receipts/handoffs/ --verbose
```

#### Check README Repo Card

```bash
python scripts/validate_readme_repo_card.py ~/SyncedProjects/C001_mission-control/README.md
```

### Key Documents to Read

| Document | Purpose | When to Read |
|----------|---------|--------------|
| `AGENT_START_HERE.md` | Agent pre-flight checklist | Before any AI agent work |
| `protocols/betty_protocol.md` | Core governance rules | Starting any project |
| `protocols/capsules/capsule_spec_v1.md` | Capsule standard | Creating capsule artifacts |
| `protocols/tier3_documentation_spec.md` | Documentation standards | Creating docs |
| `schemas/docmeta_v1.2.yaml` | Document metadata schema | Tagging documents |
| `taxonomies/topic_taxonomy.yaml` | Topic classification | Categorizing content |

---

## Architecture

### System Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           C010_standards                                     │
│                    Workspace Standards & Governance Hub                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                        PROTOCOLS LAYER                               │    │
│  │  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌────────────┐  │    │
│  │  │    Betty     │ │   Tier 3     │ │   Session    │ │  Capsule   │  │    │
│  │  │   Protocol   │ │    Docs      │ │  Closeout    │ │  Spec v1   │  │    │
│  │  │  (core gov)  │ │   (specs)    │ │  (handoff)   │ │ (capsules) │  │    │
│  │  └──────────────┘ └──────────────┘ └──────────────┘ └────────────┘  │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                    │                                         │
│  ┌─────────────────────────────────┼─────────────────────────────────┐      │
│  │                        SCHEMAS LAYER                               │      │
│  │  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────┐  │      │
│  │  │   DocMeta    │ │   CodeMeta   │ │  CapsuleMeta │ │ Houston  │  │      │
│  │  │    v1.2      │ │    v1.0      │ │    v1.0      │ │ Features │  │      │
│  │  │  (routing,   │ │  (repos,     │ │ (capsule_id, │ │  (trust  │  │      │
│  │  │  governance) │ │   scripts)   │ │  kind, etc.) │ │  phases) │  │      │
│  │  └──────────────┘ └──────────────┘ └──────────────┘ └──────────┘  │      │
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
│  │  │  Houston   │ │  Houston   │ │    Repo    │ │   Capsule      │  │      │
│  │  │  DocMeta   │ │  Features  │ │  Contract  │ │   Meta         │  │      │
│  │  │  Checker   │ │  Checker   │ │  Checker   │ │   Checker      │  │      │
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

### Core Principles

1. **Single Source of Truth** - All workspace standards originate here
2. **Evidence-Driven** - "No belief without receipts" philosophy
3. **Layered Architecture** - Protocols → Schemas → Taxonomies → Validators
4. **Composable Validation** - Individual checkers can run standalone or orchestrated
5. **Version Control** - Schemas are versioned (DocMeta v1.2, CodeMeta v1.0, CapsuleMeta v1.0)

### Component Details

#### Protocols (`protocols/`)

Core governance documents that define how the workspace operates.

**Key Files:**
- `betty_protocol.md` - Non-negotiable governance rules
- `tier3_documentation_spec.md` - Canonical documentation structure
- `session_closeout_protocol.md` - Session handoff procedures
- `cross_platform_claude_md.md` - CLAUDE.md format spec
- `META_YAML_SPEC.md` - Project metadata contract
- `capsules/capsule_spec_v1.md` - Capsule standard (c010.capsule.v1)

#### Schemas (`schemas/`)

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

**CapsuleMeta v1.0** (`capsulemeta_v1.0.yaml`):
```yaml
# Capsule frontmatter for atomic artifacts
capsule_spec: "c010.capsule.v1"  # Required
capsule_id: "<uuid>"             # Required
created_at: "<ISO 8601>"         # Required
kind: handoff | memory_export | activity | other  # Required
producer:
  tool: "<tool-name>"            # Required
  agent: "<agent-name>"          # Optional
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

#### Taxonomies (`taxonomies/`)

Controlled vocabularies for consistent classification.

| Taxonomy | Purpose | Entry Count |
|----------|---------|-------------|
| `topic_taxonomy.yaml` | Technical topics | ~50 terms |
| `content_taxonomy.yaml` | Document types | ~20 types |
| `emotion_taxonomy.yaml` | Emotional context | ~15 emotions |
| `universal_terms.yaml` | Synonym registry | ~100 terms |
| `disambiguation_rules.yaml` | Context resolution | ~30 rules |

#### Validators (`validators/`)

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

**Available Validators (8 total):**
- `check_houston_docmeta.py` - DocMeta routing and taxonomy
- `check_houston_features.py` - Feature configuration
- `check_houston_tools.py` - Tool pipeline consistency
- `check_houston_models.py` - Model deployment permissions
- `check_houston_telemetry.py` - Telemetry freshness
- `check_repo_contract.py` - Repository structure
- `check_capsulemeta.py` - Capsule frontmatter validation

### Data Flow

#### Validation Flow

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

#### Standards Consumption Flow

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

---

## Code Tour

Navigate the C010_standards codebase efficiently.

### Quick Reference

| I want to... | Look at... |
|--------------|------------|
| Understand workspace governance | `protocols/betty_protocol.md` |
| Create Tier 3 documentation | `protocols/tier3_documentation_spec.md` |
| Define document metadata | `schemas/docmeta_v1.2.yaml` |
| Create capsule artifacts | `protocols/capsules/capsule_spec_v1.md` |
| Classify content by topic | `taxonomies/topic_taxonomy.yaml` |
| Run compliance checks | `validators/run_all.py` |
| Find a project's metadata | `registry/repos.yaml` |
| Configure agent behavior | `30_config/houston-features.json` |
| Set up a new repo | `PROJECT_TEMPLATE.md` |
| Understand agent pre-flight | `AGENT_START_HERE.md` |

### Directory Map

```
C010_standards/
├── 00_admin/                    # Governance policies
├── 10_docs/                     # Documentation artifacts
│   └── examples/capsules/       # Capsule examples (3 files)
├── 20_receipts/                 # Change receipts (150+ entries)
│   ├── handoffs/                # Session handoff capsules
│   └── YYYY-MM-DD_description.md
├── 30_config/                   # Configuration files
│   ├── houston-features.json    # Feature toggles and trust phases
│   └── houston-tools.json       # Tool pipeline configuration
├── docs/                        # Tier 3 documentation
│   └── standards/               # This folder
├── protocols/                   # Standards definitions (12 docs)
│   ├── betty_protocol.md        # Core governance rules
│   ├── tier3_documentation_spec.md  # Doc standards
│   ├── session_closeout_protocol.md # Session handoff
│   ├── cross_platform_claude_md.md  # CLAUDE.md format
│   ├── META_YAML_SPEC.md        # Metadata contract
│   └── capsules/                # Capsule standards
│       └── capsule_spec_v1.md   # c010.capsule.v1 specification
├── registry/                    # Project registry
│   ├── repos.yaml               # All project metadata
│   ├── schema.md                # Registry data model
│   └── README.md                # Usage guide
├── schemas/                     # Data contracts
│   ├── docmeta_v1.2.yaml        # Document metadata
│   ├── codemeta_v1.0.yaml       # Code metadata
│   ├── capsulemeta_v1.0.yaml    # Capsule metadata template
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
├── tests/                       # Test suites
│   └── test_check_capsulemeta.py  # Capsule validator tests (37 tests)
├── validators/                  # Compliance checkers
│   ├── run_all.py               # Orchestration harness
│   ├── check_houston_docmeta.py
│   ├── check_houston_features.py
│   ├── check_houston_tools.py
│   ├── check_houston_models.py
│   ├── check_houston_telemetry.py
│   ├── check_repo_contract.py
│   └── check_capsulemeta.py     # Capsule frontmatter validator
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

### Key Entry Points

#### Validator Orchestrator (`validators/run_all.py`)

```python
# Runs all validators in sequence, stops on first failure
def main():
    validators = [
        "check_houston_features.py",
        "check_houston_tools.py",
        "check_houston_models.py",
        "check_houston_telemetry.py",
        "check_houston_docmeta.py",
        "check_repo_contract.py",
        "check_capsulemeta.py",
    ]
    for validator in validators:
        exit_code = run_validator(validator)
        if exit_code != 0:
            sys.exit(exit_code)
    sys.exit(0)
```

#### Capsule Validator (`validators/check_capsulemeta.py`)

```python
# Validates c010.capsule.v1 frontmatter
def validate_capsule(frontmatter: dict, strict: bool = False) -> list[str]:
    """
    Required fields:
    - capsule_spec == "c010.capsule.v1"
    - capsule_id (non-empty string)
    - created_at (valid ISO 8601)
    - kind (handoff | memory_export | activity | other)
    - producer.tool (non-empty string)

    Unknown fields: warn (default) or error (--strict)
    """
```

---

## Operations

Day-to-day operation of C010_standards.

### Operating Modes

#### Reference Mode (Primary)

```bash
# Consult standards before starting work
cat protocols/betty_protocol.md
cat protocols/capsules/capsule_spec_v1.md
```

Use when starting new projects or reviewing requirements.

#### Validation Mode

```bash
# Run all Houston validators (from repo root)
python validators/run_all.py
```

Use for pre-commit checks, CI/CD, and periodic audits.

#### Bootstrap Mode

```bash
# Apply Ruff config to a repo
bash scripts/bootstrap_ruff.sh ~/SyncedProjects/P050_ableton-mcp

# Add cross-platform Claude support
bash scripts/bootstrap_claude_crossplatform.sh ~/SyncedProjects/P050_ableton-mcp
```

Use when standardizing repos or setting up new projects.

### Daily Workflows

#### Session Startup (AI Agents)

1. Read `AGENT_START_HERE.md` (mandatory pre-flight)
2. Check `protocols/betty_protocol.md` for current governance
3. Verify Houston trust phase in `30_config/houston-features.json`

#### Health Check

```bash
# Run validator suite
python validators/run_all.py --config 30_config/houston-features.json
```

| Result | Status |
|--------|--------|
| Exit 0 | All checks pass |
| Exit 1 | Validation failure - review output |
| Exit 2 | Config/parse error - check file syntax |

### Validator Execution Contexts

#### Running in C010_standards (full suite)

When running validators inside C010_standards, all validators work because required config files (`30_config/houston-features.json`, etc.) are present:

```bash
cd ~/SyncedProjects/C010_standards
python validators/run_all.py
```

#### Running from consumer repos (via submodule)

Consumer repos (like C001_mission-control) consume C010 as a git submodule. The Houston-specific validators (`houston_features`, `houston_tools`, etc.) require config files that only exist in C010, so running `run_all.py` without targets will fail.

**Use `--targets` to run only applicable validators:**

```bash
cd ~/SyncedProjects/C001_mission-control
python external/standards/validators/run_all.py --targets repo_contract capsulemeta
```

**Portable validators** (work in any repo):
- `repo_contract` - Checks repository structure
- `capsulemeta` - Validates capsule frontmatter

**C010-context validators** (require `30_config/`):
- `houston_docmeta`, `houston_features`, `houston_tools`, `houston_models`, `houston_telemetry`

### Common Operations

**Check repo compliance:**
```bash
python validators/check_repo_contract.py --repo ~/SyncedProjects/P050_ableton-mcp
```

**Validate capsule frontmatter:**
```bash
python validators/check_capsulemeta.py 20_receipts/handoffs/ --verbose
```

**Validate README repo card:**
```bash
python scripts/validate_readme_repo_card.py ~/SyncedProjects/C001_mission-control/README.md
```

**List all projects:**
```bash
cat 70_evidence/workspace/KNOWN_PROJECTS.md
```

---

## Security & Privacy

Security model and data protection for C010_standards.

### Security Principles

1. **No Secrets Stored** - Standards repo contains no credentials or sensitive data
2. **Public by Design** - All protocols and schemas are meant to be shared
3. **Audit Trail** - All changes documented in receipts
4. **Controlled Vocabularies** - Taxonomies prevent ambiguity and injection
5. **Validation Before Trust** - Houston validators enforce compliance

### Repository Security

#### What This Repo Contains

| Content Type | Sensitivity | Notes |
|--------------|-------------|-------|
| Protocols | Public | Governance documentation |
| Schemas | Public | Data contracts |
| Taxonomies | Public | Controlled vocabularies |
| Validators | Public | Python compliance checkers |
| Registry | Internal | Project metadata (no secrets) |
| Configuration | Internal | Feature toggles (no credentials) |

#### What This Repo Does NOT Contain

| Content Type | Where It Lives |
|--------------|----------------|
| API keys | C001_mission-control vault |
| Passwords | Never in any repo |
| Personal data | Not stored |
| Private credentials | Environment variables only |

### Houston Configuration Security

#### Trust Phases

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

---

## Open Questions

Unresolved decisions, known limitations, and future considerations.

### Architecture Questions

#### Schema Versioning Strategy

**Current State**: Schemas use simple version suffixes (docmeta_v1.2.yaml, codemeta_v1.0.yaml, capsulemeta_v1.0.yaml)

**Question**: Should we adopt semantic versioning with breaking change indicators?

| Option | Pros | Cons |
|--------|------|------|
| Keep current (v1.2) | Simple, familiar | No breaking change signal |
| SemVer (1.2.0) | Industry standard | More complex filenames |
| Date-based (2026-01) | Clear timeline | Less intuitive |

**Resolution**: Pending - current approach works for now

#### Validator Orchestration

**Current State**: `run_all.py` stops on first failure

**Question**: Should validators continue and report all failures?

| Option | Pros | Cons |
|--------|------|------|
| Stop on first | Fast feedback | May hide other issues |
| Run all, report all | Complete picture | Slower, more output |
| Configurable | Flexible | More complex |

**Resolution**: Pending - may add `--continue-on-error` flag

### Known Limitations

#### Protocol Limitations

| Limitation | Impact | Workaround |
|------------|--------|------------|
| No protocol inheritance | Each protocol standalone | Copy shared sections |
| Manual sync to consumers | Standards drift possible | CI/CD checks |
| No protocol deprecation process | Old protocols linger | Manual cleanup |

#### Validator Limitations

| Limitation | Impact | Workaround |
|------------|--------|------------|
| Python 3.11+ required | Older environments fail | Specify version |
| No parallel execution | Slower for many repos | Run selectively |
| Console output only | No structured reports | Pipe to file or use --json-output |

### Resolved Questions

| Question | Resolution | Date |
|----------|------------|------|
| DocMeta version | v1.2 adopted as standard | 2025-12 |
| Houston validator suite | All 5 validators complete | 2025-12 |
| Tier 3 doc structure | 7 docs standard adopted | 2026-01 |
| Receipt format | Markdown with standard headers | 2025-10 |
| Taxonomy format | YAML with flat structure | 2025-09 |
| Capsule standard | c010.capsule.v1 shipped | 2026-01-17 |

---

## Capsule Standard (c010.capsule.v1)

Capsules are atomic, self-contained artifacts that carry structured YAML frontmatter. They support handoffs, memory exports, and activity logs.

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `capsule_spec` | string | Must equal `"c010.capsule.v1"` |
| `capsule_id` | string | UUID or stable identifier |
| `created_at` | string | ISO 8601 UTC datetime |
| `kind` | enum | `handoff` \| `memory_export` \| `activity` \| `other` |
| `producer.tool` | string | Tool that produced the capsule |

### Optional Fields

`producer.agent`, `title`, `summary`, `provenance.*`, `tags`, `expires_at`, `related_capsules`, `custom`

### Validation

```bash
# Validate capsule files
python validators/check_capsulemeta.py <path> --verbose

# Strict mode (unknown fields are errors)
python validators/check_capsulemeta.py <path> --strict
```

### Examples

See `10_docs/examples/capsules/` for reference capsules:
- `handoff_example.md` - Session handoff between agents
- `memory_export_example.md` - Context/memory export
- `activity_example.md` - Activity log with custom fields

---

*Generated: 2026-01-17 | SHA: 2217ce4*
