# Repo Registry Schema

**Version**: 1.1
**Location**: `C010_standards/registry/repos.yaml`

## Structure

The registry is a YAML file with a single top-level key `repos` containing a list of repo entries.

```yaml
repos:
  - repo_id: C017_brain-on-tap
    name: Brain on Tap
    purpose: Real-time context generation...
    # ... other fields
```

## Fields

### Required

| Field | Type | Description |
|-------|------|-------------|
| `repo_id` | string | Unique identifier. Format: `{series}{num}_{name}` (e.g., `C017_brain-on-tap`) |
| `name` | string | Human-readable display name |
| `purpose` | string | One to three sentences describing what this repo does |
| `authoritative_sources` | list[string] | Paths to canonical content (repo-relative, e.g., `40_src/`, `schemas/`) |
| `contracts` | list[string] | Invariants, rules, or commitments this repo makes |
| `status` | enum | One of: `active`, `deprecated` |

### Optional

| Field | Type | Description |
|-------|------|-------------|
| `philosophy` | string | Design philosophy or guiding principle |
| `interfaces` | list[string] | How to interact—**must be strings, NOT dicts** |
| `tags` | list[string] | Searchable keywords for discovery |

### Interface Format (Important)

The `interfaces` field must be a **list of strings**, not a list of dicts. This avoids YAML parsing ambiguity.

**Correct** (string format):
```yaml
interfaces:
  - "CLI: bbot render <profile>"
  - "Python: brain_on_tap.engine"
  - "API: http://localhost:8820/health"
```

**Wrong** (dict format—will cause parsing issues):
```yaml
interfaces:
  - type: CLI
    command: bbot render <profile>
```

Use the pattern `"<type>: <value>"` as a single string.

## Examples

### Minimal Entry

```yaml
- repo_id: C099_example
  name: Example Repo
  purpose: Demonstrates minimal registry entry.
  authoritative_sources:
    - README.md
  contracts:
    - Betty Protocol compliance
  status: active
```

### Full Entry

```yaml
- repo_id: C017_brain-on-tap
  name: Brain on Tap
  purpose: Real-time context generation with query playbooks. Provides dynamic primer injection for Claude Code sessions.
  philosophy: Context is computed, not stored. Generate what the agent needs at session start.
  authoritative_sources:
    - brain_on_tap/profiles/
    - brain_on_tap/playbooks/
    - brain_on_tap/engine.py
  contracts:
    - Profile YAML schema (agent_type, slices, inject patterns)
    - Primer output format (markdown with structured sections)
    - Playbook execution protocol
  interfaces:
    - CLI: bbot primer <profile>
    - CLI: bbot render <profile>
    - Python API: brain_on_tap.engine
  status: active
  tags:
    - context-generation
    - primers
    - profiles
```

## Validation

Quick check that YAML loads and has expected structure:

```bash
python3 -c "
import yaml, pathlib
p = pathlib.Path('registry/repos.yaml')
data = yaml.safe_load(p.read_text())
repos = data.get('repos', [])
print(f'repos: {len(repos)}')
for r in repos:
    assert 'repo_id' in r, f'Missing repo_id in {r}'
    assert 'status' in r, f'Missing status in {r}'
print('schema valid')
"
```

## Conventions

- Use repo-relative paths in `authoritative_sources`, not absolute filesystem paths
- `repo_id` must match the actual directory name
- Bucket entries (e.g., `W-series`) are allowed for grouping related repos
- Keep `purpose` concise—this is metadata, not documentation
