# Brain on Tap Repo Eligibility Standard

**Version:** 1.0.0
**Date:** 2025-12-28
**Status:** Active

## Purpose

Define the requirements for a repository to be eligible for Brain on Tap (BBOT) primer injection. Repos meeting this standard can be automatically included in Claude Code session primers, providing consistent context injection.

## Requirements

### MUST (Blocking)

A repo MUST meet all of these requirements to be BBOT-eligible:

| # | Requirement | Validation |
|---|-------------|------------|
| 1 | Valid README repo card block | Passes `scripts/validate_readme_repo_card.py` |
| 2 | Registry entry exists | Entry present in `registry/repos.yaml` |
| 3 | `repo_id` field present | String, matches directory name |
| 4 | `name` field present | String, human-readable display name |
| 5 | `bot_active` field present | Boolean (`true` or `false`) |
| 6 | `path_rel` field present | String, relative path from workspace root |
| 7 | `path_rel` is relative | No leading `/`, no `C:\`, no `~` |

### SHOULD (Advisory)

These improve primer quality but don't block eligibility:

| # | Requirement | Purpose |
|---|-------------|---------|
| 1 | Onboarding fields populated | Richer context for advisors |
| 2 | `tags` field present | Discovery and filtering |
| 3 | `purpose` is concise (<200 chars) | Fits in summary views |
| 4 | `commands` field present | Copy-pasteable CLI examples |

## Registry Fields for BBOT

### Minimum Required Fields

```yaml
repos:
  - repo_id: C010_standards      # MUST: matches directory name
    name: Standards & Governance Hub  # MUST: human-readable
    bot_active: true              # MUST: boolean, enables BBOT injection
    path_rel: C010_standards      # MUST: relative path from SyncedProjects
    # ... other fields
```

### Field Definitions

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `repo_id` | string | MUST | Unique identifier matching directory name |
| `name` | string | MUST | Human-readable display name |
| `bot_active` | boolean | MUST | `true` = include in BBOT primers, `false` = exclude |
| `path_rel` | string | MUST | Relative path from `SyncedProjects/` root |
| `series` | string | OPTIONAL | Inferred from `repo_id` prefix (C, P, W, U) |

### `bot_active` Semantics

- `true`: Repo is available for primer injection
- `false`: Repo exists in registry but is excluded from BBOT

Use `bot_active: false` for:
- Deprecated repos still tracked for reference
- Internal repos not suitable for LLM context
- Repos under construction

### `path_rel` Format

The `path_rel` field uses forward slashes and is relative to the SyncedProjects root:

**Correct:**
```yaml
path_rel: C010_standards
path_rel: P030_ai-services
path_rel: W006_Abandoned_Cart
```

**Wrong:**
```yaml
path_rel: /Users/jeremybradford/SyncedProjects/C010_standards  # Absolute Mac path
path_rel: C:\Users\jerem\SyncedProjects\C010_standards          # Absolute Windows path
path_rel: ~/SyncedProjects/C010_standards                       # Contains ~
path_rel: ./C010_standards                                      # Starts with ./
```

## Validation

### Using the Validator

```bash
# Validate a single repo
python scripts/validate_brain_on_tap_eligibility.py C010_standards

# Validate with verbose output
python scripts/validate_brain_on_tap_eligibility.py C010_standards --verbose

# Validate multiple repos
python scripts/validate_brain_on_tap_eligibility.py C010_standards C017_brain-on-tap C002_sadb
```

### Validation Checks

| Check | Severity | Description |
|-------|----------|-------------|
| README repo card valid | ERROR | Delegates to `validate_readme_repo_card.py` |
| Registry entry exists | ERROR | Entry with matching `repo_id` in `repos.yaml` |
| Required fields present | ERROR | All MUST fields defined |
| `bot_active` is boolean | ERROR | Must be `true` or `false`, not string |
| `path_rel` is relative | ERROR | No absolute paths |
| SHOULD fields present | WARNING | Missing advisory fields |

### Exit Codes

- `0`: All MUST requirements pass
- `1`: One or more MUST requirements fail
- `2`: Configuration or file error

## Migration Guide

### Existing Repos

To make an existing registry entry BBOT-eligible:

1. **Add README repo card** (if missing):
   ```markdown
   <!-- BOT:repo_card:start -->
   ## What this repo is
   ...
   ## Provenance
   ...
   <!-- BOT:repo_card:end -->
   ```

2. **Add BBOT fields to registry entry**:
   ```yaml
   - repo_id: P050_ableton-mcp
     name: Ableton MCP
     bot_active: true                # ADD THIS
     path_rel: P050_ableton-mcp      # ADD THIS
     purpose: ...
   ```

3. **Run validator**:
   ```bash
   python scripts/validate_brain_on_tap_eligibility.py P050_ableton-mcp --verbose
   ```

### New Repos

For new repos, include BBOT fields from the start:

```yaml
- repo_id: P999_new-project
  name: New Project
  purpose: What this project does.
  bot_active: true
  path_rel: P999_new-project
  authoritative_sources:
    - 40_src/
  contracts:
    - Betty Protocol compliance
  status: active
```

## Example: Full Entry

```yaml
- repo_id: C017_brain-on-tap
  name: Brain on Tap
  purpose: Real-time context generation with query playbooks.
  philosophy: Context is computed, not stored.
  bot_active: true
  path_rel: C017_brain-on-tap
  authoritative_sources:
    - brain_on_tap/profiles/
    - brain_on_tap/playbooks/
    - brain_on_tap/engine.py
  contracts:
    - Profile YAML schema (agent_type, slices, inject patterns)
    - Primer output format (markdown with structured sections)
  interfaces:
    - "CLI: bbot primer <profile>"
    - "CLI: bbot render <profile>"
  onboarding:
    - "Run bbot render session.primer.operator to see primer output"
    - "Read brain_on_tap/profiles/ to understand profile structure"
  entry_points:
    - "README.md"
    - "brain_on_tap/engine.py"
  commands:
    - "bbot primer <profile>"
    - "bbot render <profile>"
  status: active
  tags:
    - context-generation
    - primers
    - profiles
```

## Related Standards

- `readme_repo_card.md` - README repo card block format
- `betty_protocol.md` - Evidence-driven development requirements
- `registry/schema.md` - Full registry schema v1.2

## Changelog

- **1.0.0** (2025-12-28): Initial release
