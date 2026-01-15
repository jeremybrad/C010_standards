#!/usr/bin/env bash
#
# Local Workspace Compliance Orchestrator
#
# Runs all compliance checks locally and writes outputs to stable paths
# for Mission Control consumption. This is the ONLY way to run workspace-wide
# compliance checks - GitHub Actions cannot see ~/SyncedProjects.
#
# Usage:
#   ./scripts/run_workspace_compliance_local.sh
#   ./scripts/run_workspace_compliance_local.sh --verbose
#
# Stable Output Paths (for Mission Control):
#   ~/SyncedProjects/_SharedData/registry/compliance/
#     - compliance_state_latest.json   (current state for delta detection)
#     - WORKSPACE_COMPLIANCE_LATEST.md (human-readable report)
#     - compliance_delta_latest.md     (what changed since last run)
#     - docmeta_audit_latest.json      (DocMeta validation results)
#
# Schedule this locally via:
#   - cron (Unix): 0 6 * * * ~/SyncedProjects/C010_standards/scripts/run_workspace_compliance_local.sh
#   - launchd (macOS): Create a plist in ~/Library/LaunchAgents/
#   - Mission Control: Add to scheduled tasks
#
# This script does NOT create GitHub issues or external alerts.
# Mission Control reads the output files and surfaces alerts there.

set -uo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
C010_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
WORKSPACE="$HOME/SyncedProjects"

# Output directory - stable paths for Mission Control
OUTPUT_DIR="$WORKSPACE/_SharedData/registry/compliance"
TODAY=$(date +%Y%m%d)
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

VERBOSE=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -v|--verbose) VERBOSE=true; shift ;;
        *) echo "Unknown option: $1"; exit 1 ;;
    esac
done

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log() {
    if [ "$VERBOSE" = true ]; then
        echo -e "$1"
    fi
}

# Create output directory
mkdir -p "$OUTPUT_DIR"

echo "═══════════════════════════════════════════════════"
echo "  Local Workspace Compliance Audit"
echo "  $TIMESTAMP"
echo "═══════════════════════════════════════════════════"
echo ""
echo "Output: $OUTPUT_DIR"
echo ""

# Track results
ERRORS=0

# ─────────────────────────────────────────────────────────
# Step 1: Run folder structure audit
# ─────────────────────────────────────────────────────────
echo "1/5 Running folder structure audit..."
AUDIT_CSV="$OUTPUT_DIR/folder_audit_$TODAY.csv"
if [ -f "$SCRIPT_DIR/audit_folder_structure.sh" ]; then
    if bash "$SCRIPT_DIR/audit_folder_structure.sh" "$WORKSPACE" > "$AUDIT_CSV" 2>/dev/null; then
        FAIL_COUNT=$(grep -c ",FAIL," "$AUDIT_CSV" 2>/dev/null || echo "0")
        if [ "$FAIL_COUNT" -eq 0 ]; then
            echo -e "    ${GREEN}✅${NC} All repos compliant"
        else
            echo -e "    ${YELLOW}⚠️${NC}  $FAIL_COUNT repos with folder violations"
        fi
    else
        echo -e "    ${YELLOW}⚠️${NC}  Audit script had errors"
        ((ERRORS++))
    fi
else
    echo -e "    ${YELLOW}⚠️${NC}  audit_folder_structure.sh not found"
fi

# ─────────────────────────────────────────────────────────
# Step 2: Render compliance report
# ─────────────────────────────────────────────────────────
echo "2/5 Rendering compliance report..."
COMPLIANCE_MD="$OUTPUT_DIR/WORKSPACE_COMPLIANCE_LATEST.md"
if [ -f "$SCRIPT_DIR/render_workspace_compliance_report.py" ]; then
    if python3 "$SCRIPT_DIR/render_workspace_compliance_report.py" > "$COMPLIANCE_MD" 2>/dev/null; then
        echo -e "    ${GREEN}✅${NC} Report generated"
    else
        echo -e "    ${YELLOW}⚠️${NC}  Report renderer had errors"
        ((ERRORS++))
    fi
else
    echo -e "    ${YELLOW}⚠️${NC}  render_workspace_compliance_report.py not found"
fi

# ─────────────────────────────────────────────────────────
# Step 3: Run META.yaml drift check
# ─────────────────────────────────────────────────────────
echo "3/5 Running META.yaml drift check..."
DRIFT_TXT="$OUTPUT_DIR/meta_drift_$TODAY.txt"
if [ -f "$SCRIPT_DIR/check_meta_yaml_drift.py" ]; then
    if python3 "$SCRIPT_DIR/check_meta_yaml_drift.py" > "$DRIFT_TXT" 2>&1; then
        echo -e "    ${GREEN}✅${NC} No drift detected"
    else
        DRIFT_COUNT=$(grep -c "DRIFT:" "$DRIFT_TXT" 2>/dev/null || echo "0")
        echo -e "    ${YELLOW}⚠️${NC}  $DRIFT_COUNT drift issues found"
    fi
else
    echo -e "    ${YELLOW}⚠️${NC}  check_meta_yaml_drift.py not found"
fi

# ─────────────────────────────────────────────────────────
# Step 4: Run DocMeta validation (advisory)
# ─────────────────────────────────────────────────────────
echo "4/5 Running DocMeta validation (advisory)..."
DOCMETA_JSON="$OUTPUT_DIR/docmeta_audit_latest.json"
if [ -f "$SCRIPT_DIR/check_workspace_docmeta.py" ]; then
    if python3 "$SCRIPT_DIR/check_workspace_docmeta.py" --output "$DOCMETA_JSON" > /dev/null 2>&1; then
        DOCMETA_COUNT=$(python3 -c "import json; print(json.load(open('$DOCMETA_JSON')).get('metadata',{}).get('total_issues', 0))" 2>/dev/null || echo "0")
        if [ "$DOCMETA_COUNT" -eq 0 ]; then
            echo -e "    ${GREEN}✅${NC} All DocMeta headers valid"
        else
            echo -e "    ${YELLOW}⚠️${NC}  $DOCMETA_COUNT advisory issues"
        fi
    else
        echo -e "    ${YELLOW}⚠️${NC}  DocMeta validation had errors"
    fi
else
    echo -e "    ${YELLOW}⚠️${NC}  check_workspace_docmeta.py not found"
fi

# ─────────────────────────────────────────────────────────
# Step 5: Run delta detection
# ─────────────────────────────────────────────────────────
echo "5/5 Running compliance delta detection..."
DELTA_MD="$OUTPUT_DIR/compliance_delta_latest.md"
if [ -f "$SCRIPT_DIR/compliance_delta.py" ]; then
    DELTA_EXIT=0
    python3 "$SCRIPT_DIR/compliance_delta.py" --output "$DELTA_MD" 2>/dev/null || DELTA_EXIT=$?

    if [ $DELTA_EXIT -eq 0 ]; then
        echo -e "    ${GREEN}✅${NC} No new violations"
    elif [ $DELTA_EXIT -eq 1 ]; then
        echo -e "    ${RED}🚨${NC} New violations detected!"
        echo ""
        echo "─────────────────────────────────────────────────"
        echo "ALERT: Check $DELTA_MD for details"
        echo "─────────────────────────────────────────────────"
    else
        echo -e "    ${YELLOW}⚠️${NC}  Delta detection had errors"
        ((ERRORS++))
    fi
else
    echo -e "    ${YELLOW}⚠️${NC}  compliance_delta.py not found"
fi

# ─────────────────────────────────────────────────────────
# Summary
# ─────────────────────────────────────────────────────────
echo ""
echo "═══════════════════════════════════════════════════"
echo "  Complete ($ERRORS errors)"
echo "═══════════════════════════════════════════════════"
echo ""
echo "Stable output files (for Mission Control):"
echo "  - $OUTPUT_DIR/compliance_state_latest.json"
echo "  - $OUTPUT_DIR/WORKSPACE_COMPLIANCE_LATEST.md"
echo "  - $OUTPUT_DIR/compliance_delta_latest.md"
echo "  - $OUTPUT_DIR/docmeta_audit_latest.json"
echo ""

# Verbose: show delta report
if [ "$VERBOSE" = true ] && [ -f "$DELTA_MD" ]; then
    echo "─────────────────────────────────────────────────"
    echo "Delta Report:"
    echo "─────────────────────────────────────────────────"
    cat "$DELTA_MD"
fi

exit $ERRORS
