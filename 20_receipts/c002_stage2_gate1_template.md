# C002 Stage 2 - Gate 1 Inventory Template

**Status:** TEMPLATE (execute when Gate 0 complete)
**Gate:** 1 - Inventory and Dependency Map
**Goal:** Categorize everything. No mystery meat.

---

## Section 1: Top-Level Directory Census

Run from C002_sadb root:
```bash
ls -d */ | sed 's/\/$//' | sort
```

### Directory Classification Table

| Directory | Type | Used by Pipeline? | Destination | Notes |
|-----------|------|-------------------|-------------|-------|
| `00_admin/` | ADMIN | - | KEEP | Already compliant |
| `10_docs/` | DOCS | - | KEEP | Already compliant |
| `20_receipts/` | RECEIPTS | - | KEEP | Already compliant |
| `30_config/` | CONFIG | - | KEEP | Already compliant |
| `40_src/` | CODE | YES | KEEP | Already compliant |
| `50_data/` | DATA | - | KEEP or externalize | Already compliant |
| `70_evidence/` | EVIDENCE | - | KEEP | Already compliant |
| `90_archive/` | ARCHIVE | - | KEEP | Already compliant |
| | | | | |
| `src/` | CODE | ? | `40_src/` | Merge or redirect |
| `scripts/` | CODE/RUN | ? | `00_run/` or `40_src/scripts/` | Split by purpose |
| `tests/` | CODE | ? | `40_src/tests/` or `tests/` exception | Standard pattern |
| `test_data/` | DATA | ? | `70_evidence/test_data/` | Test fixtures |
| `tmp/` | TEMP | NO | DELETE + .gitignore | Should not exist in repo |
| | | | | |
| `2/` | LEGACY | ? | `90_archive/2/` | Needs README |
| `3/` | LEGACY | ? | `90_archive/3/` | Needs README |
| `n8n/` | LEGACY | ? | `90_archive/n8n/` | Workflow exports? |
| `and/` | LEGACY | ? | `90_archive/and/` | Mystery - investigate |
| `Sad/` | LEGACY | ? | `90_archive/Sad/` | Mystery - investigate |
| `Bees/` | LEGACY | ? | `90_archive/Bees/` | Mystery - investigate |
| `reviews/` | LEGACY | ? | `90_archive/reviews/` | Old review data? |
| `sadb_orders_1_2C/` | LEGACY | ? | `90_archive/` | Version snapshot? |

**Classification Key:**
- CODE: Python modules, scripts with logic
- RUN: Entrypoint scripts (executed directly)
- CONFIG: YAML, JSON, env templates
- DATA: SQLite, CSV, NDJSON outputs
- EVIDENCE: Exports, receipts, audit artifacts
- LEGACY: Historical, needs investigation
- TEMP: Should not be in repo

---

## Section 2: Pipeline Call Graph

### Known Pipeline Commands
```bash
make pipeline          # db-init → index → export-twin → stats
python3 40_src/sadb_q.py stats
bash scripts/ingest_chatgpt_downloads.sh
```

### Trace Script Dependencies

Run to find what `make pipeline` actually calls:
```bash
# Show Makefile targets and their commands
grep -E "^[a-z].*:" Makefile | head -20

# Trace Python imports from main modules
grep -rh "^import\|^from" 40_src/ src/ scripts/*.py 2>/dev/null | sort -u | head -50

# Find scripts called by other scripts
grep -rh "bash\|python\|sh " scripts/ Makefile 2>/dev/null | grep -v "^#" | head -30
```

### Pipeline Dependency Table

| Script/Module | Called By | Calls | Status |
|---------------|-----------|-------|--------|
| `make pipeline` | USER | ? | ENTRY |
| `40_src/sadb_q.py` | USER, pipeline | ? | ENTRY |
| `scripts/ingest_*.sh` | USER | ? | ENTRY |
| | | | |
| (fill in from trace) | | | |

---

## Section 3: Hard-Coded Path Audit

### Find Path Literals
```bash
# Absolute paths
grep -rn "/Users/\|/home/\|C:\\\\" --include="*.py" --include="*.sh" --include="*.yaml" . 2>/dev/null | grep -v ".git" | head -50

# Relative paths that assume repo structure
grep -rn "\.\./\|\./" --include="*.py" --include="*.sh" . 2>/dev/null | grep -v ".git" | grep -v "__pycache__" | head -50

# Import paths that will break
grep -rn "from src\.\|import src\." --include="*.py" . 2>/dev/null | head -30
grep -rn "from scripts\.\|import scripts\." --include="*.py" . 2>/dev/null | head -30
```

### Path Breakage Table

| File | Line | Path/Import | Will Break? | Fix Strategy |
|------|------|-------------|-------------|--------------|
| | | | | |
| | | | | |

---

## Section 4: Legacy Directory Investigation

For each legacy dir, answer:
1. What's in it? (file types, count, size)
2. When was it last modified?
3. Is it referenced anywhere in the codebase?
4. What was its original purpose?

### Investigation Commands
```bash
# For each legacy dir:
DIR="2"  # change for each
echo "=== $DIR ==="
ls -la "$DIR" | head -10
find "$DIR" -type f | wc -l
find "$DIR" -type f -name "*.py" | head -5
git log -1 --format="%ci %s" -- "$DIR" 2>/dev/null || echo "No git history"
grep -rn "$DIR" --include="*.py" --include="*.sh" --include="Makefile" . 2>/dev/null | grep -v ".git" | head -5
```

### Legacy Directory Findings

| Directory | Files | Last Modified | Referenced? | Purpose | Decision |
|-----------|-------|---------------|-------------|---------|----------|
| `2/` | ? | ? | ? | ? | ARCHIVE / DELETE |
| `3/` | ? | ? | ? | ? | ARCHIVE / DELETE |
| `n8n/` | ? | ? | ? | ? | ARCHIVE / DELETE |
| `and/` | ? | ? | ? | ? | ARCHIVE / DELETE |
| `Sad/` | ? | ? | ? | ? | ARCHIVE / DELETE |
| `Bees/` | ? | ? | ? | ? | ARCHIVE / DELETE |
| `reviews/` | ? | ? | ? | ? | ARCHIVE / DELETE |
| `sadb_orders_1_2C/` | ? | ? | ? | ? | ARCHIVE / DELETE |

---

## Section 5: Import Graph Snapshot

### Generate Crude Import Map
```bash
# All internal imports
grep -rh "^from \|^import " --include="*.py" . 2>/dev/null | \
  grep -v "^from \." | \
  sort | uniq -c | sort -rn | head -40

# Cross-directory imports (these break on move)
grep -rhn "from src\|from scripts\|from tests" --include="*.py" . 2>/dev/null | \
  grep -v ".git" | head -30
```

### Import Hotspots
| Import Pattern | Count | Files Affected | Risk Level |
|----------------|-------|----------------|------------|
| `from src.X` | ? | ? | HIGH |
| `from scripts.X` | ? | ? | HIGH |
| `import sadb_*` | ? | ? | MEDIUM |
| | | | |

---

## Section 6: Exit Checklist

Before proceeding to Gate 2:

- [ ] Every top-level dir has a row in Section 1 table
- [ ] Every dir has a classification (CODE/DATA/EVIDENCE/ARCHIVE/DELETE)
- [ ] Every dir has a destination bucket assigned
- [ ] Pipeline call graph is documented (Section 2)
- [ ] Hard-coded paths identified (Section 3)
- [ ] Legacy dirs investigated with decisions (Section 4)
- [ ] Import hotspots identified (Section 5)
- [ ] No "?" remaining in tables - all investigated

---

## Execution Notes

When running this inventory:

1. **Run from C002_sadb root:** `cd ~/SyncedProjects/C002_sadb`
2. **Capture raw output:** Pipe commands to files in `70_evidence/stage2/`
3. **Fill tables incrementally:** Don't try to do everything in one pass
4. **Mark unknowns explicitly:** Better to say "unknown - needs Jeremy" than guess
5. **Time-box legacy investigation:** 5 min per legacy dir max. If unclear, → ARCHIVE

---

## Session Attribution
Template created by Claude Code (Opus 4.5) on 2026-01-01
Execute when Gate 0 complete.
