#!/usr/bin/env bash
#
# Update project registry for SyncedProjects workspace
#
# Usage: ./scripts/update-registry.sh
#
# Outputs:
#   - SharedData/registry/project_registry.yaml (detailed YAML)
#   - KNOWN_PROJECTS.md (human-readable markdown)
#

set -euo pipefail

WORKSPACE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

cd "$WORKSPACE_ROOT"

echo "🔄 Updating project registry..."
python3 scripts/generate_project_registry.py

echo ""
echo "📍 Registry locations:"
echo "  - YAML: SharedData/registry/project_registry.yaml"
echo "  - Markdown: KNOWN_PROJECTS.md"
echo ""
echo "✅ Done! You can now hand these files to any LLM for workspace context."
