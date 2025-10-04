# DocMeta Schema v1.2 (Canonical Copy)

_Source: `/Users/jeremybradford/SyncedProjects/P002_sadb/10_docs/SADB_DocMeta_Schema_v1.2.md` • Retrieved for consolidation into P210 metadata governance repo._

Document metadata schema for SADB knowledge base, optimized for retrieval and governance.

## Schema Definition

```yaml
schema: "DocMeta.v1.2"
doc:
  sha256: "<sha256_bytes>"
  title: "<human-readable title>"
  description: |
    <3–6 sentence abstract optimized for retrieval>
  type: ["report"|"research"|"receipt"|"email"|"spec"|"note"|"conversation"|"code"|"data"]
  language: "en"
  created: "<YYYY-MM-DD>"
  authors: ["<optional>"]
  projects: ["SADB", "CloudMD", "ParallelLLMs", "GlobalWork", "Betty", "MCP", "VelvetBetty"]
  topics: ["parallel LLMs", "indexing", "audit", "fingerprints", "deduplication", "metadata"]
  keywords: ["<search terms>"]
  entities:
    people: []
    orgs: []
    products: []
  connections:
    conversations: ["<chat-id or file ref>"]
    related_docs:  ["<sha256 or path>"]
  governance:
    pii: false
    confidential: false
    license: "internal"
  routing:
    canonical: true
    live: true
    tags: ["source:incoming", "priority:high", "auto:llama-turbo"]
  notes: |
    <optional curatorial notes>
```

## Field Descriptions

### Core Fields (Required)
- **schema**: Version identifier, always "DocMeta.v1.2"
- **doc.sha256**: SHA256 hash of document content
- **doc.title**: Specific, unambiguous title for discovery
- **doc.description**: 3-6 sentence abstract optimized for retrieval
- **doc.type**: Document category (conversation, report, code, etc.)

### Temporal & Attribution
- **doc.created**: Creation date (YYYY-MM-DD format)
- **doc.authors**: List of document authors/contributors
- **doc.language**: ISO language code (default: "en")

### Classification & Discovery
- **doc.projects**: Associated projects (SADB, CloudMD, ParallelLLMs, etc.)
- **doc.topics**: High-level topics for navigation
- **doc.keywords**: Specific search terms for retrieval

### Entity Extraction
- **entities.people**: Person names mentioned
- **entities.orgs**: Organizations referenced
- **entities.products**: Products/tools mentioned

### Relationships
- **connections.conversations**: Linked chat/conversation IDs
- **connections.related_docs**: Related documents by SHA256 or path

### Governance & Compliance
- **governance.pii**: Contains personally identifiable information
- **governance.confidential**: Contains confidential information
- **governance.license**: Usage license (internal, public, restricted)

### Routing & Operations
- **routing.canonical**: Is this the authoritative version?
- **routing.live**: Should this appear in search results?
- **routing.tags**: Operational tags for filtering/routing

### Notes
- **notes**: Free-form curatorial notes, observations, or warnings

## Usage Guidelines

1. **For Documents**: Fill all core fields. Infer projects and topics from content.
2. **For Conversations**: Set type="conversation", include date range in description.
3. **For Code**: Set type="code", include language/framework in keywords.
4. **For Receipts**: Set type="receipt", link to related operations in connections.

## Examples

### Document Example
```yaml
schema: "DocMeta.v1.2"
doc:
  sha256: "a1b2c3d4e5f6..."
  title: "SADB Fingerprinting Architecture Design"
  description: |
    Technical specification for the three-layer fingerprinting system used
    in SADB for document deduplication. Covers byte-identity (SHA256),
    content-identity (SimHash), and semantic fingerprints (embeddings).
    Includes implementation details and performance benchmarks.
  type: "spec"
  language: "en"
  created: "2025-09-14"
  authors: ["Jeremy Bradford"]
  projects: ["SADB"]
  topics: ["fingerprints", "deduplication", "architecture"]
  keywords: ["simhash", "sha256", "hamming distance", "near-duplicate"]
  routing:
    canonical: true
    live: true
    tags: ["source:10_docs", "auto:llama-turbo"]
```

### Conversation Example
```yaml
schema: "DocMeta.v1.2"
doc:
  sha256: "f6e5d4c3b2a1..."
  title: "ChatGPT Export Processing and Trace Extraction Session"
  description: |
    Technical conversation about processing ChatGPT exports, extracting
    traces, and building source registries. Covers harvest scripts,
    trace normalization, and Obsidian note generation. Resulted in
    20,873 traces extracted from 157 conversations.
  type: "conversation"
  language: "en"
  created: "2025-09-14"
  projects: ["SADB", "ChatGPT"]
  topics: ["data extraction", "trace analysis", "source registry"]
  keywords: ["harvest", "traces", "jsonl", "chatgpt export"]
  connections:
    related_docs: ["kv_phase4_traces_2025-09-14_160358.md"]
  routing:
    canonical: true
    live: true
    tags: ["source:chatgpt", "batch:2025-09-14"]
```
