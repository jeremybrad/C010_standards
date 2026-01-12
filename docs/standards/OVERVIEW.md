# C010_standards Overview

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
| All P/C/W repos | Betty Protocol compliance | Active |
| CI/CD workflows | Validator execution | Active |
| NotebookLM | Documentation sync | Active |

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
