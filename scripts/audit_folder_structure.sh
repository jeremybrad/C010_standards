#!/usr/bin/env bash
# audit_folder_structure.sh - Audits repos for Betty Protocol folder structure compliance
#
# Usage: bash scripts/audit_folder_structure.sh [workspace_path] [--autofix-safe] [--dry-run]
# Default: ~/SyncedProjects
#
# Options:
#   --autofix-safe   Create missing required files (stubs only, no renames/deletions)
#   --dry-run        Show what would change without writing files
#
# Series-aware enforcement:
#   - C-series (Core) and W-series (Work): 00_run/ is REQUIRED
#   - P-series (Projects) and U-series (Utility): 00_run/ is OPTIONAL (warn-only)
#
# Outputs:
#   - Console summary (human-readable)
#   - CSV: 70_evidence/exports/folder_structure_audit_<STAMP>.csv
#   - CSV: 70_evidence/exports/folder_structure_audit_latest.csv
#   - CSV: 70_evidence/exports/folder_structure_actions_<STAMP>.csv
#   - CSV: 70_evidence/exports/folder_structure_actions_latest.csv
#   - Receipt: 20_receipts/folder_audit_<STAMP>.md
#
# Exit codes:
#   0 - All repos compliant
#   1 - One or more repos have violations
#
set -euo pipefail

# Parse arguments
AUTOFIX_SAFE=false
DRY_RUN=false
ROOT=""
for arg in "$@"; do
  case "$arg" in
    --autofix-safe)
      AUTOFIX_SAFE=true
      ;;
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
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"

# Output directories
CSV_DIR="$REPO_ROOT/70_evidence/exports"
RECEIPT_DIR="$REPO_ROOT/20_receipts"
if [[ "$DRY_RUN" != "true" ]]; then
  mkdir -p "$CSV_DIR" "$RECEIPT_DIR"
fi

# CSV file paths
CSV_FILE="$CSV_DIR/folder_structure_audit_${STAMP}.csv"
CSV_LATEST="$CSV_DIR/folder_structure_audit_latest.csv"
ACTIONS_FILE="$CSV_DIR/folder_structure_actions_${STAMP}.csv"
ACTIONS_LATEST="$CSV_DIR/folder_structure_actions_latest.csv"

# Betty Protocol Canon - allowed top-level directories
# Source: protocols/betty_protocol.md
# Updated 2025-12-27: Added 20_inbox, 20_approvals, 80_evidence_packages
# Updated 2026-01-16: Added 60_tests
ALLOWED_DIRS="00_admin|00_run|10_docs|20_receipts|20_approvals|20_inbox|30_config|40_src|50_data|60_tests|70_evidence|80_evidence_packages|90_archive"

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

# Check if exceptions file exists
has_exceptions_file() {
  local repo="$1"
  [[ -f "$repo/00_admin/audit_exceptions.yaml" ]] && echo "true" || echo "false"
}

# Load allowed_additional_dirs from exceptions file
# Returns pipe-separated list of additional allowed directories
load_additional_allowed_dirs() {
  local repo="$1"
  local exceptions_file="$repo/00_admin/audit_exceptions.yaml"

  if [[ -f "$exceptions_file" ]]; then
    # Simple YAML extraction - get allowed_additional_dirs list
    local additional_dirs
    additional_dirs=$(grep -A 100 "^allowed_additional_dirs:" "$exceptions_file" 2>/dev/null | \
                      grep "^  - " | sed 's/^  - //' | tr '\n' '|' | sed 's/|$//')
    if [[ -n "$additional_dirs" ]]; then
      echo "$additional_dirs"
      return
    fi
  fi
  echo ""
}

# Extract repo series (C/P/W/U) from name
get_repo_series() {
  local name="$1"
  if [[ "$name" =~ ^C[0-9] ]]; then echo "C"
  elif [[ "$name" =~ ^P[0-9] ]]; then echo "P"
  elif [[ "$name" =~ ^W[0-9] ]]; then echo "W"
  elif [[ "$name" =~ ^U[0-9] ]]; then echo "U"
  else echo "-"
  fi
}

# Determine if 00_run is required based on series
requires_00_run() {
  local series="$1"
  # C-series (Core) and W-series (Work) require 00_run
  # P-series (Projects) and U-series (Utility) do not
  if [[ "$series" == "C" || "$series" == "W" ]]; then
    echo "true"
  else
    echo "false"
  fi
}

# Autofix-safe: create missing stubs
autofix_repo() {
  local repo="$1"
  local name="$2"
  local series="$3"
  local missing_files="$4"
  local req_00_run="$5"
  local has_00_run="$6"

  local fixed=0

  # Create rules_now.md stub if missing
  if [[ "$missing_files" == *"rules_now.md"* ]]; then
    cat > "$repo/rules_now.md" << 'STUB'
# rules_now.md

This file points to the canonical Betty Protocol rules.

**Canonical source:** [C010_standards/protocols/betty_protocol.md](https://github.com/jeremybrad/C010_standards/blob/main/protocols/betty_protocol.md)

## Quick Reference

- Follow Betty Protocol folder structure
- All changes require receipts in `20_receipts/`
- Keep README.md accurate and current
- No data files in git - use `$SADB_DATA_DIR`

---
*This stub was auto-generated. Update with project-specific rules as needed.*
STUB
    echo "    [AUTOFIX] Created rules_now.md" >&2
    fixed=$((fixed + 1))
  fi

  # Create RELATIONS.yaml stub if missing
  if [[ "$missing_files" == *"RELATIONS.yaml"* ]]; then
    cat > "$repo/RELATIONS.yaml" << STUB
# RELATIONS.yaml - Project relationship mapping
# Auto-generated stub - update with actual relationships

project:
  name: "$name"
  series: "$series"

# TODO: Define upstream dependencies
upstream: []

# TODO: Define downstream consumers
downstream: []

# TODO: Define data sources
data_sources: []

# Canonical truth source for personal knowledge
truth_source: C002_sadb
STUB
    echo "    [AUTOFIX] Created RELATIONS.yaml" >&2
    fixed=$((fixed + 1))
  fi

  # Create 00_run/ ONLY if required (C/W series)
  if [[ "$req_00_run" == "true" && "$has_00_run" == "false" ]]; then
    mkdir -p "$repo/00_run"
    cat > "$repo/00_run/README.txt" << 'STUB'
# 00_run - Easy Buttons

This directory contains double-clickable launchers for common operations.

## Conventions
- macOS: .command files (chmod +x, double-click in Finder)
- Windows: .ps1 files (Right-click -> Run with PowerShell)

## TODO
Add launchers for common operations in this repo, such as:
- Running tests
- Building/compiling
- Starting services
- Generating reports

---
This stub was auto-generated. Add launchers as needed.
STUB
    echo "    [AUTOFIX] Created 00_run/ with README.txt" >&2
    fixed=$((fixed + 1))
  fi

  echo "$fixed"
}

# Determine recommended action for a repo
get_recommended_action() {
  local compliant="$1"
  local has_exception="$2"
  local missing_files="$3"
  local invalid_dirs="$4"
  local req_00_run="$5"
  local missing_00_run="$6"

  # Exception declared - skip
  if [[ "$has_exception" == "true" ]]; then
    echo "exception"
    return
  fi

  # Compliant - no action needed
  if [[ "$compliant" == "true" ]]; then
    echo "compliant"
    return
  fi

  # P/U series missing optional 00_run only (no other issues)
  if [[ "$req_00_run" == "false" && "$missing_00_run" == "true" && -z "$missing_files" && -z "$invalid_dirs" ]]; then
    echo "ignore"
    return
  fi

  # Has invalid directories - needs manual migration
  if [[ -n "$invalid_dirs" ]]; then
    echo "migrate"
    return
  fi

  # Missing required files or required 00_run - can autofix
  if [[ -n "$missing_files" ]] || [[ "$req_00_run" == "true" && "$missing_00_run" == "true" ]]; then
    echo "autofix"
    return
  fi

  echo "review"
}

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

violations_found=0
repos_checked=0
compliant_repos=0
autofix_count=0

# Series counters
c_total=0; c_compliant=0
p_total=0; p_compliant=0
w_total=0; w_compliant=0
u_total=0; u_compliant=0
other_total=0; other_compliant=0

# Initialize CSVs with headers (skip in dry-run)
if [[ "$DRY_RUN" != "true" ]]; then
  echo "timestamp,repo_name,repo_series,repo_path,compliant,missing_required_files,invalid_top_level_dirs,has_00_run,requires_00_run,missing_00_run,exceptions_applied" > "$CSV_FILE"
  echo "timestamp,repo_name,repo_series,compliant,recommended_action,missing_required_files,invalid_top_level_dirs,requires_00_run,missing_00_run" > "$ACTIONS_FILE"
fi

echo "=============================================="
echo "Betty Protocol Folder Structure Audit"
echo "=============================================="
if [[ "$DRY_RUN" == "true" ]]; then
  echo ">>> DRY RUN: Showing what would change"
fi
echo "Workspace: $ROOT"
echo "Timestamp: $STAMP"
echo "Autofix-safe: $AUTOFIX_SAFE"
echo "Dry-run: $DRY_RUN"
echo "Allowed dirs: ${ALLOWED_DIRS//|/, }"
echo ""
echo "Series enforcement:"
echo "  C/W series: 00_run REQUIRED"
echo "  P/U series: 00_run OPTIONAL"
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

  # Get repo series
  series=$(get_repo_series "$name")

  # Update series counters
  case "$series" in
    C) c_total=$((c_total + 1)) ;;
    P) p_total=$((p_total + 1)) ;;
    W) w_total=$((w_total + 1)) ;;
    U) u_total=$((u_total + 1)) ;;
    *) other_total=$((other_total + 1)) ;;
  esac

  # Check if 00_run exists
  has_00_run="false"
  [[ -d "$repo/00_run" ]] && has_00_run="true"

  # Check if 00_run is required for this series
  req_00_run=$(requires_00_run "$series")

  # Missing 00_run?
  missing_00_run="false"
  [[ "$has_00_run" == "false" ]] && missing_00_run="true"

  # Check if exceptions file exists/applied
  exceptions_applied=$(has_exceptions_file "$repo")

  # Load additional allowed dirs if exceptions exist
  additional_allowed=$(load_additional_allowed_dirs "$repo")
  if [[ -n "$additional_allowed" ]]; then
    repo_allowed_dirs="$ALLOWED_DIRS|$additional_allowed"
  else
    repo_allowed_dirs="$ALLOWED_DIRS"
  fi

  # Check 1: Find ALL top-level directories that aren't in the allowed list
  # Fixed 2025-12-27: Now checks ALL non-hidden dirs, not just numbered ones
  # This catches violations like bin/, ci/, docs/, --version/, python3/, etc.
  # Updated 2025-12-30: Now honors per-repo allowed_additional_dirs from exceptions
  # Fixed 2026-01-01: Space-safe enumeration using find -print0 + array
  non_compliant_dirs=()
  # Enumerate all non-hidden top-level directories (space-safe)
  while IFS= read -r -d '' d; do
    dirname="$(basename "$d")"
    [[ "$dirname" == .* ]] && continue  # skip hidden dirs
    if ! echo "$dirname" | grep -qE "^($repo_allowed_dirs)$"; then
      non_compliant_dirs+=("$dirname")
      repo_violations=$((repo_violations + 1))
    fi
  done < <(find "$repo" -mindepth 1 -maxdepth 1 -type d -print0 2>/dev/null)

  # Join array into semicolon-separated CSV field (space-safe)
  non_compliant_dirs_csv=""
  non_compliant_dirs_display=""
  if [[ ${#non_compliant_dirs[@]} -gt 0 ]]; then
    for i in "${!non_compliant_dirs[@]}"; do
      [[ $i -gt 0 ]] && non_compliant_dirs_csv+=";"
      non_compliant_dirs_csv+="${non_compliant_dirs[$i]}"
    done
    # Space-separated display version
    non_compliant_dirs_display="${non_compliant_dirs[*]}"
  fi

  # Check 2: Required files (with per-repo exceptions)
  REQUIRED_FILES=$(load_repo_exceptions "$repo")
  missing_files=""
  missing_files_csv=""
  for reqfile in $REQUIRED_FILES; do
    if [[ ! -f "$repo/$reqfile" ]]; then
      missing_files="$missing_files$reqfile "
      [[ -n "$missing_files_csv" ]] && missing_files_csv="$missing_files_csv;"
      missing_files_csv="$missing_files_csv$reqfile"
      repo_violations=$((repo_violations + 1))
    fi
  done

  # Check 3: Missing required 00_run (only counts as violation for C/W)
  if [[ "$req_00_run" == "true" && "$missing_00_run" == "true" ]]; then
    repo_violations=$((repo_violations + 1))
  fi

  # Determine compliance
  compliant="false"
  if [[ $repo_violations -eq 0 ]]; then
    compliant="true"
    compliant_repos=$((compliant_repos + 1))

    # Update series compliant counters
    case "$series" in
      C) c_compliant=$((c_compliant + 1)) ;;
      P) p_compliant=$((p_compliant + 1)) ;;
      W) w_compliant=$((w_compliant + 1)) ;;
      U) u_compliant=$((u_compliant + 1)) ;;
      *) other_compliant=$((other_compliant + 1)) ;;
    esac
  else
    violations_found=$((violations_found + repo_violations))
  fi

  # Get recommended action
  action=$(get_recommended_action "$compliant" "$exceptions_applied" "$missing_files_csv" "$non_compliant_dirs_csv" "$req_00_run" "$missing_00_run")

  # Write CSV rows (skip in dry-run)
  if [[ "$DRY_RUN" != "true" ]]; then
    echo "$STAMP,$name,$series,\"$repo\",$compliant,\"$missing_files_csv\",\"$non_compliant_dirs_csv\",$has_00_run,$req_00_run,$missing_00_run,$exceptions_applied" >> "$CSV_FILE"
    echo "$STAMP,$name,$series,$compliant,$action,\"$missing_files_csv\",\"$non_compliant_dirs_csv\",$req_00_run,$missing_00_run" >> "$ACTIONS_FILE"
  fi

  # Report results for this repo (console)
  if [[ $repo_violations -gt 0 ]]; then
    echo -e "${RED}✗ $name${NC} [$series] ($repo_violations issues) → $action"
    if [[ ${#non_compliant_dirs[@]} -gt 0 ]]; then
      echo "    Non-compliant directories: $non_compliant_dirs_display"
    fi
    if [[ -n "$missing_files" ]]; then
      echo "    Missing required files: $missing_files"
    fi
    if [[ "$req_00_run" == "true" && "$missing_00_run" == "true" ]]; then
      echo "    Missing required 00_run/ (C/W series)"
    fi

    # Autofix if enabled (skip in dry-run)
    if [[ "$AUTOFIX_SAFE" == "true" && "$action" == "autofix" && "$DRY_RUN" != "true" ]]; then
      fixed=$(autofix_repo "$repo" "$name" "$series" "$missing_files" "$req_00_run" "$has_00_run")
      autofix_count=$((autofix_count + fixed))
    elif [[ "$AUTOFIX_SAFE" == "true" && "$action" == "autofix" && "$DRY_RUN" == "true" ]]; then
      echo "    [WOULD AUTOFIX] Would create missing stubs"
    fi
  else
    # Warn about optional 00_run missing
    if [[ "$missing_00_run" == "true" && "$req_00_run" == "false" ]]; then
      echo -e "${GREEN}✓ $name${NC} [$series] ${YELLOW}(00_run optional, not present)${NC}"
    else
      echo -e "${GREEN}✓ $name${NC} [$series]"
    fi
  fi
done

# Copy to latest (skip in dry-run)
if [[ "$DRY_RUN" != "true" ]]; then
  cp "$CSV_FILE" "$CSV_LATEST"
  cp "$ACTIONS_FILE" "$ACTIONS_LATEST"
fi

echo ""
echo "----------------------------------------------"
echo "Summary"
echo "----------------------------------------------"
echo "Repos checked: $repos_checked"
echo -e "Compliant: ${GREEN}$compliant_repos${NC}"
echo -e "With violations: ${RED}$((repos_checked - compliant_repos))${NC}"
echo "Total violations: $violations_found"
if [[ "$AUTOFIX_SAFE" == "true" ]]; then
  echo -e "Files auto-fixed: ${CYAN}$autofix_count${NC}"
fi
echo ""
echo "By Series:"
echo -e "  C-series (Core):     $c_compliant / $c_total compliant"
echo -e "  W-series (Work):     $w_compliant / $w_total compliant"
echo -e "  P-series (Projects): $p_compliant / $p_total compliant"
echo -e "  U-series (Utility):  $u_compliant / $u_total compliant"
[[ $other_total -gt 0 ]] && echo -e "  Other:               $other_compliant / $other_total compliant"
echo ""
if [[ "$DRY_RUN" == "true" ]]; then
  # Dry-run: show what would be written
  echo ""
  echo "[WOULD WRITE] $CSV_FILE"
  echo "[WOULD WRITE] $CSV_LATEST"
  echo "[WOULD WRITE] $ACTIONS_FILE"
  echo "[WOULD WRITE] $ACTIONS_LATEST"
  echo "[WOULD WRITE] $RECEIPT_DIR/folder_audit_${STAMP}.md"
  echo ""
  echo "----------------------------------------------"
  echo "DRY RUN SUMMARY"
  echo "----------------------------------------------"
  echo "Repos scanned: $repos_checked"
  echo "Would report compliant: $compliant_repos"
  echo "Would report violations: $((repos_checked - compliant_repos))"
  echo ""
  echo "Run without --dry-run to write output files."
  exit 0
fi

echo "CSV output: $CSV_FILE"
echo "CSV latest: $CSV_LATEST"
echo "Actions CSV: $ACTIONS_FILE"
echo "Actions latest: $ACTIONS_LATEST"

# Count actions for receipt (use tr to strip newlines)
action_autofix=$(grep -c ",autofix," "$ACTIONS_FILE" 2>/dev/null | tr -d '\n' || printf '0')
action_migrate=$(grep -c ",migrate," "$ACTIONS_FILE" 2>/dev/null | tr -d '\n' || printf '0')
action_exception=$(grep -c ",exception," "$ACTIONS_FILE" 2>/dev/null | tr -d '\n' || printf '0')
action_ignore=$(grep -c ",ignore," "$ACTIONS_FILE" 2>/dev/null | tr -d '\n' || printf '0')
action_compliant=$(grep -c ",compliant," "$ACTIONS_FILE" 2>/dev/null | tr -d '\n' || printf '0')

# Write receipt
RECEIPT_FILE="$RECEIPT_DIR/folder_audit_${STAMP}.md"
cat > "$RECEIPT_FILE" << EOF
# Folder Structure Audit Receipt

**Timestamp:** $STAMP
**Workspace:** $ROOT
**Autofix-safe:** $AUTOFIX_SAFE

## Results Summary

| Metric | Value |
|--------|-------|
| Repos checked | $repos_checked |
| Compliant | $compliant_repos |
| With violations | $((repos_checked - compliant_repos)) |
| Total violations | $violations_found |
| Files auto-fixed | $autofix_count |

## Compliance by Series

| Series | Compliant | Total | Rate |
|--------|-----------|-------|------|
| C (Core) | $c_compliant | $c_total | $(( c_total > 0 ? c_compliant * 100 / c_total : 0 ))% |
| W (Work) | $w_compliant | $w_total | $(( w_total > 0 ? w_compliant * 100 / w_total : 0 ))% |
| P (Projects) | $p_compliant | $p_total | $(( p_total > 0 ? p_compliant * 100 / p_total : 0 ))% |
| U (Utility) | $u_compliant | $u_total | $(( u_total > 0 ? u_compliant * 100 / u_total : 0 ))% |

## Recommended Actions

| Action | Count | Description |
|--------|-------|-------------|
| compliant | $action_compliant | No action needed |
| autofix | $action_autofix | Missing required files / required 00_run - can auto-create |
| migrate | $action_migrate | Invalid top-level dirs - needs manual folder renames |
| exception | $action_exception | Repo has declared exception file |
| ignore | $action_ignore | P/U series missing optional 00_run only |

## Suggested Rollout Batches

### Batch 1: C-series Core (Priority)
C-series repos are core infrastructure. Fix first for stability.
- Total: $c_total repos
- Currently compliant: $c_compliant
- Needing attention: $((c_total - c_compliant))

### Batch 2: W-series Work
W-series repos are business/analytics. Fix after core.
- Total: $w_total repos
- Currently compliant: $w_compliant
- Needing attention: $((w_total - w_compliant))

### Batch 3: P-series Active Projects
P-series repos are projects. 00_run optional, focus on required files.
- Total: $p_total repos
- Currently compliant: $p_compliant
- Needing attention: $((p_total - p_compliant))

## Configuration

- **Allowed dirs:** ${ALLOWED_DIRS//|/, }
- **Default required files:** $DEFAULT_REQUIRED_FILES
- **00_run required for:** C-series, W-series
- **00_run optional for:** P-series, U-series
- **Exceptions:** via \`00_admin/audit_exceptions.yaml\`

## Output Files

- **Audit CSV:** \`$CSV_FILE\`
- **Audit CSV (latest):** \`$CSV_LATEST\`
- **Actions CSV:** \`$ACTIONS_FILE\`
- **Actions CSV (latest):** \`$ACTIONS_LATEST\`
EOF

echo "Receipt: $RECEIPT_FILE"

if [[ $violations_found -gt 0 ]]; then
  echo ""
  echo -e "${YELLOW}Remediation:${NC}"
  echo "1. Run with --autofix-safe to create missing stubs"
  echo "2. Migrate repos manually for invalid directory issues"
  echo "3. Re-run audit to verify compliance"
  exit 1
else
  echo ""
  echo -e "${GREEN}All repos compliant with Betty Protocol folder structure.${NC}"
  exit 0
fi
