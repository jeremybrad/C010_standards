# Repo Registry v1 Receipt

**Date**: 2025-12-27
**Agent**: Claude Code (Opus 4.5)
**Task**: Create canonical Repo Registry in C010_standards

## Summary

Created a queryable Repo Registry so consuming repos (especially C017 Brain on Tap) can render "what is this repo and why does it exist?" without relying on chat history.

## Files Created

1. `registry/repos.yaml` - Main registry file with repo metadata
2. `registry/README.md` - Usage guide
3. `registry/schema.md` - Schema specification with field definitions and examples

## Files Modified

1. `protocols/betty_protocol.md` - Added BOT slice `repo_registry_usage`

## Schema

| Field | Required | Description |
|-------|----------|-------------|
| repo_id | Yes | Unique identifier (e.g., C017_brain-on-tap) |
| name | Yes | Human-readable name |
| purpose | Yes | One-sentence purpose statement |
| philosophy | No | Design philosophy |
| authoritative_sources | Yes | Paths to canonical content |
| contracts | Yes | Commitments (APIs, formats, protocols) |
| interfaces | No | How to interact (CLI, API) |
| status | Yes | active/deprecated/archived |
| tags | No | Searchable keywords |

## Repos Included

1. **C010_standards** - Standards & Governance Hub
2. **C017_brain-on-tap** - Brain on Tap (context generation)
3. **C002_sadb** - Self-As-Database (knowledge extraction)
4. **C001_mission-control** - Mission Control (credential vault)
5. **W-series** - Work/Analytics Projects (bucket entry)

## Verification Output

```
File exists: True
Entry count: 5

Entries:
  - C010_standards: active
  - C017_brain-on-tap: active
  - C002_sadb: active
  - C001_mission-control: active
  - W-series: active

YAML validation: PASSED
```

## BOT Slice Added

Added `<!-- BOT:repo_registry_usage:start -->` marker to `protocols/betty_protocol.md` for dynamic injection by C017.

## Usage

Consuming repos read the registry:
```python
import yaml
from pathlib import Path
data = yaml.safe_load(Path("C010_standards/registry/repos.yaml").read_text())
for repo in data["repos"]:
    print(f"{repo['repo_id']}: {repo['purpose']}")
```
