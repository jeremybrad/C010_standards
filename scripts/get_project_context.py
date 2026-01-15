#!/usr/bin/env python3
"""
Query project_registry.json for project context.

Used by C016 prompt engine and other agents to inject project-level
context into prompts based on project ID or current working directory.

Usage:
    # By project ID
    python3 scripts/get_project_context.py C003
    python3 scripts/get_project_context.py P030

    # By directory path (auto-detect project)
    python3 scripts/get_project_context.py /Users/jeremy/SyncedProjects/C003_sadb_canonical
    python3 scripts/get_project_context.py .  # Use cwd

    # Output formats
    python3 scripts/get_project_context.py C003 --format json
    python3 scripts/get_project_context.py C003 --format context  # For prompt injection (default)
    python3 scripts/get_project_context.py C003 --format compact  # Single line

    # Query multiple projects
    python3 scripts/get_project_context.py C003 P030 W006

Examples:
    # Get context for current directory
    python3 scripts/get_project_context.py .

    # Get JSON for programmatic use
    python3 scripts/get_project_context.py C003 --format json | jq .

    # Inject into prompt template
    CONTEXT=$(python3 scripts/get_project_context.py C003 --format context)
    echo "Working on: $CONTEXT"

Migrated from: ~/SyncedProjects/_scripts/get_project_context.py
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional


class ProjectRegistry:
    """Query interface for project_registry.json."""

    def __init__(self, registry_path: Optional[str] = None):
        """Initialize registry reader.

        Args:
            registry_path: Path to project_registry.json. If None, uses default workspace location.
        """
        if registry_path is None:
            workspace = Path('~/SyncedProjects').expanduser()
            registry_path = workspace / '_SharedData' / 'registry' / 'project_registry.json'
        else:
            registry_path = Path(registry_path).expanduser()

        if not registry_path.exists():
            raise FileNotFoundError(f"Registry not found: {registry_path}")

        with open(registry_path, 'r', encoding='utf-8') as f:
            self.data = json.load(f)

        self.projects = self.data.get('projects', {})
        self.metadata = self.data.get('metadata', {})

    def get_by_id(self, project_id: str) -> Optional[Dict]:
        """Get project by ID (e.g., 'C003', 'P030')."""
        return self.projects.get(project_id)

    def get_by_path(self, path: str) -> Optional[Dict]:
        """Get project by directory path.

        Args:
            path: Absolute or relative path, or '.' for cwd

        Returns:
            Project dict if found, None otherwise
        """
        if path == '.':
            path = os.getcwd()

        path = Path(path).expanduser().resolve()

        # Extract project directory name from path
        # Look for pattern: C###_name, P###_name, W###_name
        for part in [path.name] + [p.name for p in path.parents]:
            # Match project directory pattern
            if len(part) > 4 and part[0] in 'CPW' and part[1:4].isdigit() and part[4] == '_':
                project_id = part[:4]  # e.g., C003, P030
                return self.get_by_id(project_id)

        return None

    def format_context(self, project: Dict, format_type: str = 'context') -> str:
        """Format project data for different use cases.

        Args:
            project: Project dictionary
            format_type: 'json', 'context', or 'compact'

        Returns:
            Formatted string
        """
        if format_type == 'json':
            return json.dumps(project, indent=2, ensure_ascii=False)

        elif format_type == 'compact':
            return (
                f"{project['id']} ({project.get('series_label', project.get('series', '?'))}) · "
                f"{project['status']} · {project['description'][:60]}..."
            )

        elif format_type == 'context':
            # Multi-line format suitable for CONTEXT blocks in prompts
            series_label = project.get('series_label', project.get('series', '?'))
            lines = [
                f"# Project: {project['name']}",
                f"ID: {project['id']} | Series: {series_label} | Status: {project['status']}",
                "",
                f"## Description",
                project['description'],
            ]

            if project.get('readme_excerpt'):
                lines.extend([
                    "",
                    f"## Overview",
                    project['readme_excerpt'],
                ])

            # Add file presence indicators
            features = []
            if project.get('has_claude_md'):
                features.append('CLAUDE.md')
            if project.get('has_makefile'):
                features.append('Makefile')
            if project.get('git_repo'):
                features.append('Git')

            if features:
                lines.extend([
                    "",
                    f"## Features",
                    ', '.join(features),
                ])

            # Add context fields if populated (future enhancement)
            if project.get('context_mini'):
                lines.extend([
                    "",
                    f"## Context (Mini)",
                    project['context_mini'],
                ])

            if project.get('context_medium'):
                lines.extend([
                    "",
                    f"## Context (Medium)",
                    project['context_medium'],
                ])

            return '\n'.join(lines)

        else:
            raise ValueError(f"Unknown format: {format_type}")


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Query project registry for context injection',
        epilog='See docstring for usage examples'
    )
    parser.add_argument(
        'identifiers',
        nargs='+',
        help='Project IDs (C003, P030) or paths (., /path/to/project)'
    )
    parser.add_argument(
        '--format',
        choices=['json', 'context', 'compact'],
        default='context',
        help='Output format (default: context)'
    )
    parser.add_argument(
        '--registry',
        help='Path to project_registry.json (default: ~/SyncedProjects/_SharedData/registry/project_registry.json)'
    )

    args = parser.parse_args()

    try:
        registry = ProjectRegistry(args.registry)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        print("\nRun: python3 scripts/generate_project_registry.py", file=sys.stderr)
        return 1

    results = []
    not_found = []

    for identifier in args.identifiers:
        # Try as project ID first
        if identifier[0] in 'CPW' and len(identifier) >= 4 and identifier[1:4].isdigit():
            project = registry.get_by_id(identifier[:4])
        else:
            # Try as path
            project = registry.get_by_path(identifier)

        if project:
            results.append(project)
        else:
            not_found.append(identifier)

    # Output results
    for i, project in enumerate(results):
        if i > 0 and args.format == 'context':
            print("\n" + "="*60 + "\n")
        print(registry.format_context(project, args.format))

    # Report not found
    if not_found:
        print(f"\nNot found: {', '.join(not_found)}", file=sys.stderr)
        return 1

    return 0


if __name__ == '__main__':
    sys.exit(main())
