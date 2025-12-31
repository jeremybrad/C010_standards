#!/bin/bash
# C010_standards - Standards Pulse (macOS)
# Double-click to generate fresh Standards inventory exports
#
# Outputs: 70_evidence/exports/Standards_Pulse.xlsx, Standards_Inventory.csv
#          20_receipts/<date>_standards_pulse.md

set -e

# Navigate to repo root (parent of 00_run/)
cd "$(dirname "$0")/.."
REPO_ROOT="$(pwd)"

echo "=============================================="
echo "C010_standards - Standards Pulse"
echo "=============================================="
echo "Repo: $REPO_ROOT"
echo ""

# Find Python (prefer venv if exists)
if [ -f ".venv/bin/python3" ]; then
    PYTHON=".venv/bin/python3"
elif [ -f "venv/bin/python3" ]; then
    PYTHON="venv/bin/python3"
else
    PYTHON="python3"
fi

echo "Using Python: $PYTHON"
echo ""

# Ensure output directories exist
mkdir -p 70_evidence/exports
mkdir -p 20_receipts

# Run the export script
echo "--- Running export_standards_pulse.py ---"
$PYTHON tools/export_standards_pulse.py

echo ""
echo "=============================================="
echo "RECEIPT"
echo "=============================================="
echo "Timestamp: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""
echo "Output files:"
ls -lh 70_evidence/exports/Standards_*.xlsx 70_evidence/exports/Standards_*.csv 2>/dev/null | awk '{print "  " $NF " (" $5 ")"}'
echo ""
echo "Receipt files:"
ls -lh 20_receipts/*_standards_pulse.md 2>/dev/null | tail -1 | awk '{print "  " $NF " (" $5 ")"}'
echo ""
echo "Done! Press any key to close..."
read -n 1
