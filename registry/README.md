# Repo Registry

Canonical registry of repositories in the SyncedProjects workspace.

**Location**: `C010_standards/registry/repos.yaml`

## Purpose

Provides structured metadata about repos so consuming tools (e.g., C017_brain-on-tap primers) can render "what is this repo?" context without relying on stale chat history.

## Schema

Each entry in `repos.yaml` follows this schema:

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| `repo_id` | Yes | string | Unique identifier (e.g., `C017_brain-on-tap`, `W-series`) |
| `name` | Yes | string | Human-readable name |
| `purpose` | Yes | string | One-sentence purpose statement |
| `philosophy` | No | string | Design philosophy or guiding principle |
| `authoritative_sources` | Yes | list | Paths to canonical content within the repo |
| `contracts` | Yes | list | Commitments this repo makes (APIs, formats, protocols) |
| `interfaces` | No | list | How to interact with this repo (CLI, API, etc.) |
| `status` | Yes | enum | One of: `active`, `deprecated`, `archived` |
| `tags` | No | list | Searchable keywords |

## Usage

### Reading the Registry (Python)

```python
import yaml
from pathlib import Path

registry_path = Path("C010_standards/registry/repos.yaml")
data = yaml.safe_load(registry_path.read_text())

for repo in data["repos"]:
    print(f"{repo['repo_id']}: {repo['purpose']}")
```

### Rendering Repo Cards

Consuming repos should:
1. Read `repos.yaml` at primer generation time
2. Filter to relevant `repo_id`
3. Render structured context (purpose, contracts, interfaces)

Do **not** duplicate registry content into other repos. Read from source.

## Maintenance

- Add new repos as they reach "active" status
- Update contracts/interfaces when repo capabilities change
- Move to `deprecated` before `archived`
- Keep entries concise—this is metadata, not documentation

## Validation

Quick syntax check:
```bash
python -c "import yaml, pathlib; p=pathlib.Path('registry/repos.yaml'); print('valid:', bool(yaml.safe_load(p.read_text())))"
```
