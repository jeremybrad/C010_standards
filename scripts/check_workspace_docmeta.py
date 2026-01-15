#!/usr/bin/env python3
"""
Workspace DocMeta v1.2 Validator.

Validates DocMeta YAML frontmatter headers across all workspace repos.
Runs in advisory mode - reports gaps but doesn't block.

Checks:
- README.md has DocMeta header
- CLAUDE.md has DocMeta header
- 10_docs/*.md files have DocMeta headers
- Topics are valid per taxonomies/topic_taxonomy.yaml

Usage:
    python3 scripts/check_workspace_docmeta.py
    python3 scripts/check_workspace_docmeta.py --repo C012_round-table
    python3 scripts/check_workspace_docmeta.py --series C
    python3 scripts/check_workspace_docmeta.py --output docmeta_report.json

Exit codes:
    0 = Advisory mode (always passes)
    1 = Error loading taxonomy or other fatal error
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False

WORKSPACE = Path('~/SyncedProjects').expanduser()
TAXONOMY_PATH = Path(__file__).parent.parent / 'taxonomies' / 'topic_taxonomy.yaml'

# Files to check in each repo
TARGET_FILES = [
    'README.md',
    'CLAUDE.md',
    'PROJECT_PRIMER.md',
]

# Directories to skip
SKIP_DIRS = {
    'node_modules', '.git', '__pycache__', 'venv', '.venv',
    'dist', 'build', 'vendor', '.claude', '90_archive'
}


def load_valid_topics() -> Set[str]:
    """Load valid topics from taxonomy file."""
    if not HAS_YAML:
        print("Warning: PyYAML not installed, skipping topic validation", file=sys.stderr)
        return set()

    if not TAXONOMY_PATH.exists():
        print(f"Warning: Taxonomy not found at {TAXONOMY_PATH}", file=sys.stderr)
        return set()

    try:
        with open(TAXONOMY_PATH, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)

        # Extract all topic names from taxonomy
        topics = set()
        if isinstance(data, dict):
            # Handle different taxonomy formats
            if 'topics' in data:
                for topic in data['topics']:
                    if isinstance(topic, dict):
                        topics.add(topic.get('name', ''))
                    else:
                        topics.add(str(topic))
            else:
                # Flat list of topics
                for key in data.keys():
                    topics.add(key)

        return {t for t in topics if t}  # Filter empty strings

    except Exception as e:
        print(f"Warning: Error loading taxonomy: {e}", file=sys.stderr)
        return set()


def extract_docmeta(file_path: Path) -> Optional[Dict]:
    """Extract DocMeta YAML frontmatter from a markdown file."""
    if not HAS_YAML:
        return None

    try:
        content = file_path.read_text(encoding='utf-8')
    except Exception as e:
        return None

    # Check for YAML frontmatter (starts with ---)
    if not content.startswith('---'):
        return None

    # Find the closing ---
    end_match = re.search(r'\n---\s*\n', content[3:])
    if not end_match:
        return None

    yaml_content = content[3:end_match.start() + 3]

    try:
        return yaml.safe_load(yaml_content)
    except Exception:
        return None


def check_docmeta(file_path: Path, valid_topics: Set[str]) -> List[Dict]:
    """Check a single file for DocMeta compliance. Returns list of issues."""
    issues = []

    if not file_path.exists():
        return issues  # File doesn't exist, not an issue

    docmeta = extract_docmeta(file_path)

    if docmeta is None:
        issues.append({
            'file': str(file_path),
            'issue': 'missing_docmeta_header',
            'severity': 'advisory',
            'message': 'No DocMeta v1.2 YAML frontmatter found',
        })
        return issues

    # Check for schema version
    schema = docmeta.get('schema', '')
    if not schema.startswith('DocMeta'):
        issues.append({
            'file': str(file_path),
            'issue': 'invalid_schema',
            'severity': 'advisory',
            'message': f"Schema '{schema}' is not DocMeta",
        })

    # Check for required doc fields
    doc = docmeta.get('doc', {})
    if not isinstance(doc, dict):
        issues.append({
            'file': str(file_path),
            'issue': 'missing_doc_block',
            'severity': 'advisory',
            'message': 'No doc: block in frontmatter',
        })
        return issues

    # Check required fields
    required_fields = ['title', 'description', 'type']
    for field in required_fields:
        if not doc.get(field):
            issues.append({
                'file': str(file_path),
                'issue': f'missing_{field}',
                'severity': 'advisory',
                'message': f"Missing required field: doc.{field}",
            })

    # Validate topics against taxonomy
    topics = doc.get('topics', [])
    if topics and valid_topics:
        invalid_topics = [t for t in topics if t not in valid_topics]
        if invalid_topics:
            issues.append({
                'file': str(file_path),
                'issue': 'invalid_topics',
                'severity': 'advisory',
                'message': f"Invalid topics: {', '.join(invalid_topics)}",
                'details': {'invalid': invalid_topics, 'valid_options': list(valid_topics)[:10]},
            })

    return issues


def scan_repo(repo_path: Path, valid_topics: Set[str]) -> List[Dict]:
    """Scan a single repo for DocMeta compliance."""
    all_issues = []

    # Check target files in repo root
    for filename in TARGET_FILES:
        file_path = repo_path / filename
        if file_path.exists():
            issues = check_docmeta(file_path, valid_topics)
            all_issues.extend(issues)

    # Check 10_docs/*.md files
    docs_dir = repo_path / '10_docs'
    if docs_dir.is_dir():
        for md_file in docs_dir.glob('*.md'):
            issues = check_docmeta(md_file, valid_topics)
            all_issues.extend(issues)

    return all_issues


def get_repos(series_filter: Optional[str] = None, repo_filter: Optional[str] = None) -> List[Path]:
    """Get list of repos to scan."""
    repos = []

    for entry in WORKSPACE.iterdir():
        if not entry.is_dir():
            continue

        name = entry.name

        # Match P###_, C###_, W###_ pattern
        if len(name) < 5 or name[0] not in 'PCW':
            continue
        if not name[1:4].isdigit() or name[4] != '_':
            continue

        # Apply filters
        if series_filter and name[0] != series_filter.upper():
            continue
        if repo_filter and name != repo_filter:
            continue

        repos.append(entry)

    return sorted(repos)


def main():
    parser = argparse.ArgumentParser(description='Validate DocMeta headers across workspace')
    parser.add_argument('--repo', help='Scan specific repo only')
    parser.add_argument('--series', choices=['C', 'P', 'W'], help='Filter by series')
    parser.add_argument('--output', '-o', help='Output file (JSON format)')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')

    args = parser.parse_args()

    if not HAS_YAML:
        print("Warning: PyYAML not installed. Install with: pip install pyyaml", file=sys.stderr)

    # Load valid topics
    valid_topics = load_valid_topics()
    if args.verbose and valid_topics:
        print(f"Loaded {len(valid_topics)} valid topics from taxonomy")

    # Get repos to scan
    repos = get_repos(args.series, args.repo)
    if not repos:
        print("No repos found to scan", file=sys.stderr)
        return 1

    # Scan all repos
    all_results = {}
    total_issues = 0

    for repo in repos:
        issues = scan_repo(repo, valid_topics)
        if issues:
            all_results[repo.name] = issues
            total_issues += len(issues)

    # Output results
    if args.output:
        output_data = {
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'repos_scanned': len(repos),
                'total_issues': total_issues,
            },
            'results': all_results,
        }
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        print(f"Results written to: {args.output}")

    # Print summary
    print(f"\nDocMeta Validation Report - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)

    if all_results:
        for repo_name, issues in sorted(all_results.items()):
            print(f"\n{repo_name}:")
            for issue in issues:
                file_rel = Path(issue['file']).name
                print(f"  - [{issue['severity'].upper()}] {file_rel}: {issue['message']}")

        print(f"\n{'=' * 60}")
        print(f"SUMMARY: {len(all_results)} repos with {total_issues} issues (advisory)")
    else:
        print(f"\nAll {len(repos)} repos have valid DocMeta headers!")

    # Advisory mode - always return 0
    return 0


if __name__ == '__main__':
    sys.exit(main())
