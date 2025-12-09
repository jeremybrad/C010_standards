#!/usr/bin/env bash
set -euo pipefail
ROOT="${1:-$HOME/SyncedProjects}"
STAMP=$(date +"%Y%m%d_%H%M%S")
echo ">>> Bootstrapping Ruff under $ROOT"
for repo in "$ROOT"/*/; do
  [ -d "$repo/.git" ] || continue
  cd "$repo"
  if ! grep -q "^\[tool\.ruff\]" pyproject.toml 2>/dev/null; then
    echo "  + $(basename "$repo") : adding Ruff"
    if [ -f "pyproject.toml" ]; then
      echo >> pyproject.toml
      cat "$ROOT/C010_standards/policy/python/pyproject.ruff.template.toml" >> pyproject.toml
    else
      cp "$ROOT/C010_standards/policy/python/pyproject.ruff.template.toml" pyproject.toml
    fi
    mkdir -p 00_admin/RECEIPTS
    echo "Ruff baseline added $STAMP" > "00_admin/RECEIPTS/ruff_${STAMP}.txt"
  else
    echo "  - $(basename "$repo") : Ruff already present"
  fi
  # Note: Ruff installation skipped (assume already installed via brew/pipx)
  # To install: brew install ruff OR pipx install ruff
done
echo ">>> Done."
