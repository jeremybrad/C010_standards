# Repo Registry v1.2 Receipt

**Date**: 2025-12-27
**Agent**: Claude Code (Opus 4.5)
**Task**: Expand registry with onboarding-grade context

## Summary

Upgraded Repo Registry from v1.1 (card data) to v1.2 (onboarding-grade context). Added 11 new optional fields for advisor primers and new agent onboarding.

## Schema Changes (v1.2)

New optional onboarding fields:
- `story`: Why this repo exists, origin, problem it solves
- `how_it_fits`: Relationship to other repos and workflow
- `architecture`: High-level structure and major components
- `onboarding`: What a new agent should do first
- `entry_points`: Key paths or commands to start
- `key_concepts`: Domain terms that appear in this repo
- `common_tasks`: Most frequent work patterns
- `gotchas`: Sharp edges, common mistakes
- `integration_points`: Interfaces with other repos/tools
- `commands`: Canonical CLI commands (copy-pasteable)
- `glossary_refs`: Pointers to glossary if it exists elsewhere

## Validator Updates

- Added type checking for new string fields (`story`, `how_it_fits`, `architecture`)
- Added type checking for new list[str] fields
- Added `--strict` mode requiring `onboarding` and `entry_points` for active repos

## BOT Slice Added

`command_discoverability` slice added to `protocols/betty_protocol.md`:
- Policy: Commands must be in persistent locations
- Locations: Registry `commands` field, `docs/COMMANDS.md`, BBOT playbooks

## Verification Output

```
$ python3 registry/validate_registry.py --verbose
Validated 5 entries: ['C010_standards', 'C017_brain-on-tap', 'C002_sadb', 'C001_mission-control', 'W-series']
✅ Registry valid: 5 entries

$ python3 registry/validate_registry.py --strict
✅ Registry valid: 5 entries
```

## Example Expanded Entry (C017_brain-on-tap excerpt)

```yaml
- repo_id: C017_brain-on-tap
  name: Brain on Tap
  purpose: Real-time context generation with query playbooks.
  story: |
    Born from the need to give Claude Code sessions rich, consistent context
    without maintaining stale documentation. Instead of static docs, BBOT
    computes primers from live repo state, registry data, and playbooks.
  how_it_fits: |
    BBOT is the context layer for all Claude Code sessions. It reads C010
    standards, queries C002 SADB for knowledge, and renders profiles.
  onboarding:
    - "Run bbot render session.primer.operator to see primer output"
    - "Read brain_on_tap/profiles/ to understand profile structure"
  entry_points:
    - "README.md"
    - "brain_on_tap/engine.py"
  key_concepts:
    - "Primer"
    - "Profile"
    - "Playbook"
  commands:
    - "bbot primer <profile>"
    - "bbot render <profile>"
    - "bbot list"
```

## Files Modified

- `registry/schema.md` - Version 1.2 with new fields documented
- `registry/repos.yaml` - All 5 entries expanded with onboarding fields
- `registry/validate_registry.py` - New field validation + --strict mode
- `protocols/betty_protocol.md` - command_discoverability BOT slice
