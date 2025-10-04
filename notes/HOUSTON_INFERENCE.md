# Houston Inference Guide

## Overview
Houston routes requests across local Ollama nodes and cloud-hosted LLMs. Target outcome: keep `qwen-coder:480b` (N3 Coder 480B) as the default coding brain while gracefully falling back to regional hardware or other cloud tiers. Configuration lives in `30_config/houston.json`; this note documents priorities, health checks, and telemetry conventions for contributors.

## Host & Model Priority
1. **Cloud (Primary)** – `qwen-coder:480b` (`use_case: coding_expert`), endpoint `https://api.ollama.cloud`. Allow manual switching to:
   - `deepseek:670b` (`complex_reasoning`)
   - `gpt-oss:120b` (`fast_general`)
2. **RTX Workstation** – `qwen2.5-coder:32b-q4_K_M`, `qwen3:72b-q4_K_M`
3. **Local Mac** – `qwen2.5-coder:14b-q4_K_M`, `mistral:7b-q4_K_M`
4. **Fallback Shelf** – Additional lightweight models under `~/models/ollama/fallbacks/`.

Maintain `houston-models.json` (see below) to map use cases → ordered model list. Enforce exact tags (include quantization suffix) so validators can detect drift.

```jsonc
{
  "coding_expert": ["qwen-coder:480b", "qwen2.5-coder:32b-q4_K_M", "qwen2.5-coder:14b-q4_K_M"],
  "complex_reasoning": ["deepseek:670b", "qwen3:72b-q4_K_M"],
  "fast_general": ["gpt-oss:120b", "mistral:7b-q4_K_M"]
}
```

## Health Monitoring & Routing
- Poll each host’s `GET /api/tags` every 30s; cache status and apply a circuit breaker (3 consecutive failures → cool-off 5 minutes).
- `InferenceRouter` (see `40_src/houston/inference-client.js`) sorts hosts by priority, drops unhealthy ones, and logs failover reasons.
- Return user-facing messages during failover: e.g., *“RTX offline — switching to cloud inference.”*

## Telemetry Envelope
Log every inference call to `70_evidence/houston_telemetry.jsonl`:
```json
{
  "timestamp": "2025-09-22T10:30:00Z",
  "host": "ollama-cloud",
  "model": "qwen-coder:480b",
  "latency_ms": 2450,
  "prompt_tokens": 1200,
  "response_tokens": 350,
  "fallback_chain": ["qwen2.5-coder:32b-q4_K_M"],
  "manual_override": false
}
```
Include `context_id` when preserving dialogue via MCP shared memory.

## Model Switching
Support manual overrides via config flag `model_switching.allow_manual_override: true`. Persist the active model per session and respect `context_preservation: true` so memory is reusable when Houston hops between clouds and local hardware.
