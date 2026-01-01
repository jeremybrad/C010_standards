#!/usr/bin/env python3
"""
Generate project registry from SyncedProjects workspace.

Scans P###_*, C###_*, W###_* directories and extracts:
- Project metadata (name, description, status)
- Git activity (last commit date)
- Key files (CLAUDE.md, Makefile, etc.)
- Dependencies and relationships

Outputs:
- YAML: SharedData/registry/project_registry.yaml
- Markdown: KNOWN_PROJECTS.md
- JSON: SharedData/registry/project_registry.json (feeds C016 prompt engine and other agents)
"""

import json
import os
import re
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

import yaml


class ProjectScanner:
    """Scan workspace and extract project metadata."""

    # Series label mapping for human-readable context
    SERIES_LABELS = {
        'C': 'Core Infrastructure',
        'P': 'Development Projects',
        'W': 'Work/Business Analytics',
    }

    def __init__(self, workspace_root: str):
        self.workspace_root = Path(workspace_root).expanduser()
        self.projects: List[Dict] = []

    def scan(self) -> List[Dict]:
        """Scan workspace for all P/C/W-series projects."""
        pattern = re.compile(r'^([PCW])(\d{3})_(.+)$')

        for entry in sorted(self.workspace_root.iterdir()):
            if not entry.is_dir():
                continue

            match = pattern.match(entry.name)
            if not match:
                continue

            series, number, slug = match.groups()
            project_info = self._extract_project_info(entry, series, number, slug)
            self.projects.append(project_info)

        return self.projects

    def _extract_project_info(self, path: Path, series: str, number: str, slug: str) -> Dict:
        """Extract metadata for a single project."""
        readme_path = path / 'README.md'
        has_readme = readme_path.exists()

        return {
            'id': f'{series}{number}',
            'series': series,
            'number': int(number),
            'slug': slug,
            'name': f'{series}{number}_{slug}',
            'path': path.name,
            'description': self._get_description(path),
            'status': self._get_status(path),
            'last_commit': self._get_last_commit(path),
            'has_claude_md': (path / 'CLAUDE.md').exists(),
            'has_makefile': (path / 'Makefile').exists(),
            'has_pyproject': (path / 'pyproject.toml').exists(),
            'has_package_json': (path / 'package.json').exists(),
            'has_readme': has_readme,
            'git_repo': (path / '.git').exists(),
            # New fields for JSON output / C016 prompt engine
            'readme_path': f'{path.name}/README.md' if has_readme else None,
            'readme_excerpt': self._get_readme_excerpt(path) if has_readme else None,
            'series_label': self.SERIES_LABELS.get(series, 'Unknown'),
            # Placeholder fields for future context enhancement
            'context_mini': None,
            'context_medium': None,
        }

    def _get_description(self, path: Path) -> str:
        """Extract description from README.md (single line for YAML/Markdown)."""
        readme = path / 'README.md'
        if not readme.exists():
            return f"Project {path.name}"

        try:
            content = readme.read_text(encoding='utf-8')
            lines = [l.strip() for l in content.split('\n') if l.strip()]

            # Skip title lines starting with #
            for line in lines:
                if not line.startswith('#'):
                    # Take first non-header line, truncate if needed
                    desc = line[:120]
                    if len(line) > 120:
                        desc += '...'
                    return desc

            return f"Project {path.name}"
        except Exception:
            return f"Project {path.name}"

    def _get_readme_excerpt(self, path: Path) -> Optional[str]:
        """Extract longer excerpt from README.md for JSON output (2-4 lines, ~400 chars)."""
        readme = path / 'README.md'
        if not readme.exists():
            return None

        try:
            content = readme.read_text(encoding='utf-8')
            lines = [l.strip() for l in content.split('\n') if l.strip()]

            # Skip pure header lines (starting with #)
            content_lines = []
            for line in lines:
                if not line.startswith('#'):
                    content_lines.append(line)
                    if len(content_lines) >= 4:
                        break

            if not content_lines:
                return None

            # Join and truncate to ~400 chars
            excerpt = ' '.join(content_lines)
            if len(excerpt) > 400:
                excerpt = excerpt[:400] + '...'

            return excerpt
        except Exception:
            return None

    def _get_status(self, path: Path) -> str:
        """Determine project status."""
        # Check if in Archive directory
        if 'Archive' in str(path) or 'archive' in str(path):
            return 'archived'

        # Check git activity - if last commit > 6 months, consider stale
        last_commit = self._get_last_commit(path)
        if last_commit:
            try:
                commit_date = datetime.fromisoformat(last_commit.replace('Z', '+00:00'))
                days_ago = (datetime.now(commit_date.tzinfo) - commit_date).days
                if days_ago > 180:
                    return 'stale'
            except Exception:
                pass

        return 'active'

    def _get_last_commit(self, path: Path) -> Optional[str]:
        """Get last git commit date."""
        if not (path / '.git').exists():
            return None

        try:
            result = subprocess.run(
                ['git', 'log', '-1', '--format=%cI'],
                cwd=path,
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                return result.stdout.strip()
        except Exception:
            pass

        return None


class RegistryWriter:
    """Write project registry in multiple formats.

    Outputs:
    - YAML: Detailed registry for human/machine consumption
    - Markdown: Human-readable project index
    - JSON: Machine-readable feed for C016 prompt engine and agents
    """

    def __init__(self, projects: List[Dict]):
        self.projects = projects

    def write_yaml(self, output_path: str):
        """Write YAML format registry."""
        output_path = Path(output_path).expanduser()
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Group by series
        c_projects = [p for p in self.projects if p['series'] == 'C']
        p_projects = [p for p in self.projects if p['series'] == 'P']
        w_projects = [p for p in self.projects if p['series'] == 'W']

        registry = {
            'metadata': {
                'version': '3.0',
                'generated_at': datetime.now().isoformat(),
                'generated_by': 'generate_project_registry.py',
                'workspace_root': str(Path('~/SyncedProjects').expanduser()),
                'total_projects': len(self.projects),
            },
            'series': {
                'C': {'name': 'Core Infrastructure', 'count': len(c_projects)},
                'P': {'name': 'Development Projects', 'count': len(p_projects)},
                'W': {'name': 'Work/Business Analytics', 'count': len(w_projects)},
            },
            'projects': {p['id']: self._format_project_yaml(p) for p in self.projects}
        }

        with open(output_path, 'w', encoding='utf-8') as f:
            yaml.safe_dump(registry, f, default_flow_style=False, sort_keys=False)

        print(f"✅ YAML registry written to {output_path}")

    def write_markdown(self, output_path: str):
        """Write Markdown format registry."""
        output_path = Path(output_path).expanduser()

        # Group by series
        c_projects = sorted([p for p in self.projects if p['series'] == 'C'], key=lambda x: x['number'])
        p_projects = sorted([p for p in self.projects if p['series'] == 'P'], key=lambda x: x['number'])
        w_projects = sorted([p for p in self.projects if p['series'] == 'W'], key=lambda x: x['number'])

        lines = [
            "# Known Projects",
            "",
            f"Auto-generated project registry for SyncedProjects workspace.",
            f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            f"**Total Projects**: {len(self.projects)} ({len(c_projects)} Core, {len(p_projects)} Development, {len(w_projects)} Work)",
            "",
            "---",
            "",
        ]

        if c_projects:
            lines.extend(self._format_series_markdown('Core Infrastructure (C-series)', c_projects))

        if p_projects:
            lines.extend(self._format_series_markdown('Development Projects (P-series)', p_projects))

        if w_projects:
            lines.extend(self._format_series_markdown('Work/Business Analytics (W-series)', w_projects))

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))

        print(f"✅ Markdown registry written to {output_path}")

    def write_json(self, output_path: str):
        """Write JSON format registry for C016 prompt engine and agents.

        JSON schema per project:
        - id, series, number, slug, name, path (identifiers)
        - description, status, last_commit (metadata)
        - has_readme, has_claude_md, has_makefile, has_pyproject, has_package_json, git_repo (booleans)
        - readme_path, readme_excerpt, series_label (new fields)
        - context_mini, context_medium (placeholders for future enhancement)
        """
        output_path = Path(output_path).expanduser()
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Group by series
        c_projects = sorted([p for p in self.projects if p['series'] == 'C'], key=lambda x: x['number'])
        p_projects = sorted([p for p in self.projects if p['series'] == 'P'], key=lambda x: x['number'])
        w_projects = sorted([p for p in self.projects if p['series'] == 'W'], key=lambda x: x['number'])

        registry = {
            'metadata': {
                'version': '3.1',
                'schema_version': '1.0',
                'generated_at': datetime.now().isoformat(),
                'generated_by': 'generate_project_registry.py',
                'workspace_root': str(Path('~/SyncedProjects').expanduser()),
                'total_projects': len(self.projects),
                'purpose': 'Feeds C016 prompt engine and other agents with project-level context',
            },
            'series': {
                'C': {'name': 'Core Infrastructure', 'count': len(c_projects)},
                'P': {'name': 'Development Projects', 'count': len(p_projects)},
                'W': {'name': 'Work/Business Analytics', 'count': len(w_projects)},
            },
            'projects': {p['id']: self._format_project_json(p) for p in self.projects}
        }

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(registry, f, indent=2, ensure_ascii=False, sort_keys=False)

        print(f"✅ JSON registry written to {output_path}")

    def _format_project_yaml(self, project: Dict) -> Dict:
        """Format project for YAML output."""
        return {
            'name': project['name'],
            'slug': project['slug'],
            'description': project['description'],
            'status': project['status'],
            'path': project['path'],
            'last_commit': project['last_commit'],
            'files': {
                'claude_md': project['has_claude_md'],
                'makefile': project['has_makefile'],
                'pyproject': project['has_pyproject'],
                'package_json': project['has_package_json'],
                'readme': project['has_readme'],
            },
            'git_repo': project['git_repo'],
        }

    def _format_project_json(self, project: Dict) -> Dict:
        """Format project for JSON output with all fields including C016 context."""
        return {
            # Identifiers
            'id': project['id'],
            'series': project['series'],
            'number': project['number'],
            'slug': project['slug'],
            'name': project['name'],
            'path': project['path'],
            # Metadata
            'description': project['description'],
            'status': project['status'],
            'last_commit': project['last_commit'],
            # File presence booleans
            'has_readme': project['has_readme'],
            'has_claude_md': project['has_claude_md'],
            'has_makefile': project['has_makefile'],
            'has_pyproject': project['has_pyproject'],
            'has_package_json': project['has_package_json'],
            'git_repo': project['git_repo'],
            # New fields for C016 prompt engine
            'readme_path': project['readme_path'],
            'readme_excerpt': project['readme_excerpt'],
            'series_label': project['series_label'],
            # Placeholder fields for future context enhancement
            'context_mini': project['context_mini'],
            'context_medium': project['context_medium'],
        }

    def _format_series_markdown(self, title: str, projects: List[Dict]) -> List[str]:
        """Format project series for Markdown output."""
        lines = [
            f"## {title}",
            "",
        ]

        for project in projects:
            status_emoji = {
                'active': '✅',
                'stale': '⚠️',
                'archived': '📦',
            }.get(project['status'], '❓')

            # Build feature badges
            badges = []
            if project['has_claude_md']:
                badges.append('📘 CLAUDE.md')
            if project['has_makefile']:
                badges.append('⚙️ Makefile')
            if project['git_repo']:
                badges.append('🔧 Git')

            badges_str = ' · '.join(badges) if badges else ''

            # Format last commit
            commit_str = ''
            if project['last_commit']:
                try:
                    commit_date = datetime.fromisoformat(project['last_commit'].replace('Z', '+00:00'))
                    commit_str = f" (last: {commit_date.strftime('%Y-%m-%d')})"
                except Exception:
                    pass

            lines.extend([
                f"### {status_emoji} {project['name']}",
                f"{project['description']}",
                "",
                f"**Path**: `{project['path']}`{commit_str}",
            ])

            if badges_str:
                lines.append(f"**Features**: {badges_str}")

            lines.append("")

        return lines


def main():
    """Main entry point."""
    workspace_root = Path('~/SyncedProjects').expanduser()

    if not workspace_root.exists():
        print(f"❌ Workspace not found: {workspace_root}")
        return 1

    print(f"🔍 Scanning workspace: {workspace_root}")

    scanner = ProjectScanner(workspace_root)
    projects = scanner.scan()

    print(f"📊 Found {len(projects)} projects")

    # Write outputs
    writer = RegistryWriter(projects)
    writer.write_yaml('~/SyncedProjects/SharedData/registry/project_registry.yaml')
    writer.write_markdown('~/SyncedProjects/KNOWN_PROJECTS.md')
    writer.write_json('~/SyncedProjects/SharedData/registry/project_registry.json')

    print("✅ Registry generation complete!")
    return 0


if __name__ == '__main__':
    exit(main())
