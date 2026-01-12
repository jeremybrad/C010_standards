# Tier 3 Documentation Specification

**Version**: 1.0.0
**Last Updated**: 2026-01-11
**Purpose**: Content specifications for NotebookLM-ready documentation

---

## Overview

This specification defines the canonical documentation structure for projects that sync to NotebookLM. Documents are organized into three tiers based on project complexity.

---

## Document Tiers

### Tier 1: Required (Every Repo)

| Document | Purpose | Content Spec |
|----------|---------|--------------|
| **README.md** | Entry point, quick mental model | Project name, purpose, install/run commands, status badges |
| **CHANGELOG.md** | Change history | Version entries with dates, semantic versioning |
| **META.yaml** | Project metadata | `version`, `status`, `maintainer`, `created_at`, `last_modified` |

### Tier 2: Extended (Complex Repos)

| Document | Purpose | Content Spec |
|----------|---------|--------------|
| **CLAUDE.md** | Claude Code session guidance | Session recovery, dev commands, key files, gotchas |
| **glossary.yaml** | Domain terms | Term → definition mappings |
| **10_docs/** | Working agreements (Betty Protocol) | Architecture decisions, ADRs |
| **20_receipts/** | Change receipts (Betty Protocol) | Date-stamped work records |

### Tier 3: NotebookLM Deep Reference (7 Docs)

All synced to NotebookLM for AI ingestion. Located in `docs/{project_name}/`.

---

## Tier 3 Content Specifications

### 1. OVERVIEW.md

**Purpose**: System overview, ecosystem fit

**Must Include**:
- What the system is (1-2 sentence summary)
- ASCII diagram showing ecosystem position
- Core components table (name, purpose, location)
- Key capabilities (numbered list)
- Operating modes
- Integration points with other systems
- Why this system exists

**Template Structure**:
```markdown
# {Project} Overview

**Last Updated**: YYYY-MM-DD
**Version**: X.Y.Z

## What Is {Project}?

{1-2 sentence description of what this system does}

## Ecosystem Position

{ASCII diagram showing where this fits in the broader system}

## Core Components

| Component | Purpose | Location |
|-----------|---------|----------|
| **{Name}** | {Brief purpose} | `path/to/file` |

## Key Capabilities

### 1. {Capability Name}
- {Bullet points of features}

### 2. {Capability Name}
- {Bullet points of features}

## Operating Modes

| Mode | Description | Use Case |
|------|-------------|----------|
| **{Mode}** | {Description} | {When to use} |

## Integration Points

| System | Integration Type | Status |
|--------|-----------------|--------|
| {System} | {Type} | Active/Planned |

## Why {Project}?

- **{Benefit 1}** - {explanation}
- **{Benefit 2}** - {explanation}

## Related Documentation

- [QUICKSTART.md](QUICKSTART.md) - Get running in 5 minutes
- [ARCHITECTURE.md](ARCHITECTURE.md) - System design details
- [OPERATIONS.md](OPERATIONS.md) - Day-to-day operation
```

---

### 2. QUICKSTART.md

**Purpose**: Install, run, verification in 5 minutes

**Must Include**:
- Prerequisites (versions, tools needed)
- Installation steps (numbered, copy-paste ready)
- Configuration for each supported tool
- First operations (example commands)
- Verification steps
- Troubleshooting quick fixes

**Template Structure**:
```markdown
# {Project} Quickstart

**Last Updated**: YYYY-MM-DD
**Version**: X.Y.Z

Get {Project} running in 5 minutes.

## Prerequisites

- {Tool} {version}+
- {Tool} {version}+

## Quick Start

### 1. Install

```bash
{installation command}
```

### 2. Configure

```bash
{configuration command}
```

### 3. Verify

```bash
{verification command}
```

## Configuration

### {Tool/Platform Name}

```bash
{configuration steps}
```

## First Operations

### {Operation Name}
```
{example command or prompt}
```

## Troubleshooting

### {Common Issue}
```bash
{fix command}
```

## Next Steps

- [OPERATIONS.md](OPERATIONS.md) - Day-to-day workflows
- [ARCHITECTURE.md](ARCHITECTURE.md) - System design
```

---

### 3. ARCHITECTURE.md

**Purpose**: Component diagram, data flow

**Must Include**:
- System overview ASCII diagram (layers, connections)
- Core principles (numbered)
- Component details (each major module)
- Data flow diagrams (tool calls, auth, etc.)
- Request/response format examples
- Integration points table

**Template Structure**:
```markdown
# {Project} Architecture

**Last Updated**: YYYY-MM-DD
**Version**: X.Y.Z

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                      {Project Name}                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  {ASCII diagram showing system layers and connections}      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Core Principles

1. **{Principle}**: {Explanation}
2. **{Principle}**: {Explanation}
3. **{Principle}**: {Explanation}

## Component Details

### {Component Name} (`path/to/file`)

{Description of component purpose}

**Key Methods:**
```python
# Example code snippet
method_name(param) -> ReturnType
```

### {Component Name} (`path/to/file`)

{Description}

## Data Flow

### {Flow Name}

```
{ASCII diagram showing data flow}
```

## Request/Response Format

### {Format Name}

```python
# Request format
{example}

# Response format
{example}
```

## Integration Points

| Component | Purpose |
|-----------|---------|
| {Name} | {Purpose} |

## Related Documentation

- [CODE_TOUR.md](CODE_TOUR.md) - Navigate the codebase
- [OPERATIONS.md](OPERATIONS.md) - Day-to-day operation
```

---

### 4. CODE_TOUR.md

**Purpose**: File map, key functions

**Must Include**:
- Quick reference table ("I want to..." → "Look at...")
- Directory map (tree structure with annotations)
- Key entry points with code snippets
- Configuration file locations
- Common patterns (with code examples)
- Development commands
- Test file locations

**Template Structure**:
```markdown
# {Project} Code Tour

**Last Updated**: YYYY-MM-DD
**Version**: X.Y.Z

Navigate the {project} codebase efficiently.

## Quick Reference

| I want to... | Look at... |
|--------------|------------|
| {Task} | `path/to/file` |
| {Task} | `path/to/file` |

## Directory Map

```
{project}/
├── src/                    # {Description}
│   ├── __init__.py         # {Description}
│   ├── main.py             # {Description}
│   └── utils/              # {Description}
├── docs/                   # {Description}
├── tests/                  # {Description}
├── pyproject.toml          # {Description}
└── README.md               # {Description}
```

## Key Entry Points

### {File} (`path/to/file`)

```python
# Key code snippet showing entry point
def main():
    ...
```

## Configuration

### {Config File} (`path/to/config`)

```toml
# Key configuration example
[section]
key = "value"
```

## Common Patterns

### {Pattern Name}

```python
# Code example demonstrating the pattern
```

## Development Commands

```bash
# Install
{command}

# Test
{command}

# Build
{command}
```

## Test Files

| Test File | Coverage |
|-----------|----------|
| `tests/test_{name}.py` | {Description} |

## Related Documentation

- [ARCHITECTURE.md](ARCHITECTURE.md) - System design
- [OPERATIONS.md](OPERATIONS.md) - Day-to-day operation
```

---

### 5. OPERATIONS.md

**Purpose**: Run modes, day-to-day workflows, troubleshooting

**Must Include**:
- Operating modes (each mode with command)
- Daily workflows (startup, health checks, recovery)
- Common operations (example commands)
- Context/resource management
- Rate limits / quotas
- Troubleshooting quick reference (symptom → fix tables)
- Tool categories (read-only, write, destructive)
- Log locations
- Upgrade procedures

**Template Structure**:
```markdown
# {Project} Operations

**Last Updated**: YYYY-MM-DD
**Version**: X.Y.Z

Day-to-day operation of {Project}.

## Operating Modes

### {Mode Name} (Primary)

```bash
{command}
```

{Description of when/how to use}

### {Mode Name}

```bash
{command}
```

## Daily Workflows

### Session Startup

1. {Step}
2. {Step}
3. {Step}

### Health Check

```
{health check command or prompt}
```

| Result | Status |
|--------|--------|
| {Result} | {Meaning} |

### Recovery

When {problem} occurs:

```bash
# 1. {Step}
{command}

# 2. {Step}
{command}
```

## Common Operations

**{Operation}:**
```
{command or prompt}
```

## Resource Management

{Description of context window, memory, or other resource considerations}

## Rate Limits

| Tier | Limit | Notes |
|------|-------|-------|
| {Tier} | {Limit} | {Notes} |

## Troubleshooting Quick Reference

### {Category} Issues

| Symptom | Fix |
|---------|-----|
| {Symptom} | {Fix} |

## Tool/Command Categories

### Read-Only
- `{command}` - {Description}

### Modification
- `{command}` - {Description}

### Destructive (Require Confirmation)
- `{command}` - {Description}

## Log Locations

| Log | Location | Purpose |
|-----|----------|---------|
| {Name} | `{path}` | {Purpose} |

## Upgrading

```bash
{upgrade command}
```

## Related Documentation

- [QUICKSTART.md](QUICKSTART.md) - Initial setup
- [ARCHITECTURE.md](ARCHITECTURE.md) - System design
```

---

### 6. SECURITY_AND_PRIVACY.md

**Purpose**: What stays local, security model

**Must Include**:
- Security principles (numbered)
- Credential storage (location, permissions)
- What gets stored (JSON example)
- What stays local (table: data, location, synced?)
- Network connections table
- Data privacy (what sent, what returned)
- Confirmation pattern explanation
- Threat model (mitigated, accepted, out of scope)
- Security checklist (initial, ongoing)
- Incident response procedures

**Template Structure**:
```markdown
# {Project} Security & Privacy

**Last Updated**: YYYY-MM-DD
**Version**: X.Y.Z

Security model and data protection for {Project}.

## Security Principles

1. **{Principle}** - {Explanation}
2. **{Principle}** - {Explanation}
3. **{Principle}** - {Explanation}

## Authentication Security

### Token/Credential Storage

| Item | Location | Permissions |
|------|----------|-------------|
| {Item} | `{path}` | {permissions} |

### What Gets Stored

```json
// {path}
{
  "key": "value"
}
```

### What Stays Local

| Data | Stored Where | Synced Externally? |
|------|--------------|-------------------|
| {Data} | `{location}` | No |

## Network Security

### Connections Made

| Endpoint | Purpose | Auth Required |
|----------|---------|---------------|
| `{endpoint}` | {Purpose} | Yes/No |

## Data Privacy

### What Data is Sent

| Data Type | When Sent |
|-----------|-----------|
| {Type} | {When} |

### What Data is Returned

| Data Type | Storage |
|-----------|---------|
| {Type} | {Where stored} |

## Confirmation Pattern

{Explanation of confirmation requirements for destructive operations}

### Operations Requiring Confirmation

| Operation | Risk Level | Notes |
|-----------|------------|-------|
| `{operation}` | High/Medium | {Notes} |

## Threat Model

### Mitigated Threats

| Threat | Mitigation |
|--------|------------|
| {Threat} | {Mitigation} |

### Accepted Risks

| Risk | Acceptance Rationale |
|------|---------------------|
| {Risk} | {Rationale} |

### Out of Scope

| Risk | Notes |
|------|-------|
| {Risk} | {Notes} |

## Security Checklist

### Initial Setup

- [ ] {Check item}
- [ ] {Check item}

### Ongoing

- [ ] {Check item}
- [ ] {Check item}

## Incident Response

### {Incident Type}

1. **{Step}**: {Action}
2. **{Step}**: {Action}

## Related Documentation

- [ARCHITECTURE.md](ARCHITECTURE.md) - System design
- [OPERATIONS.md](OPERATIONS.md) - Day-to-day operation
```

---

### 7. OPEN_QUESTIONS.md

**Purpose**: Unresolved decisions, known limitations, future considerations

**Must Include**:
- Architecture questions (current state, question, options table, resolution)
- Known limitations (tables: API, feature, specific subsystem)
- Security considerations
- Feature roadmap questions
- Integration questions
- Performance questions
- Resolved questions table (question, resolution, date)
- Contributing guidance

**Template Structure**:
```markdown
# {Project} Open Questions

**Last Updated**: YYYY-MM-DD
**Version**: X.Y.Z

Unresolved decisions, known limitations, and future considerations.

## Architecture Questions

### {Question Title}

**Current State**: {Description of current implementation}

**Question**: {The actual question}

| Option | Pros | Cons |
|--------|------|------|
| {Option 1} | {Pros} | {Cons} |
| {Option 2} | {Pros} | {Cons} |

**Resolution**: {Current decision or "Pending"}

## Known Limitations

### {Category} Limitations

| Limitation | Impact | Workaround |
|------------|--------|------------|
| {Limitation} | {Impact} | {Workaround} |

## Security Considerations

### {Consideration}

**Question**: {Question}

**Current Approach**: {Description}

**Potential Improvements**: {List}

**Resolution**: {Decision}

## Feature Roadmap Questions

### {Feature}

**Current State**: {Status}

**Question**: {Question}

**Considerations**:
- {Point}
- {Point}

**Resolution**: {Decision}

## Integration Questions

### {Integration}

**Current State**: {Status}

**Question**: {Question}

**Resolution**: {Decision}

## Performance Questions

### {Topic}

**Current State**: {Status}

**Question**: {Question}

**Resolution**: {Decision}

## Resolved Questions

| Question | Resolution | Date |
|----------|------------|------|
| {Question} | {Resolution} | YYYY-MM |

## Contributing Questions

If you encounter an unresolved question:

1. Check existing issues on GitHub
2. Add question to this document with context
3. Propose options if you have ideas
4. Reference related code or API behavior

## Related Documentation

- [ARCHITECTURE.md](ARCHITECTURE.md) - System design context
- [SECURITY_AND_PRIVACY.md](SECURITY_AND_PRIVACY.md) - Security decisions
```

---

## Document Header Format

Every Tier 3 document **must** have this header:

```markdown
# {Title}

**Last Updated**: YYYY-MM-DD
**Version**: X.Y.Z
```

---

## NotebookLM Artifacts (Standard 7)

After docs sync, these artifacts are generated:

| Artifact | Tool | Purpose |
|----------|------|---------|
| Mind Map | `mind_map_create` | Visual concept map |
| Briefing Doc | `report_create` | Executive summary |
| Study Guide | `report_create` | Learning material |
| Audio Overview | `audio_overview_create` | Podcast discussion |
| Infographic | `infographic_create` | Visual summary |
| Flashcards | `flashcards_create` | Memory aids |
| Quiz | `quiz_create` | Comprehension check |

---

## Tier Classification

| Tier | Classification | Criteria |
|------|----------------|----------|
| **simple** | Tier 1 only | README + CHANGELOG + META.yaml |
| **extended** | Tier 1 + Tier 2 | + CLAUDE.md, 10_docs/, 20_receipts/ |
| **kitted** | Tier 1 + 2 + 3 | + all 7 Tier 3 docs |

---

## Path Resolution

Tier 3 docs can be located in:

1. `docs/{repo_name}/` (preferred, e.g., `docs/brain_on_tap/`)
2. `docs/deep_reference/` (alternative naming)
3. `docs/` (flat structure fallback)

Configure per-repo overrides in `canonical_docs.yaml`.

---

## Validation Rules

| Rule | Description |
|------|-------------|
| `has_metadata_header` | First lines contain Version: or Last Updated: or YAML frontmatter |
| `accurate_claims` | Statements about the repo match actual state |
| `code_refs_valid` | File paths and line numbers in the doc exist |
| `working_links` | Internal markdown links resolve |

---

## Related Standards

- [betty_protocol.md](betty_protocol.md) - Folder structure and receipts
- [cross_platform_claude_md.md](cross_platform_claude_md.md) - CLAUDE.md format
- [META_YAML_SPEC.md](META_YAML_SPEC.md) - META.yaml contract

---

*Maintained by: Jeremy Bradford & Claude*
