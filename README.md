# C000_info-center

**🗺️ Your Workspace Orientation & Standards Hub**

Welcome to the information center for Jeremy Bradford's development workspace. Before working with ANY repository in SyncedProjects, start here.

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

1. **[workspace/KNOWN_PROJECTS.md](workspace/KNOWN_PROJECTS.md)** (5 min)
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
C000_info-center/
├── AGENT_START_HERE.md          # ⭐ Required reading for AI agents
├── README.md                     # This file - your starting point
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
│   └── bootstrap_claude_crossplatform.sh
│
├── tests/                        # 🧪 Validator tests
├── policy/                       # Python/Ruff standards
├── 30_config/                    # Houston configuration
├── notes/                        # Planning & ADRs
└── Archive/                      # Archived legacy files
```

---

## Common Tasks

### 1. Find a Project

```bash
# View all projects with status
cat workspace/KNOWN_PROJECTS.md

# Search for a specific project
grep -i "sadb" workspace/KNOWN_PROJECTS.md
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
| [workspace/KNOWN_PROJECTS.md](workspace/KNOWN_PROJECTS.md) | Project inventory | Nightly (auto) |
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

**workspace/KNOWN_PROJECTS.md** is generated nightly by:
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

### Phase 3 (Planned)
1. [ ] Draft migration checklist for schema adoption
2. [ ] Expose standards in Mission Control UI/docs
3. [ ] Add schema versioning policy (v1.3, v2.0 guidelines)
4. [ ] Complete validator test coverage (docmeta, tools, models, telemetry)
5. [ ] Generate API documentation for validators

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

*Last Updated: 2025-11-19*
*Formerly: C010_standards*
*Renamed to: C000_info-center for better visibility and clarity*
*Maintained by: Jeremy Bradford & Claude*

_All downstream repositories should treat this repo as the authoritative metadata spec. Updates here require versioning, changelog, and communication across projects._
