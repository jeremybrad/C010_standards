# Workspace Compliance Launchd Agent Setup

**Date**: 2026-01-15
**Agent**: Claude Opus 4.5

## Summary

Configured macOS launchd agent to run nightly workspace compliance checks at 03:10 local time.

## Plist Location

```
~/Library/LaunchAgents/com.sadb.c010.workspace_compliance.plist
```

## Plist Contents

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.sadb.c010.workspace_compliance</string>

    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>/Users/jeremybradford/SyncedProjects/C010_standards/scripts/run_workspace_compliance_local.sh</string>
    </array>

    <key>WorkingDirectory</key>
    <string>/Users/jeremybradford/SyncedProjects/C010_standards</string>

    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin</string>
        <key>HOME</key>
        <string>/Users/jeremybradford</string>
    </dict>

    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>3</integer>
        <key>Minute</key>
        <integer>10</integer>
    </dict>

    <key>StandardOutPath</key>
    <string>/Users/jeremybradford/SyncedProjects/_SharedData/registry/compliance/logs/compliance_stdout.log</string>

    <key>StandardErrorPath</key>
    <string>/Users/jeremybradford/SyncedProjects/_SharedData/registry/compliance/logs/compliance_stderr.log</string>

    <key>RunAtLoad</key>
    <false/>
</dict>
</plist>
```

## Load Commands

```bash
# Bootstrap agent for current GUI user
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.sadb.c010.workspace_compliance.plist

# Verify agent is loaded
launchctl print gui/$(id -u)/com.sadb.c010.workspace_compliance

# Manual kickstart (run immediately)
launchctl kickstart gui/$(id -u)/com.sadb.c010.workspace_compliance

# Unload if needed
launchctl bootout gui/$(id -u)/com.sadb.c010.workspace_compliance
```

## Output Paths

All compliance outputs written to stable paths for Mission Control consumption:

```
~/SyncedProjects/_SharedData/registry/compliance/
├── compliance_state_latest.json    # Current state for delta detection
├── compliance_delta_latest.md      # What changed since last run
├── docmeta_audit_latest.json       # DocMeta validation results
├── WORKSPACE_COMPLIANCE_LATEST.md  # Human-readable report
├── folder_audit_YYYYMMDD.csv       # Raw folder audit data
├── meta_drift_YYYYMMDD.txt         # META.yaml drift report
└── logs/
    ├── compliance_stdout.log       # Run output
    └── compliance_stderr.log       # Error output
```

## Verification

Kickstart executed at 2026-01-15 16:00:50. Files updated:

| File | Timestamp |
|------|-----------|
| compliance_state_latest.json | 2026-01-15 16:00 |
| compliance_delta_latest.md | 2026-01-15 16:00 |
| docmeta_audit_latest.json | 2026-01-15 16:00 |
| WORKSPACE_COMPLIANCE_LATEST.md | 2026-01-15 16:00 |

stdout log excerpt:
```
═══════════════════════════════════════════════════
  Local Workspace Compliance Audit
  2026-01-15 16:00:50
═══════════════════════════════════════════════════

Output: /Users/jeremybradford/SyncedProjects/_SharedData/registry/compliance

1/5 Running folder structure audit...
    ⚠️  Audit script had errors
2/5 Rendering compliance report...
    ⚠️  Report renderer had errors
3/5 Running META.yaml drift check...
    ⚠️  109 drift issues found
4/5 Running DocMeta validation (advisory)...
    ⚠️  350 advisory issues
5/5 Running compliance delta detection...
    ✅ No new violations

═══════════════════════════════════════════════════
  Complete (2 errors)
═══════════════════════════════════════════════════
```

## Schedule

- **Time**: 03:10 local time daily
- **RunAtLoad**: false (only runs on schedule, not at login)

## Notes

- Some sub-scripts (folder audit, report renderer) have path/dependency issues to resolve
- Delta detection and DocMeta validation running correctly
- Mission Control can read stable output files at any time
