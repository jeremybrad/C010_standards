#!/usr/bin/env bash
# bootstrap_tier2_wseries.sh - Scaffold Tier 2 documentation for W-series repos
#
# Usage:
#   bash scripts/bootstrap_tier2_wseries.sh [--dry-run] [repo_name...]
#   bash scripts/bootstrap_tier2_wseries.sh --dry-run W001 W003 W008 W009 W011
#   bash scripts/bootstrap_tier2_wseries.sh W001 W003 W008
#
# Options:
#   --dry-run   Show what would change without writing files
#   --verbose   Show detailed progress
#
# If no repo names provided, processes ALL W-series repos in workspace.
#
# Outputs (when not --dry-run):
#   - Scaffolds missing META.yaml, CHANGELOG.md, glossary.yaml
#   - Creates missing 10_docs/ and 20_receipts/ directories
#   - Creates receipts in both C010 and target repos
#   - Updates tracking file in 70_evidence/
#
set -euo pipefail

# Configuration
WORKSPACE="${HOME}/SyncedProjects"
C010_DIR="${WORKSPACE}/C010_standards"
TEMPLATES_DIR="${C010_DIR}/10_docs/policy/templates"
TRACKING_FILE="${C010_DIR}/70_evidence/tier2_bootstrap_status.yaml"

# Templates
META_TEMPLATE="${TEMPLATES_DIR}/meta_yaml_wseries.template.yaml"
CHANGELOG_TEMPLATE="${TEMPLATES_DIR}/changelog.template.md"
GLOSSARY_TEMPLATE="${TEMPLATES_DIR}/glossary.template.yaml"

# Timestamp
STAMP=$(date +"%Y%m%d_%H%M%S")
TODAY=$(date +"%Y-%m-%d")

# Parse arguments
DRY_RUN=false
VERBOSE=false
REPOS=()

for arg in "$@"; do
  case "$arg" in
    --dry-run)
      DRY_RUN=true
      ;;
    --verbose)
      VERBOSE=true
      ;;
    W*)
      REPOS+=("$arg")
      ;;
    *)
      echo "WARNING: Ignoring unknown argument: $arg" >&2
      ;;
  esac
done

# Helper functions
log_verbose() {
  if [[ "$VERBOSE" == "true" ]]; then
    echo "  [VERBOSE] $1"
  fi
}

log_action() {
  local action="$1"
  local target="$2"
  if [[ "$DRY_RUN" == "true" ]]; then
    echo "  [WOULD $action] $target"
  else
    echo "  [$action] $target"
  fi
}

# Verify templates exist
verify_templates() {
  local missing=0
  for template in "$META_TEMPLATE" "$CHANGELOG_TEMPLATE" "$GLOSSARY_TEMPLATE"; do
    if [[ ! -f "$template" ]]; then
      echo "ERROR: Template not found: $template" >&2
      missing=1
    fi
  done
  if [[ $missing -eq 1 ]]; then
    exit 1
  fi
}

# Get repo full path from short name
get_repo_path() {
  local short_name="$1"
  # Handle both "W001" and "W001_cmo-weekly-reporting" formats
  local matches
  matches=$(find "$WORKSPACE" -maxdepth 1 -type d -name "${short_name}*" 2>/dev/null | head -1)
  echo "$matches"
}

# Pre-flight check for a repo
preflight_check() {
  local repo_path="$1"
  local repo_name
  repo_name=$(basename "$repo_path")

  # Check if git repo
  if [[ ! -d "$repo_path/.git" ]]; then
    echo "  [SKIP] $repo_name: Not a git repository"
    return 1
  fi

  # Check README.md exists
  if [[ ! -f "$repo_path/README.md" ]]; then
    echo "  [SKIP] $repo_name: Missing README.md (required)"
    return 1
  fi

  # Check CLAUDE.md exists
  if [[ ! -f "$repo_path/CLAUDE.md" ]]; then
    echo "  [SKIP] $repo_name: Missing CLAUDE.md (required)"
    return 1
  fi

  log_verbose "$repo_name passed pre-flight checks"
  return 0
}

# Process single template with substitutions
process_template() {
  local template="$1"
  local repo_id="$2"

  sed -e "s/{REPO_ID}/$repo_id/g" \
      -e "s/{TODAY}/$TODAY/g" \
      -e "s/{STAMP}/$STAMP/g" \
      -e "s/{SUMMARY}/TODO: Add project summary/g" \
      -e "s/{CLIENT}/TODO: Add client name/g" \
      -e "s/{VERSION}/0.1.0/g" \
      -e "s/{PLACEHOLDER_TERM}/TODO/g" \
      -e "s/{PLACEHOLDER_DEFINITION}/TODO: Add definition/g" \
      -e "s/{TAG}/todo/g" \
      "$template"
}

# Bootstrap single repo
bootstrap_repo() {
  local repo_path="$1"
  local repo_name
  repo_name=$(basename "$repo_path")

  echo ""
  echo ">>> Processing: $repo_name"

  # Pre-flight check
  if ! preflight_check "$repo_path"; then
    return 1
  fi

  local changes_made=0

  # 1. META.yaml
  if [[ -f "$repo_path/META.yaml" ]]; then
    # Check if it has required fields
    if grep -q "client:" "$repo_path/META.yaml" 2>/dev/null; then
      log_verbose "META.yaml exists with client field"
    else
      echo "  [WARN] META.yaml exists but missing 'client:' field - manual fix needed"
    fi
  else
    log_action "CREATE" "META.yaml"
    if [[ "$DRY_RUN" == "false" ]]; then
      process_template "$META_TEMPLATE" "$repo_name" > "$repo_path/META.yaml"
    fi
    changes_made=$((changes_made + 1))
  fi

  # 2. CHANGELOG.md
  if [[ -f "$repo_path/CHANGELOG.md" ]]; then
    log_verbose "CHANGELOG.md already exists"
  else
    log_action "CREATE" "CHANGELOG.md"
    if [[ "$DRY_RUN" == "false" ]]; then
      process_template "$CHANGELOG_TEMPLATE" "$repo_name" > "$repo_path/CHANGELOG.md"
    fi
    changes_made=$((changes_made + 1))
  fi

  # 3. 10_docs/ directory
  if [[ -d "$repo_path/10_docs" ]]; then
    log_verbose "10_docs/ already exists"
  else
    log_action "CREATE" "10_docs/"
    if [[ "$DRY_RUN" == "false" ]]; then
      mkdir -p "$repo_path/10_docs"
    fi
    changes_made=$((changes_made + 1))
  fi

  # 4. glossary.yaml in 10_docs/
  if [[ -f "$repo_path/10_docs/glossary.yaml" ]]; then
    log_verbose "10_docs/glossary.yaml already exists"
  else
    log_action "CREATE" "10_docs/glossary.yaml"
    if [[ "$DRY_RUN" == "false" ]]; then
      process_template "$GLOSSARY_TEMPLATE" "$repo_name" > "$repo_path/10_docs/glossary.yaml"
    fi
    changes_made=$((changes_made + 1))
  fi

  # 5. 20_receipts/ directory
  if [[ -d "$repo_path/20_receipts" ]]; then
    log_verbose "20_receipts/ already exists"
  else
    log_action "CREATE" "20_receipts/"
    if [[ "$DRY_RUN" == "false" ]]; then
      mkdir -p "$repo_path/20_receipts"
    fi
    changes_made=$((changes_made + 1))
  fi

  # 6. Create bootstrap receipt in target repo
  if [[ $changes_made -gt 0 && "$DRY_RUN" == "false" ]]; then
    local receipt_file="$repo_path/20_receipts/tier2_bootstrap_${STAMP}.md"
    cat > "$receipt_file" << EOF
# Receipt: Tier 2 Documentation Bootstrap

**Date**: $(date "+%Y-%m-%d %H:%M:%S")
**Repo**: $repo_name
**Bootstrap Script**: C010_standards/scripts/bootstrap_tier2_wseries.sh v1.0

## Actions Taken

Files scaffolded by this bootstrap run. Review and populate content.

## Next Steps

1. Edit META.yaml: Fill in summary, client, folders, files
2. Edit CHANGELOG.md: Add recent changes
3. Edit 10_docs/glossary.yaml: Add domain-specific terms (3+ recommended)
4. Validate: \`python scripts/validate_tier2_compliance.py $repo_path\`
5. Generate primer: \`generate-project-primer $repo_name\`

## Compliance Check

Run from C010_standards:
\`\`\`bash
python scripts/validate_tier2_compliance.py $repo_path
\`\`\`
EOF
    log_action "CREATE" "20_receipts/tier2_bootstrap_${STAMP}.md"
  fi

  # Summary for this repo
  if [[ $changes_made -eq 0 ]]; then
    echo "  [OK] $repo_name: Already has Tier 2 structure"
  else
    echo "  [DONE] $repo_name: $changes_made items scaffolded"
  fi

  return 0
}

# Update tracking file
update_tracking() {
  local repos_processed=("$@")

  if [[ "$DRY_RUN" == "true" ]]; then
    echo ""
    echo "[WOULD UPDATE] $TRACKING_FILE"
    return
  fi

  # Ensure directory exists
  mkdir -p "$(dirname "$TRACKING_FILE")"

  # Create or update tracking file
  cat > "$TRACKING_FILE" << EOF
# Tier 2 Bootstrap Status Tracker
# Updated by: bootstrap_tier2_wseries.sh
# Last run: $(date "+%Y-%m-%dT%H:%M:%S")

last_run: "$(date "+%Y-%m-%dT%H:%M:%S")"
version: "1.0"
script: "scripts/bootstrap_tier2_wseries.sh"

# Repos processed in this run
repos_processed:
EOF

  for repo in "${repos_processed[@]}"; do
    echo "  - $repo" >> "$TRACKING_FILE"
  done

  echo "" >> "$TRACKING_FILE"
  echo "# To validate compliance, run:" >> "$TRACKING_FILE"
  echo "# python scripts/validate_tier2_compliance.py ~/SyncedProjects/<repo_name>" >> "$TRACKING_FILE"
}

# Main
main() {
  echo "=============================================="
  echo "Tier 2 W-Series Documentation Bootstrap"
  echo "=============================================="

  if [[ "$DRY_RUN" == "true" ]]; then
    echo ">>> DRY RUN MODE - No changes will be made"
  fi

  # Verify templates
  verify_templates
  log_verbose "Templates verified"

  # Build list of repos to process
  local repos_to_process=()

  if [[ ${#REPOS[@]} -eq 0 ]]; then
    # No repos specified - find all W-series repos
    echo ">>> No repos specified, scanning for all W-series repos..."
    for repo_dir in "$WORKSPACE"/W*/; do
      if [[ -d "$repo_dir" ]]; then
        repos_to_process+=("$repo_dir")
      fi
    done
  else
    # Specific repos provided
    for repo_short in "${REPOS[@]}"; do
      local repo_path
      repo_path=$(get_repo_path "$repo_short")
      if [[ -n "$repo_path" && -d "$repo_path" ]]; then
        repos_to_process+=("$repo_path")
      else
        echo "WARNING: Could not find repo matching: $repo_short" >&2
      fi
    done
  fi

  if [[ ${#repos_to_process[@]} -eq 0 ]]; then
    echo "ERROR: No repos to process" >&2
    exit 1
  fi

  echo ">>> Found ${#repos_to_process[@]} repos to process"

  # Process each repo
  local processed=()
  local skipped=0
  local modified=0

  for repo_path in "${repos_to_process[@]}"; do
    if bootstrap_repo "$repo_path"; then
      processed+=("$(basename "$repo_path")")
      modified=$((modified + 1))
    else
      skipped=$((skipped + 1))
    fi
  done

  # Update tracking file
  if [[ ${#processed[@]} -gt 0 ]]; then
    update_tracking "${processed[@]}"
  fi

  # Final summary
  echo ""
  echo "=============================================="
  if [[ "$DRY_RUN" == "true" ]]; then
    echo "DRY RUN SUMMARY:"
    echo "  Would process: $modified repos"
    echo "  Would skip: $skipped repos"
    echo ""
    echo "Run without --dry-run to apply changes."
  else
    echo "BOOTSTRAP COMPLETE:"
    echo "  Processed: $modified repos"
    echo "  Skipped: $skipped repos"
    echo ""
    echo "Next steps:"
    echo "  1. Review and populate scaffolded files in each repo"
    echo "  2. Run: python scripts/validate_tier2_compliance.py <repo_path>"
    echo "  3. Generate primers: generate-project-primer <repo_name>"
  fi
  echo "=============================================="
}

main "$@"
