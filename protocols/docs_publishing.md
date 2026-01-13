# Workspace Documentation Publishing & Search

**Version**: 1.0.0
**Last Updated**: 2026-01-13
**Status**: Active

## Overview

This protocol defines how workspace documentation is authored, published, and made searchable across the 66+ project ecosystem. It establishes clear ownership boundaries and prevents ad-hoc documentation sprawl.

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     Documentation Lifecycle                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   ┌──────────────────┐                                                      │
│   │  C010_standards  │  AUTHORING                                           │
│   │  (Source of      │  - Protocols, schemas, taxonomies                    │
│   │   Truth)         │  - Tier 3 standards documentation                    │
│   └────────┬─────────┘                                                      │
│            │                                                                 │
│            │ DOCS_GLOBS patterns                                            │
│            ▼                                                                 │
│   ┌──────────────────┐                                                      │
│   │  C019_docs-site  │  PUBLISHING + SEARCH                                 │
│   │  ├── MkDocs      │  - Static site (port 8085)                          │
│   │  └── Docs RAG    │  - Semantic search API (port 8123)                  │
│   └────────┬─────────┘                                                      │
│            │                                                                 │
│            │ HTTP API                                                        │
│            ▼                                                                 │
│   ┌──────────────────┐                                                      │
│   │ C001_mission-    │  UI CLIENT (optional)                                │
│   │ control /docs    │  - Dashboard integration                             │
│   └──────────────────┘                                                      │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Ownership Boundaries

### C010_standards (Authoring)

**Owns**:
- Protocol definitions (`protocols/`)
- Schema specifications (`schemas/`)
- Taxonomies and controlled vocabularies (`taxonomies/`)
- Validator documentation (`validators/`)
- Standards overview and architecture docs (`docs/standards/`)

**Does Not Own**:
- MkDocs site configuration
- FAISS vector indexes
- RAG server implementation
- Search UI components

### C019_docs-site (Publishing + Search)

**Owns**:
- MkDocs configuration and theming
- Static site build pipeline
- FAISS index generation (`rag-export`, `rag-index`)
- Docs RAG API server (port 8123)
- MkDocs server (port 8085)

**Does Not Own**:
- Source content (consumes from C010 and other repos)
- Standards definitions
- Protocol specifications

### C001_mission-control (UI Client)

**May**:
- Consume C019 RAG API for `/docs` search functionality
- Embed C019 MkDocs site in iframe or proxy

**Does Not Own**:
- Documentation authoring
- Search index maintenance

## Update Workflow

When documentation changes in C010:

1. **Edit Source**: Modify files in C010_standards
2. **Commit**: Push changes to C010 main branch
3. **Trigger C019**: Manual or automated trigger to rebuild
4. **Export**: `python -m docs_rag export` extracts markdown
5. **Index**: `python -m docs_rag index` rebuilds FAISS vectors
6. **Build**: `mkdocs build` regenerates static site
7. **Verify**: Query RAG API to confirm new content indexed

```bash
# Example C019 rebuild commands
cd ~/SyncedProjects/C019_docs-site
python -m docs_rag export    # Export from DOCS_GLOBS sources
python -m docs_rag index     # Rebuild FAISS index
mkdocs build                 # Regenerate static site
```

## Configuration

### C019 DOCS_GLOBS

C019 defines which documentation sources to include via `DOCS_GLOBS` patterns:

```yaml
# Example globs in C019 config
docs_globs:
  - "~/SyncedProjects/C010_standards/protocols/*.md"
  - "~/SyncedProjects/C010_standards/docs/**/*.md"
  - "~/SyncedProjects/C010_standards/validators/API.md"
```

### Ports

| Service | Port | Purpose |
|---------|------|---------|
| Docs RAG API | 8123 | Semantic search queries |
| MkDocs server | 8085 | Static documentation site |

## Anti-Patterns (Do Not)

1. **No Ad-Hoc Docs Sites**: Do not create MkDocs, Sphinx, or other doc sites in individual repos. Register documentation publishing needs through C010 → C019 pipeline.

2. **No Duplicate Indexes**: Do not create FAISS or other vector indexes in repos other than C019 for workspace documentation.

3. **No Content Migration**: Do not move protocol/schema authoring from C010 to C019. C019 consumes; C010 authors.

4. **No Direct Embedding**: UI clients should consume C019's API, not embed C010 content directly (loses search capability).

## Discovery

### Finding the Docs Site

- **Registry**: `C019_docs-site` in `registry/repos.yaml`
- **META.yaml**: Listed in C010's `relates_to` section
- **RELATIONS.yaml**: Documented as publishing surface relationship

### Health Check

```bash
# Verify C019 services are running
curl http://localhost:8123/healthz  # RAG API
curl http://localhost:8085          # MkDocs site
```

## Related Documents

- [OVERVIEW.md](../docs/standards/OVERVIEW.md) - C010 ecosystem position
- [betty_protocol.md](betty_protocol.md) - Workspace governance
- [registry/repos.yaml](../registry/repos.yaml) - C019 registry entry
