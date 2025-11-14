#!/usr/bin/env bash
# Bootstrap cross-platform awareness into CLAUDE.md files across workspace
# Part of C010_standards cross-platform protocol

set -euo pipefail

# Configuration
STAMP=$(date +"%Y%m%d_%H%M%S")
DRY_RUN=false
ROOT=""

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --dry-run)
      DRY_RUN=true
      shift
      ;;
    *)
      ROOT="$1"
      shift
      ;;
  esac
done

# Set defaults after parsing
if [ -z "$ROOT" ]; then
  ROOT="$HOME/SyncedProjects"
fi

TEMPLATE="$ROOT/C010_standards/policy/templates/claude_md_crossplatform.template.md"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo ">>> Bootstrapping cross-platform awareness in CLAUDE.md files"
echo "    Workspace: $ROOT"
echo "    Template: $TEMPLATE"
if [ "$DRY_RUN" = true ]; then
  echo -e "    ${YELLOW}DRY RUN MODE - no changes will be made${NC}"
fi
echo

# Check template exists
if [ ! -f "$TEMPLATE" ]; then
  echo -e "${RED}ERROR: Template not found at $TEMPLATE${NC}"
  exit 1
fi

# Load template content
TEMPLATE_CONTENT=$(cat "$TEMPLATE")

# Track statistics
TOTAL=0
UPDATED=0
SKIPPED=0
ERRORS=0

# Process each repository
for repo in "$ROOT"/*/; do
  # Skip if not a directory
  [ -d "$repo" ] || continue

  # Skip special directories
  basename_repo=$(basename "$repo")
  if [[ "$basename_repo" == "Archive" ]] || \
     [[ "$basename_repo" == "_receipts" ]] || \
     [[ "$basename_repo" == "SharedData" ]]; then
    continue
  fi

  # Look for CLAUDE.md
  CLAUDE_MD="$repo/CLAUDE.md"

  if [ ! -f "$CLAUDE_MD" ]; then
    continue
  fi

  TOTAL=$((TOTAL + 1))

  # Check if already has platform compatibility section
  if grep -q "## Platform Compatibility" "$CLAUDE_MD"; then
    echo -e "  ${GREEN}✓${NC} $basename_repo - already has platform compatibility section"
    SKIPPED=$((SKIPPED + 1))
    continue
  fi

  echo -e "  ${YELLOW}+${NC} $basename_repo - adding platform compatibility section"

  if [ "$DRY_RUN" = true ]; then
    echo "    [DRY RUN] Would add platform compatibility section"
    UPDATED=$((UPDATED + 1))
    continue
  fi

  # Create backup
  cp "$CLAUDE_MD" "$CLAUDE_MD.backup.$STAMP"

  # Try to insert after "## Overview" section, or before "## Common Commands"
  # This uses awk to find the right insertion point
  if grep -q "^## Overview" "$CLAUDE_MD"; then
    # Insert after Overview section (after the next blank line)
    awk -v template="$TEMPLATE_CONTENT" '
      /^## Overview/ { overview=1; print; next }
      overview && /^$/ && !inserted {
        print;
        print "";
        print template;
        print "";
        inserted=1;
        next
      }
      { print }
    ' "$CLAUDE_MD.backup.$STAMP" > "$CLAUDE_MD"

  elif grep -q "^## Common Commands" "$CLAUDE_MD"; then
    # Insert before Common Commands section
    awk -v template="$TEMPLATE_CONTENT" '
      /^## Common Commands/ && !inserted {
        print template;
        print "";
        inserted=1
      }
      { print }
    ' "$CLAUDE_MD.backup.$STAMP" > "$CLAUDE_MD"

  else
    # Fallback: append at end of file
    {
      cat "$CLAUDE_MD.backup.$STAMP"
      echo ""
      echo ""
      echo "$TEMPLATE_CONTENT"
    } > "$CLAUDE_MD"
  fi

  # Check if update was successful
  if grep -q "## Platform Compatibility" "$CLAUDE_MD"; then
    UPDATED=$((UPDATED + 1))

    # Create receipt if repo has 00_admin structure
    if [ -d "$repo/00_admin/RECEIPTS" ]; then
      echo "Cross-platform awareness added to CLAUDE.md at $STAMP" > \
        "$repo/00_admin/RECEIPTS/claude_crossplatform_${STAMP}.txt"
      echo "    Receipt created: 00_admin/RECEIPTS/claude_crossplatform_${STAMP}.txt"
    fi

    # Clean up backup
    rm "$CLAUDE_MD.backup.$STAMP"
  else
    echo -e "    ${RED}ERROR: Failed to add platform compatibility section${NC}"
    # Restore from backup
    mv "$CLAUDE_MD.backup.$STAMP" "$CLAUDE_MD"
    ERRORS=$((ERRORS + 1))
  fi
done

# Summary
echo
echo ">>> Summary"
echo "    Total CLAUDE.md files found: $TOTAL"
echo -e "    ${GREEN}Updated: $UPDATED${NC}"
echo -e "    ${YELLOW}Skipped (already present): $SKIPPED${NC}"
if [ $ERRORS -gt 0 ]; then
  echo -e "    ${RED}Errors: $ERRORS${NC}"
fi

if [ "$DRY_RUN" = true ]; then
  echo
  echo -e "${YELLOW}This was a dry run. Run without --dry-run to apply changes.${NC}"
fi

echo
echo ">>> Done."

# Exit with error if any errors occurred
if [ $ERRORS -gt 0 ]; then
  exit 1
fi
