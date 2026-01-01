# PR Execution Hub

**Status:** Active modernization effort
**Location:** `/Users/jeremybradford/SyncedProjects/PR-execution-hub/`

---

## What This Is

This directory tracks the systematic modernization of all SyncedProjects repositories. The active execution environment lives in `PR-execution-hub/` (parent directory level), but we track high-level status here in the info-center for visibility.

---

## Current Status

**Modernization Goal:** Apply Betty Protocol standards to all 66 projects

**Standards Being Applied:**
- YAML frontmatter in documentation
- CLAUDE.md files with AI guidance
- WHY_I_CARE.md (purpose and motivation)
- ROADMAP.md (plans and next steps)
- Consistent folder structure (00_, 10_, 20_, 30_, 40_, etc.)
- Code linting and quality checks
- Test coverage (where applicable)

---

## Execution Strategy

### Current Approach (Systematic, One at a Time)

We're using Claude Code Cloud to execute PRs systematically:

1. **Generate PR** for a single repo (using templates from PR-execution-hub)
2. **Submit to Claude Code** Cloud for execution
3. **Review changes** on feature branch
4. **Merge** if acceptable
5. **Track progress** in MODERNIZATION_STATUS.md (to be created)
6. **Repeat** for next repo

**Why One at a Time:**
- Manageable scope per execution
- Clear success/failure per repo
- Easier to review changes
- Lower risk than batch operations

### Tools & Resources

**Active Repository:**
`/Users/jeremybradford/SyncedProjects/PR-execution-hub/`

Contains:
- `modernize_all_v2.py` - Betty-approved modernization script
- `prs/` - Generated PR files for each repo
- `analysis/` - Code inventories and doc coverage reports
- `scripts/` - Automation utilities
- Execution guides and safety procedures

**Key Files:**
- `START_HERE.md` - Quick prompt for Claude Code Cloud
- `CLAUDE_CODE_EXECUTION_PROMPT.md` - Detailed execution instructions
- `BULLETPROOF_PROCESS.md` - Verified workflow for PRs

---

## Priority Repos

**High Priority:**
1. **C004_star-extraction** - Critical for job search (STAR stories for interviews)
2. **C002_sadb** - Core memory system
3. **C003_sadb_canonical** - Pipeline refinement
4. **C008_CBFS** - Biographical facts system

**Medium Priority:**
- All other C-series (Core infrastructure)
- P-series projects actively in use

**Lower Priority:**
- Archived projects
- Experimental/test projects
- Projects marked for deprecation

---

## Progress Tracking

**To Be Created:** `workspace/MODERNIZATION_STATUS.md`

Will track:
- Repos completed (with links to merged PRs)
- Repos in progress (with branch names)
- Repos pending (in priority order)
- Repos skipped (with reasons)
- Credit usage (Claude Code Cloud)

---

## Previous Attempt: Mega-Repo Strategy (Abandoned)

**What We Tried:**
Clone all repos into one mega-repo, apply changes in bulk, push back out.

**Why It Failed:**
- Too complex to track which changes went where
- Hard to review comprehensively
- Risk of cross-contamination between repos
- Difficult to rollback individual repos

**Location of Attempt:**
`/Users/jeremybradford/SyncedProjects/PR/`

**Status:**
Some valuable work exists there, but extracting it is more effort than redoing systematically. May archive for reference.

---

## Using This System

### For Humans

1. **Check current status:** (MODERNIZATION_STATUS.md when created)
2. **Pick next repo:** Prioritize based on need
3. **Generate PR:** Use templates from PR-execution-hub
4. **Execute:** Submit to Claude Code Cloud
5. **Review:** Check branch before merging
6. **Update status:** Mark as complete

### For AI Agents

**Before modernizing a repo:**
1. Check if it's already been modernized (MODERNIZATION_STATUS.md)
2. Read the repo's current CLAUDE.md (if exists)
3. Use PR templates from `/Users/jeremybradford/SyncedProjects/PR-execution-hub/`
4. Follow Betty Protocol strictly
5. Create receipts for all changes

**Don't:**
- Apply changes directly to main
- Skip pre-flight checks
- Batch multiple repos without clear boundaries
- Forget to document what was changed and why

---

## Integration with Info-Center

This directory is part of C000_info-center to provide visibility into workspace-wide modernization efforts.

**Related Documents:**
- [workspace/KNOWN_PROJECTS.md](../KNOWN_PROJECTS.md) - See which repos exist
- [protocols/betty_protocol.md](../../protocols/betty_protocol.md) - Standards being applied
- [COMPREHENSIVE_PR_TEMPLATE.md](../../COMPREHENSIVE_PR_TEMPLATE.md) - Template structure

---

## Resources

### Execution Environment
**Primary Location:** `/Users/jeremybradford/SyncedProjects/PR-execution-hub/`

**Key Scripts:**
- `modernize_all_v2.py` - Main modernization script
- `execute_all.sh` - Batch execution wrapper
- `scripts/create_github_repos.sh` - GitHub repo setup

**Documentation:**
- `CLAUDE_CODE_EXECUTION_PROMPT.md` - How to use Claude Code Cloud
- `SAFE_EXECUTION_PLAN.md` - Risk mitigation
- `WHAT_ACTUALLY_MATTERS.md` - Focus areas

### Templates
**Location:** `/Users/jeremybradford/SyncedProjects/PR-execution-hub/prs/`

Contains PRs for ~24 repos already generated.

**Template Structure:**
- Pre-flight checks (verify repo state)
- Change specifications (what to add/update)
- Validation steps (how to verify)
- Rollback plan (if something goes wrong)

---

## Credit Management

**Claude Code Cloud Credit:**
- Extended deadline (as of November 2025)
- Use strategically on high-value repos
- Heavy compute tasks (testing, doc generation) are worthwhile
- Track usage in MODERNIZATION_STATUS.md

---

## Next Steps

1. [ ] Create `workspace/MODERNIZATION_STATUS.md`
2. [ ] Review which repos already have PRs generated
3. [ ] Execute PRs for C004_star-extraction (highest priority)
4. [ ] Build momentum with smaller repos
5. [ ] Document lessons learned for future modernizations

---

*Last Updated: 2025-11-19*
*Part of: C000_info-center/workspace/*
*See Also: /Users/jeremybradford/SyncedProjects/PR-execution-hub/*
