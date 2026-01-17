---
capsule_spec: "c010.capsule.v1"
capsule_id: "661f9511-f39c-52e5-b827-557766551111"
created_at: "2026-01-17T10:15:00Z"
kind: "memory_export"
producer:
  tool: "context-manager"
  agent: "memory-exporter"
title: "Project Architecture Context Export"
summary: "Exported understanding of the Mission Control project architecture, key patterns, and integration points."
tags:
  - "architecture"
  - "mission-control"
  - "context"
expires_at: "2026-02-17T10:15:00Z"
provenance:
  source_session: "session-xyz789"
  version: "2.1.0"
---

# Project Architecture Context Export

## Overview

Mission Control is a retro-styled operations dashboard that provides monitoring, alerting, and automation for the workspace infrastructure.

## Key Architectural Decisions

### Technology Stack

- **Frontend**: React with TypeScript, styled-components for theming
- **Backend**: Python FastAPI, async-first design
- **Database**: PostgreSQL for persistence, Redis for caching
- **Message Queue**: RabbitMQ for async task processing

### Design Patterns

1. **Event Sourcing**: All state changes are captured as events
2. **CQRS**: Separate read and write models for performance
3. **Circuit Breaker**: Used for external service calls
4. **Retry with Backoff**: All network operations use exponential backoff

## Integration Points

### External Systems

| System | Protocol | Purpose |
|--------|----------|---------|
| Houston Agent | REST/WebSocket | Operations automation |
| SADB | GraphQL | Knowledge retrieval |
| VPS Fleet | SSH/API | Infrastructure management |

### Internal Components

```
┌─────────────────┐     ┌─────────────────┐
│   Web Frontend  │────>│   API Gateway   │
└─────────────────┘     └────────┬────────┘
                                 │
                    ┌────────────┼────────────┐
                    ▼            ▼            ▼
            ┌───────────┐ ┌───────────┐ ┌───────────┐
            │  Auth Svc │ │ Monitor   │ │ Automation│
            └───────────┘ └───────────┘ └───────────┘
```

## Learned Patterns

### Error Handling

All errors flow through a centralized error handler that:
- Logs to structured logging system
- Emits metrics for monitoring
- Returns consistent error response format

### Configuration

Configuration follows 12-factor app principles:
- Environment variables for secrets
- YAML files for static configuration
- Runtime config via feature flags

## Key Files

- `src/api/main.py` - API entry point
- `src/core/events.py` - Event sourcing implementation
- `src/services/houston.py` - Houston integration
- `config/settings.yaml` - Main configuration

## Notes

This context was exported to enable session continuity. The architecture is stable but the Houston integration is under active development.
