# Project Relationships & Data Flow

**Last Updated:** 2025-11-19
**Maintained By:** Jeremy Bradford & Claude

This document maps how data flows through Jeremy's memory, knowledge, and work systems. Use this to understand dependencies before making changes.

---

## Quick Navigation

- [Memory System Architecture](#memory-system-architecture) - SADB → CBFS → MyBuddy pipeline
- [Additional Memory Systems](#additional-memory-systems) - P190, Terminal Insights, MCP Memory
- [Work Systems Integration](#work-systems-integration) - How memory feeds into analytics
- [Critical Dependencies](#critical-dependencies) - What depends on what
- [For LLMs: Finding Canonical Versions](#for-llms-finding-canonical-versions) - How to avoid grabbing old files

---

## Memory System Architecture

### The Canonical Pipeline (Multi-Stage Refinement)

This is the core data flow for processing conversations into structured knowledge:

```
┌─────────────────────────────────────────────────────────────────┐
│ STAGE 0: CONVERSATION SOURCES                                    │
├─────────────────────────────────────────────────────────────────┤
│  • ChatGPT exports (conversations.json in .zip files)           │
│  • Claude exports (from claude.ai)                              │
│  • Council logs (terminal interaction history)                  │
│  • Location: ~/Downloads → $SADB_DATA_DIR/conversation-exports/ │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│ C002_sadb: SADB CORE PROCESSING                                 │
├─────────────────────────────────────────────────────────────────┤
│  Purpose: Initial extraction and consensus validation           │
│                                                                  │
│  Process:                                                        │
│   1. Chunking (semantic + sliding window)                       │
│      • 1.5k tokens per chunk, 400 token overlap                 │
│   2. 3-Pass Consensus Extraction                                │
│      • Local LLMs via Ollama/vLLM/LM Studio                     │
│      • Multi-model agreement required                           │
│   3. Validation & Enrichment                                    │
│      • Speaker attribution                                      │
│      • Metadata overlay                                         │
│   4. Human Review Queue                                         │
│      • Web UI or CLI for approval                               │
│                                                                  │
│  Outputs:                                                        │
│   • SQLite canonical store (entries, runs, contradictions)      │
│   • twin_feed_v1.ndjson (facts + preferences only)              │
│   • Location: $SADB_DATA_DIR/twin/                              │
│                                                                  │
│  Data Policy: All artifacts external to git ($SADB_DATA_DIR)    │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│ C003_sadb_canonical: REFINEMENT PIPELINE (Stages S0-S2, M1-B1) │
├─────────────────────────────────────────────────────────────────┤
│  Purpose: Deterministic normalization and multi-stage enrichment│
│  Status: Production (v0.2) with GPU acceleration                │
│                                                                  │
│  STAGE S0 - CAPTURE:                                            │
│   • Dry-run ingest with SHA256 deduplication                    │
│   • Receipt generation for provenance                           │
│   • Search ledger maintenance                                   │
│                                                                  │
│  STAGE S1 - NORMALIZE:                                          │
│   • Schema validation (JSON structure)                          │
│   • Leak scanning (PII detection)                               │
│   • Data sanitization                                           │
│   • Output: 95,266 messages across 601 conversations            │
│                                                                  │
│  STAGE S2 - ENRICH:                                             │
│   • Semantic windowing (context preservation)                   │
│   • BERTopic GPU clustering (RTX 5080, 527x speedup!)          │
│   • Semantic filtering (Topic 0 reduced from 22% → 0.46%)      │
│   • Embedding generation (vector representations)               │
│   • Output: 70,539 enriched windows                             │
│                                                                  │
│  STAGE M1 - Q/A MEMORY:                                         │
│   • Extract Q/A pairs from normalized messages                  │
│   • Purpose: Feed memory systems (CBFS, MyBuddy, digital twin)  │
│   • Output: 4,092 Q/A pairs from 601 conversations              │
│   • Contract: 10_docs/STAGE_M1_QA_CONTRACT.md                   │
│                                                                  │
│  STAGE U1 - UTTERANCE SEGMENTATION:                             │
│   • Segment M1 Q/A pairs into atomic units                      │
│   • Flag code blocks, log entries, questions                    │
│   • Purpose: Fine-grained fact extraction units                 │
│   • Output: 108,487 segments with metadata flags                │
│   • Contract: 10_docs/STAGE_U1_SEGMENTS_CONTRACT.md             │
│                                                                  │
│  STAGE J1 - FACT CANDIDATES:                                    │
│   • LLM-based fact extraction from U1 segments                  │
│   • Format: Subject-predicate-object triples                    │
│   • Includes certainty/stance scoring                           │
│   • Test run: 7 facts from 20 segments (v0)                     │
│   • Web import (Nov 2025): 508 merged facts                     │
│   • Contract: 10_docs/STAGE_J1_FACT_CANDIDATES_CONTRACT.md      │
│                                                                  │
│  STAGE B1 - BRAIDED TIMELINE:                                   │
│   • Merge S1 chat messages + P181 terminal commands             │
│   • Creates unified event timeline                              │
│   • Shows what Jeremy discussed + what he executed              │
│   • Output: 95,266 events (Sep 2023 → Oct 2025)                │
│   • Contract: 10_docs/STAGE_B1_BRAIDED_TIMELINE_CONTRACT.md     │
│   • Integration: ~/SyncedProjects/P181_terminal-insights/       │
│                  docs/SADB_INTEGRATION_BRAIDING.md              │
│                                                                  │
│  STAGE J1↔B1 PROXIMITY JOIN:                                    │
│   • Link J1 facts to nearby B1 timeline events                  │
│   • Uses ±15min temporal window (capped at 10 events)          │
│   • Enables query: "What was Jeremy doing when this fact emerged?"│
│   • Result: 282/282 facts linked, avg 9.86 events per fact      │
│   • Receipt: 20_receipts/J1B1_PROXIMITY_COMPLETE_20251115.md    │
│                                                                  │
│  ⚠️ STAGES M2/M3 - FUTURE/PLANNED:                             │
│   • M2: [Purpose TBD - Memory consolidation/synthesis?]         │
│   • M3: [Purpose TBD - Memory validation/integration?]          │
│   • TODO: Document these stages when implemented                │
│                                                                  │
│  Key Artifacts:                                                  │
│   • GPU Environment: WSL Ubuntu, bertopic-blackwell conda env   │
│   • Filtered Corpus: 60_artifacts/filtered/ (70,539 windows)    │
│   • Fact Runs: 60_artifacts/enriched/j1/                        │
│   • Neo4j Knowledge Graph: 270 Wikidata entities, 4k topics     │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│ C008_CBFS: CANONICAL BIO FACTS SYSTEM                           │
├─────────────────────────────────────────────────────────────────┤
│  Purpose: Provenance-first biographical memory for AI agents    │
│  Status: Production (v1.3) with 232 facts                       │
│                                                                  │
│  Architecture:                                                   │
│   • Every fact has confidence score (0.0-1.0)                   │
│   • Full source attribution with timestamps                     │
│   • Privacy tiers: public → contacts → private → sensitive      │
│   • Memori taxonomy: Facts/Preferences/Skills/Rules/Context     │
│                                                                  │
│  Data Organization (13 domains):                                │
│   • identity: Name, birthdate, identifiers (14 facts)           │
│   • contact: Email, phone, addresses (3 facts)                  │
│   • professional: LinkedIn, work history, skills (64 facts)     │
│   • digital_infrastructure: Devices, repos, stack (101 facts!)  │
│   • relationship_networks: Family, friends (22 facts)           │
│   • behavioral_patterns: Decision style, communication (13)     │
│   • past_residences: Array of cities with temporal validity     │
│   • routines: Work hours, daily patterns (8 facts)              │
│   • health: Allergies, blood type (1 fact)                      │
│   • temporal_patterns: Weekly rhythms, recurring events         │
│   • goals: Short/long term objectives                           │
│   • constraints: Time, resource, energy limitations             │
│   • metadata: Schema tracking, update timestamps                │
│                                                                  │
│  Import Pipeline:                                                │
│   • Source: C003 SADB L2 database (J1 facts)                    │
│   • Process: 315 raw facts → 232 deduplicated fields            │
│   • Validation: Schema v1.3 (40_src/validate_cbfs.py)           │
│   • Status: Ready for human verification & Betty integration    │
│                                                                  │
│  File Location: 30_config/cbfs_v1.3.yaml                        │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│ P005_mybuddy: DIGITAL TWIN (Conversational Interface)          │
├─────────────────────────────────────────────────────────────────┤
│  Purpose: Local-first conversational AI simulating Jeremy       │
│  Status: Active with SADB integration                           │
│  Privacy: PRIVATE - No public data sharing                      │
│                                                                  │
│  Architecture:                                                   │
│   • RAG with Chroma vector database                             │
│   • Local LLMs via Ollama (no cloud dependencies)               │
│   • Strict provenance tracking                                  │
│   • Ethics guardrails built-in                                  │
│                                                                  │
│  Dual Data Pipeline:                                             │
│   Path 1 (Standalone): CSV chunks → ingest → topics → index    │
│   Path 2 (SADB): twin_feed_v1.ndjson → ingest-sadb → Chroma    │
│                                                                  │
│  Key Features:                                                   │
│   • Interactive CLI chat (make chat)                            │
│   • FastAPI server on port 8000 (make api)                      │
│   • Evaluation harness for quality testing                      │
│   • Web test interface for debugging                            │
│                                                                  │
│  Data Location: $SADB_DATA_DIR (all artifacts externalized)     │
└─────────────────────────────────────────────────────────────────┘
```

---

## Additional Memory Systems

### P190_conversation-exports-web (Metadata Extraction Pipeline)

**Status:** Active (2025-11-18 implementation)
**Purpose:** Rich metadata extraction from conversation sources

```
Anthropic Conversations + Betty (ChatGPT) Conversations
    ↓
P190_conversation-exports-web
    ↓
Structured Metadata Extraction
    ↓
[FUTURE] Merge back into SADB canonical pipeline
```

**What Makes This Special:**
- Parallel extraction system (not yet integrated with main SADB flow)
- Rich source of contextual information
- Captures metadata that standard SADB pipeline might miss
- Planned integration point with C003_sadb_canonical

**Current State:**
- Operational but standalone
- Contains valuable context not in main SADB database
- Integration strategy being developed

### P181_terminal-insights (Action Layer)

**Status:** Production, feeding B1 Braided Timeline
**Purpose:** Terminal command history with full context

```
zsh_history + Command Context
    ↓
P181_terminal-insights Processing
    ↓
Structured Command Events
    ↓
B1 Braided Timeline (in C003_sadb_canonical)
```

**Why This Matters:**
- Shows what Jeremy *did* (actions) alongside what he *discussed* (conversations)
- Provides concrete evidence of technical work
- Critical for understanding cause-effect relationships
- Enables temporal correlation: "What was I doing when I mentioned X?"

**Integration:**
- Feeds directly into C003's B1 stage
- 95,266 total events when combined with chat messages
- Time range: Sep 2023 → Oct 2025
- Documentation: P181_terminal-insights/docs/SADB_INTEGRATION_BRAIDING.md

### C009_mcp-memory-http (MCP Memory Server)

**Status:** Active
**Purpose:** Persistent memory for local LLMs via HTTP

**Architecture:**
- HTTP-based Model Context Protocol (MCP)
- Provides `memory_write` and `memory_read` tools
- Designed for Claude and local LLM integration
- Lightweight, focused on real-time memory access

**Use Case:**
- Real-time memory persistence during conversations
- Cross-session context retention
- Complements SADB's batch processing approach

### P159_memory-system (ChromaDB Memory)

**Status:** Active
**Purpose:** ChromaDB-based persistent memory system

**Features:**
- Works with Claude and local LLMs
- Vector similarity search for context retrieval
- Alternative to SADB for lightweight memory needs
- More immediate than SADB's batch pipeline

---

## Work Systems Integration

### How Memory Feeds Analytics

Several work projects depend on SADB data for context and insights:

#### W001_cmo-weekly-reporting
**Dependency:** C002_sadb
**How:** Queries SADB for personal context to enrich marketing analytics
**Example:** "Mention if Jeremy discussed competitor analysis this week"

#### W009_context_library
**Role:** "Front desk for knowledge access"
**Dependency:** C002_sadb, potentially CBFS
**How:** Central query point for retrieving contextual information
**Purpose:** Provides quick access to relevant memories for work tasks

#### Other Work Projects (W002-W012)
Most work projects are standalone but may benefit from:
- Personal context from CBFS (understanding Jeremy's perspective)
- Historical decisions from SADB (why choices were made)
- Timeline correlation from B1 (when events happened)

---

## The SADB Ecosystem (Sprawling - Needs Consolidation)

⚠️ **This section documents a known problem area requiring cleanup.**

### What Exists

Current SADB-related folders and their purposes:

| Location | Purpose | Status | Cleanup Need |
|----------|---------|--------|--------------|
| C002_sadb | Core processing pipeline | ✅ Active | Low - well-defined |
| C003_sadb_canonical | Refinement stages (S0-B1) | ✅ Active | Low - documented |
| $SADB_DATA_DIR | External data directory | ✅ Active | Medium - some old runs |
| SADB_backups/ | Various backup locations | ⚠️ Scattered | High - consolidate |
| Multiple extraction runs | Historical test runs | ⚠️ Unclear | High - archive old runs |

### The Problem

**Symptoms:**
- Hard to tell what's current vs historical vs test data
- Multiple directories with "SADB" in the name
- Old extraction runs mixed with current ones
- Unclear which outputs are canonical

**Impact on LLMs:**
- May grab outdated fact extraction runs
- Confusion about which SADB repo to use (C002 vs C003)
- Difficulty determining "ground truth" data location

### The Solution (Planned)

**Phase 1: Documentation**
- Mark current/canonical files explicitly in README files
- Add "DEPRECATED" warnings to old runs
- Create clear date stamps on extraction directories

**Phase 2: Archival**
- Move old extraction runs to `90_archive/extractions_YYYY/`
- Consolidate scattered backups
- Create manifest of what was archived and why

**Phase 3: Guardrails**
- Pre-commit hooks to prevent new scattered directories
- Naming conventions enforced (runs_YYYYMMDD_HHMMSS format)
- Automatic cleanup scripts for >90 day old test runs

---

## Critical Dependencies

### Execution Order (Must Follow This Sequence)

When working with memory systems, respect these dependencies:

1. **C002_sadb** must run first
   - Creates canonical SQLite store
   - Generates twin_feed_v1.ndjson
   - All downstream systems depend on this output

2. **C003_sadb_canonical** refines C002 output
   - Cannot run without C002 data
   - Stages S0-S2 prepare data for M1-B1
   - M1, U1, J1 depend on S1/S2 completion
   - B1 requires both S1 data AND P181 terminal data

3. **C008_CBFS** imports from C003
   - Specifically depends on J1 fact extraction
   - Requires C003 L2 database to exist
   - Import pipeline: C003 J1 → CBFS YAML

4. **P005_mybuddy** queries twin feed OR CBFS
   - Can use C002 twin feed directly (path 2)
   - Can use standalone CSV (path 1)
   - Future: May query CBFS for richer context

5. **Other systems** query SADB or CBFS as needed
   - W001, W009 query C002_sadb
   - P190 operates in parallel (not dependent)
   - P181 feeds into C003 but doesn't depend on it

### Dependency Graph

```
                   ┌──────────────────┐
                   │  Conversations   │
                   └────────┬─────────┘
                            │
                   ┌────────▼─────────┐
                   │   C002_sadb      │
                   │  (core pipeline) │
                   └────────┬─────────┘
                            │
                ┌───────────┴───────────┐
                │                       │
       ┌────────▼─────────┐    ┌───────▼────────┐
       │ C003_sadb        │    │ W001, W009     │
       │ (refinement)     │    │ (work queries) │
       └────────┬─────────┘    └────────────────┘
                │
       ┌────────┴────────┐
       │                 │
┌──────▼──────┐   ┌──────▼──────┐
│  C008_CBFS  │   │ P005_mybuddy│
│  (facts)    │   │ (twin)      │
└─────────────┘   └─────────────┘

    [P181 terminal data] ───────┐
                                 │
                        ┌────────▼─────────┐
                        │  C003 B1 Stage   │
                        │ (braided timeline)│
                        └──────────────────┘

    [P190 metadata extraction]  (parallel, future integration)
```

---

## For LLMs: Finding Canonical Versions

### The Problem We're Solving

LLMs frequently make these mistakes:
1. ❌ Grabbing test scripts instead of production code
2. ❌ Using outdated extraction runs instead of current ones
3. ❌ Confusing C002_sadb with C003_sadb_canonical
4. ❌ Working on archived projects instead of active ones

### Solution: Always Follow This Checklist

#### Step 1: Check Project Status
```bash
# Read this first!
cat ~/SyncedProjects/C000_info-center/workspace/KNOWN_PROJECTS.md
```

Look for:
- Last modified date (is it recent?)
- Status indicators (Active? Archived?)
- Project ID (C### for core, P### for personal)

#### Step 2: Read the Project's CLAUDE.md
```bash
# This file exists in EVERY active project
cat ~/SyncedProjects/PROJECT_NAME/CLAUDE.md
```

Contains:
- Quick start commands
- Canonical file paths
- Common pitfalls
- Build instructions

#### Step 3: Understand Multi-Version Scenarios

**SADB Disambiguation:**
- `C002_sadb` = Core processing, creates SQLite + twin feed
- `C003_sadb_canonical` = Refinement pipeline, stages S0-B1
- When in doubt: C003 is the newer, more sophisticated version
- But C002 must run BEFORE C003 can process its output

**Rule:** If you need fact extraction (J1), use C003. If you need basic ingestion, use C002.

#### Step 4: Look for Temporal Markers

**Good file naming:**
```
runs_gptoss_20251104_235333/     ← Timestamp shows this is Nov 4, 2025
facts_llm_gptoss_merged.kept.jsonl
```

**Bad file naming:**
```
test_output/         ← No date, unclear status
results/             ← Generic, could be anything
```

**Rule:** Prefer files/folders with ISO timestamps (YYYYMMDD_HHMMSS)

#### Step 5: Check for "Canonical" Markers

Look for these indicators:
- "canonical" in folder/file names
- "current" or "latest" symlinks
- "DEPRECATED" or "ARCHIVED" warnings
- Date stamps in README files

#### Step 6: Verify with Last Modified Dates

```bash
# When choosing between similar files
ls -lt ~/SyncedProjects/C003_sadb_canonical/60_artifacts/enriched/j1/

# Most recent is usually (but not always) canonical
# Cross-reference with project's CLAUDE.md to be sure
```

### Common Confusion Points (Reference Guide)

| User Says | Might Mean | Check This |
|-----------|------------|------------|
| "Work on SADB" | C002? C003? Both? | KNOWN_PROJECTS.md + user intent |
| "Use twin feed" | C002 output OR P005 input? | Context of conversation |
| "Latest facts" | J1 stage? J2? J3? | C003 CLAUDE.md canonical paths |
| "Memory system" | SADB? CBFS? MyBuddy? MCP? | What type of memory operation? |
| "Terminal data" | P181 output OR B1 integration? | User's specific need |

### Decision Tree for File Selection

```
START: User asks to "work on X"
│
├─ Is X mentioned in KNOWN_PROJECTS.md?
│  ├─ NO → Ask user for clarification
│  └─ YES → Continue
│
├─ Is project status "Active"?
│  ├─ NO (Archived/Maintenance) → Confirm with user before proceeding
│  └─ YES → Continue
│
├─ Does CLAUDE.md specify canonical paths?
│  ├─ YES → Use those exact paths
│  └─ NO → Check for timestamps/date markers
│
├─ Multiple versions exist?
│  ├─ NO → Use the one available
│  └─ YES → Prefer: "canonical" name > most recent date > ask user
│
└─ SUCCESS: You have the right file!
```

### When to Ask Instead of Guess

**Always ask if:**
- Multiple projects have similar names (C002 vs C003)
- Files/folders lack date stamps
- Status is unclear (Active vs Archived)
- User says "the usual file" but you don't know which one
- Last modified dates are all old (maybe project is stale?)

**Better to ask:** "Should I use C002_sadb or C003_sadb_canonical for this task?"
**Than to guess wrong** and waste 20 minutes on the wrong pipeline.

---

## Maintenance Notes

### Update Triggers

This document should be updated when:
- New memory systems are added (e.g., M2/M3 stages implemented)
- Pipeline stages change (S0-S2 evolve)
- Dependencies shift (new integration points)
- Cleanup initiatives complete (SADB consolidation)

### Document Owners

- **Memory Architecture:** Jeremy Bradford
- **Technical Details:** Claude (with Jeremy's review)
- **Work Integration:** Jeremy Bradford
- **Canonical Paths:** Auto-discovered + manually verified

### Version History

- 2025-11-19: Initial creation with S0-S2, M1, U1, J1, B1 stages documented
- [Future]: M2/M3 stages to be added when implemented
- [Future]: P190 integration pathway when finalized

---

*Last Updated: 2025-11-19*
*Location: C000_info-center/workspace/PROJECT_RELATIONSHIPS.md*
*Maintained by: Jeremy Bradford & Claude*
