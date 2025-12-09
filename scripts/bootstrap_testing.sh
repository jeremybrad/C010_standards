#!/usr/bin/env bash
# bootstrap_testing.sh
# Apply testing standards to SyncedProjects repositories
#
# Usage:
#   ./bootstrap_testing.sh [--dry-run] [project_path...]
#
# Examples:
#   ./bootstrap_testing.sh                           # All C-series projects
#   ./bootstrap_testing.sh --dry-run                 # Preview changes
#   ./bootstrap_testing.sh ~/SyncedProjects/C002_sadb  # Specific project

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STANDARDS_DIR="$(dirname "$SCRIPT_DIR")"
TESTING_DIR="$STANDARDS_DIR/policy/testing"
WORKSPACE="${WORKSPACE:-$HOME/SyncedProjects}"

DRY_RUN=false
VERBOSE=false

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }
log_dry() { echo -e "${YELLOW}[DRY-RUN]${NC} $1"; }

usage() {
    cat << EOF
Usage: $(basename "$0") [OPTIONS] [PROJECT_PATH...]

Apply testing standards to SyncedProjects repositories.

OPTIONS:
    --dry-run       Preview changes without applying
    --verbose       Show detailed output
    -h, --help      Show this help message

EXAMPLES:
    $(basename "$0")                              # All C-series projects
    $(basename "$0") --dry-run                    # Preview changes
    $(basename "$0") ~/SyncedProjects/C002_sadb   # Specific project
EOF
}

# Check if project has Python source code
has_python_source() {
    local project_path="$1"
    find "$project_path" -name "*.py" -not -path "*/.venv/*" -not -path "*/venv/*" \
        -not -path "*/node_modules/*" -not -path "*/__pycache__/*" | head -1 | grep -q .
}

# Check if project has Node.js source code
has_node_source() {
    local project_path="$1"
    [[ -f "$project_path/package.json" ]]
}

# Check if pytest.ini already exists and has coverage configured
needs_pytest_config() {
    local project_path="$1"
    if [[ -f "$project_path/pytest.ini" ]]; then
        if grep -q "cov-fail-under" "$project_path/pytest.ini" 2>/dev/null; then
            return 1  # Already has coverage configured
        fi
    fi
    return 0  # Needs configuration
}

# Determine test directory for project
detect_test_dir() {
    local project_path="$1"
    if [[ -d "$project_path/90_tests" ]]; then
        echo "90_tests"
    elif [[ -d "$project_path/tests" ]]; then
        echo "tests"
    elif [[ -d "$project_path/40_src/tests" ]]; then
        echo "40_src/tests"
    else
        echo "tests"  # Default
    fi
}

# Determine source directory for coverage
detect_src_dir() {
    local project_path="$1"
    if [[ -d "$project_path/40_src" ]]; then
        echo "40_src"
    elif [[ -d "$project_path/src" ]]; then
        echo "src"
    else
        # Use project name as source dir
        basename "$project_path"
    fi
}

# Apply pytest.ini to a project
apply_pytest_config() {
    local project_path="$1"
    local test_dir src_dir

    test_dir=$(detect_test_dir "$project_path")
    src_dir=$(detect_src_dir "$project_path")

    local target="$project_path/pytest.ini"

    if [[ "$DRY_RUN" == "true" ]]; then
        log_dry "Would create $target (testpaths=$test_dir, cov=$src_dir)"
        return 0
    fi

    # Create customized pytest.ini
    sed -e "s|testpaths = tests|testpaths = $test_dir|g" \
        -e "s|--cov=40_src|--cov=$src_dir|g" \
        -e "s|source = 40_src|source = $src_dir|g" \
        "$TESTING_DIR/pytest.ini.template" > "$target"

    log_info "Created $target (testpaths=$test_dir, cov=$src_dir)"
}

# Apply jest.config.js to a project
apply_jest_config() {
    local project_path="$1"
    local target="$project_path/jest.config.js"

    if [[ -f "$target" ]] && grep -q "coverageThreshold" "$target" 2>/dev/null; then
        log_info "Skipping $target (already has coverage configured)"
        return 0
    fi

    if [[ "$DRY_RUN" == "true" ]]; then
        log_dry "Would create $target"
        return 0
    fi

    cp "$TESTING_DIR/jest.config.js.template" "$target"
    log_info "Created $target"
}

# Process a single project
process_project() {
    local project_path="$1"
    local project_name
    project_name=$(basename "$project_path")

    [[ "$VERBOSE" == "true" ]] && log_info "Processing $project_name..."

    # Python projects
    if has_python_source "$project_path" && needs_pytest_config "$project_path"; then
        apply_pytest_config "$project_path"
    elif has_python_source "$project_path"; then
        [[ "$VERBOSE" == "true" ]] && log_info "Skipping $project_name (pytest.ini already configured)"
    fi

    # Node.js projects
    if has_node_source "$project_path"; then
        apply_jest_config "$project_path"
    fi
}

# Main
main() {
    local projects=()

    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --dry-run)
                DRY_RUN=true
                shift
                ;;
            --verbose|-v)
                VERBOSE=true
                shift
                ;;
            -h|--help)
                usage
                exit 0
                ;;
            *)
                projects+=("$1")
                shift
                ;;
        esac
    done

    # Default to C-series projects if none specified
    if [[ ${#projects[@]} -eq 0 ]]; then
        for dir in "$WORKSPACE"/C[0-9][0-9][0-9]_*; do
            [[ -d "$dir" ]] && projects+=("$dir")
        done
    fi

    [[ "$DRY_RUN" == "true" ]] && log_warn "DRY RUN MODE - no changes will be made"

    log_info "Processing ${#projects[@]} projects..."

    for project in "${projects[@]}"; do
        if [[ -d "$project" ]]; then
            process_project "$project"
        else
            log_error "Project not found: $project"
        fi
    done

    log_info "Done!"
}

main "$@"
