# Repo Registry Schema

**Version**: 1.3
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

### Required (Card Fields)

| Field | Type | Description |
|-------|------|-------------|
| `repo_id` | string | Unique identifier. Format: `{series}{num}_{name}` (e.g., `C017_brain-on-tap`) |
| `name` | string | Human-readable display name |
| `purpose` | string | One to three sentences describing what this repo does |
| `authoritative_sources` | list[string] | Paths to canonical content (repo-relative, e.g., `40_src/`, `schemas/`) |
| `contracts` | list[string] | Invariants, rules, or commitments this repo makes |
| `status` | enum | One of: `active`, `deprecated` |

### Optional (Card Fields)

| Field | Type | Description |
|-------|------|-------------|
| `philosophy` | string | Design philosophy or guiding principle |
| `interfaces` | list[string] | How to interact—**must be strings, NOT dicts** |
| `tags` | list[string] | Searchable keywords for discovery |

### Optional (Standards Applicability) — v1.3

These fields define the repo's compliance obligations. **Missing fields use defaults** during validation (no auto-backfill).

| Field | Type | Description | Default |
|-------|------|-------------|---------|
| `tier` | enum | Documentation level: `1`=basic, `2`=structured, `3`=canonical | `1` |
| `pool` | enum | Rigor level: `personal`, `work`, `archive` | `personal` |
| `enforcement` | enum | Gate behavior: `none`, `advisory`, `hard_gated` | `advisory` |

**Interpretation:**
- `tier` maps to tiered documentation requirements (Tier 1: README only, Tier 2: + CLAUDE.md/rules_now.md, Tier 3: + full Betty Protocol canon)
- `pool: work` activates work pool requirements (evidence packages, verify entrypoints, DATA_SOURCES.md)
- `enforcement: hard_gated` means CI will block on violations; `advisory` means warnings only

### Optional (Onboarding Fields) — v1.2

These fields provide richer context for advisor primers and new agent onboarding.

| Field | Type | Description |
|-------|------|-------------|
| `story` | string | Why this repo exists, its origin, the problem it solves |
| `how_it_fits` | string | Relationship to other repos and overall workflow |
| `architecture` | string | High-level structure and major components |
| `onboarding` | list[string] | What a new agent should do first |
| `entry_points` | list[string] | Key paths or commands to start (README, main modules) |
| `key_concepts` | list[string] | Domain terms that appear in this repo |
| `common_tasks` | list[string] | Most frequent work patterns |
| `gotchas` | list[string] | Sharp edges, common mistakes |
| `integration_points` | list[string] | Interfaces with other repos/tools |
| `commands` | list[string] | Canonical CLI commands (copy-pasteable) |
| `glossary_refs` | list[string] | Pointers to glossary if it exists elsewhere |

**Truncation**: Consumers rendering short cards should truncate `purpose` to ~80 chars. Full context available in onboarding fields.

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
