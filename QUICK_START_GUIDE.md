# Quick Start Guide: Using Claude Code for SADB Research

## What You'll Do

1. **Open Claude Code** in your workspace root
2. **Give it the master prompt** (from CLAUDE_CODE_RESEARCH_PROMPT.md)
3. **Let it work** - it will save progress as it goes
4. **Check progress** periodically via RESEARCH_PROGRESS.md on your Desktop

---

## Step-by-Step Instructions

### Step 1: Open Claude Code
```bash
cd /Users/jeremybradford/SyncedProjects
claude-code
```

### Step 2: Give Claude Code This Prompt

**Copy/paste this into Claude Code:**

```
I need you to conduct deep research across my SyncedProjects repositories.

I have a detailed instruction file on my Desktop with the complete methodology,
file paths, and requirements.

Please read and follow:
/Users/jeremybradford/Desktop/CLAUDE_CODE_RESEARCH_PROMPT.md

Start with Session 3 (Core Infrastructure - 8 projects). The most critical
project is P160_open-webui-ollama-setup (my main LLM hub).

Save all output to:
/Users/jeremybradford/SyncedProjects/C010_standards/docs/ecosystem/

Update progress to:
/Users/jeremybradford/Desktop/RESEARCH_PROGRESS.md

Begin when ready.
```

### Step 3: Monitor Progress

**Check this file periodically:**
```bash
cat /Users/jeremybradford/Desktop/RESEARCH_PROGRESS.md
```

You should see updates like:
```
✅ P160_open-webui-ollama-setup (2025-11-14 14:30)
✅ C001_mission-control (2025-11-14 14:45)
⏸️ P015_claude-agent-orchestrator (in progress)
```

---

## What Claude Code Will Create

### Session Files (Detailed Analysis)
```
C010_standards/docs/ecosystem/sessions/SESSION_3_CORE_INFRASTRUCTURE.md
```

### Progress Tracker (Desktop)
```
/Users/jeremybradford/Desktop/RESEARCH_PROGRESS.md
```

---

## If Claude Code Needs to Stop Mid-Session

Claude Code will:
1. Save all findings so far
2. Update RESEARCH_PROGRESS.md with exact stopping point
3. You can resume with: "Continue from where you left off"

---

## After Session 3 Completes

Claude Code will have:
- ✅ Analyzed all 8 Core Infrastructure projects
- ✅ Documented connections and dependencies
- ✅ Created comprehensive SESSION_3 file
- ✅ Updated progress tracker

You can then review with me (Claude Desktop) and decide:
- Continue to Session 4 (Applications)?
- Make any adjustments to methodology?
- Create synthesis documents?

---

## Why This Works Better

**Claude Code advantages:**
- ✅ Better token management across long sessions
- ✅ Can resume from exact stopping point
- ✅ Designed for deep code/file analysis
- ✅ Saves frequently automatically

**Claude Desktop role (me):**
- ✅ Architecture & organization
- ✅ Quality review
- ✅ Synthesis & recommendations
- ✅ Integration with other systems

---

## Files on Your Desktop

1. **CLAUDE_CODE_RESEARCH_PROMPT.md** - Complete instructions for Claude Code
2. **RESEARCH_PROGRESS.md** - Will be created by Claude Code, tracks progress
3. **SESSION_HANDOFF_SADB_RESEARCH.md** - Our earlier handoff doc (for reference)

---

**Ready to start?** Open Claude Code and give it the prompt above! 🚀
