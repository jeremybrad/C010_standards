# C010_standards: How Standards Work

**For Jeremy & Betty — A practical guide to workspace standards governance**

---

## What This Repo Is

C010_standards is the **canonical source of truth** for workspace-wide conventions. It answers three questions:
1. **What rules exist?** (protocols, schemas, taxonomies)
2. **How do we enforce them?** (validators, bootstrap scripts)
3. **How do we adopt new ones?** (the process below)

---

## Where Standards Live

```
C010_standards/
│
├── protocols/                 ← HUMAN-READABLE RULES
│   ├── betty_protocol.md      # Workspace governance (folder structure, receipts)
│   ├── universal_claude_standards.md  # AI agent behavior standards
│   ├── cross_platform_claude_md.md    # Cross-platform CLAUDE.md format
│   ├── META_YAML_SPEC.md      # META.yaml contract specification
│   ├── tier3_documentation_spec.md    # Documentation tier system
│   ├── project_primer_protocol.md     # PROJECT_PRIMER.md generation
│   ├── session_closeout_protocol.md   # Session receipt standards
│   ├── docs_publishing.md     # C019 docs site publishing
│   ├── CANONICAL_STRUCTURE.md # Standard folder structure
│   ├── capsules/              # Capsule artifact specs
│   │   └── capsule_spec_v1.md
│   ├── ops/                   # Operational specs
│   │   └── epoch_as_code_v1.md
│   └── playbooks/             # Compliance playbooks
│       └── COMPLIANCE_PLAYBOOK.md
│
├── schemas/                   ← MACHINE-PARSEABLE SPECS
│   ├── docmeta_v1.2.yaml      # Document metadata schema
│   ├── codemeta_v1.0.yaml     # Code artifact metadata schema
│   ├── capsulemeta_v1.0.yaml  # Capsule artifact schema
│   └── houston_features.schema.json  # Houston agent config schema
│
├── taxonomies/                ← CONTROLLED VOCABULARIES
│   ├── topic_taxonomy.yaml    # Technical topic classifications
│   ├── content_taxonomy.yaml  # Document type classifications
│   └── emotion_taxonomy.yaml  # Emotional context tagging
│
├── validators/                ← ENFORCEMENT TOOLS
│   ├── check_houston_docmeta.py   # DocMeta validation
│   ├── check_houston_features.py  # Houston features validation
│   ├── check_houston_tools.py     # Tool pipeline validation
│   ├── check_houston_models.py    # Model deployment validation
│   ├── check_houston_telemetry.py # Telemetry health validation
│   ├── check_capsulemeta.py       # Capsule metadata validation
│   ├── check_epoch.py             # Epoch-as-Code validation
│   ├── check_windows_filename.py  # Windows filename compatibility
│   ├── check_repo_contract.py     # Repo contract validation
│   ├── check_constitution.py      # Constitution validation
│   ├── common.py              # Shared utilities (safe_print, etc.)
│   └── run_all.py             # Orchestration harness
│
├── scripts/                   ← ROLLOUT AUTOMATION
│   ├── bootstrap_ruff.sh      # Add Ruff linting to all repos
│   ├── bootstrap_testing.sh   # Add test standards to repos
│   ├── bootstrap_claude_crossplatform.sh  # Cross-platform CLAUDE.md
│   └── audit_folder_structure.sh  # Folder structure audit
│
├── policy/                    ← TEMPLATES & CONFIG FILES
│   ├── python/                # pyproject.toml templates
│   ├── templates/             # Reusable snippets
│   └── testing/               # pytest/jest config templates
│
├── docs/standards/            ← TIER 4 PACKAGE DOCUMENTATION
│   ├── ARCHITECTURE.md        # System architecture overview
│   ├── CLI.md                 # CLI and Makefile reference
│   ├── CODE_TOUR.md           # Guided codebase walkthrough
│   ├── OPERATIONS.md          # Operational procedures
│   ├── OVERVIEW.md            # High-level overview
│   ├── QUICKSTART.md          # Getting started guide
│   ├── SCHEMAS.md             # Schema documentation
│   └── SECURITY_AND_PRIVACY.md
│
├── CHANGELOG.md               ← VERSION HISTORY (Tier 1)
├── README.md                  ← REPOSITORY OVERVIEW (Tier 1)
└── META.yaml                  ← PROJECT METADATA (Tier 1)
```

---

## The Canonical List of Standards

### Documentation Tier System

Per `protocols/tier3_documentation_spec.md`, every repo follows this tiered documentation structure:

| Tier | Name | Required Files | Freshness Rule |
|------|------|----------------|----------------|
| **Tier 1** | Critical | `README.md`, `CHANGELOG.md`, `META.yaml` | Must be current |
| **Tier 2** | Extended | `CLAUDE.md`, `glossary.yaml` | Update when behavior changes |
| **Tier 3** | Generated | `PROJECT_PRIMER.md` | Regenerate when HEAD advances |
| **Tier 4** | Package | `docs/**/*.md` | Update when related code changes |

### Governance Standards (Non-Negotiable)
| Standard | Location | Enforced By |
|----------|----------|-------------|
| **Betty Protocol** | `protocols/betty_protocol.md` | Pre-commit hooks, manual review |
| **Folder Structure** | `protocols/CANONICAL_STRUCTURE.md` | `audit_folder_structure.sh` |
| **Naming Convention** | `REPOSITORY_ORGANIZATION.md` | Manual review |
| **Windows Compatibility** | `CLAUDE.md` (filename rules) | `check_windows_filename.py` |

### Documentation Standards
| Standard | Location | Enforced By |
|----------|----------|-------------|
| **CLAUDE.md Format** | `protocols/cross_platform_claude_md.md` | Bootstrap script |
| **META.yaml Contract** | `protocols/META_YAML_SPEC.md` | `check_repo_contract.py` |
| **Tier 3 Docs** | `protocols/tier3_documentation_spec.md` | `bbot render docs.freshness.v1` |
| **Project Primer** | `protocols/project_primer_protocol.md` | `check_epoch.py` |
| **Session Closeout** | `protocols/session_closeout_protocol.md` | Manual review |

### Metadata Schemas
| Standard | Location | Enforced By |
|----------|----------|-------------|
| **DocMeta v1.2** | `schemas/docmeta_v1.2.yaml` | `check_houston_docmeta.py` |
| **CodeMeta v1.0** | `schemas/codemeta_v1.0.yaml` | Manual review |
| **CapsuleMeta v1.0** | `schemas/capsulemeta_v1.0.yaml` | `check_capsulemeta.py` |
| **Houston Features** | `schemas/houston_features.schema.json` | `check_houston_features.py` |

### Operational Standards
| Standard | Location | Enforced By |
|----------|----------|-------------|
| **Epoch-as-Code** | `protocols/ops/epoch_as_code_v1.md` | `check_epoch.py` |
| **Capsule Artifacts** | `protocols/capsules/capsule_spec_v1.md` | `check_capsulemeta.py` |
| **Docs Publishing** | `protocols/docs_publishing.md` | C019 regeneration |

### Code Style
| Standard | Location | Enforced By |
|----------|----------|-------------|
| **Python (Ruff)** | `policy/python/pyproject.ruff.template.toml` | `bootstrap_ruff.sh` |
| **Testing (pytest)** | `policy/testing/pytest.ini` | `bootstrap_testing.sh` |

---

## Process for Adding a New Standard

### Step 1: Define the Standard
Create or update the appropriate file:

| Standard Type | Where to Put It |
|--------------|-----------------|
| Governance rule | `protocols/<name>.md` |
| Metadata schema | `schemas/<name>_v<version>.yaml` |
| Controlled vocabulary | `taxonomies/<name>.yaml` |
| Code style config | `policy/<language>/<filename>` |

**Example for folder structure:**
```markdown
# In protocols/folder_structure_standard.md

## Canon (per repo)
Allowed top level: 00_admin, 10_docs, 20_receipts, 30_config, 40_src, 70_evidence, 90_archive
...
```

### Step 2: Document the Change
Update `CHANGELOG.md` (in repo root) with:
```markdown
## YYYY-MM-DD
- **New Standard**: [Name] - [Brief description]
- Location: `protocols/<file>.md`
- Enforcement: [how it will be enforced]
```

### Step 3: Create a Bootstrap Script (Optional but Recommended)
If the standard needs to be applied to existing repos, create `scripts/bootstrap_<name>.sh`:

```bash
#!/usr/bin/env bash
set -euo pipefail
ROOT="${1:-$HOME/SyncedProjects}"
STAMP=$(date +"%Y%m%d_%H%M%S")

echo ">>> Bootstrapping <standard> under $ROOT"
for repo in "$ROOT"/*/; do
  [ -d "$repo/.git" ] || continue
  cd "$repo"

  # Check if standard is already applied
  if [[ <condition> ]]; then
    echo "  + $(basename "$repo") : applying standard"
    # Apply the standard here

    # Create receipt
    mkdir -p 00_admin/RECEIPTS
    echo "<Standard> applied $STAMP" > "00_admin/RECEIPTS/<name>_${STAMP}.txt"
  else
    echo "  - $(basename "$repo") : already compliant"
  fi
done
echo ">>> Done."
```

### Step 4: Create a Validator (Optional but Recommended)
For machine-checkable standards, add `validators/check_<name>.py`:

```python
#!/usr/bin/env python3
"""Validator for <standard name>."""
import sys
from pathlib import Path

def validate(path: Path, verbose: bool = False) -> list[str]:
    errors = []
    # Validation logic here
    return errors

def cli(argv: list[str] | None = None) -> int:
    # Parse args, run validation, return 0 or 1
    ...

if __name__ == "__main__":
    sys.exit(cli())
```

Register it in `validators/__init__.py`:
```python
AVAILABLE_VALIDATORS = {
    "houston_docmeta": "check_houston_docmeta",
    "<your_name>": "check_<your_name>",  # Add this line
}
```

### Step 5: Rollout
```bash
# Dry run first
bash scripts/bootstrap_<name>.sh --dry-run

# Apply to all repos
bash scripts/bootstrap_<name>.sh

# Verify
python validators/run_all.py --targets <your_name>
```

---

## Adding a New Folder Structure Standard

Since you mentioned a folder structure standard specifically, here's the exact process:

### 1. Update the Protocol
Edit `protocols/betty_protocol.md`, specifically the **Canon (per repo)** section:

```markdown
## Canon (per repo)
- Allowed top level: 00_admin, 10_docs, 20_receipts, 30_config, 40_src, 50_data, 70_evidence, 90_archive
- **NEW**: 50_data is now allowed (symlink to $SADB_DATA_DIR)
```

### 2. Create an Audit Script
Create `scripts/audit_folder_structure.sh`:

```bash
#!/usr/bin/env bash
# Audits repos for folder structure compliance
set -euo pipefail
ROOT="${1:-$HOME/SyncedProjects}"

ALLOWED="00_admin|10_docs|20_receipts|30_config|40_src|50_data|70_evidence|90_archive"

echo ">>> Auditing folder structure under $ROOT"
for repo in "$ROOT"/*/; do
  [ -d "$repo/.git" ] || continue
  name=$(basename "$repo")

  # Find non-compliant top-level directories
  violations=$(find "$repo" -maxdepth 1 -type d -name '[0-9]*' | \
    grep -vE "($ALLOWED)" | \
    sed "s|$repo||" || true)

  if [[ -n "$violations" ]]; then
    echo "  ✗ $name : non-compliant directories:"
    echo "$violations" | sed 's/^/      /'
  else
    echo "  ✓ $name : compliant"
  fi
done
```

### 3. Create a Pre-commit Hook (Optional)
Add to `policy/git-hooks/pre-commit`:

```bash
# Block new top-level numbered directories outside allowed list
ALLOWED="00_admin|10_docs|20_receipts|30_config|40_src|50_data|70_evidence|90_archive"
new_dirs=$(git diff --cached --name-only --diff-filter=A | grep -E '^[0-9]{2}_' | cut -d'/' -f1 | sort -u)
for dir in $new_dirs; do
  if ! echo "$dir" | grep -qE "^($ALLOWED)$"; then
    echo "ERROR: $dir is not an allowed top-level directory"
    echo "Allowed: $ALLOWED"
    exit 1
  fi
done
```

---

## How to Confirm Standards Are In Place

### Quick Check: Single Repo
```bash
cd ~/SyncedProjects/P###_projectname

# Check documentation freshness (recommended)
bbot render docs.freshness.v1

# Check folder structure manually
ls -d */ | grep -E '^[0-9]{2}_'

# Check for required Tier 1 files
ls README.md CHANGELOG.md META.yaml 2>/dev/null || echo "Missing Tier 1 files"

# Check for Tier 2 files (optional but recommended)
ls CLAUDE.md glossary.yaml 2>/dev/null || echo "No Tier 2 files"
```

### Workspace-Wide Audit
```bash
# Run all validators
python validators/run_all.py

# Run specific validator
python validators/check_houston_docmeta.py path/to/doc.yaml

# Audit folder structure
bash scripts/audit_folder_structure.sh

# Check Windows filename compatibility
python validators/check_windows_filename.py --recursive ~/SyncedProjects

# Validate epoch sync (strict mode)
python validators/check_epoch.py --strict --require
```

### Documentation Freshness Audit
```bash
# Check any repo's documentation health
cd ~/SyncedProjects/C010_standards
bbot render docs.freshness.v1

# The report shows:
# - Tier 1-4 document freshness
# - Repo Change Ledger (receipts vs docs)
# - Conditional Doc Modules (API/CLI/Schema/Ops)
# - Epoch-as-Code sync status
# - C019 Publishing Sync status
```

### CI/CD Integration
C010_standards is a submodule in C001_mission-control. The CI workflow runs:
```yaml
# .github/workflows/standards.yml
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          submodules: true
      - run: python external/standards/validators/run_all.py
```

---

## Summary: The Standards Lifecycle

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   DEFINE    │───▶│  DOCUMENT   │───▶│  BOOTSTRAP  │───▶│  VALIDATE   │
│             │    │             │    │             │    │             │
│ protocols/  │    │ CHANGELOG   │    │ scripts/    │    │ validators/ │
│ schemas/    │    │ README      │    │ bootstrap_  │    │ run_all.py  │
│ taxonomies/ │    │             │    │ <name>.sh   │    │             │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
```

**Key insight**: Standards only work if they're both documented AND enforced. The bootstrap script applies them; the validator confirms they stay applied.

### Documentation Freshness Workflow

The `docs-checker` skill (via `bbot render docs.freshness.v1`) provides a comprehensive audit:

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   TIER 1    │───▶│   TIER 2    │───▶│   TIER 3    │───▶│   TIER 4    │
│             │    │             │    │             │    │             │
│ README      │    │ CLAUDE.md   │    │ PROJECT_    │    │ docs/**     │
│ CHANGELOG   │    │ glossary    │    │ PRIMER      │    │             │
│ META.yaml   │    │             │    │             │    │             │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
        │                 │                 │                 │
        ▼                 ▼                 ▼                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│ CHANGE LEDGER: receipts + changelog vs doc dates                    │
│ CONDITIONAL MODULES: API/CLI/Schema/Ops detection                   │
│ EPOCH SYNC: EPOCH.yaml vs git HEAD                                  │
│ PUBLISHING SYNC: C019 docs site regeneration status                 │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Quick Reference: Common Tasks

| Task | Command |
|------|---------|
| **Documentation Freshness** | |
| Check docs freshness | `bbot render docs.freshness.v1` |
| Regenerate PROJECT_PRIMER | `generate-project-primer <repo_id>` |
| | |
| **Validation** | |
| Run all validators | `python validators/run_all.py` |
| Validate epoch sync | `python validators/check_epoch.py --strict` |
| Check Windows filenames | `python validators/check_windows_filename.py --recursive .` |
| Validate capsule metadata | `python validators/check_capsulemeta.py path/to/capsule.yaml` |
| | |
| **Bootstrap** | |
| Add Ruff to all repos | `bash scripts/bootstrap_ruff.sh` |
| Add cross-platform CLAUDE.md | `bash scripts/bootstrap_claude_crossplatform.sh` |
| Audit folder structure | `bash scripts/audit_folder_structure.sh` |
| | |
| **Reference** | |
| View changelog | `cat CHANGELOG.md` |
| List all standards | `ls protocols/ schemas/ taxonomies/` |
| View available validators | `ls validators/check_*.py` |

---

## Available Validators

| Validator | Purpose | Key Flags |
|-----------|---------|-----------|
| `check_houston_docmeta` | Routing tags, taxonomy alignment | `--verbose`, `--json-output` |
| `check_houston_features` | Feature config, trust phases | `--schema` |
| `check_houston_tools` | Tool pipeline, phase gating | `--verbose` |
| `check_houston_models` | Deployment permissions | `--verbose` |
| `check_houston_telemetry` | Freshness, latency thresholds | `--max-age` |
| `check_capsulemeta` | Capsule artifact validation | `--strict` |
| `check_epoch` | Epoch-as-Code sync | `--strict`, `--require` |
| `check_windows_filename` | Windows filename compatibility | `--recursive` |
| `check_repo_contract` | Repo metadata contract | `--verbose` |
| `check_constitution` | Constitution validation | `--verbose` |

All validators follow the same contract:
- Exit 0 = pass
- Exit 1 = validation failure
- Exit 2 = config/parse error

---

*Last Updated: 2026-01-24*
*Maintained by: Jeremy Bradford & Betty*
