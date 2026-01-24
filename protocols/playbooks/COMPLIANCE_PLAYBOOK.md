# Workspace Compliance Playbook

**Purpose**: Step-by-step procedures for handling compliance violations detected by the nightly automation.

**Related**: See `protocols/betty_protocol.md` for the rules this playbook enforces.

---

## Quick Reference

| Task | Command |
|------|---------|
| View latest compliance report | `cat ~/SyncedProjects/_SharedData/registry/compliance/WORKSPACE_COMPLIANCE_LATEST.md` |
| Run compliance check manually | `cd ~/SyncedProjects/C010_standards && bash scripts/run_workspace_compliance_local.sh` |
| Check launchd status | `launchctl list \| grep c010` |

---

## Weekly Compliance Review (Saturday 10 AM)

A launchd job triggers a reminder every Saturday at 10:00 AM. When you see the notification:

### Step 1: Check the Report

```bash
cat ~/SyncedProjects/_SharedData/registry/compliance/WORKSPACE_COMPLIANCE_LATEST.md
```

Or open in your editor:
```bash
code ~/SyncedProjects/_SharedData/registry/compliance/WORKSPACE_COMPLIANCE_LATEST.md
```

### Step 2: Triage Violations

Look for the **"STOP: Unclassified Violations"** section. For each repo listed:

#### Decision Tree

```
Is this folder/file intentional?
├── YES → Create audit_exceptions.yaml (see below)
└── NO → Fix the violation
    ├── Wrong folder name? → Rename to canonical (git mv)
    ├── Stray folder? → Move to 90_archive/ or delete
    └── Missing required file? → Create it
```

### Step 3: Create Exception File (if needed)

For intentional deviations, create `00_admin/audit_exceptions.yaml`:

```yaml
version: 1
repo: REPO_NAME

owner: "Jeremy (Al) Bradford"
created_at: "YYYY-MM-DD"
review:
  cadence: "quarterly"
  next_review: "YYYY-MM-DD"
  goal: "Brief explanation of why this exception exists"

notes: |
  Longer explanation if needed.

allowed_additional_dirs:
  - folder_name

per_dir:
  folder_name:
    owner: "Al"
    justification: "Why this folder exists"
    planned_destination: "Keep as-is OR future plan"
    review_cadence: "permanent OR quarterly"
```

### Step 4: Commit and Verify

```bash
cd ~/SyncedProjects/REPO_NAME
git add 00_admin/audit_exceptions.yaml
git commit -m "chore: add audit_exceptions.yaml for compliance"

# Re-run compliance to verify
cd ~/SyncedProjects/C010_standards
bash scripts/run_workspace_compliance_local.sh
```

### Step 5: Review Temporary Exceptions

Check repos with **"Temporary Exceptions"** that have missing register entries. These need:
1. Register entry in `C010_standards/registry/repos.yaml`, OR
2. Remediation to remove the exception

---

## Nightly Automation Details

| Job | Schedule | Purpose |
|-----|----------|---------|
| `com.sadb.c010.workspace_compliance` | 3:10 AM daily | Runs folder audit, META drift check, DocMeta validation |
| `com.sadb.c010.compliance_reminder` | 10:00 AM Saturday | Popup reminder to review compliance |

### Output Locations

```
~/SyncedProjects/_SharedData/registry/compliance/
├── WORKSPACE_COMPLIANCE_LATEST.md    # Human-readable summary
├── compliance_delta_latest.md        # Changes since last run
├── compliance_state_latest.json      # Machine-readable state
├── folder_audit_YYYYMMDD.csv         # Daily audit results
├── meta_drift_YYYYMMDD.txt           # META.yaml drift report
├── docmeta_audit_latest.json         # DocMeta validation (advisory)
└── logs/
    ├── compliance_stdout.log         # Script output
    └── compliance_stderr.log         # Errors
```

---

## Troubleshooting

### Launchd job not running

```bash
# Check if loaded
launchctl list | grep c010

# Reload if needed
launchctl unload ~/Library/LaunchAgents/com.sadb.c010.workspace_compliance.plist
launchctl load ~/Library/LaunchAgents/com.sadb.c010.workspace_compliance.plist

# Check for errors
cat ~/SyncedProjects/_SharedData/registry/compliance/logs/compliance_stderr.log
```

### Script failing

```bash
# Run manually to see errors
cd ~/SyncedProjects/C010_standards
bash -x scripts/run_workspace_compliance_local.sh
```

---

## Future Integrations

- **Notion dashboard**: Show repo status and alerts (planned)
- **Mission Control**: Hook compliance state into central dashboard

---

*Last Updated: 2026-01-24*
*Location: C010_standards/protocols/playbooks/COMPLIANCE_PLAYBOOK.md*
