# SyncedProjects Repository Organization

## Overview
SyncedProjects is synchronized across three devices (PC, Mac Mini, MacBook) using Syncthing. All repositories follow a strict prefix-based naming convention to maintain clarity and organization.

## Naming Convention

### Prefixes

#### **C (Core Infrastructure)**
Projects that are foundational to the entire ecosystem. Not actively developed features, but essential infrastructure used across multiple projects.

**Numbering**: C001-C099
**Examples:**
- C001_mission-control: Central orchestration hub
- C002_sadb: Self-Aware Database project (promoted from P002, 2025-10-11)
- C003_agents: Agent definitions and frameworks
- C009_mcp-memory-http: HTTP interface for memory system
- C010_standards: This repository - canonical standards and governance

**Key Characteristics:**
- Single source of truth for shared concerns
- Changes here affect multiple downstream projects
- Should be version-controlled and documented
- Often used as git submodules in other projects

#### **P (Personal Projects)**
Personal experiments, tools, and projects not related to day job work.

**Numbering**: P001-P999
**Examples:**
- P001_bettymirror: Betty AI system core
- ~~P002_sadb~~ → Promoted to C002_sadb (2025-10-11)
- P110_knowledge-synthesis-tool: KST development
- P170_memory-cathedral: Advanced memory architecture

**Key Characteristics:**
- Independent development
- May depend on C-projects
- Can be experimental or production-grade

#### **W (Work Projects)**
Projects directly related to work at Huawei - day job analytics and reporting.

**Numbering**: W001-W099
**Examples:**
- W001_Lighthouse: Work project (possibly CMO dashboard)
- W001_cmo-weekly-reporting: Weekly reporting system
- W002_analytics: Analytics infrastructure

**Key Characteristics:**
- Work-specific and possibly sensitive
- Should be clearly separated from personal projects
- May have different backup/security requirements

### Special Folders

#### **_receipts/**
Audit trail and log directory for automated systems
- Contains timestamped operation logs
- Includes subdirectories for specific systems (auditor, doctor, drift, etc.)
- Should NOT be manually modified
- Historical record of automated operations

#### **SharedData/**
Truly shared data that doesn't fit into any single project
- Cross-project resources
- Obsidian vault
- AI models
- Analytics dashboards
- Should remain at root level as special case

#### **Archive/**
Historical content and deprecated projects
- Projects no longer active
- Timestamped archive folders
- Should be reviewed periodically for deletion

#### **Workspace/** (Deprecated)
⚠️ **SHOULD BE MIGRATED**: Contains duplicate P-projects that should be at root level
- P001_bettymirror (duplicate)
- C002_sadb (duplicate, formerly P002)
- P005_mybuddy (duplicate)
- P070_midi-gesture (needs to be moved to root)

## Root Level Files

### Allowed Files
Only essential protocol and operational files should be at root:

**Protocol Documents:**
- `WORKSPACE_BETTY_PROTOCOL.md` - Core workspace rules
- `BETTY_PRELUDE.md` - Betty system documentation
- `CLAUDE.md` - Claude interaction guidelines

**Operational Scripts:**
- `workspace_autocontain.sh` - Betty Protocol cleanup automation

**Documentation:**
- `README.md` - Workspace overview
- `KNOWN_PROJECTS.md` - Auto-generated project inventory (can be regenerated)

### Files to Relocate
- `ROOT_CLEANUP_COMPLETE_20250907_205408.md` → Archive or _receipts

## Cleanup Procedures

### Finding Lost Projects
1. Use `find` to locate git repositories:
   ```bash
   find /Users/jeremybradford/SyncedProjects -name ".git" -type d -maxdepth 3
   ```

2. Check for orphaned projects in Archive and Workspace folders

3. Verify against project inventory

### Moving Projects to Correct Location
1. Ensure project is not a duplicate
2. Move to root level if it follows C/P/W naming
3. Update any references in other projects
4. Update git submodule references if applicable

### Dealing with Non-Conforming Names
Projects that don't follow C/P/W naming:

**REF001_Analytics_Canonical**
- Assess: Is this work-related? → Should be W003_analytics-canonical
- Assess: Is this reference material? → Consider C-prefix or Archive

## Best Practices

### Before Creating a New Project
1. Choose appropriate prefix (C/P/W)
2. Find next available number in sequence
3. Use descriptive kebab-case name: `P999_descriptive-name`
4. Create at root level of SyncedProjects
5. Initialize git repository
6. Add README.md with purpose

### Avoiding Project Loss
1. Never nest projects more than 1 level deep
2. Always check root level first when looking for projects
3. Use `KNOWN_PROJECTS.md` as reference (regenerate if needed)
4. Set up git to auto-fetch/status in mission-control

### When in Doubt
1. Check C010_standards for guidance
2. Consult WORKSPACE_BETTY_PROTOCOL.md
3. Ask Claude to validate structure against standards

## Promoting Projects to Core (C-prefix) & Git Submodule Pattern

### When to Promote a Project to Core

A project should be promoted from P-prefix to C-prefix when it meets these criteria:

**Infrastructure Criteria:**
- The project is consumed across multiple repos/projects
- The project provides infrastructure, not only experimental code (e.g., UI orchestration, agents, toolchains)
- Changes to this project affect downstream projects and require governance and testing
- The project has evolved from prototype to production-grade stability

**Examples:**
- P002 → C002_sadb: Knowledge extraction system consumed by Mission Control, validators, and infrastructure projects
- P160 → C004_open-web-ui: Evolved from experiment to core LLM interface serving 123+ models
- P210 → C010_standards: Became the canonical source for workspace governance

### Promotion Process

1. **Create an ADR** documenting the rationale (see `notes/ADR/001-modularity-architecture.md` as example)
2. **Update PROJECT_MAP.md** to mark the old P-project as migrated and add the new C-project entry
3. **Rename the repository** from `P###_name` to `C###_name`
4. **Update all references** in consuming projects, CI configs, and documentation
5. **Update CHANGELOG.md** in C010_standards to record the promotion
6. **Consider git submodule integration** if other core projects need to consume it

### Git Submodule Pattern for Core Projects

Core projects should be referenced by other projects via git submodules to:
- Maintain independent lifecycles and version control
- Reduce cascading failures (modularity over monolithic design)
- Enable independent testing and development

**Adding a Core Project as Submodule:**
```bash
# From the repo that must consume the core project
cd ~/SyncedProjects/C001_mission-control
git submodule add git@github.com:username/C004_open-web-ui.git external/open-web-ui
git commit -m "chore: add C004_open-web-ui as submodule"
```

**Updating Submodules:**
```bash
# Update to latest version
cd ~/SyncedProjects/C001_mission-control
git submodule update --remote --merge

# After updating, commit the new submodule reference
git add external/open-web-ui
git commit -m "chore: update C004_open-web-ui submodule"
```

**Example Architecture:**
```
C001_mission-control/
  external/
    ├── standards/      (submodule → C010_standards) ✓ Already implemented
    ├── agents/         (submodule → C003_agents)    ← Future
    └── mcp-tools/      (submodule → C005_mcp-tools) ← Future

C004_open-web-ui/
  └── integrations/     (connects to C001, C003 via APIs)
```

### Division of Responsibilities

**C010_standards (Governance):**
- Defines WHAT should exist (prescriptive, normative)
- Documents HOW things should be organized
- Validates compliance (validators, linters)
- NOT operational - doesn't run services

**C001_mission-control (Operations):**
- Implements monitoring and orchestration
- Runs health checks on other core services
- Provides runtime intelligence (Houston agent)
- Consumes C010_standards via submodule

**Other Core Projects (C003, C004, C005):**
- Follow standards defined in C010
- Report health to C001 when applicable
- Can be developed and tested independently

## Migration Checklist

### Immediate Actions
- [ ] Move P-projects from Workspace/ to root level
- [ ] Decide on REF001_Analytics_Canonical naming (W003?)
- [ ] Archive or relocate ROOT_CLEANUP_COMPLETE file
- [ ] Remove duplicate P-projects from Workspace/

### Future Improvements
- [ ] Create automated project discovery script
- [ ] Add validation script to check naming conventions
- [ ] Set up alerts for projects created outside root level
- [ ] Document what belongs in SharedData vs C-projects

---

**Last Updated:** 2025-10-11
**Maintained By:** Jeremy Bradford
**Authority:** This is the canonical definition of SyncedProjects organization
