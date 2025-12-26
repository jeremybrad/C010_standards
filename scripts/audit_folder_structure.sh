#!/usr/bin/env bash
# audit_folder_structure.sh - Audits repos for Betty Protocol folder structure compliance
#
# Usage: bash scripts/audit_folder_structure.sh [workspace_path]
# Default: ~/SyncedProjects
#
# Exit codes:
#   0 - All repos compliant
#   1 - One or more repos have violations
#
set -euo pipefail

ROOT="${1:-$HOME/SyncedProjects}"
STAMP=$(date +"%Y%m%d_%H%M%S")

# Betty Protocol Canon - allowed top-level numbered directories
# Source: protocols/betty_protocol.md
ALLOWED_DIRS="00_admin|00_run|10_docs|20_receipts|30_config|40_src|50_data|70_evidence|90_archive"

# Required files per Betty Protocol (default)
# Can be overridden per-repo via 00_admin/audit_exceptions.yaml
DEFAULT_REQUIRED_FILES="README.md rules_now.md RELATIONS.yaml"

# Load per-repo exceptions if present
# Format: required_files: [README.md] (YAML list of required files)
load_repo_exceptions() {
  local repo="$1"
  local exceptions_file="$repo/00_admin/audit_exceptions.yaml"

  if [[ -f "$exceptions_file" ]]; then
    # Simple YAML extraction - get required_files list
    local custom_files
    custom_files=$(grep -A 10 "^required_files:" "$exceptions_file" 2>/dev/null | \
                   grep "^  - " | sed 's/^  - //' | tr '\n' ' ')
    if [[ -n "$custom_files" ]]; then
      echo "$custom_files"
      return
    fi
  fi
  echo "$DEFAULT_REQUIRED_FILES"
}

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

violations_found=0
repos_checked=0
compliant_repos=0

echo "=============================================="
echo "Betty Protocol Folder Structure Audit"
echo "=============================================="
echo "Workspace: $ROOT"
echo "Timestamp: $STAMP"
echo "Allowed dirs: ${ALLOWED_DIRS//|/, }"
echo "----------------------------------------------"
echo ""

for repo in "$ROOT"/*/; do
  # Skip non-git directories
  [ -d "$repo/.git" ] || continue

  # Skip meta-folders (underscore prefix)
  basename "$repo" | grep -q "^_" && continue

  name=$(basename "$repo")
  repos_checked=$((repos_checked + 1))
  repo_violations=0

  # Check 1: Find numbered directories that aren't in the allowed list
  non_compliant_dirs=""
  while IFS= read -r dir; do
    [ -z "$dir" ] && continue
    dirname=$(basename "$dir")
    if ! echo "$dirname" | grep -qE "^($ALLOWED_DIRS)$"; then
      non_compliant_dirs="$non_compliant_dirs$dirname "
      repo_violations=$((repo_violations + 1))
    fi
  done < <(find "$repo" -maxdepth 1 -type d -name '[0-9][0-9]_*' 2>/dev/null)

  # Check 2: Required files (with per-repo exceptions)
  REQUIRED_FILES=$(load_repo_exceptions "$repo")
  missing_files=""
  for reqfile in $REQUIRED_FILES; do
    if [[ ! -f "$repo/$reqfile" ]]; then
      missing_files="$missing_files$reqfile "
      repo_violations=$((repo_violations + 1))
    fi
  done

  # Report results for this repo
  if [[ $repo_violations -gt 0 ]]; then
    echo -e "${RED}✗ $name${NC} ($repo_violations issues)"
    if [[ -n "$non_compliant_dirs" ]]; then
      echo "    Non-compliant directories: $non_compliant_dirs"
    fi
    if [[ -n "$missing_files" ]]; then
      echo "    Missing required files: $missing_files"
    fi
    violations_found=$((violations_found + repo_violations))
  else
    echo -e "${GREEN}✓ $name${NC}"
    compliant_repos=$((compliant_repos + 1))
  fi
done

echo ""
echo "----------------------------------------------"
echo "Summary"
echo "----------------------------------------------"
echo "Repos checked: $repos_checked"
echo -e "Compliant: ${GREEN}$compliant_repos${NC}"
echo -e "With violations: ${RED}$((repos_checked - compliant_repos))${NC}"
echo "Total violations: $violations_found"
echo ""

# Write receipt
RECEIPT_DIR="$ROOT/C010_standards/20_receipts"
mkdir -p "$RECEIPT_DIR"
RECEIPT_FILE="$RECEIPT_DIR/folder_audit_${STAMP}.txt"
cat > "$RECEIPT_FILE" << EOF
Folder Structure Audit Receipt
==============================
Timestamp: $STAMP
Workspace: $ROOT
Repos checked: $repos_checked
Compliant: $compliant_repos
Violations: $violations_found
Allowed dirs: ${ALLOWED_DIRS//|/, }
Default required files: $DEFAULT_REQUIRED_FILES
Exceptions: via 00_admin/audit_exceptions.yaml (if present)
EOF
echo "Receipt written: $RECEIPT_FILE"

if [[ $violations_found -gt 0 ]]; then
  echo ""
  echo -e "${YELLOW}Remediation:${NC}"
  echo "1. Move non-compliant directories to allowed locations"
  echo "2. Or update ALLOWED_DIRS in this script if the standard has changed"
  echo "3. Re-run audit to verify compliance"
  exit 1
else
  echo ""
  echo -e "${GREEN}All repos compliant with Betty Protocol folder structure.${NC}"
  exit 0
fi
