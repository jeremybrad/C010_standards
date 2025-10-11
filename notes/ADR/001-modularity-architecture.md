# ADR 001 — Modularity Architecture & P160 → C004 Migration

**Date:** 2025-10-11
**Status:** accepted

## Context

P160 (Open Web UI) has evolved into a core interface used across many projects and now hosts critical functionality (Roundtable, model integrations, plugin points). Previously, agents, tools, and health scripts were tightly coupled to Mission Control (C001), causing cascading failures when Mission Control broke.

## Decision

1. Promote P160 → `C004_open-web-ui` and treat it as a core project.
2. Adopt a modular repo layout: separate Agents (C003), MCP Tools (C005), and Core UIs (C004). Use git submodules to reference standards (C010) and keep independent lifecycles.
3. Keep operational monitoring in Mission Control (C001), but define health-check schemas and validator contracts in C010_standards.

## Consequences

**Positive:**
- Independent development and testing for agents and tools
- Reduced blast radius when a single system (e.g., Mission Control) fails
- Clear separation of concerns between operational monitoring (C001) and standards/governance (C010)
- Better reusability across projects

**Negative:**
- Requires migration work: repo renames, updates to CI, and adding submodules
- Slightly more operational overhead (submodule updates, cross-repo coordination)

## Implementation Plan (high-level)

**Phase 1 — Planning (this ADR)**
- Update PROJECT_MAP.md, REPOSITORY_ORGANIZATION.md and CHANGELOG to record decision
- Document architectural patterns and migration rationale

**Phase 2 — Migration**
- Rename P160 → C004 in source repos
- Add C004 as a core repo entry; update CI and docs
- Create C005_mcp-tools and move MCP helper scripts into it

**Phase 3 — Operational**
- Add health endpoints to C004 and register them in C001 Houston config
- Implement agent submodules in C003 and refactor Mission Control to consume them as external submodules
- Define standardized health check schema in C010_standards

## Alternatives Considered

- **Centralize everything in Mission Control** — Rejected due to high coupling and cascading failure risk
- **Keep projects as P* prototypes** — Rejected because C004 now behaves like core infrastructure, not experimental code

## Notes

- Use standardized health JSON schema in `C010_standards/schemas/service_health_v1.0.yaml` (to be created)
- C004 currently serves 123+ models across OLLAMA, LM Studio, OpenAI, Anthropic, Grok, and other providers
- The Roundtable project has been successfully rebirthed within Open Web UI and is performing better than the previous implementation
