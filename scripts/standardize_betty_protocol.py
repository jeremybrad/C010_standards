#!/usr/bin/env python3
"""
Betty Protocol Standardization Script
Applies Betty Protocol standards to projects in the SyncedProjects workspace.

Migrated from: ~/SyncedProjects/_scripts/standardize_betty_protocol.py
"""

import os
import sys
import json
import yaml
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

class ProjectAnalyzer:
    """Analyzes existing project structure and identifies gaps."""

    BETTY_FILES = [
        'README.md', 'CLAUDE.md', 'WHY_I_CARE.md',
        'RELATIONS.yaml', 'rules_now.md', 'Makefile'
    ]

    BETTY_DIRS = [
        '00_admin', '10_docs', '20_receipts', '30_config',
        '40_src', '70_evidence', '90_archive'
    ]

    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.project_name = project_path.name
        self.analysis = {}

    def analyze(self) -> Dict:
        """Analyze project compliance with Betty Protocol."""
        self.analysis = {
            'project': self.project_name,
            'path': str(self.project_path),
            'existing_files': [],
            'missing_files': [],
            'existing_dirs': [],
            'missing_dirs': [],
            'tech_stack': self._detect_tech_stack(),
            'project_type': self._detect_project_type(),
            'has_git': (self.project_path / '.git').exists()
        }

        # Check files
        for file in self.BETTY_FILES:
            if (self.project_path / file).exists():
                self.analysis['existing_files'].append(file)
            else:
                self.analysis['missing_files'].append(file)

        # Check directories
        for dir in self.BETTY_DIRS:
            if (self.project_path / dir).exists():
                self.analysis['existing_dirs'].append(dir)
            else:
                self.analysis['missing_dirs'].append(dir)

        return self.analysis

    def _detect_tech_stack(self) -> List[str]:
        """Detect project technology stack."""
        stack = []
        if (self.project_path / 'package.json').exists():
            stack.append('node.js')
        if (self.project_path / 'requirements.txt').exists():
            stack.append('python')
        if (self.project_path / 'pyproject.toml').exists():
            stack.append('python')
        if (self.project_path / 'go.mod').exists():
            stack.append('go')
        if (self.project_path / 'Cargo.toml').exists():
            stack.append('rust')
        return stack

    def _detect_project_type(self) -> str:
        """Detect project type based on structure."""
        if (self.project_path / 'server.js').exists() or \
            (self.project_path / 'app.py').exists():
            return 'service'
        elif (self.project_path / 'cli.py').exists() or \
              (self.project_path / 'bin').exists():
            return 'tool'
        elif (self.project_path / '__init__.py').exists():
            return 'library'
        return 'unknown'


class BettyProtocolGenerator:
    """Generates Betty Protocol compliant files and structure."""

    def __init__(self, project_path: Path, analysis: Dict):
        self.project_path = project_path
        self.analysis = analysis
        self.project_name = project_path.name
        self.project_id = self._extract_project_id()
        self.series = self.project_id[0] if self.project_id else 'P'

    def _extract_project_id(self) -> Optional[str]:
        """Extract project ID from name (e.g., P001 from P001_bettymirror)."""
        parts = self.project_name.split('_')
        if parts[0] and parts[0][0] in ['P', 'C', 'W', 'T']:
            return parts[0]
        return None

    def standardize(self, status='active', dry_run=False):
        """Apply Betty Protocol standardization."""
        actions = []

        # Create missing directories
        for dir_name in self.analysis['missing_dirs']:
            dir_path = self.project_path / dir_name
            if not dry_run:
                dir_path.mkdir(exist_ok=True)
            actions.append(f"Created directory: {dir_name}")

        # Generate missing files
        if 'README.md' in self.analysis['missing_files']:
            content = self._generate_readme(status)
            if not dry_run:
                (self.project_path / 'README.md').write_text(content)
            actions.append("Created README.md")
        elif 'README.md' in self.analysis['existing_files']:
            # Add frontmatter if missing
            content = self._add_readme_frontmatter(status)
            if content and not dry_run:
                (self.project_path / 'README.md').write_text(content)
                actions.append("Added frontmatter to README.md")

        if 'CLAUDE.md' in self.analysis['missing_files']:
            content = self._generate_claude_md()
            if not dry_run:
                (self.project_path / 'CLAUDE.md').write_text(content)
            actions.append("Created CLAUDE.md")

        if 'WHY_I_CARE.md' in self.analysis['missing_files']:
            content = self._generate_why_i_care()
            if not dry_run:
                (self.project_path / 'WHY_I_CARE.md').write_text(content)
            actions.append("Created WHY_I_CARE.md")

        if 'RELATIONS.yaml' in self.analysis['missing_files']:
            content = self._generate_relations()
            if not dry_run:
                (self.project_path / 'RELATIONS.yaml').write_text(content)
            actions.append("Created RELATIONS.yaml")

        if 'rules_now.md' in self.analysis['missing_files']:
            content = self._generate_rules_now()
            if not dry_run:
                (self.project_path / 'rules_now.md').write_text(content)
            actions.append("Created rules_now.md")

        if '.gitignore' not in self.analysis['existing_files']:
            content = self._generate_gitignore()
            if not dry_run:
                (self.project_path / '.gitignore').write_text(content)
            actions.append("Created .gitignore")

        # Create .kst directory and status
        kst_dir = self.project_path / '.kst'
        if not kst_dir.exists() and not dry_run:
            kst_dir.mkdir(exist_ok=True)
            self._generate_kst_status(kst_dir, status)
            actions.append("Created .kst/status.json")

        # Create receipt
        if not dry_run:
            self._create_receipt(actions)

        return actions

    def _generate_readme(self, status: str) -> str:
        """Generate README.md with frontmatter."""
        human_name = self.project_name.replace('_', ' ').title()

        return f"""---
project: {self.project_name}
name: {human_name}
series: {self.series}
type: {self.analysis['project_type']}
status: {status}
last_updated: {datetime.now().strftime('%Y-%m-%d')}
primary_maintainer: jeremybradford
purpose: >
  [TODO: Add one-line purpose]
tech_stack:
  - {', '.join(self.analysis['tech_stack']) if self.analysis['tech_stack'] else 'python'}
key_dependencies: []
deployment: local
integration_points: {{}}
---

# {human_name}

## Overview

[TODO: Add project overview]

## Setup

```bash
# Clone repository
git clone [repository-url]
cd {self.project_name}

# Install dependencies
{'npm install' if 'node.js' in self.analysis['tech_stack'] else 'pip install -r requirements.txt'}
```

## Health Check

```bash
make health  # Run comprehensive health check
```

## Development

[TODO: Add development instructions]

## Testing

```bash
make test  # Run tests
```

## Documentation

See [CLAUDE.md](CLAUDE.md) for AI assistant guidance.
"""

    def _add_readme_frontmatter(self, status: str) -> Optional[str]:
        """Add frontmatter to existing README if missing."""
        readme_path = self.project_path / 'README.md'
        content = readme_path.read_text()

        if content.startswith('---'):
            return None  # Already has frontmatter

        human_name = self.project_name.replace('_', ' ').title()
        frontmatter = f"""---
project: {self.project_name}
name: {human_name}
series: {self.series}
type: {self.analysis['project_type']}
status: {status}
last_updated: {datetime.now().strftime('%Y-%m-%d')}
primary_maintainer: jeremybradford
purpose: >
  [TODO: Add one-line purpose from existing content]
tech_stack:
  - {', '.join(self.analysis['tech_stack']) if self.analysis['tech_stack'] else 'python'}
key_dependencies: []
deployment: local
integration_points: {{}}
---

"""
        return frontmatter + content

    def _generate_claude_md(self) -> str:
        """Generate CLAUDE.md file."""
        return f"""# CLAUDE.md

Project-specific guidance for Claude when working on {self.project_name}.

## Project Context

This project is part of the Betty Protocol ecosystem in the SyncedProjects workspace.
- **Series**: {self.series}-series
- **Type**: {self.analysis['project_type']}
- **Status**: Active development

## Key Files and Directories

- `40_src/` - Main source code
- `30_config/` - Configuration files
- `20_receipts/` - Change evidence and receipts
- `70_evidence/` - Test outputs and artifacts

## Development Workflow

1. Always read existing code before proposing changes
2. Create receipts in `20_receipts/` for significant changes
3. Run health checks before declaring work complete
4. Update README.md when behavior changes

## Forbidden Actions

**NEVER:**
- Force push to git
- Delete git history
- Remove evidence/receipts
- Commit sensitive data (API keys, passwords)
- Auto-commit without explicit user request
- Create files unless necessary
- Make changes outside project scope

## Testing

Run tests with:
```bash
make test
```

## Dependencies

{chr(10).join(['- ' + dep for dep in self.analysis['tech_stack']])}
"""

    def _generate_why_i_care(self) -> str:
        """Generate WHY_I_CARE.md file."""
        return f"""# WHY I CARE

## Personal Significance

This project matters because [TODO: Add personal motivation].

## Problem It Solves

[TODO: Describe the problem this project addresses]

## Future Vision

[TODO: Where this project is heading]

## Success Metrics

- [ ] [TODO: Add success criteria]
- [ ] [TODO: Add measurable outcomes]

## Related Projects

- [TODO: Link to related projects in workspace]
"""

    def _generate_relations(self) -> str:
        """Generate RELATIONS.yaml file."""
        return f"""# Project relationships and dependencies

project: {self.project_name}
series: {self.series}
type: {self.analysis['project_type']}

dependencies:
  runtime: []
  development: []

integrations:
  upstream: []  # Projects that feed data to this one
  downstream: []  # Projects that consume this project's output

related:
  similar: []  # Similar projects in workspace
  alternatives: []  # Alternative approaches

ports: []  # If service, list ports used

apis:
  provides: []  # APIs this project exposes
  consumes: []  # APIs this project uses
"""

    def _generate_rules_now(self) -> str:
        """Generate rules_now.md file."""
        return f"""# RULES NOW

Current operational rules for {self.project_name}.

## Active Rules

1. **Evidence First** - All changes must produce evidence in `20_receipts/`
2. **Test Before Done** - Run `make health` before declaring complete
3. **No Self-Certification** - Work is pending until human approval
4. **Clean Commits** - One logical change per commit
5. **Document Changes** - Update README when behavior changes

## Development Constraints

- [ ] Virtual environment must be active for Python work
- [ ] Dependencies must be in requirements.txt or package.json
- [ ] Secrets must use credential vault (C001_mission-control)
- [ ] Large files (>10MB) must be in .gitignore
- [ ] Data files go in `$SADB_DATA_DIR` not in repo

## Current Focus

[TODO: Add current development priorities]

## Blockers

[TODO: List any current blockers]
"""

    def _generate_gitignore(self) -> str:
        """Generate .gitignore file."""
        base = """.DS_Store
.env
.venv/
venv/
*-env/
node_modules/
*.pyc
__pycache__/
*.log
*.pid
data/
chroma_data/
*.db
*.sqlite
tmp/
temp/
"""
        # Add tech-specific ignores
        if 'node.js' in self.analysis['tech_stack']:
            base += "\nnpm-debug.log*\nyarn-error.log*\n.npm/\n"
        if 'python' in self.analysis['tech_stack']:
            base += "\n*.egg-info/\ndist/\nbuild/\n.pytest_cache/\n"
        return base

    def _generate_kst_status(self, kst_dir: Path, status: str):
        """Generate .kst/status.json file."""
        status_data = {
            "project": self.project_name,
            "series": self.series,
            "status": status,
            "last_updated": datetime.now().isoformat(),
            "health_check_command": "make health",
            "betty_protocol_compliant": True,
            "standardization_date": datetime.now().strftime('%Y-%m-%d')
        }

        with open(kst_dir / 'status.json', 'w') as f:
            json.dump(status_data, f, indent=2)

    def _create_receipt(self, actions: List[str]):
        """Create standardization receipt."""
        receipt_dir = self.project_path / '20_receipts'
        receipt_dir.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        receipt_file = receipt_dir / f"betty_standardization_{timestamp}.md"

        content = f"""# Betty Protocol Standardization Receipt

**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Project**: {self.project_name}
**Executed By**: standardize_betty_protocol.py

## Actions Performed

{chr(10).join(['- ' + action for action in actions])}

## Compliance Status

- Betty Protocol Files: {len(self.analysis['existing_files'])} existing, {len(actions)} created
- Betty Protocol Directories: All required directories present
- Standardization: COMPLETE

## Next Steps

1. Review generated files and customize placeholders
2. Run `make health` to verify health check
3. Commit changes with message: "Apply Betty Protocol standardization [{self.project_id}]"
"""
        receipt_file.write_text(content)


def main():
    parser = argparse.ArgumentParser(description='Standardize projects to Betty Protocol')
    parser.add_argument('project', help='Project path or name')
    parser.add_argument('--series', default='P', choices=['P', 'C', 'W', 'T'],
                       help='Project series (default: P)')
    parser.add_argument('--status', default='active',
                       choices=['experimental', 'active', 'paused', 'archived', 'legacy'],
                       help='Project status (default: active)')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be done without making changes')
    parser.add_argument('--batch', help='Process multiple projects from file')

    args = parser.parse_args()

    if args.batch:
        # Process multiple projects
        with open(args.batch) as f:
            projects = [line.strip() for line in f if line.strip()]
        for project in projects:
            process_project(project, args)
    else:
        process_project(args.project, args)


def process_project(project_name: str, args):
    """Process a single project."""
    # Handle relative or absolute paths
    if os.path.isabs(project_name):
        project_path = Path(project_name)
    else:
        # Assume it's in SyncedProjects
        workspace = Path.home() / 'SyncedProjects'
        if (workspace / project_name).exists():
            project_path = workspace / project_name
        else:
            # Try to find by pattern
            matches = list(workspace.glob(f"*{project_name}*"))
            if not matches:
                print(f"Project not found: {project_name}")
                return
            project_path = matches[0]

    if not project_path.exists():
        print(f"Project path does not exist: {project_path}")
        return

    print(f"\nAnalyzing {project_path.name}...")

    # Analyze project
    analyzer = ProjectAnalyzer(project_path)
    analysis = analyzer.analyze()

    print(f"  - Existing files: {len(analysis['existing_files'])}")
    print(f"  - Missing files: {len(analysis['missing_files'])}")
    print(f"  - Tech stack: {', '.join(analysis['tech_stack']) or 'Unknown'}")

    # Generate Betty Protocol structure
    generator = BettyProtocolGenerator(project_path, analysis)
    actions = generator.standardize(status=args.status, dry_run=args.dry_run)

    if args.dry_run:
        print(f"\n  Would perform {len(actions)} actions:")
        for action in actions:
            print(f"    - {action}")
    else:
        print(f"\n  Performed {len(actions)} actions")
        for action in actions:
            print(f"    - {action}")

    print(f"\n{'  Dry run complete' if args.dry_run else '  Standardization complete!'}")


if __name__ == '__main__':
    main()
