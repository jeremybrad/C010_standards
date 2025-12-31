# Receipt: C010 README Repo Card Self-Hosting

**Date**: 2025-12-28
**Session**: Phase B2 - Making README repo card standard self-hosting

## Problem

C010_standards defines the README repo card standard (`protocols/readme_repo_card.md`) and provides the validator (`scripts/validate_readme_repo_card.py`), but its own README.md was missing the BOT:repo_card markers. The standard was not self-hosting.

```bash
$ python3 scripts/validate_readme_repo_card.py ~/SyncedProjects/C010_standards --verbose
Checking C010_standards/README.md...
ERROR: C010_standards: Missing start marker: <!-- BOT:repo_card:start -->
```

## Fix

Added repo card block to `README.md` with all 10 required headings:

1. What this repo is
2. What it is not
3. When to use it
4. Entry points
5. Core architecture
6. Interfaces and contracts
7. Common workflows
8. Footguns and gotchas
9. Related repos
10. Provenance

Content accurately describes C010_standards' role as the workspace standards hub, including:
- Protocols & schemas overview
- Validator usage
- Bootstrap scripts
- Integration with C001 (submodule)
- Common gotchas (KNOWN_PROJECTS.md auto-generation, etc.)

## Validation Output

```bash
$ python3 scripts/validate_readme_repo_card.py ~/SyncedProjects/C010_standards --verbose
Checking C010_standards/README.md...
  Found repo card block (7359 chars)
  Found 10/10 required headings
PASS: C010_standards

$ python3 scripts/validate_readme_repo_card.py ~/SyncedProjects/C010_standards --strict
PASS: C010_standards
```

## Git Status

```
$ git status --short
M  README.md
?? 20_receipts/2025-12-28_c010_readme_repo_card_self_hosting.md
```

## Documentation Impact

DOC_IMPACT: major
DOC_TOUCH: README.md
DOC_NOTE: README now contains self-hosting repo card block with BOT markers. This demonstrates the standard and enables extraction by C017 Brain on Tap.

## Next Steps

- Phase C: Run validator across C001, C002, C003, C017 and add repo cards where missing
- Phase D: Update C017 to prefer README repo card over YAML registry
