# Session 3: Core Infrastructure Analysis

**Date:** 2025-11-14
**Focus:** 8 projects that form the backbone of Jeremy's AI ecosystem
**Status:** 🔄 IN PROGRESS

## Overview

This session analyzes the critical infrastructure projects that everything else depends on. These are the projects that must be stable, well-documented, and always operational.

## Projects in This Session

### 🔴 CRITICAL PRIORITY
1. **P160_open-webui-ollama-setup** - Main LLM communication hub

### 🟡 HIGH PRIORITY
2. **C001_mission-control** - Credential vault & health monitoring
3. **P015_claude-agent-orchestrator** (Orky) - Agent coordination
4. **P181_terminal-insights** - Real-time collaboration monitoring
5. **C010_standards** - Workspace-wide metadata standards
6. **C011_agents** - Agent persona definitions
7. **P090_relay** - Communication layer
8. **P092_mirrorlab** - Memory integration

---

## P160: Open WebUI + Ollama Setup

**Status:** 🔴 CRITICAL INFRASTRUCTURE - Main communication hub
**Location:** `/Users/jeremybradford/SyncedProjects/P160_open-webui-ollama-setup`

### Purpose
P160 is Jeremy's central nervous system for AI interaction. It's not just an interface—it's the primary integration point where multiple systems converge.

### Key Capabilities

#### 1. **Main LLM Interface** (Port 3000)
- Web-based chat interface for local and API models
- Model switching between Ollama (local) and API providers
- RAG document upload and processing
- Custom JavaScript injection for extended functionality

#### 2. **SADB Filesystem Server** (Port 8082)
- Serves SADB data to Open WebUI
- Enables RAG queries against conversation history
- Integration point for knowledge retrieval

#### 3. **Betty Voice Integration**
- Multiple persona voices:
  - Default Betty (friendly/clear)
  - Velvet Betty (warm/intimate)
  - Excited Betty (energetic)
  - Oracle Betty (wise/contemplative)
  - Thoughtful Betty (reflective)
- Auto-persona detection from message content
- Voice toggle and commands
- ElevenLabs TTS integration

#### 4. **Roundtable Coordinator**
- Dev mode for testing
- Multi-agent conversation orchestration
- Integration with agent personas from C011

#### 5. **Memory Integration**
- MirrorLab prepared for persistent memory
- Connection to Betty Protocol
- Cross-session context preservation

### Technical Stack
- **Container:** Docker Compose
- **Services:**
  - Open WebUI (main interface)
  - Ollama (local LLM inference)
  - Betty Voice Server (TTS)
  - SADB Filesystem Server (RAG data)
- **Voice:** ElevenLabs Edge TTS
- **Data:** Docker volume `open-webui-data`

### Critical Dependencies
- C003_sadb_canonical (data source for filesystem server)
- C011_agents (persona definitions)
- P092_mirrorlab (memory layer - planned)
- ElevenLabs API (voice synthesis)

### Integration Points
- **Upstream:** Receives queries from user
- **Downstream:**
  - Ollama models (local inference)
  - OpenRouter/Anthropic APIs (cloud models)
  - SADB filesystem (knowledge retrieval)
  - Betty Voice Server (TTS)
  - MirrorLab (memory - planned)

### Operational Status
- ✅ Core functionality operational
- ✅ Voice integration working
- ✅ SADB filesystem server running
- ✅ Roundtable dev mode active
- ⚠️ File upload troubleshooting ongoing
- 🔄 MirrorLab memory integration in progress

### Documentation Quality
- README.md: Comprehensive setup guide
- AGENTS.md: Repository guidelines
- Voice setup scripts with clear instructions
- Custom JavaScript for UI extensions

### Recommendations
1. **Priority:** Resolve file upload issues (blocking RAG workflows)
2. **Enhancement:** Complete MirrorLab memory integration
3. **Documentation:** Create architecture diagram showing all integration points
4. **Monitoring:** Add health checks to Mission Control
5. **Backup:** Document data recovery procedures for `open-webui-data` volume

---

*Research continues with remaining 7 projects...*

**Next Update:** After completing all 8 projects (~50k tokens from now)
