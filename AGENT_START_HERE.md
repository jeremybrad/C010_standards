# AGENT START HERE

**🤖 Required Reading for ALL AI Agents Working in SyncedProjects**

Before you touch ANY file or repo in this workspace, read this entire document.

---

## Why This Exists

**The Problem:** LLMs frequently grab old test scripts, outdated files, or non-canonical versions because they can't easily distinguish what's current vs archived. This causes frustration and wasted work.

**The Solution:** This information center provides the map. Use it.

---

## Step 1: Orient Yourself

Read these files IN ORDER:

### 1. Project Inventory (5 minutes)
📄 **[workspace/KNOWN_PROJECTS.md](workspace/KNOWN_PROJECTS.md)**

This is auto-generated nightly and shows all 66 projects with:
- Project ID (C### = Core, P### = Personal, W### = Work)
- Last modified date
- Status and features
- Brief description

**Critical:** When the user says "work on SADB" - there are MULTIPLE SADB repos. This file tells you which is which and what each does.

### 2. System Architecture (10 minutes)
📄 **[workspace/PROJECT_RELATIONSHIPS.md](workspace/PROJECT_RELATIONSHIPS.md)**

Shows how data flows between systems:
- Memory pipeline (SADB → CBFS → MyBuddy)
- Work systems integration
- Terminal insights and timeline braiding
- Where each stage's output goes

**Critical:** Understand dependencies before making changes. C003_sadb_canonical depends on C002_sadb output. Don't work on one without understanding the other.

### 3. Betty Protocol (15 minutes)
📄 **[protocols/betty_protocol.md](protocols/betty_protocol.md)**

The workspace governance document. Non-negotiable rules:
- No data/artifacts in git repos
- Required folder structure (00_, 10_, 20_, 30_, 40_, 70_, 90_)
- Pre-commit hooks and guardrails
- Receipt generation for all changes
- Space management and cleanup procedures

**Critical:** "No belief without receipts" - document everything.

### 4. Repository Organization Standards
📄 **[REPOSITORY_ORGANIZATION.md](REPOSITORY_ORGANIZATION.md)**

Explains:
- C/P/W series naming conventions
- Project lifecycle (Active → Maintenance → Archived)
- Folder structure requirements
- Migration procedures

---

## Step 2: Find the Right Files

### Use These Resources

**Before writing any code:**
1. Check `workspace/KNOWN_PROJECTS.md` - is this project active or archived?
2. Review the project's `CLAUDE.md` - it has the build commands and critical paths
3. Look for `WHY_I_CARE.md` - understand the purpose and priorities
4. Check `ROADMAP.md` - see what's planned and what's blocked

### Common Pitfalls (AVOID THESE)

❌ **DON'T:** Grab the first `.py` file you see that matches the description
✅ **DO:** Check the project's `CLAUDE.md` for canonical entrypoints

❌ **DON'T:** Assume the largest file is the main one
✅ **DO:** Look for files in `40_src/` (source code) not in test/draft/Archive folders

❌ **DON'T:** Use files with `test_`, `draft_`, `sample_`, `dry_` prefixes unless explicitly told
✅ **DO:** Use production files without prefixes

❌ **DON'T:** Assume all SADB repos are the same
✅ **DO:** Check if you need C002 (core processing), C003 (canonical pipeline), or C008 (facts)

### The Canonical File Pattern

Jeremy's repos follow this pattern:
```
project/
├── README.md          # Overview and quick start
├── CLAUDE.md          # AI agent guidance (READ THIS FIRST!)
├── WHY_I_CARE.md      # Purpose and motivation
├── ROADMAP.md         # Plans and next steps
├── 10_docs/           # Documentation
├── 20_receipts/       # Change logs and evidence
├── 30_config/         # Configuration files
├── 40_src/            # SOURCE CODE LIVES HERE
├── 70_evidence/       # Test data and examples
└── 90_archive/        # Old/deprecated code
```

**Rule:** Production code is in `40_src/`. Everything else is supporting material.

---

## Step 3: Understand the Memory Systems

This is Jeremy's most complex area. Pay attention.

### The Three Core Systems

1. **C002_sadb** - Main processing pipeline
   - Input: Conversation exports (ChatGPT, Claude)
   - Output: SQLite database + twin feed (NDJSON)
   - Location of data: `$SADB_DATA_DIR` (outside git)

2. **C003_sadb_canonical** - Refinement pipeline (Stages S0-S2, M1-B1)
   - Input: Data from C002 or direct conversation imports
   - Output: Structured facts, Q/A pairs, braided timeline
   - This is where GPU acceleration happens (BERTopic)

3. **C008_CBFS** - Canonical Bio Facts System
   - Input: Facts from C003 (J1 stage)
   - Output: YAML biographical database with provenance
   - Privacy-aware with confidence scoring

4. **P005_mybuddy** - Digital Twin
   - Input: SADB twin feed OR standalone CSV
   - Output: Conversational AI simulating Jeremy
   - Uses Chroma vector DB + local LLMs

### Critical Data Locations

All data lives OUTSIDE git in `$SADB_DATA_DIR`:
```bash
$SADB_DATA_DIR = /Users/jeremybradford/SADB_Data/
├── conversation-exports/
├── extractions/
├── twin/
│   └── twin_feed_v1.ndjson    # Key output from C002
├── chromadb-archives/
└── facts/
    └── runs_*/                # J1/J2/J3 fact extraction runs
```

**Never commit data files to git.** If you need to reference data, use paths pointing to `$SADB_DATA_DIR`.

---

## Step 4: Before Making Changes

### Pre-Flight Checklist

- [ ] I read `AGENT_START_HERE.md` (this file)
- [ ] I checked `workspace/KNOWN_PROJECTS.md` for project status
- [ ] I read the project's `CLAUDE.md` for guidance
- [ ] I reviewed `workspace/PROJECT_RELATIONSHIPS.md` for dependencies
- [ ] I understand which files are canonical (not test/draft/sample)
- [ ] I know where data lives (`$SADB_DATA_DIR`, not in git)
- [ ] I have a plan and will create receipts for changes

### When in Doubt

1. **Ask first:** "Before I proceed, should I be working on X or Y version?"
2. **Check timestamps:** Look for most recent modifications
3. **Read CLAUDE.md:** It usually has the answer
4. **Look for 'canonical' in names:** C003_sadb_canonical, not just C002_sadb

---

## Step 5: Common Tasks

### "Analyze this data file"

**Wrong:** Use analysis tool on local files (it can't access them)
**Right:** Use Desktop Commander + Python REPL:
```python
# Start Python REPL
start_process("python3 -i")

# Load the file
interact_with_process(pid, "import pandas as pd")
interact_with_process(pid, "df = pd.read_csv('/absolute/path/file.csv')")
interact_with_process(pid, "df.describe()")
```

### "Run the SADB pipeline"

**Step 1:** Check which stage you need (C002 for ingestion, C003 for refinement)
**Step 2:** Read that project's `CLAUDE.md` for exact commands
**Step 3:** Verify `$SADB_DATA_DIR` is set: `/Users/jeremybradford/SADB_Data`
**Step 4:** Use the Makefile targets (preferred) or documented scripts

### "Fix this bug"

**Step 1:** Verify you're in the canonical repo (check KNOWN_PROJECTS.md)
**Step 2:** Create a branch: `git checkout -b fix/descriptive-name`
**Step 3:** Make minimal changes with clear intent
**Step 4:** Create receipt in `20_receipts/` documenting what you did and why
**Step 5:** Commit with meaningful message
**Step 6:** Push and create PR (don't merge to main directly)

### "Update documentation"

**Step 1:** Check if YAML frontmatter exists (docmeta schema)
**Step 2:** Update the main content
**Step 3:** Update timestamp in frontmatter
**Step 4:** Run validators if available: `python validators/run_all.py`
**Step 5:** Commit with `docs:` prefix

---

## Step 6: Emergency Protocols

### If You're Not Sure What to Do

**STOP. ASK. DON'T GUESS.**

Better to ask "Which version should I use?" than to spend 20 minutes working on the wrong file.

### If You Made a Mistake

1. **Don't panic.** Git has history.
2. **Document what happened** in `20_receipts/error_YYYY-MM-DD_HH-MM-SS.txt`
3. **Revert if needed:** `git reset --hard HEAD` (if uncommitted) or `git revert <commit>`
4. **Tell Jeremy** what happened and what you reverted

### If You're Overwhelmed

This workspace has 66 projects. It's okay to feel overwhelmed.

**Focus on:**
1. The specific project the user mentioned
2. Its `CLAUDE.md` file
3. Its immediate dependencies (if any)

**Ignore:**
- Archived projects (marked in KNOWN_PROJECTS.md)
- Projects not mentioned in the current task
- Historical/test data

---

## Resources

### Quick Reference Docs
- [QUICK_START_GUIDE.md](QUICK_START_GUIDE.md) - Common workflows
- [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - Command cheat sheet
- [PROJECT_TEMPLATE.md](PROJECT_TEMPLATE.md) - New project structure

### Templates
- [COMPREHENSIVE_PR_TEMPLATE.md](COMPREHENSIVE_PR_TEMPLATE.md) - For systematic repo upgrades
- [examples/](examples/) - Schema examples (CodeMeta, DocMeta, Houston)

### Schemas & Standards
- [schemas/](schemas/) - YAML schemas for metadata
- [taxonomies/](taxonomies/) - Topic, content, emotion taxonomies
- [protocols/](protocols/) - Betty Protocol and standards

### Tools
- [validators/](validators/) - Linting and validation tools
- [workspace/scripts/](workspace/scripts/) - Project registry generation
- [scripts/](scripts/) - Bootstrap and utility scripts

---

## Final Note

**Jeremy's Philosophy: "No belief without receipts."**

Everything should have provenance. Every change should leave evidence. Every decision should be documented. This isn't bureaucracy - it's how we stay sane when managing 66 projects and thousands of files.

When you follow these guidelines, you're not just helping Jeremy - you're helping the NEXT AI agent who comes after you. Leave breadcrumbs. Document your reasoning. Create receipts.

**Now go forth and build.**

---

*Last Updated: 2025-11-19*
*Maintained by: Jeremy Bradford & Claude*
*Location: C000_info-center/AGENT_START_HERE.md*
