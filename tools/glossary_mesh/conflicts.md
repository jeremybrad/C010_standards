# Glossary Mesh v1 — Conflicts Report

**Generated**: 2025-12-22
**Source Repos**: 17 (C001-C011, C015-C020)
**Total Terms**: 168
**Terms with Multi-Repo Presence**: 16

---

## Conflict Classification

| Level | Description | Action Required |
|-------|-------------|-----------------|
| 🔴 **Critical** | Same term, incompatible meanings | Rename or disambiguate |
| 🟡 **Minor** | Same term, complementary meanings | Document relationship |
| 🟢 **Aligned** | Same term, consistent definitions | No action needed |

---

## 🟢 Aligned Terms (No Conflicts)

These terms appear in multiple repos with consistent or complementary definitions:

### Betty Protocol
- **C001_mission-control**: Evidence-driven development protocol with receipts, no self-certification
- **C010_standards**: Mandatory governance protocol with same core principles
- **Status**: ✅ Definitions are consistent — both describe the same protocol

### Twin Feed
- **C002_sadb**: Export format (NDJSON) with approved facts/preferences
- **C005_mybuddy**: NDJSON export from CBFS for semantic indexing
- **Status**: ✅ Same format, complementary descriptions

### Semantic Chunking
- **C002_sadb**: 1500 tokens, 400 overlap for extraction
- **C003_sadb_canonical**: S2 Enrich process for segmentation
- **Status**: ✅ Same concept, different detail levels

### HITL (Human-in-the-Loop)
- **C002_sadb**: Approval workflow before canonical store
- **C008_CBFS**: Human review loop via HTML reviewer
- **C018_terminal-insights**: Pause node in LangGraph pipeline
- **Status**: ✅ Same principle applied in different contexts

### RAG (Retrieval-Augmented Generation)
- **C007_the_cavern_club**: Document upload with local embeddings
- **C019_docs-site**: Complete pipeline with FAISS indexing
- **Status**: ✅ Same technology, different implementations

### Topic Taxonomy
- **C005_mybuddy**: YAML classification for fact filtering
- **C010_standards**: Controlled vocabulary for content classification
- **Status**: ✅ Complementary purposes

### BERTopic
- **C003_sadb_canonical**: Topic labeling in S2 Enrich
- **C005_mybuddy**: Optional clustering upgrade
- **Status**: ✅ Same library, different usage contexts

### ChromaDB
- **C005_mybuddy**: Vector store for biographical facts
- **C007_the_cavern_club**: Memory storage for MirrorLab
- **Status**: ✅ Same technology, different data domains

---

## 🟡 Minor Variations (Document Relationship)

These terms have related but distinct meanings requiring clarification:

### Houston
| Repo | Definition | Scope |
|------|------------|-------|
| C001_mission-control | AI infrastructure assistant and copilot | Infrastructure ops |
| C011_agents | Coordinator agent orchestrating multi-agent workflows | Agent orchestration |

**Resolution**: Houston in C001 is the *implementation* of the Houston persona; C011 documents the *agent specification*. Cross-reference recommended.

**Recommended alias**:
- C001: "Houston (Implementation)"
- C011: "Houston (Agent Spec)"

---

### Orpheus / Scribe / Archivist
These three agents appear in both C001 and C011:

| Agent | C001 Definition | C011 Definition |
|-------|-----------------|-----------------|
| Orpheus | Mission playlists and composition | Creative/music assistant with broader scope |
| Scribe | Condenses transcripts | Documentation specialist with broader scope |
| Archivist | Ingests SADB snapshots | SADB query manager with broader scope |

**Resolution**: C001 describes *operational usage* within Mission Control; C011 describes *canonical agent capabilities*. C011 definitions are more comprehensive.

**Recommendation**: C001 glossary should reference C011 as authoritative source for agent specs.

---

### Validators
| Repo | Definition | Focus |
|------|------------|-------|
| C004_star-extraction | JSON Schema + Pydantic validation | Story data quality |
| C010_standards | Houston compliance validators | Houston configuration |

**Resolution**: Different validator implementations for different domains. Not a true conflict.

**Recommendation**: Add domain prefix when referencing:
- "Story Validators" (C004)
- "Houston Validators" (C010)

---

### Voice Commands
| Repo | Definition | Focus |
|------|------------|-------|
| C007_the_cavern_club | TTS with personality-aware voices | Text-to-Speech output |
| C016_prompt-engine | Speech-to-text for prompt generation | Speech-to-Text input |
| C017_brain-on-tap | Natural language input adapter | Speech-to-Text input |

**Resolution**: C007 is about voice *output* (TTS); C016/C017 are about voice *input* (STT). Different directions.

**Recommendation**:
- Rename C007 entry to "Betty Voice" (already an alias)
- Keep "Voice Commands" for STT contexts

---

### Query Playbooks
| Repo | Definition | Status |
|------|------------|--------|
| C016_prompt-engine | Being ported to Brain on Tap | Deprecated |
| C017_brain-on-tap | Active query plans for context generation | Active |

**Resolution**: C016 is archived, C017 is the active implementation.

**Recommendation**: Remove from C016 glossary (marked deprecated) or add "DEPRECATED" prefix.

---

## 🔴 Critical Conflicts

**None identified.** All term variations are either aligned or have minor differences that can be documented.

---

## Term Consolidation Recommendations

### High Priority
1. **Houston**: Add cross-reference between C001 (implementation) and C011 (spec)
2. **Agent specs (Orpheus/Scribe/Archivist)**: C011 should be authoritative; C001 should reference

### Medium Priority
3. **Voice terminology**: Disambiguate TTS (Betty Voice) from STT (Voice Commands)
4. **Validators**: Add domain prefixes when used across repos

### Low Priority
5. **Query Playbooks**: Mark C016 entry as deprecated, point to C017
6. **RAG**: Consider consolidating under universal schema with implementation variants

---

## Statistics

| Category | Count |
|----------|-------|
| Total unique terms | 168 |
| Terms in 2+ repos | 16 |
| Aligned (no action) | 8 |
| Minor variations | 6 |
| Critical conflicts | 0 |
| Repos processed | 17 |

---

## Next Steps

1. **Update C001 glossary**: Add references to C011 for agent specifications
2. **Create alias registry**: Track term → canonical term mappings
3. **Implement glossary linter**: Validate cross-references in future glossary updates
4. **Quarterly review**: Re-run mesh analysis to catch drift

---

*Generated by Betty/AI Glossary Mesh v1 — Swarm Pass*
