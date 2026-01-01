# C009 MCP-HTTP Quick Reference

**For PR Preparation**

---

## What Is C009?

**C009_mcp-memory-http** is a lightweight HTTP-based persistent memory service for AI agents.

**Think of it as:** A shared scratch pad where agents can store and retrieve simple key-value data.

---

## The Three Memory Systems

Your ecosystem has **three distinct memory systems**:

| System | Purpose | When to Use |
|--------|---------|-------------|
| **C002 SADB** | Biographical facts | "What facts do we know about Jeremy?" |
| **P159 Memory** | Conversational context | "What did we discuss in our last session?" |
| **C009 MCP-HTTP** | Agent state/preferences | "What's Houston's current status?" |

**All three are needed** - they solve different problems.

---

## C009's Role In The Ecosystem

### Architecture
```
┌─────────────────────────────────────┐
│  AI Agents & Systems                │
│  • C002_sadb (SADB)                 │
│  • C001_mission-control (Houston)   │
│  • Claude Desktop                   │
│  • P015_claude-agent-orchestrator   │
└──────────┬──────────────────────────┘
           │ HTTP POST
           ↓
┌─────────────────────────────────────┐
│  C009 MCP Memory Server (VPS)       │
│  Port: 8927                         │
│  Network: N8N Docker (internal)     │
└──────────┬──────────────────────────┘
           │ File I/O
           ↓
┌─────────────────────────────────────┐
│  memory_store.json                  │
│  Simple key-value pairs             │
│  Persistent Docker volume           │
└─────────────────────────────────────┘
```

### Active Integrations

**C002_sadb (SADB):**
- Namespace: `sadb:*`
- Uses: Track manifest timestamps, extraction run state
- Example: `sadb:manifest:last_build` → "2025-11-15T10:30:00Z"

**C001_mission-control:**
- Namespaces: `houston:*`, `agents:*`, `services:*`
- Uses: Agent status, service health, operational state
- Example: `houston:status` → "idle" | "processing" | "error"

**Claude Desktop:**
- Integration via `mcp-stdio-bridge.js` (STDIO → HTTP adapter)
- Provides memory_write/memory_read tools
- Uses: Cross-session context retention

---

## Production Details

**Deployment:**
- VPS: srv999538.hstgr.cloud
- Port: 8927 (internal only, N8N Docker network)
- Status: 🟢 Production running
- Storage: Docker volume (persistent)

**API:**
- Simple HTTP: POST /memory/write, POST /memory/read
- MCP JSON-RPC: Full protocol support
- Health: GET /health

**Not Exposed Externally:** Internal network only (secure by design)

---

## Use Cases

### ✅ Good Use Cases
- Agent status tracking
- Build timestamps and run metadata
- User preferences (theme, display settings)
- Cache frequently accessed values
- Cross-agent communication (shared state)
- Session bookmarks

### ❌ Not Suitable For
- Large data storage (use SADB instead)
- Semantic search (use P159 ChromaDB instead)
- High-volume transactions (file-based, not optimized)
- Sensitive credentials (no encryption, internal network only)

---

## PR Preparation Notes

### Current State
- ✅ Production deployed and running
- ✅ Comprehensive documentation exists
- ✅ Active integrations with C002 and C001
- ⚠️ README needs YAML frontmatter
- ⚠️ Missing retirement assessment

### PR Tasks (Estimated: 40-50 credits)

**Documentation (Quick wins):**
1. Add YAML frontmatter to README
2. Add status indicators (🟢 Production)
3. Document VPS deployment details
4. Clarify JSON-RPC vs Simple HTTP APIs

**Betty Protocol (Standard):**
1. Verify CLAUDE.md is current
2. Check directory organization
3. Update .gitignore (protect memory_store.json)
4. Ensure RELATIONS.yaml exists

**No Code Changes:** This is documentation-only (production system!)

---

## Comparison With Other Memory Systems

### vs SADB (C002)
- **SADB:** Structured biographical facts from conversations
- **C009:** Lightweight key-value storage
- **Use together:** SADB for facts, C009 for agent state

### vs P159 Memory
- **P159:** Real-time conversational memory with semantic search (ChromaDB)
- **C009:** Simple key-value persistence
- **Use together:** P159 for "what did we discuss", C009 for "what's the status"

### vs P005 MyBuddy
- **MyBuddy:** Digital twin using RAG + Chroma
- **C009:** Persistent preferences/cache
- **Use together:** MyBuddy queries, C009 stores preferences

---

## Key Takeaways

1. **C009 is production infrastructure** - Handle with care during standardization
2. **No breaking API changes** - Documentation only
3. **Already integrated** - C002 and C001 depend on it
4. **Complements other memory systems** - Doesn't replace SADB or P159
5. **VPS deployed** - Don't need local testing for basic docs

---

## PR Strategy

**Safe Approach:**
1. Review README and add frontmatter
2. Update CLAUDE.md with latest info
3. Verify .gitignore is comprehensive
4. Check RELATIONS.yaml for accuracy
5. Test: Just verify health endpoint works

**Avoid:**
- API changes (production system)
- Deployment modifications (already running)
- Major refactors (save for dedicated PR)

**Credit Budget:** 40-50 credits (documentation-focused)

---

*Created: 2025-11-19*
*For: C009 PR preparation*
*Location: C000_info-center/workspace/C009_BRIEF.md*
