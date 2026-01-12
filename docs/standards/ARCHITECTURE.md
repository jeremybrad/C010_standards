# C010_standards Architecture

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
