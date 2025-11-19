#!/usr/bin/env python3
"""
Repo Dashboard - Simple local web dashboard for Git repositories
Just run this file - it will open your browser automatically.
"""

import http.server
import json
import os
import socketserver
import subprocess
import webbrowser
from pathlib import Path
from threading import Timer

PORT = 8765
SYNCED_PROJECTS = Path.home() / "SyncedProjects"


def get_repo_status(repo_path):
    """Get status of a single Git repository."""
    try:
        # Check if it's a git repo
        result = subprocess.run(
            ['git', '-C', str(repo_path), 'status'],
            capture_output=True,
            text=True,
            timeout=5
        )

        if result.returncode != 0:
            return None

        # Get current branch
        branch = subprocess.run(
            ['git', '-C', str(repo_path), 'branch', '--show-current'],
            capture_output=True,
            text=True,
            timeout=5
        ).stdout.strip()

        # Get status
        status_output = subprocess.run(
            ['git', '-C', str(repo_path), 'status', '--porcelain'],
            capture_output=True,
            text=True,
            timeout=5
        ).stdout

        # Count changes
        staged = 0
        unstaged = 0
        untracked = 0

        for line in status_output.split('\n'):
            if not line:
                continue
            if line.startswith('??'):
                untracked += 1
            elif line[0] in 'MADRC':
                staged += 1
            if len(line) > 1 and line[1] in 'MADRC':
                unstaged += 1

        # Check ahead/behind
        ahead = 0
        behind = 0
        if branch:
            ab = subprocess.run(
                ['git', '-C', str(repo_path), 'rev-list', '--left-right', '--count', f'HEAD...origin/{branch}'],
                capture_output=True,
                text=True,
                timeout=5
            ).stdout.strip()

            if ab and '\t' in ab:
                ahead_str, behind_str = ab.split('\t')
                ahead = int(ahead_str)
                behind = int(behind_str)

        # Check for Claude branches
        branches = subprocess.run(
            ['git', '-C', str(repo_path), 'branch', '-r'],
            capture_output=True,
            text=True,
            timeout=5
        ).stdout

        claude_branches = [b.strip() for b in branches.split('\n') if 'claude/' in b]

        return {
            'name': repo_path.name,
            'path': str(repo_path),
            'branch': branch or 'DETACHED',
            'staged': staged,
            'unstaged': unstaged,
            'untracked': untracked,
            'ahead': ahead,
            'behind': behind,
            'claude_branches': len(claude_branches),
            'is_clean': (staged + unstaged + untracked == 0),
            'is_synced': (ahead == 0 and behind == 0)
        }
    except Exception as e:
        return None


def scan_repos():
    """Scan all repos in SyncedProjects."""
    repos = []

    if not SYNCED_PROJECTS.exists():
        return repos

    for item in SYNCED_PROJECTS.iterdir():
        if item.is_dir() and (item / '.git').exists():
            status = get_repo_status(item)
            if status:
                repos.append(status)

    return sorted(repos, key=lambda x: x['name'])


# HTML Dashboard (embedded)
HTML = """<!DOCTYPE html>
<html>
<head>
    <title>Git Repo Dashboard</title>
    <meta charset="UTF-8">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: #1a1a1a;
            color: #e0e0e0;
            padding: 20px;
        }
        .header {
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 2px solid #333;
        }
        h1 {
            color: #4a9eff;
            margin-bottom: 10px;
            display: inline-block;
        }
        .header-actions {
            float: right;
            display: flex;
            gap: 15px;
            align-items: center;
        }
        .help-link {
            background: #4a9eff;
            color: white;
            padding: 10px 20px;
            border-radius: 6px;
            text-decoration: none;
            font-weight: 500;
            transition: all 0.2s;
            cursor: pointer;
            border: none;
            font-size: 14px;
        }
        .help-link:hover {
            background: #3a8eef;
            transform: translateY(-1px);
        }
        .legend {
            background: #2a2a2a;
            border: 1px solid #444;
            border-radius: 8px;
            padding: 20px;
            margin: 20px 0;
        }
        .legend-title {
            color: #4a9eff;
            font-weight: 600;
            margin-bottom: 15px;
            font-size: 16px;
        }
        .legend-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 12px;
        }
        .legend-item {
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .legend-item-desc {
            font-size: 13px;
            color: #ccc;
        }
        .search {
            width: 100%;
            max-width: 400px;
            padding: 12px;
            background: #2a2a2a;
            border: 1px solid #444;
            border-radius: 6px;
            color: #e0e0e0;
            font-size: 16px;
            margin-top: 15px;
        }
        .stats {
            display: flex;
            gap: 20px;
            margin: 15px 0;
            flex-wrap: wrap;
        }
        .stat {
            background: #2a2a2a;
            padding: 15px 20px;
            border-radius: 8px;
            border: 1px solid #333;
        }
        .stat-value { font-size: 24px; font-weight: bold; color: #4a9eff; }
        .stat-label { font-size: 12px; color: #999; margin-top: 5px; }
        .repo-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 20px;
        }
        .repo {
            background: #2a2a2a;
            border: 1px solid #333;
            border-radius: 8px;
            padding: 20px;
            transition: all 0.2s;
        }
        .repo:hover {
            border-color: #4a9eff;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(74, 158, 255, 0.2);
        }
        .repo-name {
            font-size: 18px;
            font-weight: 600;
            color: #4a9eff;
            margin-bottom: 12px;
        }
        .repo-branch {
            font-size: 14px;
            color: #999;
            margin-bottom: 15px;
            font-family: 'Monaco', monospace;
        }
        .indicators {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }
        .indicator {
            padding: 6px 12px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: 500;
        }
        .clean { background: #1a4d2e; color: #4ade80; }
        .modified { background: #4d3800; color: #fbbf24; }
        .ahead { background: #4d3800; color: #fbbf24; }
        .behind { background: #4d1a1a; color: #f87171; }
        .claude { background: #4d1a4d; color: #c084fc; }
        .auto-refresh {
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: #2a2a2a;
            border: 1px solid #333;
            padding: 10px 15px;
            border-radius: 6px;
            font-size: 12px;
            color: #999;
        }

        .help-overlay {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.9);
            z-index: 1000;
            overflow-y: auto;
            padding: 40px 20px;
        }
        .help-content {
            max-width: 800px;
            margin: 0 auto;
            background: #2a2a2a;
            border: 1px solid #444;
            border-radius: 12px;
            padding: 40px;
        }
        .help-content h2 {
            color: #4a9eff;
            margin: 30px 0 15px 0;
            font-size: 24px;
        }
        .help-content h2:first-child { margin-top: 0; }
        .help-content h3 {
            color: #4a9eff;
            margin: 20px 0 10px 0;
            font-size: 18px;
        }
        .help-content p, .help-content li {
            line-height: 1.6;
            margin-bottom: 10px;
        }
        .help-example {
            background: #1a1a1a;
            border-left: 3px solid #4a9eff;
            padding: 15px;
            margin: 15px 0;
            border-radius: 4px;
        }
        .help-indicator {
            display: inline-block;
            padding: 4px 10px;
            border-radius: 4px;
            margin: 5px 5px 5px 0;
            font-size: 13px;
            font-weight: 500;
        }
        .close-help {
            float: right;
            background: none;
            border: none;
            color: #999;
            font-size: 32px;
            cursor: pointer;
            line-height: 1;
        }
        .close-help:hover { color: #fff; }
        code {
            background: #1a1a1a;
            padding: 2px 6px;
            border-radius: 3px;
            color: #4a9eff;
            font-family: 'Monaco', monospace;
            font-size: 13px;
        }
    </style>
</head>
<body>
    <div class="help-overlay" id="helpOverlay" onclick="if(event.target === this) toggleHelp()">
        <div class="help-content">
            <button class="close-help" onclick="toggleHelp()">×</button>
            <h2>How This Dashboard Works</h2>
            <p>This dashboard shows the status of all your Git repositories in <code>~/SyncedProjects/</code>. The goal is to get them all <span class="help-indicator clean">✓ Clean</span>!</p>

            <h2>Status Indicators Explained</h2>

            <h3><span class="help-indicator clean">✓ Clean</span></h3>
            <p><strong>What it means:</strong> This repo is perfect! No uncommitted changes, nothing to push or pull, no Claude Code branches waiting.</p>
            <p><strong>What to do:</strong> Nothing! It's good.</p>

            <h3><span class="help-indicator modified">M 6 files</span> (Yellow)</h3>
            <p><strong>What it means:</strong> You have 6 files with uncommitted changes (either staged, modified, or untracked).</p>
            <p><strong>What to do:</strong></p>
            <div class="help-example">
                <code>cd ~/SyncedProjects/REPO_NAME</code><br>
                <code>git status</code> &nbsp;&nbsp;# See what changed<br>
                <code>git add .</code> &nbsp;&nbsp;# Stage everything<br>
                <code>git commit -m "Save my work"</code><br>
                <code>git push</code>
            </div>

            <h3><span class="help-indicator ahead">↑ 1 ahead</span> (Yellow)</h3>
            <p><strong>What it means:</strong> You have 1 commit on your computer that's not on GitHub yet.</p>
            <p><strong>What to do:</strong></p>
            <div class="help-example">
                <code>cd ~/SyncedProjects/REPO_NAME</code><br>
                <code>git push</code>
            </div>

            <h3><span class="help-indicator behind">↓ 2 behind</span> (Red)</h3>
            <p><strong>What it means:</strong> GitHub has 2 commits you don't have locally yet.</p>
            <p><strong>What to do:</strong></p>
            <div class="help-example">
                <code>cd ~/SyncedProjects/REPO_NAME</code><br>
                <code>git pull</code>
            </div>

            <h3><span class="help-indicator claude">C 2 branches</span> (Purple)</h3>
            <p><strong>What it means:</strong> Claude Code created 2 branches on GitHub that you haven't merged yet.</p>
            <p><strong>What to do:</strong></p>
            <div class="help-example">
                1. Go to GitHub: <code>https://github.com/YOUR_USERNAME/REPO_NAME</code><br>
                2. Find the Claude branches (they start with <code>claude/</code>)<br>
                3. Either merge them if you want the work, or delete them if you don't need them anymore
            </div>

            <h2>Quick Clean-Up Steps</h2>

            <h3>Goal: Make Everything <span class="help-indicator clean">✓ Clean</span></h3>

            <p><strong>Step 1:</strong> For each repo with <span class="help-indicator modified">M</span>, commit your changes:</p>
            <div class="help-example">
                <code>cd ~/SyncedProjects/REPO_NAME</code><br>
                <code>git add .</code><br>
                <code>git commit -m "Describe what you changed"</code>
            </div>

            <p><strong>Step 2:</strong> For each repo with <span class="help-indicator ahead">↑</span>, push to GitHub:</p>
            <div class="help-example">
                <code>git push</code>
            </div>

            <p><strong>Step 3:</strong> For each repo with <span class="help-indicator behind">↓</span>, pull from GitHub:</p>
            <div class="help-example">
                <code>git pull</code>
            </div>

            <p><strong>Step 4:</strong> For repos with <span class="help-indicator claude">C</span>, decide what to do with those branches on GitHub (merge or delete).</p>

            <h2>Tips</h2>
            <ul>
                <li>The dashboard auto-refreshes every 30 seconds</li>
                <li>Use the search box to find specific repos</li>
                <li>The stats at the top show your overall progress</li>
                <li>Focus on one repo at a time - don't try to fix everything at once!</li>
            </ul>
        </div>
    </div>

    <div class="header">
        <h1>📊 Git Repository Dashboard</h1>
        <div class="header-actions">
            <button class="help-link" onclick="toggleHelp()">📖 How to Use This Dashboard</button>
        </div>
        <div style="clear: both;"></div>

        <div class="legend">
            <div class="legend-title">🎨 Status Colors & What They Mean</div>
            <div class="legend-grid">
                <div class="legend-item">
                    <span class="indicator clean">✓ Clean</span>
                    <span class="legend-item-desc">Perfect! Nothing to do</span>
                </div>
                <div class="legend-item">
                    <span class="indicator modified">M 6 files</span>
                    <span class="legend-item-desc">Yellow: Uncommitted changes</span>
                </div>
                <div class="legend-item">
                    <span class="indicator ahead">↑ 2 ahead</span>
                    <span class="legend-item-desc">Yellow: Need to push</span>
                </div>
                <div class="legend-item">
                    <span class="indicator behind">↓ 1 behind</span>
                    <span class="legend-item-desc">Red: Need to pull</span>
                </div>
                <div class="legend-item">
                    <span class="indicator claude">C 2 branches</span>
                    <span class="legend-item-desc">Purple: Claude Code branches</span>
                </div>
            </div>
        </div>

        <div class="stats" id="stats"></div>
        <input type="text" class="search" id="search" placeholder="Search repositories...">
    </div>
    <div class="repo-grid" id="repos"></div>
    <div class="auto-refresh">Auto-refresh: <span id="countdown">30</span>s</div>

    <script>
        let repos = [];
        let countdown = 30;

        function toggleHelp() {
            const overlay = document.getElementById('helpOverlay');
            overlay.style.display = overlay.style.display === 'block' ? 'none' : 'block';
        }

        async function loadRepos() {
            const response = await fetch('/api/repos');
            repos = await response.json();
            renderRepos();
            renderStats();
        }

        function renderStats() {
            const total = repos.length;
            const clean = repos.filter(r => r.is_clean && r.is_synced).length;
            const modified = repos.filter(r => !r.is_clean).length;
            const needsSync = repos.filter(r => !r.is_synced).length;
            const claudeBranches = repos.filter(r => r.claude_branches > 0).length;

            document.getElementById('stats').innerHTML = `
                <div class="stat">
                    <div class="stat-value">${total}</div>
                    <div class="stat-label">Total Repos</div>
                </div>
                <div class="stat">
                    <div class="stat-value">${clean}</div>
                    <div class="stat-label">Clean & Synced</div>
                </div>
                <div class="stat">
                    <div class="stat-value">${modified}</div>
                    <div class="stat-label">Modified</div>
                </div>
                <div class="stat">
                    <div class="stat-value">${needsSync}</div>
                    <div class="stat-label">Need Sync</div>
                </div>
                <div class="stat">
                    <div class="stat-value">${claudeBranches}</div>
                    <div class="stat-label">Claude Branches</div>
                </div>
            `;
        }

        function renderRepos() {
            const search = document.getElementById('search').value.toLowerCase();
            const filtered = repos.filter(r => r.name.toLowerCase().includes(search));

            const html = filtered.map(repo => {
                const indicators = [];

                if (repo.is_clean && repo.is_synced && repo.claude_branches === 0) {
                    indicators.push('<span class="indicator clean">✓ Clean</span>');
                } else {
                    if (!repo.is_clean) {
                        const total = repo.staged + repo.unstaged + repo.untracked;
                        indicators.push(`<span class="indicator modified">M ${total} files</span>`);
                    }
                    if (repo.ahead > 0) {
                        indicators.push(`<span class="indicator ahead">↑ ${repo.ahead} ahead</span>`);
                    }
                    if (repo.behind > 0) {
                        indicators.push(`<span class="indicator behind">↓ ${repo.behind} behind</span>`);
                    }
                    if (repo.claude_branches > 0) {
                        indicators.push(`<span class="indicator claude">C ${repo.claude_branches} branches</span>`);
                    }
                }

                return `
                    <div class="repo">
                        <div class="repo-name">${repo.name}</div>
                        <div class="repo-branch">${repo.branch}</div>
                        <div class="indicators">${indicators.join('')}</div>
                    </div>
                `;
            }).join('');

            document.getElementById('repos').innerHTML = html;
        }

        function updateCountdown() {
            countdown--;
            document.getElementById('countdown').textContent = countdown;

            if (countdown === 0) {
                loadRepos();
                countdown = 30;
            }
        }

        document.getElementById('search').addEventListener('input', renderRepos);

        loadRepos();
        setInterval(updateCountdown, 1000);
        setInterval(loadRepos, 30000);
    </script>
</body>
</html>
"""


class DashboardHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(HTML.encode())
        elif self.path == '/api/repos':
            repos = scan_repos()
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(repos).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        pass  # Suppress log messages


def open_browser():
    """Open browser after a short delay."""
    webbrowser.open(f'http://localhost:{PORT}')


if __name__ == '__main__':
    print(f"\n🚀 Git Repo Dashboard starting...")
    print(f"📊 Scanning: {SYNCED_PROJECTS}")
    print(f"🌐 Opening: http://localhost:{PORT}")
    print(f"\nPress Ctrl+C to stop\n")

    # Open browser after 1 second
    Timer(1.0, open_browser).start()

    # Start server
    with socketserver.TCPServer(("", PORT), DashboardHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n👋 Dashboard stopped")
