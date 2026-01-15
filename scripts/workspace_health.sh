#!/usr/bin/env bash
#
# Workspace Health Dashboard
# Runs health checks across key projects and reports status
#
# Usage: ./scripts/workspace_health.sh
#        ./scripts/workspace_health.sh --verbose
#        ./scripts/workspace_health.sh --json
#
# Exit codes:
#   0 - All checks passed
#   1 - One or more checks failed
#
# Migrated from: ~/SyncedProjects/_scripts/workspace_health.sh

set -uo pipefail

WORKSPACE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$WORKSPACE_ROOT"

# Configuration
VERBOSE=false
JSON_OUTPUT=false
TIMESTAMP=$(date +%Y-%m-%d_%H%M%S)
LOG_DIR="$WORKSPACE_ROOT/_receipts/health"
mkdir -p "$LOG_DIR"

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -v|--verbose) VERBOSE=true; shift ;;
        -j|--json) JSON_OUTPUT=true; shift ;;
        *) echo "Unknown option: $1"; exit 1 ;;
    esac
done

# Projects with make health targets
HEALTH_PROJECTS=(
    "C001_mission-control"
    "C002_sadb"
    "C003_sadb_canonical"
    "P030_ai-services"
)

# Projects to check for META.yaml
ALL_PROJECTS=$(ls -d C[0-9][0-9][0-9]_* P[0-9][0-9][0-9]_* W[0-9][0-9][0-9]_* 2>/dev/null || true)

# Counters
PASSED=0
FAILED=0
WARNINGS=0
RESULTS=()

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log() {
    if [ "$VERBOSE" = true ]; then
        echo -e "$1"
    fi
}

check_project_health() {
    local proj=$1
    local status="unknown"
    local message=""

    if [ -d "$proj" ]; then
        cd "$proj"
        if [ -f "Makefile" ] && grep -q "^health:" Makefile 2>/dev/null; then
            output=$(make health 2>&1) || true
            if echo "$output" | grep -q "PASSED\|✅\|OK"; then
                status="passed"
                ((PASSED++))
            else
                status="failed"
                message=$(echo "$output" | tail -1)
                ((FAILED++))
            fi
        else
            status="no_health_target"
            message="No make health target"
            ((WARNINGS++))
        fi
        cd "$WORKSPACE_ROOT"
    else
        status="not_found"
        message="Directory not found"
        ((FAILED++))
    fi

    RESULTS+=("{\"project\":\"$proj\",\"status\":\"$status\",\"message\":\"$message\"}")

    # Print status
    case $status in
        passed)
            echo -e "${GREEN}✅${NC} $proj"
            ;;
        failed)
            echo -e "${RED}❌${NC} $proj: $message"
            ;;
        no_health_target)
            echo -e "${YELLOW}⚠️${NC}  $proj: $message"
            ;;
        not_found)
            echo -e "${RED}❌${NC} $proj: $message"
            ;;
    esac
}

check_meta_yaml() {
    local missing=0
    local total=0

    echo ""
    echo "META.yaml Coverage:"

    for proj in $ALL_PROJECTS; do
        if [ -d "$proj" ]; then
            ((total++))
            if [ ! -f "$proj/META.yaml" ]; then
                ((missing++))
                log "   Missing: $proj"
            fi
        fi
    done

    local coverage=$((100 - (missing * 100 / total)))
    if [ $missing -eq 0 ]; then
        echo -e "   ${GREEN}✅${NC} All $total projects have META.yaml"
    else
        echo -e "   ${YELLOW}⚠️${NC}  $missing/$total projects missing META.yaml ($coverage% coverage)"
        ((WARNINGS++))
    fi
}

check_services() {
    echo ""
    echo "Service Status:"

    # Check Mission Control vault
    if curl -s --connect-timeout 2 http://localhost:8820/health >/dev/null 2>&1; then
        echo -e "   ${GREEN}✅${NC} Mission Control vault (8820)"
    else
        echo -e "   ${YELLOW}⚠️${NC}  Mission Control vault (8820) - not running"
    fi

    # Check Ollama
    if curl -s --connect-timeout 2 http://localhost:11434/api/tags >/dev/null 2>&1; then
        echo -e "   ${GREEN}✅${NC} Ollama (11434)"
    else
        echo -e "   ${YELLOW}⚠️${NC}  Ollama (11434) - not running"
    fi

    # Check cognitive layer
    if curl -s --connect-timeout 2 http://localhost:11435/health >/dev/null 2>&1; then
        echo -e "   ${GREEN}✅${NC} Cognitive layer (11435)"
    else
        echo -e "   ${YELLOW}⚠️${NC}  Cognitive layer (11435) - not running"
    fi
}

check_disk_usage() {
    echo ""
    echo "Disk Usage:"

    # Workspace size
    ws_size=$(du -sh "$WORKSPACE_ROOT" 2>/dev/null | cut -f1)
    echo "   Workspace: $ws_size"

    # SADB_Data size
    if [ -d "$HOME/SADB_Data" ]; then
        sadb_size=$(du -sh "$HOME/SADB_Data" 2>/dev/null | cut -f1)
        echo "   SADB_Data: $sadb_size"
    fi

    # Large directories warning
    large_dirs=$(find "$WORKSPACE_ROOT" -maxdepth 3 -type d \( -name "node_modules" -o -name ".venv" -o -name "venv" \) 2>/dev/null | wc -l | tr -d ' ')
    if [ "$large_dirs" -gt 0 ]; then
        echo -e "   ${YELLOW}⚠️${NC}  Found $large_dirs virtual env/node_modules directories"
    fi
}

# Main execution
echo "═══════════════════════════════════════════════════"
echo "  SyncedProjects Health Dashboard"
echo "  $(date '+%Y-%m-%d %H:%M:%S')"
echo "═══════════════════════════════════════════════════"
echo ""
echo "Project Health Checks:"

for proj in "${HEALTH_PROJECTS[@]}"; do
    check_project_health "$proj"
done

check_meta_yaml
check_services
check_disk_usage

# Summary
echo ""
echo "═══════════════════════════════════════════════════"
echo -e "  Summary: ${GREEN}$PASSED passed${NC}, ${RED}$FAILED failed${NC}, ${YELLOW}$WARNINGS warnings${NC}"
echo "═══════════════════════════════════════════════════"

# Save log
LOG_FILE="$LOG_DIR/health_$TIMESTAMP.log"
{
    echo "Timestamp: $TIMESTAMP"
    echo "Passed: $PASSED"
    echo "Failed: $FAILED"
    echo "Warnings: $WARNINGS"
} > "$LOG_FILE"

# JSON output if requested
if [ "$JSON_OUTPUT" = true ]; then
    echo ""
    echo "{"
    echo "  \"timestamp\": \"$TIMESTAMP\","
    echo "  \"passed\": $PASSED,"
    echo "  \"failed\": $FAILED,"
    echo "  \"warnings\": $WARNINGS,"
    echo "  \"results\": [$(IFS=,; echo "${RESULTS[*]}")]"
    echo "}"
fi

# Exit code
if [ $FAILED -gt 0 ]; then
    exit 1
else
    exit 0
fi
