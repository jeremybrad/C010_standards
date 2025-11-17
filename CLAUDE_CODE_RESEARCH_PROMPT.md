# SADB Ecosystem Research Project - Claude Code Instructions

**Your Role:** You are conducting deep research across Jeremy's 62 SyncedProjects repositories to document the complete ecosystem architecture, connections, and relationships.

**Critical:** Claude Desktop has tried this 4+ times and keeps hitting token limits without documenting findings. You have better token management and can execute this systematically across multiple sessions.

---

## File Locations (ABSOLUTE PATHS - NO VARIATION)

### Output Location
**ALL documentation goes here:**
```
/Users/jeremybradford/SyncedProjects/C010_standards/docs/ecosystem/
```

### Session Files (Detailed Analysis)
```
/Users/jeremybradford/SyncedProjects/C010_standards/docs/ecosystem/sessions/SESSION_3_CORE_INFRASTRUCTURE.md
/Users/jeremybradford/SyncedProjects/C010_standards/docs/ecosystem/sessions/SESSION_4_APPLICATIONS.md
/Users/jeremybradford/SyncedProjects/C010_standards/docs/ecosystem/sessions/SESSION_5_ANALYTICS.md
(etc...)
```

### Master Files (Synthesized Documentation)
```
/Users/jeremybradford/SyncedProjects/C010_standards/docs/ecosystem/COMPLETE_ECOSYSTEM_MAP.md
/Users/jeremybradford/SyncedProjects/C010_standards/docs/ecosystem/ABSTRACTION_LAYERS.md
/Users/jeremybradford/SyncedProjects/C010_standards/docs/ecosystem/MEMORY_INFRASTRUCTURE_GUIDE.md
```

### Progress Tracking
```
/Users/jeremybradford/Desktop/RESEARCH_PROGRESS.md (update after each project)
```

---

## Research Phases

### ✅ Phase 1: COMPLETE (by Claude Desktop)
- **C003_sadb_canonical** - Full documentation of SADB pipeline
- Location: `/Users/jeremybradford/SyncedProjects/C003_sadb_canonical/docs/`

### ✅ Phase 2: COMPLETE (by Claude Desktop)
- **Memory Systems** - 8 memory-related projects analyzed
- Output: `/Users/jeremybradford/SyncedProjects/C003_sadb_canonical/docs/SESSION_2_MEMORY_SYSTEMS.md`

### 🔄 Phase 3: IN PROGRESS (YOU START HERE)
**Core Infrastructure** - 8 critical backbone projects

**Projects to analyze:**
1. **P160_open-webui-ollama-setup** (⭐ CRITICAL - main LLM hub)
2. C001_mission-control
3. P015_claude-agent-orchestrator (Orky)
4. P181_terminal-insights
5. C010_standards (self-documentation)
6. C011_agents
7. P090_relay
8. P092_mirrorlab

**Output file:**
```
/Users/jeremybradford/SyncedProjects/C010_standards/docs/ecosystem/sessions/SESSION_3_CORE_INFRASTRUCTURE.md
```

### 📋 Future Phases (After Session 3)
- Phase 4: Application Layer (10 projects)
- Phase 5: Analytics & Work Tools (10 projects)
- Phase 6: Creative & Specialized (remaining projects)

---

## Research Methodology

### For Each Project:

1. **Read Key Files** (in this order):
   - `README.md` (overview & purpose)
   - `AGENTS.md` or `CLAUDE.md` (agent instructions)
   - `pyproject.toml` or `package.json` (dependencies)
   - Any architecture/design docs
   - Configuration files (`.env.example`, config files)

2. **Document These Aspects:**
   ```markdown
   ## [Project Name]

   **Status:** [Active/Prototype/Archived/etc]
   **Type:** [Core Infrastructure/Memory System/Application/etc]
   **Location:** [Full path]

   ### Purpose
   [1-2 sentences: What problem does this solve?]

   ### Key Capabilities
   - [Bullet list of main features]

   ### Dependencies
   **Depends on:** [Projects this needs to function]
   **Used by:** [Projects that depend on this]

   ### Technical Stack
   - Language: [Python/Node/etc]
   - Key libraries: [List major dependencies]
   - Ports/Services: [If applicable]

   ### Integration Points
   - [How it connects to other projects]
   - [APIs, file paths, protocols used]

   ### Current Status
   - [Operational status]
   - [Known issues or TODOs from docs]

   ### Notes for Future Sessions
   - [Anything unclear that needs investigation]
   - [Potential improvements or consolidation opportunities]
   ```

3. **Track Connections:**
   - Note when Project A imports/uses Project B
   - Track shared dependencies (SADB, Mission Control, etc.)
   - Identify integration patterns

4. **Update Progress File:**
   After completing each project, update `/Users/jeremybradford/Desktop/RESEARCH_PROGRESS.md`:
   ```markdown
   ## Session 3 Progress

   ✅ P160_open-webui-ollama-setup (2025-11-14 14:30)
   ⏸️ C001_mission-control (next)
   ⏳ P015_claude-agent-orchestrator
   ...

   **Last updated:** [timestamp]
   **Projects complete:** X/8
   **Current project:** [name]
   ```

---

## Critical Rules

### File Management
- ✅ **NEVER CREATE DUPLICATE FOLDERS** - Use exact paths above
- ✅ **UPDATE existing files** if they already have content
- ✅ **APPEND to session files** as you research each project
- ✅ **Git commit** after completing each project or every ~5 projects

### Session Management
- ✅ **Save progress frequently** - After each project minimum
- ✅ **Update RESEARCH_PROGRESS.md** after every project
- ✅ **If you need to stop mid-session:**
  1. Document exactly where you left off in RESEARCH_PROGRESS.md
  2. Save the session file with current findings
  3. Note what files you were about to read next

### Quality Standards
- ✅ **Be thorough but efficient** - Don't re-read files you've already analyzed
- ✅ **Note uncertainties** - If something is unclear, document it
- ✅ **Track technical debt** - Note duplicate functionality or cleanup opportunities
- ✅ **Preserve Jeremy's voice** - These are his systems, document them respectfully

---

## Special Focus: P160 (CRITICAL)

P160 is Jeremy's main LLM interface and deserves extra attention:
- Document ALL ports and services
- Map ALL integration points
- Identify ALL dependencies (Ollama, SADB, MirrorLab, etc.)
- Note the Betty Voice integration details
- Understand the Roundtable coordinator functionality
- Document RAG capabilities and how they connect to SADB

This is the **central nervous system** - everything else connects to it.

---

## When You're Done with Session 3

Create a summary at the top of SESSION_3_CORE_INFRASTRUCTURE.md:

```markdown
# Session 3: Core Infrastructure Analysis - Summary

**Completed:** 2025-11-14
**Projects Analyzed:** 8/8

## Key Findings

### Critical Discovery #1: [Major architectural insight]
[Details]

### Critical Discovery #2: [Important connection pattern]
[Details]

### Integration Map
[Visual or text diagram showing how these 8 projects connect]

### Recommendations
1. [Consolidation opportunities]
2. [Documentation needs]
3. [Technical debt items]

---
[Detailed project analyses follow...]
```

---

## How to Start

1. **Open Claude Code** in the workspace root:
   ```bash
   cd /Users/jeremybradford/SyncedProjects
   ```

2. **Create the progress tracker:**
   ```bash
   touch /Users/jeremybradford/Desktop/RESEARCH_PROGRESS.md
   ```

3. **Begin with P160:**
   Read `/Users/jeremybradford/SyncedProjects/P160_open-webui-ollama-setup/README.md`

4. **Follow the methodology** for each project

5. **Update Jeremy** via RESEARCH_PROGRESS.md after each project

---

## Questions or Issues?

If you encounter:
- **Missing files:** Note in documentation, continue
- **Unclear connections:** Document the uncertainty
- **Conflicting information:** Note both sources
- **Very large codebases:** Focus on README, docs, and entry points

**Remember:** Jeremy needs this to be complete and accurate. Take your time, document thoroughly, save frequently.

---

**Now begin with P160. Good luck! 🚀**
