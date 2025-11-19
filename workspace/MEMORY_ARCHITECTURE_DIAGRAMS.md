# Memory System Architecture Diagrams

**Visual guide to Jeremy's memory and knowledge systems**

---

## Complete Memory Ecosystem

```mermaid
flowchart TB
    subgraph Sources["Data Sources"]
        Chat[ChatGPT Exports]
        Claude[Claude Exports]
        Council[Council Logs]
        Terminal[Terminal History]
        Live[Live Conversations]
    end

    subgraph RealTime["Real-Time Memory (P159)"]
        Session[CLAUDE_SESSION.md<br/>Auto-rotates @ 100KB]
        Context[CLAUDE_CONTEXT.md<br/>Curated context]
        ChromaDB[ChromaDB Vector DB<br/>Semantic search]
        MCP[MCP Memory Server<br/>Docker-based]
        Obsidian[Obsidian Vault<br/>Knowledge management]
    end

    subgraph Batch["Batch Processing (SADB)"]
        C002[C002_sadb<br/>Core Processing]
        C003[C003_sadb_canonical<br/>Refinement Pipeline]
        C008[C008_CBFS<br/>Biographical Facts]
        P005[P005_mybuddy<br/>Digital Twin]
    end

    subgraph Additional["Additional Systems"]
        P190[P190_metadata<br/>Parallel extraction]
        P181[P181_terminal<br/>Terminal insights]
        C009[C009_mcp-http<br/>MCP server]
    end

    %% Real-time flow
    Live --> Session
    Session --> Context
    Context --> ChromaDB
    ChromaDB --> MCP
    MCP --> Obsidian

    %% Batch flow
    Chat --> C002
    Claude --> C002
    Council --> C002
    C002 --> C003
    C003 --> C008
    C008 --> P005

    %% Additional flows
    Chat --> P190
    Claude --> P190
    Terminal --> P181
    P181 --> C003

    %% Integration points
    ChromaDB -.-> C002
    Obsidian -.-> C008
    MCP -.-> P005

    style RealTime fill:#e1f5ff
    style Batch fill:#fff4e1
    style Additional fill:#f0f0f0
```

---

## SADB Pipeline (Detailed Stages)

```mermaid
flowchart LR
    subgraph Input["Raw Data"]
        ChatGPT[ChatGPT<br/>conversations.json]
        Claude[Claude<br/>Exports]
    end

    subgraph C002["C002_sadb (Core)"]
        Chunk[Chunking<br/>1.5k tokens<br/>400 overlap]
        Consensus[3-Pass Consensus<br/>Multi-model agreement]
        Review[Human Review<br/>Web UI/CLI]
        SQLite[(SQLite DB)]
        Twin[twin_feed_v1.ndjson<br/>Facts + Preferences]
    end

    subgraph C003["C003_sadb_canonical (Stages)"]
        S0[S0: Capture<br/>SHA256 dedup<br/>Receipts]
        S1[S1: Normalize<br/>Schema validation<br/>Leak scanning]
        S2[S2: Enrich<br/>BERTopic GPU<br/>70,539 windows]
        M1[M1: Q/A Memory<br/>4,092 pairs]
        U1[U1: Segments<br/>108K utterances]
        J1[J1: Fact Extraction<br/>508 merged facts]
        B1[B1: Braided Timeline<br/>95K events]
    end

    subgraph C008["C008_CBFS"]
        Import[Import from J1]
        YAML[(YAML Database<br/>232 facts)]
        Privacy[Privacy Tiers<br/>Confidence Scores]
    end

    subgraph P005["P005_mybuddy"]
        Chroma[(Chroma Vector DB)]
        RAG[RAG Engine]
        LLM[Local LLMs<br/>via Ollama]
    end

    ChatGPT --> Chunk
    Claude --> Chunk
    Chunk --> Consensus
    Consensus --> Review
    Review --> SQLite
    Review --> Twin

    SQLite --> S0
    S0 --> S1
    S1 --> S2
    S2 --> M1
    M1 --> U1
    U1 --> J1
    S1 --> B1
    J1 --> B1

    J1 --> Import
    Import --> YAML
    YAML --> Privacy

    Twin --> Chroma
    Privacy -.-> Chroma
    Chroma --> RAG
    RAG --> LLM

    style C002 fill:#fff4e1
    style C003 fill:#e1f5ff
    style C008 fill:#e1ffe1
    style P005 fill:#ffe1f5
```

---

## Memory System Integration Points

```mermaid
graph TB
    subgraph Work["Work Analytics"]
        W001[W001 CMO<br/>Weekly Reports]
        W009[W009 Context<br/>Library]
    end

    subgraph Core["Core Memory"]
        CBFS[C008 CBFS<br/>Biographical Facts]
        MyBuddy[P005 MyBuddy<br/>Digital Twin]
        RealTime[P159 Memory<br/>Real-time ChromaDB]
    end

    subgraph Processing["Data Processing"]
        SADB[C002 SADB<br/>Core Pipeline]
        Canonical[C003 Canonical<br/>S0-S2, M1-B1]
        P190[P190 Metadata<br/>Extraction]
    end

    subgraph Context["Contextual Data"]
        Terminal[P181 Terminal<br/>Command History]
        MCP[C009 MCP<br/>HTTP Memory]
    end

    %% Work queries
    W001 --> CBFS
    W009 --> SADB
    W009 --> CBFS

    %% Core memory feeds
    CBFS --> MyBuddy
    RealTime --> MyBuddy

    %% Processing flows
    SADB --> Canonical
    Canonical --> CBFS
    P190 -.Future.-> Canonical

    %% Context integration
    Terminal --> Canonical
    MCP --> RealTime

    %% Cross-system queries
    RealTime -.Query.-> CBFS
    MyBuddy -.Query.-> Terminal

    style Work fill:#fff4e1
    style Core fill:#e1f5ff
    style Processing fill:#e1ffe1
    style Context fill:#ffe1f5
```

---

## Real-Time vs Batch Memory

```mermaid
flowchart LR
    subgraph RealTime["Real-Time (P159)"]
        direction TB
        Live[Live Conversation]
        Session[Session Buffer<br/>CLAUDE_SESSION.md]
        Rotate{Size > 100KB?}
        Archive[CLAUDE_ARCHIVE/]
        Vector[(ChromaDB<br/>Vector Search)]

        Live --> Session
        Session --> Rotate
        Rotate -->|Yes| Archive
        Rotate -->|No| Session
        Session --> Vector
    end

    subgraph Batch["Batch (SADB)"]
        direction TB
        Export[Export Files<br/>.zip downloads]
        Process[Process Pipeline<br/>C002 → C003]
        Store[(SQLite<br/>Structured Data)]
        Facts[Biographical Facts<br/>C008 CBFS]

        Export --> Process
        Process --> Store
        Store --> Facts
    end

    subgraph Usage["Use Cases"]
        direction TB
        Continuity[Session Continuity<br/>Remember this chat]
        Search[Semantic Search<br/>What did I say about X?]
        Analysis[Historical Analysis<br/>Extract all facts about Y]
        Biography[Biography Building<br/>Comprehensive facts DB]

        RealTime --> Continuity
        RealTime --> Search
        Batch --> Analysis
        Batch --> Biography
    end

    Vector -.Context Feed.-> Process

    style RealTime fill:#e1f5ff
    style Batch fill:#fff4e1
    style Usage fill:#f0f0f0
```

---

## Data Flow: From Conversation to Knowledge

```mermaid
flowchart TD
    Start[💬 User talks with AI]

    subgraph Capture["1. Capture"]
        Live[Live conversation<br/>captured in real-time]
        Export[Export downloaded<br/>from platform]
    end

    subgraph RealTime["2. Real-Time Memory (P159)"]
        Session[Append to<br/>CLAUDE_SESSION.md]
        Check{Size check}
        Rotate[Rotate to archive]
        Embed[Generate embeddings]
        ChromaDB[(Store in ChromaDB)]
    end

    subgraph Batch["3. Batch Processing (SADB)"]
        Import[Import export file]
        Chunk[Semantic chunking]
        Extract[3-pass extraction]
        Normalize[Normalize & validate]
        Enrich[GPU enrichment]
    end

    subgraph Knowledge["4. Knowledge Layer"]
        Facts[(Biographical Facts<br/>C008 CBFS)]
        Twin[Digital Twin<br/>P005 MyBuddy]
        Work[Work Analytics<br/>W001, W009]
    end

    Start --> Capture
    Capture --> Live
    Capture --> Export

    Live --> Session
    Session --> Check
    Check -->|>100KB| Rotate
    Check -->|<100KB| Embed
    Rotate --> Embed
    Embed --> ChromaDB

    Export --> Import
    Import --> Chunk
    Chunk --> Extract
    Extract --> Normalize
    Normalize --> Enrich

    ChromaDB --> Twin
    Enrich --> Facts
    Facts --> Twin
    Facts --> Work
    ChromaDB -.Context.-> Work

    style Capture fill:#fff4e1
    style RealTime fill:#e1f5ff
    style Batch fill:#e1ffe1
    style Knowledge fill:#ffe1f5
```

---

## System Dependencies

```mermaid
graph TB
    subgraph External["External Data"]
        ChatGPT[ChatGPT<br/>Platform]
        Claude[Claude<br/>Platform]
        Terminal[Terminal<br/>Shell History]
    end

    subgraph Core["Core Infrastructure (C-series)"]
        C000[C000 Info-Center<br/>🗺️ Standards Hub]
        C001[C001 Mission Control<br/>⚙️ Orchestration]
        C002[C002 SADB Core<br/>💾 Data Ingestion]
        C003[C003 SADB Canonical<br/>🔬 Refinement]
        C008[C008 CBFS<br/>📋 Biographical Facts]
        C009[C009 MCP HTTP<br/>🔌 Memory Server]
        C010[C010 Standards<br/>📜 Schemas]
    end

    subgraph Personal["Personal Projects (P-series)"]
        P005[P005 MyBuddy<br/>🤖 Digital Twin]
        P159[P159 Memory<br/>💭 Real-Time]
        P181[P181 Terminal<br/>💻 Command History]
        P190[P190 Metadata<br/>📊 Extraction]
    end

    subgraph Work["Work Projects (W-series)"]
        W001[W001 CMO<br/>📈 Reporting]
        W009[W009 Context<br/>📚 Library]
    end

    %% External inputs
    ChatGPT --> C002
    ChatGPT --> P190
    Claude --> C002
    Claude --> P190
    Claude --> P159
    Terminal --> P181

    %% Core dependencies
    C000 -.Standards.-> C002
    C000 -.Standards.-> C003
    C001 -.Orchestrates.-> C002
    C002 --> C003
    C003 --> C008
    P181 --> C003

    %% Personal integrations
    C008 --> P005
    C002 --> P005
    P159 --> P005
    C009 --> P159

    %% Work integrations
    C002 --> W001
    C008 --> W001
    C002 --> W009
    C008 --> W009
    P159 -.Context.-> W009

    %% Future integrations
    P190 -.Planned.-> C003

    style Core fill:#e1f5ff
    style Personal fill:#fff4e1
    style Work fill:#e1ffe1
    style External fill:#f0f0f0

    linkStyle 19,20,21,22 stroke:#999,stroke-dasharray:5
```

---

## Legend

**Color Coding:**
- 🔵 Blue: Core Infrastructure (C-series)
- 🟡 Yellow: Personal Projects (P-series)
- 🟢 Green: Data Processing/Refinement
- 🔴 Pink: Knowledge Output/Usage
- ⚪ Gray: External Systems/Context

**Line Styles:**
- Solid line (→): Direct data flow
- Dotted line (-.->): Context/query relationship
- Dashed line (--): Planned/future integration

**System Prefixes:**
- C### = Core infrastructure
- P### = Personal projects
- W### = Work projects

---

*Generated: 2025-11-19*
*Location: C000_info-center/workspace/MEMORY_ARCHITECTURE_DIAGRAMS.md*
