#!/usr/bin/env python3
"""
Compliance Delta Detection.

Compares current compliance state with previous state to detect:
- New repos added to workspace
- New violations (repos that became non-compliant)
- Fixed violations (repos that became compliant)
- Removed repos

Usage:
    python3 scripts/compliance_delta.py
    python3 scripts/compliance_delta.py --output delta_report.md
    python3 scripts/compliance_delta.py --dry-run

Exit codes:
    0 = No new violations
    1 = New violations detected (or errors)
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# State file location - stable paths for Mission Control consumption
STATE_DIR = Path('~/SyncedProjects/_SharedData/registry/compliance').expanduser()
STATE_FILE = STATE_DIR / 'compliance_state_latest.json'
WORKSPACE = Path('~/SyncedProjects').expanduser()


def load_previous_state() -> Dict:
    """Load the previous compliance state from file."""
    if not STATE_FILE.exists():
        return {'repos': {}, 'metadata': {'version': '1.0'}}

    with open(STATE_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_state(state: Dict) -> None:
    """Save compliance state to file."""
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    state['metadata']['last_updated'] = datetime.now().isoformat()

    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(state, f, indent=2, ensure_ascii=False)


def get_current_repos() -> Dict[str, Dict]:
    """Scan workspace for current P/C/W repos and their compliance status."""
    repos = {}

    for entry in WORKSPACE.iterdir():
        if not entry.is_dir():
            continue

        # Match P###_, C###_, W###_ pattern
        name = entry.name
        if len(name) < 5 or name[0] not in 'PCW':
            continue
        if not name[1:4].isdigit() or name[4] != '_':
            continue

        project_id = name[:4]  # e.g., C012

        repos[project_id] = {
            'name': name,
            'path': str(entry),
            'has_meta_yaml': (entry / 'META.yaml').exists(),
            'has_readme': (entry / 'README.md').exists(),
            'has_claude_md': (entry / 'CLAUDE.md').exists(),
            'has_00_run': (entry / '00_run').is_dir() if name[0] in 'CW' else True,  # Only required for C/W
            'last_checked': datetime.now().isoformat(),
        }

        # Determine compliance status
        # PASS = has META.yaml + README + (00_run if C/W series)
        # WARN = missing optional files
        # FAIL = missing required files
        issues = []
        if not repos[project_id]['has_meta_yaml']:
            issues.append('missing_meta_yaml')
        if not repos[project_id]['has_readme']:
            issues.append('missing_readme')
        if name[0] in 'CW' and not repos[project_id]['has_00_run']:
            issues.append('missing_00_run')

        if issues:
            repos[project_id]['status'] = 'FAIL'
            repos[project_id]['issues'] = issues
        elif not repos[project_id]['has_claude_md']:
            repos[project_id]['status'] = 'WARN'
            repos[project_id]['issues'] = ['missing_claude_md']
        else:
            repos[project_id]['status'] = 'PASS'
            repos[project_id]['issues'] = []

    return repos


def compute_delta(previous: Dict, current: Dict) -> Dict:
    """Compute the delta between two compliance states."""
    prev_repos = set(previous.get('repos', {}).keys())
    curr_repos = set(current.keys())

    delta = {
        'new_repos': [],
        'removed_repos': [],
        'newly_violated': [],
        'newly_compliant': [],
        'status_changes': [],
    }

    # New repos
    for repo_id in curr_repos - prev_repos:
        repo = current[repo_id]
        delta['new_repos'].append({
            'id': repo_id,
            'name': repo['name'],
            'status': repo['status'],
            'issues': repo.get('issues', []),
        })

    # Removed repos
    for repo_id in prev_repos - curr_repos:
        prev_repo = previous['repos'][repo_id]
        delta['removed_repos'].append({
            'id': repo_id,
            'name': prev_repo.get('name', repo_id),
        })

    # Status changes for existing repos
    for repo_id in prev_repos & curr_repos:
        prev_status = previous['repos'][repo_id].get('status', 'UNKNOWN')
        curr_status = current[repo_id]['status']

        if prev_status != curr_status:
            change = {
                'id': repo_id,
                'name': current[repo_id]['name'],
                'old_status': prev_status,
                'new_status': curr_status,
                'issues': current[repo_id].get('issues', []),
            }
            delta['status_changes'].append(change)

            # Categorize the change
            if curr_status == 'FAIL' and prev_status in ('PASS', 'WARN'):
                delta['newly_violated'].append(change)
            elif curr_status == 'PASS' and prev_status in ('FAIL', 'WARN'):
                delta['newly_compliant'].append(change)

    return delta


def generate_delta_report(delta: Dict, current: Dict) -> str:
    """Generate a markdown report from the delta."""
    lines = [
        '# Nightly Compliance Delta Report',
        '',
        f'**Generated**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',
        '',
    ]

    # Summary counts
    total_repos = len(current)
    pass_count = sum(1 for r in current.values() if r['status'] == 'PASS')
    warn_count = sum(1 for r in current.values() if r['status'] == 'WARN')
    fail_count = sum(1 for r in current.values() if r['status'] == 'FAIL')

    lines.extend([
        '## Summary',
        '',
        f'- **Total Repos**: {total_repos}',
        f'- **PASS**: {pass_count} ({100*pass_count//total_repos}%)',
        f'- **WARN**: {warn_count}',
        f'- **FAIL**: {fail_count}',
        '',
    ])

    # New repos
    if delta['new_repos']:
        lines.append(f"## New Repos Detected ({len(delta['new_repos'])})")
        lines.append('')
        for repo in delta['new_repos']:
            status_emoji = {'PASS': '✅', 'WARN': '⚠️', 'FAIL': '❌'}.get(repo['status'], '❓')
            lines.append(f"- {status_emoji} **{repo['name']}** ({repo['status']})")
            if repo['issues']:
                lines.append(f"  - Issues: {', '.join(repo['issues'])}")
        lines.append('')

    # New violations (ALERT!)
    if delta['newly_violated']:
        lines.append(f"## 🚨 New Violations ({len(delta['newly_violated'])})")
        lines.append('')
        for repo in delta['newly_violated']:
            lines.append(f"- **{repo['name']}**: {repo['old_status']} → {repo['new_status']}")
            if repo['issues']:
                lines.append(f"  - Issues: {', '.join(repo['issues'])}")
        lines.append('')

    # Fixed violations
    if delta['newly_compliant']:
        lines.append(f"## ✅ Fixed ({len(delta['newly_compliant'])})")
        lines.append('')
        for repo in delta['newly_compliant']:
            lines.append(f"- **{repo['name']}**: {repo['old_status']} → {repo['new_status']}")
        lines.append('')

    # Removed repos
    if delta['removed_repos']:
        lines.append(f"## Removed Repos ({len(delta['removed_repos'])})")
        lines.append('')
        for repo in delta['removed_repos']:
            lines.append(f"- {repo['name']}")
        lines.append('')

    # All status changes
    other_changes = [c for c in delta['status_changes']
                     if c not in delta['newly_violated'] and c not in delta['newly_compliant']]
    if other_changes:
        lines.append(f"## Other Status Changes ({len(other_changes)})")
        lines.append('')
        for change in other_changes:
            lines.append(f"- **{change['name']}**: {change['old_status']} → {change['new_status']}")
        lines.append('')

    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='Detect compliance changes between runs')
    parser.add_argument('--output', '-o', help='Output file for delta report (markdown)')
    parser.add_argument('--dry-run', action='store_true', help='Do not update state file')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')

    args = parser.parse_args()

    # Load previous state
    previous = load_previous_state()

    # Get current state
    current = get_current_repos()

    # Compute delta
    delta = compute_delta(previous, current)

    # Generate report
    report = generate_delta_report(delta, current)

    # Output report
    if args.output:
        output_path = Path(args.output)
        output_path.write_text(report, encoding='utf-8')
        print(f"Delta report written to: {args.output}")

    if args.verbose or not args.output:
        print(report)

    # Save new state (unless dry run)
    if not args.dry_run:
        new_state = {
            'metadata': {
                'version': '1.0',
                'last_updated': datetime.now().isoformat(),
                'generator': 'compliance_delta.py',
            },
            'repos': current,
            'summary': {
                'total': len(current),
                'pass': sum(1 for r in current.values() if r['status'] == 'PASS'),
                'warn': sum(1 for r in current.values() if r['status'] == 'WARN'),
                'fail': sum(1 for r in current.values() if r['status'] == 'FAIL'),
            }
        }
        save_state(new_state)
        if args.verbose:
            print(f"\nState saved to: {STATE_FILE}")

    # Set GHA output for workflow integration
    has_new_violations = len(delta['newly_violated']) > 0 or any(
        r['status'] == 'FAIL' for r in delta['new_repos']
    )

    # Write to GITHUB_OUTPUT if available
    github_output = os.environ.get('GITHUB_OUTPUT')
    if github_output:
        with open(github_output, 'a') as f:
            f.write(f"has_new_violations={'true' if has_new_violations else 'false'}\n")
            f.write(f"new_repo_count={len(delta['new_repos'])}\n")
            f.write(f"violation_count={len(delta['newly_violated'])}\n")

    # Exit with code 1 if new violations
    if has_new_violations:
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
