# BETTY PROTOCOL: UNIVERSAL REPO AUDIT CHECKLIST

**Version:** 1.0 (Draft 0 - Brainstorm Edition)
**Created:** 2025-11-14
**Status:** Comprehensive brainstorm - to be refined
**Purpose:** Universal protocol for repo health, compliance, and standardization assessment

---

## Overview

This checklist provides a comprehensive framework for auditing repositories across Jeremy's ecosystem. It spans critical requirements through optional enhancements, covering structure, documentation, ecosystem integration, and retirement criteria.

**Use this checklist to:**
- Assess repo health before modernization
- Identify candidates for archival or deletion
- Ensure Betty Protocol compliance
- Guide PR generation priorities
- Maintain ecosystem standards

---

# 🟥 1. CRITICAL (Hard Requirements)

**If these are missing, repo may need deletion or major overhaul.**

## 1.1 Repository Must Have a Clear Identity

- [ ] README.md exists
- [ ] README.md clearly states **what the repo is for**
- [ ] README.md has a **short elevator pitch**
- [ ] README.md includes a **Quick Start** section
- [ ] README.md includes **how to run the project**
- [ ] README.md includes **status: (active / stale / archived)**
- [ ] Repo has an obvious **entry point** (main script, service, page, etc.)

## 1.2 No Sensitive Data / Credential Leaks

- [ ] No API keys, tokens, passwords, cookies, DB credentials
- [ ] No service account JSON
- [ ] No hardcoded secrets in code
- [ ] No sensitive logs
- [ ] No raw outputs containing PII
- [ ] `.gitignore` blocks `.env`, `node_modules`, `data`, etc.
- [ ] Project does NOT contain `.librarian_card` or other auto-generated metadata

## 1.3 Directory Structure Must Exist

- [ ] `00_admin/` — receipts, snapshots, planning notes
- [ ] `10_docs/` — user-facing docs
- [ ] `20_receipts/` — operational logs, provenance, run receipts
- [ ] `40_src/` — actual code
- [ ] `run/` or `scripts/` — helper scripts
- [ ] No loose files in root unless intentionally placed

## 1.4 Workflows Must Run

- [ ] Project builds without errors
- [ ] Tests (if any) run cleanly
- [ ] Scripts referenced in README actually exist
- [ ] Commands in README actually work
- [ ] Repo passes lint (or intentionally ignores lint)

## 1.5 Version Control Health

- [ ] No giant files (>10MB) committed
- [ ] Git history sane (no 200k-line accidental dumps)
- [ ] Project doesn't depend on uncommitted local files
- [ ] No duplicate dirs (e.g., `src/src/`, `scripts-old/`, `backup2/`)

---

# 🟧 2. HIGH PRIORITY (Ecosystem Integration + Standardization)

**Required for Betty Protocol compliance and ecosystem coherence.**

## 2.1 Betty Protocol Documents

Each repo should have:

- [ ] WHY_I_CARE.md
- [ ] ROADMAP.md
- [ ] RELATIONS.yaml
- [ ] rules_now.md
- [ ] CLAUDE.md (AI instructions)
- [ ] ONBOARDING.md (or exists in 10_docs/)
- [ ] HEALTH.yaml (if repo exposes or consumes services)

## 2.2 Metadata Block (YAML Frontmatter in README)

**NEW - High-value structured metadata**

At the top of README.md:

```yaml
---
project_id: "C###" or "P###"
project_name: "[descriptive name]"
status: "active|maintenance|archived|experimental"
primary_language: "python|javascript|typescript|shell"
classification: "core|personal|work"
maintainer: "jeremy"
last_review: "YYYY-MM-DD"
depends_on: ["C003_sadb_canonical", "other_projects"]
integrates_with: ["systems", "it", "connects", "to"]
---
```

## 2.3 Standard Git Hygiene

- [ ] `.gitignore` matches Betty baseline
- [ ] `.editorconfig` exists
- [ ] `.pre-commit-config.yaml` exists
- [ ] Pre-commit hooks block:
  - large files
  - new top-level directories
  - committing data
  - committing auto-generated artifacts

## 2.4 Service or Script Validation

**For services:**
- [ ] SERVICE.yaml exists
- [ ] Ports documented
- [ ] Health endpoints defined
- [ ] Start/stop commands documented

**For scripts:**
- [ ] Scripts have executable permissions
- [ ] Follow naming convention: `verb_noun.sh`
- [ ] Documented in README and/or Quick Commands

## 2.5 Reproducibility

- [ ] `requirements.txt` pinned (Python)
- [ ] `package-lock.json` committed (Node)
- [ ] Docker images specify explicit tags (no `:latest`)
- [ ] Scripts use relative paths, not absolute

---

# 🟩 3. MEDIUM PRIORITY (Quality-of-Life + Developer Experience)

**Recommended for completeness and usability.**

## 3.1 Documentation Completeness

- [ ] Quick Commands table in README
- [ ] Screenshots, diagrams, or examples exist
- [ ] Status badges (optional but nice)
- [ ] CHANGELOG.md exists (required for C-series)
- [ ] DEPENDENCIES.md exists if repo is complex
- [ ] RELATED_PROJECTS.md exists for ecosystem clarity

## 3.2 Data Handling

**PROMOTED FROM MEDIUM TO HIGH PRIORITY - Critical for SADB ecosystem**

- [ ] Repo clearly states where data is stored
- [ ] Data paths use `$SADB_DATA_DIR`
- [ ] Backup and restore documented
- [ ] `.env.example` exists (when needed)

## 3.3 Stability & Runtime

- [ ] Logging behavior consistent
- [ ] Repo has a DEBUG mode or config mode
- [ ] Config files use YAML not ad hoc text
- [ ] Repo avoids magical hidden directories

## 3.4 AI-Explainability

**For repos intended to be used by Claude/Betty/agents:**

- [ ] Clear high-level architecture
- [ ] Guidance on "safe mutations" AI can perform
- [ ] Clear boundaries for what AI must not modify
- [ ] Example workflows for agents

---

# 🟦 4. NEW IDEAS (Optional but Awesome, High Leverage)

**Aspirational - implement when beneficial.**

## 4.1 Migration Breadcrumbs

**If a repo was renamed or moved:**

- [ ] `.FORMERLY` file exists
- [ ] Symlink or pointer documented
- [ ] MIGRATIONS.md updated
- [ ] Old IDs mapped to new ones

## 4.2 Ecosystem Awareness

**Repo should explicitly declare:**

- [ ] Who uses it (downstream)
- [ ] What it consumes (upstream)
- [ ] What it generates (artifacts / data)
- [ ] What breaks if repo disappears
- [ ] How it fits into the larger system

## 4.3 DevOps Integration

- [ ] GitHub Actions exist OR intentionally skipped
- [ ] `health-check` workflow (for core repos)
- [ ] Nightly scans supported
- [ ] `.librarian_card` auto-generated (ignored in git)

## 4.4 Optional Enhancements

- [ ] Mermaid architecture diagrams
- [ ] Makefile with common tasks
- [ ] Auto-generated docs script
- [ ] Jupyter notebooks removed or moved to `/notebooks/`
- [ ] CPU/GPU capabilities documented (for ML repos)

---

# 🟪 5. SPECIAL CASES (Apply Selectively)

**Category-specific requirements.**

## 5.1 Services

- [ ] SERVICE.yaml
- [ ] Health endpoint reachable
- [ ] Logs stored outside repo (`$SADB_DATA_DIR/services/...`)
- [ ] Crash recovery documented
- [ ] Monitoring targets defined in HEALTH.yaml

## 5.2 Data Pipelines

- [ ] Determinism guaranteed
- [ ] Receipt files required
- [ ] Schema validation required
- [ ] Stage-by-stage outputs recorded
- [ ] No transient data stored in repo

## 5.3 Memory Projects

- [ ] Rotation logic documented
- [ ] Archive strategy documented
- [ ] Limits and thresholds defined
- [ ] Context and session guidelines clear

## 5.4 Templates Repos (e.g., Mirrorlab)

- [ ] **NO DATA**
- [ ] Only templates + metadata
- [ ] Versioned templates
- [ ] Example filled templates
- [ ] `.gitignore` aggressively blocks everything except templates

---

# 🟫 6. CANDIDATE FOR RETIREMENT / DELETION FLAGS

**These signals indicate repo should be archived or deleted.**

**Retirement Flags:**

- [ ] Repo duplicates another repo's functionality
- [ ] Repo is empty or "just a folder"
- [ ] Repo contains only 1 script and no README
- [ ] Repo depends on deprecated code
- [ ] Repo hasn't been touched in > 2 years
- [ ] You cannot remember what this repo does
- [ ] Repo exists only to store data (should go to `$SADB_DATA_DIR`)
- [ ] Repo builds on old workflows from before the modern ecosystem
- [ ] Repo cannot pass modernization within 1–2 hours of work
- [ ] Repo used for "experiment sessions" that are now fully replaced

## Retirement Decision Matrix

**Flag Count → Action:**
- **0-2 flags:** ✅ Keep & Modernize
- **3-4 flags:** 🗄️ Archive (move to 90_archive/ or separate archive repo)
- **5+ flags:** 🗑️ Delete (completely remove)

**If evaluating between Keep vs Archive:**
- Does it provide unique functionality? → Keep
- Does it integrate with active projects? → Keep
- Is it referenced in RELATIONS.yaml by active projects? → Keep
- Otherwise → Archive

---

# 🟨 7. AUTOMATION TARGETS (For Cloud Code and Mission Control)

**Future automation capabilities.**

## 7.1 Structural Auto-fixes

- [ ] Ensure `.gitignore` matches baseline
- [ ] Create missing directories (`00_admin`, `10_docs`, etc.)
- [ ] Generate `CLAUDE.md` from template
- [ ] Generate `Makefile` if test suite detected
- [ ] Create project metadata block

## 7.2 Validation

- [ ] Check README completeness
- [ ] Validate `HEALTH.yaml` syntax
- [ ] Validate `RELATIONS.yaml` structure
- [ ] Validate dependencies match manifests
- [ ] Check for data leaks
- [ ] Scan repo size for anomalies

## 7.3 Metrics

- [ ] Time since last commit
- [ ] Number of undocumented folders
- [ ] Number of files >10MB
- [ ] Missing Betty Protocol files
- [ ] Missing metadata
- [ ] Missing ROADMAP.md milestones
- [ ] Missing integration points

---

# 🟦 8. CLOUD CODE INTEGRATION

**Future automation format.**

When checklist stabilizes, Cloud Code will run:

```bash
cloud_code analyze-repo --checklist BETTY_PROTOCOL_V1.yaml
```

**YAML will include:**
- Required files
- Required structure
- Required metadata
- Required integration docs
- Allowed/forbidden directories
- Required service definitions
- Required secrets posture
- Required metadata and project ID
- Retirement heuristics
- Auto-fix suggestions

See `AUDIT_PROTOCOL.yaml` for machine-readable version.

---

## Usage Guidelines

### For Manual Audits

1. Open repo in question
2. Go through Section 1 (Critical) - must pass all
3. Evaluate Section 6 (Retirement Flags) - count flags
4. If 5+ flags → recommend deletion
5. If 3-4 flags → recommend archival
6. If 0-2 flags → proceed with Sections 2-3
7. Generate PR with compliance checklist included

### For Automated Audits

1. Parse `AUDIT_PROTOCOL.yaml`
2. Score repo against all sections
3. Generate compliance report
4. Recommend: Keep/Archive/Delete
5. If Keep → generate modernization PR
6. If Archive → suggest archival location
7. If Delete → request confirmation

### For PR Generation

Every PR should include:

```markdown
## Repository Evaluation

### Retirement Assessment
**Flag Count:** X/10
**Recommendation:** [Keep & Modernize / Archive / Delete]

### Compliance Score
**Section 1 (Critical):** X/10 ✅
**Section 2 (High Priority):** X/12 ✅
**Section 3 (Medium Priority):** X/10 ⚠️
```

---

## Revision History

**v1.0 (2025-11-14):**
- Initial comprehensive brainstorm
- 8 sections: Critical → Optional → Retirement → Automation
- Section 3.2 (Data Handling) promoted to High Priority
- Section 2.2 (YAML Frontmatter) added as new requirement
- Retirement decision matrix formalized

**Next Revisions:**
- Gather feedback from actual repo audits
- Refine scoring weights
- Add more examples
- Create decision tree flowcharts
- Expand special case scenarios

---

## Related Documents

- **RETIREMENT_HEURISTICS.md** - Detailed retirement scoring and examples
- **AUDIT_PROTOCOL.yaml** - Machine-readable checklist
- **COMPREHENSIVE_PR_TEMPLATE.md** - PR template using this checklist
- **REPOSITORY_ORGANIZATION.md** - Betty Protocol directory structure
- **WORKSPACE_BETTY_PROTOCOL.md** - General workspace standards

---

**Maintained by:** Jeremy Bradford + Betty (AI co-architect)
**Status:** Living document - evolve as ecosystem grows
**License:** Internal use only
