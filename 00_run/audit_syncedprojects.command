#!/usr/bin/env bash
# audit_syncedprojects.command - Double-click launcher for folder structure audit
# macOS: Double-click this file in Finder
#
# Audits all repos in ~/SyncedProjects for Betty Protocol compliance.
# Produces CSV output for pivoting compliance across repos.
#
set -euo pipefail

# Navigate to repo root (regardless of where script is called from)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$REPO_ROOT"

echo "=============================================="
echo "C010_standards - Folder Structure Audit"
echo "=============================================="
echo "Repo: $REPO_ROOT"
echo ""

# Default workspace
WORKSPACE="${1:-$HOME/SyncedProjects}"

echo "Auditing: $WORKSPACE"
echo ""

# Run the audit script
bash scripts/audit_folder_structure.sh "$WORKSPACE"
EXIT_CODE=$?

echo ""
echo "=============================================="
echo "OUTPUT FILES"
echo "=============================================="
echo ""

# Show CSV location
CSV_LATEST="$REPO_ROOT/70_evidence/exports/folder_structure_audit_latest.csv"
if [[ -f "$CSV_LATEST" ]]; then
  echo "CSV (latest): $CSV_LATEST"
  echo ""
  echo "Preview (first 5 rows):"
  head -6 "$CSV_LATEST" | column -t -s ','
  echo ""
fi

# Show latest receipt
RECEIPT_LATEST=$(ls -t "$REPO_ROOT/20_receipts/folder_audit_"*.md 2>/dev/null | head -1)
if [[ -n "$RECEIPT_LATEST" ]]; then
  echo "Receipt: $RECEIPT_LATEST"
fi

echo ""
echo "Done! Press any key to close..."
read -n 1 -s

exit $EXIT_CODE
