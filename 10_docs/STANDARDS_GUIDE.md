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
│   └── META_YAML_SPEC.md      # META.yaml contract specification
│
├── schemas/                   ← MACHINE-PARSEABLE SPECS
│   ├── docmeta_v1.2.yaml      # Document metadata schema
│   ├── codemeta_v1.0.yaml     # Code artifact metadata schema
│   └── houston_features.schema.json  # Houston agent config schema
│
├── taxonomies/                ← CONTROLLED VOCABULARIES
│   ├── topic_taxonomy.yaml    # Technical topic classifications
│   ├── content_taxonomy.yaml  # Document type classifications
│   └── emotion_taxonomy.yaml  # Emotional context tagging
│
├── validators/                ← ENFORCEMENT TOOLS
│   ├── check_houston_docmeta.py
│   ├── check_houston_features.py
│   └── run_all.py             # Orchestration harness
│
├── scripts/                   ← ROLLOUT AUTOMATION
│   ├── bootstrap_ruff.sh      # Add Ruff linting to all repos
│   ├── bootstrap_testing.sh   # Add test standards to repos
│   └── bootstrap_claude_crossplatform.sh  # Cross-platform CLAUDE.md
│
├── policy/                    ← TEMPLATES & CONFIG FILES
│   ├── python/                # pyproject.toml templates
│   ├── templates/             # Reusable snippets
│   └── testing/               # pytest/jest config templates
│
└── notes/CHANGELOG.md         ← VERSION HISTORY
```

---

## The Canonical List of Standards

### Tier 1: Governance (Non-Negotiable)
| Standard | Location | Enforced By |
|----------|----------|-------------|
| **Betty Protocol** | `protocols/betty_protocol.md` | Pre-commit hooks, manual review |
| **Folder Structure** | `protocols/betty_protocol.md` (Canon section) | Pre-commit hooks |
| **Naming Convention** | `REPOSITORY_ORGANIZATION.md` | Manual review |

### Tier 2: Documentation Standards
| Standard | Location | Enforced By |
|----------|----------|-------------|
| **CLAUDE.md Format** | `protocols/cross_platform_claude_md.md` | Bootstrap script |
| **META.yaml Contract** | `protocols/META_YAML_SPEC.md` | Validator (planned) |

### Tier 3: Metadata Schemas
| Standard | Location | Enforced By |
|----------|----------|-------------|
| **DocMeta v1.2** | `schemas/docmeta_v1.2.yaml` | `check_houston_docmeta.py` |
| **CodeMeta v1.0** | `schemas/codemeta_v1.0.yaml` | Manual review |
| **Houston Features** | `schemas/houston_features.schema.json` | `check_houston_features.py` |

### Tier 4: Code Style
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
Update `notes/CHANGELOG.md` with:
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

# Check folder structure manually
ls -d */ | grep -E '^[0-9]{2}_'

# Check for required files
ls README.md META.yaml CLAUDE.md 2>/dev/null || echo "Missing required files"
```

### Workspace-Wide Audit
```bash
# Run all validators
python validators/run_all.py

# Run specific validator
python validators/check_houston_docmeta.py path/to/doc.yaml

# Audit folder structure (if you create the script)
bash scripts/audit_folder_structure.sh
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

---

## Quick Reference: Common Tasks

| Task | Command |
|------|---------|
| Add Ruff to all repos | `bash scripts/bootstrap_ruff.sh` |
| Add cross-platform CLAUDE.md | `bash scripts/bootstrap_claude_crossplatform.sh` |
| Run all validators | `python validators/run_all.py` |
| Run specific validator | `python validators/check_houston_features.py` |
| View changelog | `cat notes/CHANGELOG.md` |
| List all standards | `ls protocols/ schemas/ taxonomies/` |

---

*Last Updated: 2025-12-26*
*Maintained by: Jeremy Bradford & Betty*
