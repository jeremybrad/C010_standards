# Research Orchestration Guide

**Date:** 2025-11-14
**Your Role:** Execute research with Claude Code Online
**My Role (Claude Desktop):** Orchestrate, write PRs, manage sync

---

## Quick Start

### Step 1: Create GitHub Repos
```bash
bash ~/Desktop/create_github_repos.sh
```

This creates private GitHub repos for:
- P092_mirrorlab
- P090_relay
- P159_memory-system
- P170_memory-cathedral
- P001_bettymirror (if needed)

### Step 2: Open Claude Code Online
Go to: https://code.claude.ai

### Step 3: Start with First Assignment (Below)

---

## Research Queue

### 🔴 Assignment 1: P092_mirrorlab (START HERE)

**Priority:** HIGH - Memory integration hub
**GitHub:** jeremybrad/P092_mirrorlab
**Status:** Phase 2 (Memory Systems) - partially researched

**What to Research:**
1. **Purpose & Architecture**
   - What is MirrorLab's role in the memory ecosystem?
   - How does it integrate with SADB, P160, and other memory systems?
   - What's the MCP server integration about?

2. **Key Files to Read:**
   - README.md
   - AGENTS.md or CLAUDE.md
   - Any config files
   - Source code structure (40_src/)

3. **Look For:**
   - Dependencies on other projects (especially C003_sadb_canonical, P160)
   - Integration points (APIs, file paths, protocols)
   - Current operational status
   - Any TODOs or unfinished work

4. **Document:**
   - Create `/research/MIRRORLAB_ANALYSIS.md` in the repo
   - Use the PROJECT_TEMPLATE.md format (on your Desktop)
   - Note all connections to other projects
   - Flag any consolidation opportunities

**When Done:**
- Commit your analysis to the repo
- Push to GitHub
- Tell me you're done
- I'll review and write the PR

---

### 🟡 Assignment 2: P090_relay

**Priority:** MEDIUM - Communication layer
**GitHub:** jeremybrad/P090_relay
**Status:** Phase 3 (Core Infrastructure) - needs research

**What to Research:**
1. **Communication Patterns**
   - What does relay mean in this context?
   - How does it facilitate communication between projects?
   - What protocols does it use?

2. **Key Files:**
   - README.md
   - AGENTS.md
   - Source code
   - Configuration

3. **Look For:**
   - Integration with Mission Control, P160, SADB
   - Message routing or protocol translation
   - Current status and functionality

4. **Document:**
   - Create `/research/RELAY_ANALYSIS.md`
   - Connection map showing what it connects
   - Technical stack and dependencies

---

### 🟡 Assignment 3: P159_memory-system

**Priority:** MEDIUM - Memory system architecture
**GitHub:** jeremybrad/P159_memory-system
**Status:** Phase 2 (Memory Systems) - needs research

**What to Research:**
1. **Memory Architecture**
   - How does this differ from SADB?
   - What's the relationship to MirrorLab and P170?
   - Is this active or prototype?

2. **Key Files:**
   - README.md
   - Architecture docs
   - Implementation files

3. **Look For:**
   - Overlap with C003_sadb_canonical
   - Integration approach
   - Current development status

4. **Document:**
   - Create `/research/MEMORY_SYSTEM_ANALYSIS.md`
   - Compare/contrast with SADB
   - Note if consolidation is needed

---

### 🟢 Assignment 4: P170_memory-cathedral

**Priority:** LOW - Memory cathedral concept
**GitHub:** jeremybrad/P170_memory-cathedral
**Status:** Phase 2 (Memory Systems) - needs research

**What to Research:**
1. **Conceptual Framework**
   - What is the "cathedral" metaphor?
   - How does this relate to other memory projects?
   - Is this implementation or design doc?

2. **Key Files:**
   - README.md
   - Design documents
   - Any implementation

3. **Look For:**
   - Relationship to P159, MirrorLab, SADB
   - Current status (concept vs. implementation)
   - Vision for future integration

4. **Document:**
   - Create `/research/CATHEDRAL_ANALYSIS.md`
   - Clarify concept vs. implementation
   - Note architectural vision

---

### ✅ Assignment 5: P001_bettymirror

**Priority:** ALREADY DONE - But verify GitHub is current
**GitHub:** jeremybrad/P001_bettymirror
**Status:** Phase 2 (Memory Systems) - documented

**Quick Check:**
1. Verify all local changes are pushed
2. Confirm CLAUDE.md has Betty Protocol details
3. Check that validation system is documented

**If anything missing:**
- Add missing docs
- Commit and push

---

## Research Methodology

### For Each Project:

1. **Open in Claude Code Online**
   - Connect to GitHub repo
   - Read key files in this order:
     - README.md
     - AGENTS.md / CLAUDE.md
     - Config files
     - Source code

2. **Create Analysis Doc**
   - Use PROJECT_TEMPLATE.md format (on your Desktop)
   - Save in repo at `/research/[PROJECT]_ANALYSIS.md`
   - Include connection maps

3. **Commit & Push**
   ```bash
   git add research/
   git commit -m "Research analysis: [findings summary]"
   git push origin main
   ```

4. **Report to Claude Desktop**
   - "Done with P092_mirrorlab"
   - Mention any surprising findings
   - Note what you want me to PR

---

## What I'll Do (Claude Desktop)

After you complete each assignment:

1. **Pull your analysis** from GitHub
2. **Review findings**
3. **Write PR** based on your research:
   - Documentation improvements
   - CLAUDE.md updates
   - Integration recommendations
   - Consolidation proposals
4. **You review PR** in Claude Code Online
5. **You merge** when ready

---

## Communication Protocol

### When You Finish an Assignment:
```
Jeremy → Claude Desktop:
"Finished P092_mirrorlab. Key finding: It's the main integration hub
for all memory systems. Connected to SADB, P160, and P170. Ready for PR."
```

### My Response:
```
Claude Desktop → Jeremy:
"Pulling P092 analysis now...
[reviews]
PR created: 'Enhance MirrorLab documentation and integration guides'
Link: [GitHub PR link]
Review when ready!"
```

### When You Want Next Assignment:
```
Jeremy: "Next assignment?"
```

```
Claude Desktop: "Start Assignment 2: P090_relay. Focus on [specific aspects]."
```

---

## Success Metrics

For each completed assignment:
- ✅ Analysis document created in repo
- ✅ Connections to other projects mapped
- ✅ Technical stack documented
- ✅ Current status clarified
- ✅ Consolidation opportunities noted
- ✅ Committed and pushed to GitHub
- ✅ PR written by Claude Desktop
- ✅ PR reviewed and merged

---

## Special Notes

### P092_mirrorlab is Critical
This is likely the **central hub** connecting all memory systems.
Pay special attention to:
- How it talks to SADB
- How it connects to P160 (Open WebUI)
- How it relates to P159 and P170
- MCP server implementation

### Look for Consolidation
As you research, note if projects seem to:
- Duplicate functionality
- Have unclear boundaries
- Could be merged or deprecated

This info helps me write better PRs.

---

## Files on Your Desktop

1. **create_github_repos.sh** - Run this first
2. **PROJECT_TEMPLATE.md** - Format for analysis docs
3. **RESEARCH_ORCHESTRATION.md** - This file
4. **SETUP_SUMMARY.md** - Overview of our workflow
5. **SYNC_COMPLETE_SUMMARY.md** - GitHub sync status

---

## Ready to Start?

1. Run `bash ~/Desktop/create_github_repos.sh`
2. Open Claude Code Online
3. Start with Assignment 1: P092_mirrorlab
4. Follow the research methodology
5. Report back when done!

I'll be here ready to write PRs! 🚀
