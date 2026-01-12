#!/usr/bin/env bash
# bootstrap_ruff.sh - Add Ruff configuration to repos missing it
#
# Usage:
#   bash scripts/bootstrap_ruff.sh [workspace_path] [--dry-run]
#   Default workspace: ~/SyncedProjects
#
# Options:
#   --dry-run   Show what would change without writing files
#
# Outputs (when not --dry-run):
#   - Appends/creates pyproject.toml with Ruff config
#   - Creates receipt in 00_admin/RECEIPTS/ruff_<STAMP>.txt
#
set -euo pipefail

# Parse arguments
DRY_RUN=false
ROOT=""
for arg in "$@"; do
  case "$arg" in
    --dry-run)
      DRY_RUN=true
      ;;
    *)
      if [[ -z "$ROOT" ]]; then
        ROOT="$arg"
      fi
      ;;
  esac
done
ROOT="${ROOT:-$HOME/SyncedProjects}"

STAMP=$(date +"%Y%m%d_%H%M%S")
TEMPLATE="$ROOT/C010_standards/10_docs/policy/python/pyproject.ruff.template.toml"

# Verify template exists
if [[ ! -f "$TEMPLATE" ]]; then
  echo "ERROR: Ruff template not found: $TEMPLATE" >&2
  exit 1
fi

if [[ "$DRY_RUN" == "true" ]]; then
  echo ">>> DRY RUN: Showing what would change under $ROOT"
  echo ">>> Template: $TEMPLATE"
  echo ""
else
  echo ">>> Bootstrapping Ruff under $ROOT"
fi

would_add=0
already_present=0

for repo in "$ROOT"/*/; do
  [ -d "$repo/.git" ] || continue
  name=$(basename "$repo")
  pyproject="$repo/pyproject.toml"

  if ! grep -q "^\[tool\.ruff\]" "$pyproject" 2>/dev/null; then
    would_add=$((would_add + 1))

    if [[ "$DRY_RUN" == "true" ]]; then
      # Dry-run: show patch summary
      if [[ -f "$pyproject" ]]; then
        echo "  [WOULD APPEND] $name/pyproject.toml"
        echo "    + [tool.ruff] section from template"
      else
        echo "  [WOULD CREATE] $name/pyproject.toml"
        echo "    + Full Ruff template (new file)"
      fi
      echo "  [WOULD CREATE] $name/00_admin/RECEIPTS/ruff_${STAMP}.txt"
      echo ""
    else
      # Real execution
      echo "  + $name : adding Ruff"
      cd "$repo"
      if [[ -f "pyproject.toml" ]]; then
        echo >> pyproject.toml
        cat "$TEMPLATE" >> pyproject.toml
      else
        cp "$TEMPLATE" pyproject.toml
      fi
      mkdir -p 00_admin/RECEIPTS
      echo "Ruff baseline added $STAMP" > "00_admin/RECEIPTS/ruff_${STAMP}.txt"
    fi
  else
    already_present=$((already_present + 1))
    if [[ "$DRY_RUN" == "true" ]]; then
      echo "  [SKIP] $name : Ruff already present"
    else
      echo "  - $name : Ruff already present"
    fi
  fi
done

echo ""
echo "----------------------------------------------"
if [[ "$DRY_RUN" == "true" ]]; then
  echo "DRY RUN SUMMARY:"
  echo "  Would modify: $would_add repos"
  echo "  Already present: $already_present repos"
  echo ""
  echo "Run without --dry-run to apply changes."
else
  echo "SUMMARY:"
  echo "  Modified: $would_add repos"
  echo "  Already present: $already_present repos"
fi
echo ">>> Done."
