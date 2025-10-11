# SyncedProjects Project Map

**Generated:** 2025-10-08
**Purpose:** Quick reference for all projects in SyncedProjects

## Core Infrastructure (C-prefix)

| Project | Purpose | Status |
|---------|---------|--------|
| C001_mission-control | Central orchestration hub, Houston agent | Active |
| C003_agents | Agent definitions and frameworks | Active |
| C003_mirrorlab | Mirror/testing lab | Active |
| C004_open-web-ui | Core LLM interface for local & cloud models (formerly P160) | **MIGRATED 2025-10-11** |
| C005_mcp-tools | Model Context Protocol tooling library | **PROPOSED** |
| C009_mcp-memory-http | HTTP interface for MCP memory | Active |
| C010_standards | Canonical standards, schemas, taxonomies (this repo) | Active |

### C004_open-web-ui (formerly P160)
- **Role:** Core LLM interface and orchestration UI for local & cloud models (OLLAMA, LM Studio, OpenAI, Anthropic, Grok, etc.)
- **Path:** ../C004_open-web-ui (rename/migrate from P160)
- **Status:** MIGRATED from P160 → C004 (2025-10-11)
- **Maintainers:** Jeremy Bradford (Al) / Team
- **Tags:** core, ui, models, roundtable
- **Depends on:** C001_mission-control (monitoring), C010_standards (policy), C005_mcp-tools (dev tools)
- **Notes:** Hosts the Roundtable UI injection; exposes plugin points for Coordinator. Treat as core infra; follow Betty standards. Currently serves 123+ models across multiple providers.

### C005_mcp-tools (proposed)
- **Role:** Library/repo for Model Context Protocol (MCP) tooling (Chrome DevTools MCP clients, server helpers, test harnesses)
- **Path:** ../C005_mcp-tools
- **Status:** PROPOSED
- **Notes:** Move scattered MCP helper scripts and Chrome DevTools integrations here. Provides reusable MCP tooling for development across Mission Control and Open Web UI.

## Personal Projects (P-prefix)

### Core Betty Ecosystem
| Project | Purpose | Status |
|---------|---------|--------|
| P001_bettymirror | Betty AI system core | Active |
| P010_betty-ai | Betty AI implementation | Active |
| P011_betty-mcp | Betty MCP integration | Active |
| P012_betty-metadata-capture | Metadata capture for Betty | Active |
| P013_betty-source-tracker | Source tracking system | Active |

### SADB & Knowledge Systems
| Project | Purpose | Status |
|---------|---------|--------|
| C002_sadb | Self-Aware Database project (formerly P002) | **MIGRATED 2025-10-11** |
| P110_knowledge-synthesis-tool | KST development | Active |
| P159_memory-system | Memory architecture | Active |
| P170_memory-cathedral | Advanced memory architecture | Active |

### AI Services & Voice
| Project | Purpose | Status |
|---------|---------|--------|
| P030_ai-services | AI service infrastructure | Active |
| P031_sillytavern | SillyTavern integration | Active |
| P032_enhanced-whisper | Enhanced Whisper transcription | Active |
| P033_resonance-prime | Resonance project | Active |
| P034_whisper-speech | Whisper speech processing | Active |
| P091_voice-notes-pipeline | Voice notes processing pipeline | Active |
| P158_local-tts | Local text-to-speech | Active |

### MCP & Integration
| Project | Purpose | Status |
|---------|---------|--------|
| P050_ableton-mcp | Ableton MCP integration | Active |
| P051_mcp-servers | MCP server implementations | Active |
| P052_n8n-mcp-setup | n8n MCP setup | Active |
| P162_servers-from-workspace | Server configurations | Active |
| P167_dj-claude-mcp | DJ Claude MCP integration | Active |

### Tools & Utilities
| Project | Purpose | Status |
|---------|---------|--------|
| P003_biographer | Biography tool | Active |
| P004_adaptive | Adaptive system | Active |
| P005_mybuddy | Buddy assistant | Active |
| P006_earn | Earnings tracker | Active |
| P007_n8n_and_the_sad_bees | n8n workflow system | Active |
| P090_relay | Relay system | Active |
| P113_docs-site | Documentation site | Active |
| P150_claude | Claude integrations | Active |
| P151_clouddriveinventory | Cloud drive inventory | Active |
| P152_cognitiveplayback | Cognitive playback system | Active |
| P153_seo-cannibalization | SEO analysis | Active |
| P154_agents | Agent implementations | Active |
| P157_dashboards | Dashboard systems | Active |
| ~~P160_open-webui-ollama-setup~~ | ~~Open WebUI + Ollama~~ | **MIGRATED → C004_open-web-ui (2025-10-11)** |
| P163_taxonomy-analysis | Taxonomy analysis tools | Active |
| P164_utilities | General utilities | Active |
| P166_fiber-vs-home_reconciliation | Fiber/home reconciliation | Active |
| P168_velvet-console | Velvet console interface | Active |
| P169_workflow-harvest | Workflow harvesting | Active |
| P181_terminal-insights | Terminal insights tool | Active |

### Archived/Deprecated
| Project | Purpose | Status |
|---------|---------|--------|
| ~~P002_sadb~~ | ~~Self-Aware Database~~ | **MIGRATED → C002_sadb (2025-10-11)** |
| ~~P160_open-webui-ollama-setup~~ | ~~Open WebUI + Ollama~~ | **MIGRATED → C004_open-web-ui (2025-10-11)** |
| ~~P210_metadata-governance~~ | ~~Old name for C010_standards~~ | **DELETED 2025-10-08** |

## Work Projects (W-prefix)

| Project | Purpose | Status |
|---------|---------|--------|
| W001_Lighthouse | Work project (Huawei) | Active |
| W001_cmo-weekly-reporting | CMO weekly reporting | Active |
| W002_analytics | Analytics infrastructure | Active |

## Projects Needing Attention

### In Workspace/ Folder (Should Be Migrated)
- **P001_bettymirror** - Duplicate of root-level project
- **C002_sadb** - Duplicate of root-level project (formerly P002)
- **P005_mybuddy** - Duplicate of root-level project
- **P070_midi-gesture** - Unique, needs to be moved to root

### Non-Conforming Names
- **REF001_Analytics_Canonical** - Needs proper prefix (W003? C011?)

## Special Directories

| Directory | Purpose | Should Modify? |
|-----------|---------|----------------|
| _receipts | Audit trail and logs | ❌ No - automated |
| SharedData | Shared resources across projects | ⚠️ Carefully |
| Archive | Historical/deprecated projects | ⚠️ For cleanup only |
| Workspace | **DEPRECATED** - migrate projects out | 🔄 Migrate then remove |

## Quick Stats
- **Core Projects:** 7 active + 1 proposed (C002 migrated from P002, C004 migrated from P160, C005 proposed)
- **Personal Projects:** 38 active (P002 → C002, P160 → C004)
- **Work Projects:** 3 (plus 1 unclassified)
- **Projects to Migrate:** 4
- **Naming Issues:** 1

## Next Actions

1. **Migrate from Workspace/**
   ```bash
   # Check if truly duplicates first
   diff -r Workspace/P001_bettymirror P001_bettymirror
   
   # If unique, move
   mv Workspace/P070_midi-gesture ./
   
   # Remove duplicates after verification
   rm -rf Workspace/P001_bettymirror  # if confirmed duplicate
   ```

2. **Fix REF001_Analytics_Canonical**
   ```bash
   # Determine if work or reference
   # If work: mv REF001_Analytics_Canonical W003_analytics-canonical
   # If reference: mv REF001_Analytics_Canonical C011_analytics-reference
   ```

3. **Update this file** after migrations

---

**Maintenance:** Regenerate this file when projects are added/removed/renamed
**Source of Truth:** Check actual directory listing if discrepancies exist
