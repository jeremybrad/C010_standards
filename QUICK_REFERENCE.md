# Quick Reference Card 🎯

**Keep this open while researching!**

---

## 1️⃣ First Time Setup (Do Once)

```bash
# Create GitHub repos (5 private repos)
bash ~/Desktop/create_github_repos.sh
```

---

## 2️⃣ For Each Research Assignment

### Open Claude Code Online
https://code.claude.ai → Connect to GitHub → Select repo

### Research Template Location
`~/Desktop/PROJECT_TEMPLATE.md`

### Create Analysis Doc
Location: `/research/[PROJECT]_ANALYSIS.md` in the repo
Format: Use PROJECT_TEMPLATE.md structure

### Key Sections to Document
- Purpose (why it exists)
- Key Capabilities (what it does)
- Dependencies (what it needs)
- Used By (who uses it)
- Integration Points (how it connects)
- Current Status (active/prototype/deprecated)
- Connection Map (visual of relationships)

### Commit & Push
```bash
git add research/
git commit -m "Research analysis: [brief summary]"
git push origin main
```

### Tell Claude Desktop
"Done with [PROJECT]. Key findings: [1-2 sentences]"

---

## 3️⃣ Research Queue (Priority Order)

1. 🔴 **P092_mirrorlab** (START HERE)
2. 🟡 **P090_relay**
3. 🟡 **P159_memory-system**
4. 🟢 **P170_memory-cathedral**
5. ✅ **P001_bettymirror** (verify only)

---

## 4️⃣ What to Look For

### In Every Project:
- README.md (overview)
- AGENTS.md or CLAUDE.md (AI instructions)
- pyproject.toml / package.json (dependencies)
- Source code structure (40_src/)
- Config files (30_config/)

### Questions to Answer:
- What problem does this solve?
- What other projects does it depend on?
- What projects depend on it?
- How does it integrate (APIs, files, protocols)?
- Is it actively used or prototype?
- Could it be consolidated with something else?

---

## 5️⃣ Communication Protocol

### When Done:
```
You: "Done with P092_mirrorlab. It's the central memory hub connecting
SADB, P160, P159, and P170. Ready for PR."
```

### Next Assignment:
```
You: "Next assignment?"
Me: "Start P090_relay. Focus on communication patterns."
```

---

## 6️⃣ Files on Desktop

| File | Purpose |
|------|---------|
| `create_github_repos.sh` | Create GitHub repos (run once) |
| `WORKFLOW_SUMMARY.md` | Complete workflow overview |
| `RESEARCH_ORCHESTRATION.md` | Detailed research assignments |
| `PROJECT_TEMPLATE.md` | Analysis document format |
| `QUICK_REFERENCE.md` | This file! |

---

## 7️⃣ Common Commands

```bash
# Clone repo locally (if needed)
cd ~/SyncedProjects
git clone git@github.com:jeremybrad/[REPO_NAME].git

# Check status
git status

# Create research folder
mkdir research

# Add and commit
git add research/
git commit -m "Research analysis: [PROJECT]"
git push origin main

# Pull changes (if Claude Desktop made PRs)
git pull origin main
```

---

## 8️⃣ Success Checklist

After each project:
- ✅ Analysis doc created
- ✅ All sections filled out
- ✅ Connection map included
- ✅ Committed to GitHub
- ✅ Pushed to remote
- ✅ Reported to Claude Desktop
- ✅ Waiting for PR

---

## 9️⃣ Tips

- **Be thorough but efficient** - Don't spend hours on one project
- **Note uncertainties** - If unclear, document the question
- **Map connections** - This is the most valuable insight
- **Think consolidation** - Could projects be merged?
- **Use template** - Consistency helps me write better PRs

---

## 🔟 Emergency Contact

If something breaks:
1. Check WORKFLOW_SUMMARY.md for context
2. Check SYNC_COMPLETE_SUMMARY.md for sync status
3. Ask Claude Desktop for help
4. GitHub issues are okay too!

---

**Current Assignment:** Run `create_github_repos.sh`, then start with P092_mirrorlab! 🚀

**Claude Desktop Status:** Token usage: 93k/190k (48%) - Ready to write PRs!
