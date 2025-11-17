# Retirement Heuristics for Repository Management

**Version:** 1.0
**Created:** 2025-11-14
**Purpose:** Systematic methodology for deciding whether to keep, archive, or delete repositories

---

## Overview

Not all repositories deserve to live forever. As ecosystems evolve, some repos become redundant, obsolete, or simply don't justify their maintenance burden. This guide provides a systematic framework for making these difficult decisions.

**Goal:** Focus credits and attention on repos that matter, gracefully retire those that don't.

---

## The Core Question

**"If this repo disappeared tomorrow, what would break?"**

- **Nothing breaks:** Strong deletion candidate
- **Something breaks, but alternatives exist:** Archive candidate
- **Critical systems break:** Keep and modernize

---

## Retirement Flags (Section 6 of Audit Checklist)

### Flag 1: Duplicates Another Repo's Functionality

**How to detect:**
- Search for similar project names
- Check if RELATIONS.yaml shows overlap
- Ask: "Do we have another repo that does this?"

**Examples:**
- Two repos for the same memory extraction pipeline
- Multiple implementations of the same API client
- Duplicate experiment repos trying similar approaches

**Decision:**
- If one is clearly better → Delete the worse one
- If both have value → Merge into single repo
- If experimenting → Keep the one you're actively using

---

### Flag 2: Empty or "Just a Folder"

**How to detect:**
- `find . -type f | wc -l` returns < 5 files
- No README
- No src/ or code directories
- Just .git and maybe a .gitignore

**Examples:**
- Repo created "to claim the name" but never built
- Template that was copied elsewhere and original abandoned
- Folder created during planning that never materialized

**Decision:**
- If it's truly empty → Delete immediately
- If it has 1-2 meaningful files → Extract to appropriate repo, then delete
- If it's a template placeholder → Document in TODO.md and delete

---

### Flag 3: No README or Unclear Purpose

**How to detect:**
- README missing entirely
- README says "TODO" or is template boilerplate
- You can't explain what it does in one sentence
- Project description is vague ("misc utilities")

**Examples:**
- `P0XX_experiments` with no context
- `test-thing` with no explanation
- `old-scripts` with no inventory

**Decision:**
- If you remember what it is → Write README, evaluate other flags
- If you don't remember → Archive if it looks functional, delete if not
- If it's experimental cruft → Delete

---

### Flag 4: Untouched in >2 Years

**How to detect:**
```bash
git log -1 --format="%ar" | grep "year"
```

**But consider:**
- Some stable utilities don't need updates
- Some experiments succeeded and became stable
- Some infrastructure "just works"

**Examples:**
- Script that runs perfectly and needs no changes
- Stable library with no bugs or feature requests
- Abandoned experiment from 2022

**Decision:**
- If it's stable and used → Keep (but document stability in README)
- If it's stable and unused → Archive
- If it was an experiment that ended → Delete
- If you're not sure → Check RELATIONS.yaml for dependencies

---

### Flag 5: Only Stores Data (Should Be in $SADB_DATA_DIR)

**How to detect:**
- Repo is 90%+ `.json`, `.csv`, `.jsonl` files
- No scripts, just data files
- Named like a data dump (e.g., `exports-backup`)

**Examples:**
- Conversation export dumps
- Raw data collections
- Output artifact archives

**Decision:**
- **Always move data to `$SADB_DATA_DIR`**
- Delete the repo after migration
- Keep only processing scripts if valuable
- Data belongs in SADB, not git repos

---

### Flag 6: Depends on Deprecated Code

**How to detect:**
- Uses Python 2
- Requires libraries that no longer exist
- Depends on old API endpoints that shut down
- Built for pre-Sonnet Claude models

**Examples:**
- Python 2.7 scripts
- Node.js 8.x projects
- Code using deprecated OpenAI engines

**Decision:**
- If worth upgrading → Add to modernization backlog
- If not worth upgrading → Archive with note about deprecation
- If completely unusable → Delete

---

### Flag 7: Purpose Unclear or Forgotten

**How to detect:**
- You look at the repo and think "what is this?"
- No documentation explains why it exists
- Can't find references to it in other projects
- Not mentioned in any RELATIONS.yaml files

**Examples:**
- `temp-2023-experiment`
- `quick-test-thing`
- `P0XX_misc`

**Decision:**
- Spend 5 minutes trying to remember
- Check git history for clues
- If still unclear → Archive (safer than deletion)
- If clearly throwaway → Delete

---

### Flag 8: Builds on Old Workflows

**How to detect:**
- Predates Betty Protocol entirely
- Uses outdated directory structure
- Built for deprecated tools (e.g., old Ollama versions)
- Incompatible with modern ecosystem

**Examples:**
- Projects from early 2024 before SADB
- Repos using old memory systems
- Tools built for deprecated APIs

**Decision:**
- If core functionality still needed → Rewrite using modern patterns
- If peripheral → Archive
- If superseded → Delete

---

### Flag 9: Cannot Modernize in 1-2 Hours

**How to detect:**
- Estimate time to bring up to standards
- If estimate > 2 hours of focused work → Flag
- Consider: Is the value worth the effort?

**Examples:**
- Complex projects with no docs requiring archaeology
- Repos needing major refactoring
- Projects with unclear dependencies

**Decision:**
- If high-value (core infrastructure) → Accept the work
- If medium-value → Archive and document what it did
- If low-value → Delete

---

### Flag 10: Was an Experiment Now Replaced

**How to detect:**
- README says "experiment" or "prototype"
- Functionality exists in another repo now
- Was exploring an approach you didn't take

**Examples:**
- Memory extraction v1 (replaced by v3)
- Early Houston Router experiments
- API client experiments (before stable version)

**Decision:**
- If it has historical value → Archive with "superseded by [X]" note
- If it's just cruft → Delete
- Keep only if it's teaching material

---

## Scoring Methodology

### Step 1: Count Flags (0-10)

Go through all 10 flags, check which apply.

### Step 2: Apply Decision Matrix

**0-2 flags:** ✅ **Keep & Modernize**
- Repo is healthy or needs minor work
- Worth the modernization investment
- Focus PR generation here

**3-4 flags:** 🗄️ **Archive**
- Repo has issues but isn't broken
- May have historical value
- Not worth active maintenance
- Move to `90_archive/` in a meta-repo or export to separate archive

**5+ flags:** 🗑️ **Delete**
- Repo is broken, obsolete, or redundant
- Keeping it creates clutter
- No one will miss it
- Delete confidently

### Step 3: Check Edge Cases

**Before deleting, check:**
- [ ] No other repos reference this in RELATIONS.yaml
- [ ] No active systems depend on this
- [ ] No unique data will be lost
- [ ] No credentials stored here that need extraction

**Before archiving, check:**
- [ ] Document why archived (in archive README)
- [ ] Note what replaced it (if applicable)
- [ ] Preserve any unique learnings or approaches

---

## Special Considerations

### High-Value Exceptions

**Even with 3-4 flags, keep if:**
- Core infrastructure (C-series)
- Actively used in daily workflow
- Part of job search (e.g., STAR extraction)
- Foundation for other projects

### Low-Value Deletions

**Even with 0-2 flags, delete if:**
- Trivial utility (10-line script easily recreated)
- Duplicate of functionality elsewhere
- Created by accident or typo
- Test repo never meant to persist

### Archive Strategy

**Good archive candidates:**
- Completed experiments with learnings
- Superseded implementations (v1 when v3 exists)
- Historical approaches (pre-Betty Protocol)
- Reference implementations

**Archive format:**
```
90_archive/
├── PXXX_old_project/
│   ├── ARCHIVED.md  # Why archived, what replaced it
│   ├── [original files...]
│   └── README.md  # Original documentation
```

---

## Decision Tree

```
START
  │
  ├─ Count retirement flags (0-10)
  │
  ├─ 0-2 flags?
  │   ├─ YES → Is it high-value or actively used?
  │   │   ├─ YES → ✅ KEEP & MODERNIZE
  │   │   └─ NO → Is it trivial or duplicate?
  │   │       ├─ YES → 🗑️ DELETE
  │   │       └─ NO → ✅ KEEP & MODERNIZE
  │   │
  │   └─ NO → Continue...
  │
  ├─ 3-4 flags?
  │   ├─ YES → Is it core infrastructure?
  │   │   ├─ YES → ✅ KEEP & MODERNIZE (exception)
  │   │   └─ NO → Does it have historical value?
  │   │       ├─ YES → 🗄️ ARCHIVE
  │   │       └─ NO → 🗑️ DELETE
  │   │
  │   └─ NO → Continue...
  │
  └─ 5+ flags?
      └─ YES → Does it contain unique data or learnings?
          ├─ YES → Extract first, then 🗑️ DELETE
          └─ NO → 🗑️ DELETE IMMEDIATELY
```

---

## Examples from Jeremy's Ecosystem

### ✅ Keep: C002_sadb
**Flags:** 0/10
- Core infrastructure
- Actively used
- Well-documented
- Foundation for memory system
**Decision:** Keep & Modernize

### ✅ Keep: C004_star-extraction
**Flags:** 0/10
- Critical for job search
- Actively developing
- Unique functionality
- High personal value
**Decision:** Keep & Modernize (HIGH PRIORITY)

### 🗄️ Archive: P092_mirrorlab (current state with data)
**Flags:** 3/10
- ✅ Contains 50MB of extraction data (should be in SADB)
- ✅ Purpose has evolved (templates only now)
- ✅ Needs major cleanup
**Decision:** Clean up data first, then keep as templates repo

### 🗑️ Delete: P0XX_temp_test (hypothetical)
**Flags:** 6/10
- ✅ Empty folder
- ✅ No README
- ✅ Untouched in 3 years
- ✅ Purpose forgotten
- ✅ No dependencies
- ✅ Was a quick test
**Decision:** Delete immediately

---

## Automation Potential

**Future Mission Control feature:**

```python
def assess_retirement_risk(repo_path):
    """Score repo for retirement."""
    flags = 0
    reasons = []

    # Check each flag
    if duplicates_functionality(repo_path):
        flags += 1
        reasons.append("Duplicates another repo")

    if is_empty(repo_path):
        flags += 1
        reasons.append("Empty or minimal")

    # ... check all 10 flags

    if flags >= 5:
        return "DELETE", flags, reasons
    elif flags >= 3:
        return "ARCHIVE", flags, reasons
    else:
        return "KEEP", flags, reasons
```

---

## Workflow Integration

### Before Generating PRs

1. **Run triage scan** on all repos
2. **Score retirement flags** for each
3. **Generate REPO_TRIAGE.md** with recommendations
4. **Get Jeremy's approval** on deletions/archives
5. **Focus PR generation** on Keep repos only

**Credits saved:** 150-250 credits by not modernizing doomed repos

### During PR Generation

Include retirement assessment:
```markdown
## Repository Evaluation

### Retirement Flags: 1/10
- [x] Untouched in >2 years
- [ ] All other flags: false

**Recommendation:** Keep & Modernize
**Justification:** Stable utility, still useful, just hasn't needed updates
```

---

## Key Principles

1. **Default to Keep** - Only archive/delete with confidence
2. **Document Decisions** - Future you will thank present you
3. **Extract Value First** - Pull out data/learnings before deletion
4. **Be Honest** - Some repos don't deserve to live
5. **Trust the Flags** - The scoring works, follow it

**Remember:** A well-maintained 40-repo ecosystem beats a cluttered 60-repo ecosystem every time.

---

## Related Documents

- **AUDIT_CHECKLIST.md** - Full repo audit protocol
- **AUDIT_PROTOCOL.yaml** - Machine-readable version
- **COMPREHENSIVE_PR_TEMPLATE.md** - PR template with retirement assessment

---

**Last Updated:** 2025-11-14
**Maintained by:** Jeremy Bradford + Betty
