# Comprehensive Repo Modernization PR Template

## What This PR Does

Modernizes `[REPO_NAME]` to follow all C010_standards + Betty Protocol requirements, plus adds modern DevOps practices for health monitoring, automation, and team onboarding.

---

## Files to Create

### 1. WHY_I_CARE.md (Personal Relationship File)
```markdown
# Why [REPO_NAME] Matters

## The Problem It Solves
[What pain point does this address?]

## Why I Care
[Personal connection - why does this matter to you?]

## What Success Looks Like
[When is this project "done" or successful?]

## My Relationship to This Project
- **Started:** [Date/context]
- **Current Status:** [Active development / Maintenance / Experimental]
- **Time Investment:** [How much time do you spend on this?]
- **Emotional Investment:** [High/Medium/Low and why]

## Long-term Vision
[Where should this go in 6 months? 1 year? 5 years?]

## What Would Make Me Abandon This
[Under what conditions would you stop maintaining this?]
```

### 2. ROADMAP.md
```markdown
# [REPO_NAME] Roadmap

## Current Status
**Phase:** [Discovery / Development / Production / Maintenance]
**Version:** [If applicable]
**Last Major Update:** [Date]

## Completed Milestones
- ✅ [Milestone 1] - [Date]
- ✅ [Milestone 2] - [Date]

## Active Work (This Month)
- 🔄 [Current focus]
- 🔄 [Current priority]

## Next Up (Next 3 Months)
- 📋 [Planned feature/improvement]
- 📋 [Tech debt to address]

## Future Vision (6-12 Months)
- 💭 [Aspirational goal]
- 💭 [Integration opportunity]

## Known Issues / Tech Debt
- ⚠️ [Issue 1]
- ⚠️ [Issue 2]

## Blocked / On Hold
- 🚫 [What's blocked and why]

## Dependencies / Prerequisites
- [ ] [What needs to happen first]
```

### 3. RELATIONS.yaml (Ecosystem Connections)
```yaml
project:
  name: "[REPO_NAME]"
  type: "[Core Infrastructure / Memory System / Application / Analytics / Work Tool]"
  status: "[Active / Prototype / Archived / Deprecated]"

# Connection to SADB (truth source)
sadb_integration:
  reads_from: "[Path in SADB_DATA or 'none']"
  writes_to: "[Path in SADB_DATA or 'none']"
  depends_on_sadb: [true/false]

# Project dependencies
depends_on:
  - project: "C003_sadb_canonical"
    why: "Knowledge extraction and refinement pipeline"
  - project: "C001_mission-control"
    why: "Credentials and secrets management"
  # Add more as needed

# Projects that depend on this
used_by:
  - project: "[PROJECT_CODE]"
    how: "[Brief description]"
  # Add more as needed

# External services
external_dependencies:
  apis:
    - name: "[API name]"
      url: "[URL]"
      auth: "[How authenticated]"
  databases:
    - type: "[postgres/sqlite/chromadb/etc]"
      location: "[Path or connection string]"
  services:
    - name: "[Docker service / background process]"
      ports: "[If applicable]"

# Integration points
integrations:
  filesystem:
    reads:
      - "[Path 1]"
      - "[Path 2]"
    writes:
      - "[Path 1]"
    shared:
      - "[Shared location]"
  network:
    exposes:
      - port: [number]
        protocol: "[HTTP/WebSocket/gRPC/etc]"
        purpose: "[What it does]"
    consumes:
      - service: "[Name]"
        endpoint: "[URL/port]"

# Data flow
data_flow:
  inputs:
    - source: "[Where data comes from]"
      format: "[JSON/CSV/JSONL/etc]"
  outputs:
    - destination: "[Where data goes]"
      format: "[Format]"
```

### 4. rules_now.md (Current Project Rules)
```markdown
# Current Rules for [REPO_NAME]

## Active Conventions
1. [Convention 1 - e.g., "All scripts must log to 20_receipts/"]
2. [Convention 2 - e.g., "Use Python 3.11+"]
3. [Convention 3 - e.g., "Branch naming: feat/*, fix/*, chore/*"]

## Data Policies
- [Where data lives]
- [Backup strategy]
- [Retention policy]

## Testing Requirements
- [What must be tested before commit]
- [How to run tests]

## Deployment Process
- [How to deploy/run this project]
- [Prerequisites]
- [Post-deployment verification]

## Breaking Changes Protocol
- [How to handle breaking changes]
- [Who to notify]

## Review & Approval
- [Who reviews PRs]
- [Approval requirements]
```

### 5. CLAUDE.md or AGENTS.md (AI Instructions)
[Only if missing - update if exists]

```markdown
# AI Agent Instructions for [REPO_NAME]

## Project Context
[REPO_NAME] [brief purpose in 1-2 sentences]

## Key Files to Read First
1. WHY_I_CARE.md - Understand Jeremy's relationship to this project
2. ROADMAP.md - Current status and direction
3. RELATIONS.yaml - Dependencies and integrations
4. README.md - Technical overview

## When Working on This Project

### Always Do:
- Read receipts in 20_receipts/ before making changes
- Document decisions in new receipt files
- Update ROADMAP.md if priorities shift
- Check RELATIONS.yaml for dependency impacts

### Never Do:
- Commit data or artifacts to git
- Make changes without receipts
- Break connections defined in RELATIONS.yaml without discussion

### Testing
[How to test changes in this project]

### Tools Available
[List of tools, scripts, or commands available]

## Integration Awareness
This project integrates with:
[List from RELATIONS.yaml with brief notes]

## Current Focus
[From ROADMAP.md - what's the current priority?]
```

### 6. HEALTH.yaml (Health Monitoring Config)
```yaml
# Health monitoring configuration for Mission Control integration

project:
  name: "[REPO_NAME]"
  health_check_enabled: true

# Git health
git:
  alert_on_uncommitted: true
  alert_threshold_days: 7  # Warn if no commits for 7 days
  protected_branches:
    - main
    - production

# Services (if applicable)
services:
  - name: "[Service name]"
    type: "[Docker / systemd / cron / etc]"
    should_be_running: true
    health_endpoint: "[URL for health check or 'none']"
    port: [port number or null]
    restart_command: "[Command to restart]"

# Dependencies
dependencies:
  external:
    - name: "[Dependency name]"
      critical: [true/false]
      check_command: "[Command to verify it's available]"
  internal:
    - project: "[PROJECT_CODE]"
      critical: [true/false]

# Metrics (optional)
metrics:
  collect: [true/false]
  endpoints:
    - url: "[Prometheus/metrics endpoint]"
      interval: "5m"

# Alerts
alerts:
  slack_channel: "#[channel]"
  email: "[email or 'none']"
  on_failure: [true/false]
  on_recovery: [true/false]
```

### 7. .github/workflows/health-check.yml (if repo has CI/CD)
```yaml
name: Health Check

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]
  schedule:
    - cron: '0 2 * * *'  # 2 AM daily

jobs:
  health:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Check repo structure
        run: |
          # Verify required directories
          test -d 00_admin || echo "::warning::Missing 00_admin/"
          test -d 10_docs || echo "::warning::Missing 10_docs/"
          test -d 20_receipts || echo "::warning::Missing 20_receipts/"

      - name: Check required files
        run: |
          test -f README.md || echo "::error::Missing README.md"
          test -f WHY_I_CARE.md || echo "::warning::Missing WHY_I_CARE.md"
          test -f ROADMAP.md || echo "::warning::Missing ROADMAP.md"
          test -f RELATIONS.yaml || echo "::warning::Missing RELATIONS.yaml"

      - name: Report to Mission Control
        if: always()
        run: |
          # POST health status to Mission Control
          # curl -X POST https://mission-control/api/health/report ...
          echo "Health check complete"
```

### 8. 00_admin/SNAPSHOT_[timestamp] (Initial State)
```
=== Snapshot: [REPO_NAME] at [timestamp] ===

Git Status:
[Output of git status]

Directory Tree (4 levels):
[Output of tree -L 4]

README Paths:
[List of all README.md files]

File Counts:
- Total files: [count]
- Python files: [count]
- JavaScript files: [count]
- Markdown files: [count]

Recent Activity:
- Last commit: [date and message]
- Uncommitted changes: [count]
- Branch: [current branch]

Health Status:
- ✅ / ⚠️ / ❌ for each requirement

Next Steps:
[What this PR will address]
```

### 9. 10_docs/ONBOARDING.md (Team Onboarding)
```markdown
# Onboarding: [REPO_NAME]

## Welcome!
[Brief welcome and project purpose]

## Quick Start (5 minutes)
1. Read WHY_I_CARE.md to understand the vision
2. Read README.md for technical setup
3. Check ROADMAP.md to see where we're going

## Setup (15-30 minutes)
\`\`\`bash
# Clone
git clone [repo URL]
cd [REPO_NAME]

# Install dependencies
[Installation commands]

# Run tests
[Test commands]

# Start development
[How to run locally]
\`\`\`

## Architecture Overview
[High-level architecture diagram or description]

## Key Concepts
- **[Concept 1]:** [Explanation]
- **[Concept 2]:** [Explanation]

## Common Tasks
### Adding a feature
1. [Step 1]
2. [Step 2]

### Running tests
\`\`\`bash
[Test command]
\`\`\`

### Deploying
[Deployment process]

## Troubleshooting
### Problem: [Common issue]
**Solution:** [How to fix]

### Problem: [Common issue 2]
**Solution:** [How to fix]

## Getting Help
- Read receipts in 20_receipts/ for recent decisions
- Check RELATIONS.yaml for dependency questions
- Ask [person/team]

## Contributing
1. Create branch: `feat/your-feature` or `fix/your-fix`
2. Make changes with receipts
3. Test thoroughly
4. Submit PR

## Resources
- [Link to relevant docs]
- [Link to related projects]
```

### 10. 10_docs/BettyBeat_INDEX.md (Journal Index)
```markdown
# Betty Beat Journal Index

Private development journal entries are stored in:
`$SADB_DATA_DIR/betty_beat/[REPO_NAME]/YYYY/YYYY-MM-DD.md`

## Recent Entries
- [YYYY-MM-DD] - [Brief summary]
- [YYYY-MM-DD] - [Brief summary]

## Purpose
Betty Beat captures:
- What: Work completed
- Why: Decisions made
- Risks: Identified issues
- Next: Upcoming priorities
- Git Summary: Last commit details

Journal entries are private and not committed to git.
```

---

## Files to Update

### Update README.md
Add sections if missing:
- Prerequisites
- Installation
- Usage
- Configuration
- Testing
- Deployment
- Troubleshooting
- Contributing
- License

Link to new files:
```markdown
## 📚 Documentation
- [Why This Matters](WHY_I_CARE.md) - Project philosophy
- [Roadmap](ROADMAP.md) - Current status and future plans
- [Onboarding](10_docs/ONBOARDING.md) - Get started quickly
- [Relations](RELATIONS.yaml) - Ecosystem connections

## 🤖 For AI Agents
- [CLAUDE.md](CLAUDE.md) - AI collaboration guidelines
```

### Update .gitignore
Ensure it includes Betty Protocol standards:
```gitignore
# OS
.DS_Store

# Virtual environments
.venv/
*-env/
node_modules/

# Data (belongs in $SADB_DATA_DIR)
data/
50_data/
*.ndjson
*.jsonl

# Artifacts
extractions/
tmp/
*.wav

# Logs
pipeline/logs/
api.log
api.pid

# Environment
.env
.env.local

# Build outputs
dist/
build/
*.pyc
__pycache__/

# ChromaDB
chroma_data/
```

---

## Mission Control Integration

### Add health reporting endpoint (if applicable)
Create `health_reporter.py` or similar:
```python
import requests
import yaml

def report_health():
    with open('HEALTH.yaml') as f:
        config = yaml.safe_load(f)

    health_data = {
        'project': config['project']['name'],
        'status': check_status(),
        'timestamp': datetime.now().isoformat()
    }

    # POST to Mission Control
    requests.post(
        'https://mission-control/api/health/report',
        json=health_data
    )
```

---

## Nightly Automation Hooks

### Create .librarian_card (Metadata for automation)
```yaml
project:
  name: "[REPO_NAME]"
  type: "[Core/Personal/Work]"
  language: "[Python/JavaScript/etc]"

status:
  active: [true/false]
  last_scan: "[timestamp]"

health:
  git_clean: [true/false]
  has_uncommitted: [true/false]
  days_since_commit: [number]

structure:
  follows_betty_protocol: [true/false]
  has_required_files: [true/false]
  missing_files: ["list", "of", "missing"]

services:
  running: ["list", "of", "services"]
  ports: [1234, 5678]

alerts:
  loose_files_in_root: [number]
  large_files: ["list", "of", "large", "files"]
  security_issues: ["list", "if", "any"]
```

This file is auto-generated by nightly scans and should be in .gitignore.

---

## Pre-commit Hooks

Ensure `.pre-commit-config.yaml` includes:
```yaml
repos:
  - repo: local
    hooks:
      - id: betty-protocol
        name: Betty Protocol Structure Check
        entry: scripts/check_structure.sh
        language: system
        pass_filenames: false

      - id: no-large-files
        name: Block Large Files
        entry: scripts/check_file_size.sh
        language: system

      - id: no-artifacts
        name: Block Artifacts
        entry: scripts/check_artifacts.sh
        language: system
```

---

## Quality Checks

Before marking this PR complete:
- [ ] All required files created
- [ ] WHY_I_CARE.md reflects Jeremy's true relationship to project
- [ ] ROADMAP.md has realistic milestones
- [ ] RELATIONS.yaml accurately maps dependencies
- [ ] HEALTH.yaml configured for monitoring
- [ ] README.md updated with links to new docs
- [ ] .gitignore follows Betty Protocol
- [ ] Pre-commit hooks configured
- [ ] Snapshot created in 00_admin/
- [ ] ONBOARDING.md tested by reading through it

---

## After Merging

1. Report health to Mission Control: `python health_reporter.py`
2. Create initial Betty Beat entry
3. Verify nightly automation picks up .librarian_card
4. Test pre-commit hooks
5. Share ONBOARDING.md with team (if applicable)

---

## Notes

[Any repo-specific notes or considerations]
