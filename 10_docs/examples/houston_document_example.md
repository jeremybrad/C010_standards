---
schema: "DocMeta.v1.2"
doc:
  sha256: "placeholder_generate_on_save"
  title: "Houston Emergency Protocol - Service Recovery"
  description: |
    Step-by-step procedure for Houston to recover from critical service
    failures in autonomous mode. Includes rollback procedures, log collection,
    and notification escalation paths.
  type: "spec"
  language: "en"
  created: "2025-11-08"
  authors:
    - "Mission Control Team"
  projects:
    - "Mission Control"
    - "C010"
  topics:
    - "monitoring"
    - "deployment"
    - "troubleshooting"
  keywords:
    - "emergency protocol"
    - "service recovery"
    - "autonomous operations"
    - "rollback"
  entities:
    products:
      - "Houston Agent"
      - "Docker"
      - "Vault"
      - "Nginx"

routing:
  canonical: true
  live: true
  tags:
    - "agent:houston"
    - "sensitivity:internal"
    - "priority:critical"
    - "playbook:emergency"

connections:
  related_docs:
    - "../30_config/houston-features.json"
    - "../validators/check_houston_telemetry.py"
---

# Houston Emergency Protocol - Service Recovery

## Purpose

This document defines the emergency protocol for Houston when operating in autonomous mode (Phase 3) and encountering critical service failures.

## Scope

Applies to:
- Docker daemon failures
- Vault unsealing issues
- Nginx service crashes
- Database connection losses

## Prerequisites

- Houston must be in Phase 3 (autonomous mode)
- Emergency protocols must be enabled in `houston-features.json`
- Rollback capability must be configured
- All actions are logged to audit trail

## Procedure

### 1. Detection

Houston monitors critical services every 30 seconds:

```json
{
  "monitoring": {
    "system_health": {
      "check_interval_seconds": 30,
      "critical_services": ["docker", "vault", "nginx"]
    }
  }
}
```

**Trigger**: Service down for >15 seconds (critical threshold)

### 2. Initial Response

**Immediate actions** (no confirmation required in autonomous mode):

1. **Log collection**: Capture last 100 lines of service logs
2. **Status snapshot**: Record system state before intervention
3. **Notification**: Send critical alert to all configured channels

**Audio cue**: Red alert siren with "Critical service failure detected" voice notification

### 3. Recovery Attempt

Houston follows this decision tree:

```
Service Failure
    ├─ First failure in 24h?
    │   └─ YES → Attempt restart
    │       ├─ Success → Monitor for 5 min
    │       └─ Failure → Escalate
    └─ Repeated failure?
        └─ YES → Rollback and escalate
```

#### 3.1 Restart Procedure

For docker/nginx/vault:

```bash
# Houston executes
systemctl restart <service>

# Verify
systemctl status <service>

# Test endpoint
curl -f http://localhost:<port>/health
```

**Timeout**: 60 seconds maximum
**Retry**: Once if timeout occurs

#### 3.2 Rollback Procedure

If restart fails or repeated failures detected:

1. **Identify last known good state**
   - Check deployment history
   - Find last successful health check timestamp

2. **Execute rollback**
   ```bash
   # For containerized services
   docker-compose down
   docker-compose up -d --force-recreate

   # For system services
   systemctl revert <service>
   systemctl restart <service>
   ```

3. **Verify recovery**
   - Run health checks
   - Monitor for 10 minutes
   - Confirm no error logs

### 4. Escalation

If recovery fails after rollback:

**STOP**: Houston enters safe mode
- Disable autonomous actions
- Require confirmation for all operations
- Continuous monitoring only

**NOTIFY**: Emergency escalation
- Page on-call engineer
- Post to Slack #alerts-critical
- Email mission-control-team@example.com
- Visual: Dashboard shows red alert state

**PRESERVE**: Evidence collection
- Complete logs from last 24 hours
- System metrics snapshot
- Houston's decision audit trail
- Network traffic capture (if configured)

### 5. Recovery Verification

Once service is restored (manually or via Houston):

**Checklist**:
- [ ] Service responding to health checks
- [ ] Dependent services operational
- [ ] No error logs in last 5 minutes
- [ ] Performance metrics within normal range
- [ ] Houston telemetry shows stable state

**Duration**: Monitor for 30 minutes before returning to normal operations

### 6. Post-Incident

Houston automatically:
1. **Generates incident report**
   - Timeline of events
   - Actions taken
   - Outcome
   - Saved to `70_evidence/incidents/`

2. **Updates telemetry**
   - Increment failure counter for service
   - Record recovery time
   - Update reliability metrics

3. **Self-assessment**
   - Was autonomous action successful?
   - Would manual intervention have been faster?
   - Should trust phase be adjusted?

## Safety Controls

All emergency actions respect these limits:

- **Require password**: For system shutdown or data deletion
- **Rate limiting**: Max 3 restart attempts per hour per service
- **Timeout**: All operations must complete within configured timeout
- **Audit log**: Every action logged with timestamp and reasoning

## Testing

**IMPORTANT**: Test this protocol regularly:

```bash
# Simulate service failure
systemctl stop docker

# Watch Houston respond
tail -f /var/log/houston/emergency.log

# Verify recovery
docker ps
```

**Frequency**: Monthly drill recommended

## Configuration Reference

See `30_config/houston-features.json`:

```json
{
  "safety_controls": {
    "emergency_protocols": {
      "panic_button": true,
      "auto_shutdown_threshold": 90,
      "graceful_degradation": true
    }
  }
}
```

## Related Documents

- [Houston Features Schema](../../schemas/houston_features.schema.json)
- [Telemetry Validator](../../validators/check_houston_telemetry.py)
- [Houston Interface Blueprint](../notes/HOUSTON_INTERFACE.md)

## Changelog

- **2025-11-08**: Initial protocol definition
- **Phase 3 only**: Not applicable in Phase 1 or 2
