# Houston Tooling Architecture

## Scope
Defines the tool stack Houston can invoke while operating locally or through remote MCP servers. Covers Phase 1 (essential) and Phase 2 (enhanced) capabilities; Phase 3 full-agency operations are noted as future work and intentionally disabled.

## Phased Capability Matrix
| Phase | Focus | Enabled Tools |
|-------|-------|---------------|
| 1 – Essential | Observation & diagnostics | filesystem.read/list/search, process monitoring, port checks, git status/diff/log, basic web search, HTTP client |
| 2 – Enhanced | Collaboration & remediation | docker inspect/build, service restarts (gated), browser automation (Playwright), Hugging Face downloads, advanced file ops |
| 3 – Full Agency | Deployment & autonomous ops | **Deferred** (system shutdowns, automated deploys, network config) |

## Tool Pipelines
- `research_pipeline`: `web_search → browser_automation → content_summarization → fact_checking`
- `deployment_pipeline`: `git_status_check → dependency_verification → docker_build → health_monitoring`
- `troubleshooting_pipeline`: `system_diagnostics → log_analysis → service_restart → verification`

Configure these sequences via `30_config/houston-tools.json`. Phase 1 runs the first step of each pipeline; later steps remain disabled until trust level increases.

## Access Control
- Local tools default to **strict sandbox** (read/search only) with optional opt-in for write/execute when Phase 2 is active.
- VPS tools (MCP server at `https://mcp.<domain>`) stay disabled until remote infrastructure is ready; see “VPS Integration” below.
- Cloud provider tooling (Hugging Face, GitHub, Docker Hub) remains off by default; enable per feature flag once API credentials are stored safely.

## Safety Guardrails
- Token budgets limit tool invocation cost (`per_tool_call`: 1k, `per_session`: 10k).
- Rate limits: 60 calls/minute with burst allowance of 10.
- Dangerous operations (`file_deletion`, `system_shutdown`, `network_changes`) require confirmations or higher trust phases.

## VPS Integration Notes
Running MCP tooling on a VPS provides high availability, security isolation, and remote access. Recommended approach:
1. Start locally to validate pipelines and permissions.
2. Mirror the tool stack on the VPS once telemetry and validators are stable.
3. Route Houston’s tool calls through the VPS when both local machines may be offline or remote access is needed. Maintain API key rotation and access logs.

Document readiness milestones in `10_docs/notes/ROADMAP.md` before enabling Phase 2 or VPS tooling to ensure validators cover new capabilities.
