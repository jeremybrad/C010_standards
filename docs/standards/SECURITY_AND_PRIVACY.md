# C010_standards Security & Privacy

**Last Updated**: 2026-01-12
**Version**: 1.0.0

Security model and data protection for C010_standards.

## Security Principles

1. **No Secrets Stored** - Standards repo contains no credentials or sensitive data
2. **Public by Design** - All protocols and schemas are meant to be shared
3. **Audit Trail** - All changes documented in receipts
4. **Controlled Vocabularies** - Taxonomies prevent ambiguity and injection
5. **Validation Before Trust** - Houston validators enforce compliance

## Repository Security

### What This Repo Contains

| Content Type | Sensitivity | Notes |
|--------------|-------------|-------|
| Protocols | Public | Governance documentation |
| Schemas | Public | Data contracts |
| Taxonomies | Public | Controlled vocabularies |
| Validators | Public | Python compliance checkers |
| Registry | Internal | Project metadata (no secrets) |
| Configuration | Internal | Feature toggles (no credentials) |

### What This Repo Does NOT Contain

| Content Type | Where It Lives |
|--------------|----------------|
| API keys | C001_mission-control vault |
| Passwords | Never in any repo |
| Personal data | Not stored |
| Private credentials | Environment variables only |

## Houston Configuration Security

### Trust Phases

```json
{
  "trust_phases": ["supervised", "advisory", "autonomous"],
  "current_phase": "advisory"
}
```

| Phase | Description | Dangerous Ops |
|-------|-------------|---------------|
| **Supervised** | Human approves all actions | All blocked |
| **Advisory** | Agent suggests, human executes | Most blocked |
| **Autonomous** | Agent executes with limits | Minimal blocking |

### Phase Gates

Operations gated by trust phase:

| Operation | Supervised | Advisory | Autonomous |
|-----------|------------|----------|------------|
| File read | Allowed | Allowed | Allowed |
| File write | Approval | Allowed | Allowed |
| Git commit | Approval | Allowed | Allowed |
| Git push | Blocked | Approval | Allowed |
| Force push | Blocked | Blocked | Approval |
| Delete files | Blocked | Approval | Approval |

### Feature Toggles

```json
{
  "features": {
    "auto_commit": false,
    "auto_push": false,
    "dangerous_operations": {
      "enabled": false
    }
  }
}
```

## Data Privacy

### What Data is Processed

| Data Type | Processing |
|-----------|------------|
| Project metadata | Aggregated in registry |
| Document routing | Classification only |
| Taxonomy terms | Lookup and validation |
| Validation results | Console output only |

### What Data is NOT Collected

- Personal information
- Usage analytics
- Telemetry (beyond local Houston metrics)
- External service calls

## Validation Security

### Validator Behavior

All validators:
- Read configuration files (no network)
- Output to stdout only
- Return exit codes (0/1/2)
- Make no file modifications

### Input Validation

```python
# Validators use safe YAML loading
config = yaml.safe_load(file)  # Not yaml.load()

# JSON schema validation
jsonschema.validate(config, schema)
```

## Threat Model

### Mitigated Threats

| Threat | Mitigation |
|--------|------------|
| Malicious protocol injection | Git history + review |
| Invalid taxonomy terms | Schema validation |
| Configuration tampering | Houston validators |
| Unauthorized standards changes | Protected branches + receipts |
| Schema version confusion | Explicit versioning (v1.2, v1.3) |

### Accepted Risks

| Risk | Acceptance Rationale |
|------|---------------------|
| Standards publicly visible | Intentionally public for transparency |
| Validator bypass | Enforcement at CI/CD level |
| Local config modification | User's machine, user's choice |

### Out of Scope

| Risk | Notes |
|------|-------|
| Code execution vulnerabilities | Validators are read-only |
| Network attacks | No network connections |
| Authentication bypass | No authentication system |

## Security Checklist

### Initial Setup

- [ ] Verify no secrets in commit history
- [ ] Confirm Houston features are conservative
- [ ] Enable protected branches on main

### Ongoing

- [ ] Review protocol changes before merge
- [ ] Validate schema changes against consumers
- [ ] Audit receipts periodically
- [ ] Keep validator dependencies updated

## Incident Response

### Accidental Secret Commit

1. **Immediately**: Remove from HEAD
   ```bash
   git reset HEAD~1
   git push --force-with-lease  # Only if not yet pushed
   ```

2. **If pushed**: Rotate the credential immediately

3. **Document**: Create receipt documenting incident

4. **Prevent**: Add to `.gitignore`

### Invalid Standard Published

1. **Identify**: Which protocol/schema affected
2. **Assess**: Impact on consuming repos
3. **Fix**: Create corrected version
4. **Notify**: Update CHANGELOG with notice
5. **Document**: Receipt with timeline and fix

### Validator Producing False Positives

1. **Verify**: Reproduce the issue
2. **Analyze**: Check validator logic
3. **Fix**: Update validator code
4. **Test**: Verify against known good configs
5. **Document**: Receipt with fix details

## Audit Trail

All changes to standards tracked in:
- Git commit history
- `20_receipts/` directory (148+ entries)
- CHANGELOG.md

Receipt format ensures:
- Date and agent identification
- Summary of changes
- Verification steps
- Cross-references to related work

## Related Documentation

- [ARCHITECTURE.md](ARCHITECTURE.md) - System design
- [OPERATIONS.md](OPERATIONS.md) - Day-to-day operation
- [OPEN_QUESTIONS.md](OPEN_QUESTIONS.md) - Unresolved decisions
