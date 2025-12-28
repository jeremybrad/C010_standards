# Receipt: README Repo Card Standard and Validator

**Date**: 2025-12-28
**Session**: Phase B of deterministic "Repo Card inside README" system

## Summary

Added the README repo card standard document and validator script to C010_standards. This completes Phase B of the repo card system implementation.

## Changes

### protocols/readme_repo_card.md (NEW)

Standard document defining:
- Marker format (`<!-- BOT:repo_card:start -->` / `<!-- BOT:repo_card:end -->`)
- 10 required headings with purposes
- Content guidelines
- Provenance section requirements
- Extraction API reference

### scripts/validate_readme_repo_card.py (NEW)

Validator script with:
- README.md existence check
- Single block validation (rejects duplicates)
- Required heading verification (10 headings)
- Provenance content checks (warnings for missing version/SHA)
- `--strict` mode (treats warnings as errors)
- `--verbose` mode (detailed output)

## Verification

```bash
# Test against C017 (gold standard) - verbose
$ python3 scripts/validate_readme_repo_card.py ~/SyncedProjects/C017_brain-on-tap --verbose
Checking C017_brain-on-tap/README.md...
  Found repo card block (5443 chars)
  Found 10/10 required headings
PASS: C017_brain-on-tap

# Test against C017 - strict mode
$ python3 scripts/validate_readme_repo_card.py ~/SyncedProjects/C017_brain-on-tap --strict
PASS: C017_brain-on-tap

# Test against C010 (no repo card) - should fail
$ python3 scripts/validate_readme_repo_card.py ~/SyncedProjects/C010_standards --verbose
Checking C010_standards/README.md...
ERROR: C010_standards: Missing start marker: <!-- BOT:repo_card:start -->
```

## Usage

```bash
# Basic validation
python scripts/validate_readme_repo_card.py /path/to/repo

# Strict mode (warnings become errors)
python scripts/validate_readme_repo_card.py /path/to/repo --strict

# Verbose output
python scripts/validate_readme_repo_card.py /path/to/repo --verbose
```

## Exit Codes

- `0`: All checks pass
- `1`: One or more errors (or warnings in strict mode)

## Documentation Impact

DOC_IMPACT: major
DOC_TOUCH: protocols/readme_repo_card.md, scripts/validate_readme_repo_card.py
DOC_NOTE: New standard for deterministic README repo card blocks. Enables automated extraction for LLM primers.

## Related

- C017_brain-on-tap: Gold standard implementation
- C017: `brain_on_tap/sources/external_standards.py` - extraction helper
- C017: `brain_on_tap/sources/repo_registry.py` - integration with long-mode repo cards

## Next Steps

1. Add repo card blocks to other C0xx repos
2. Consider adding validator to CI/pre-commit hooks
3. Document in C010 README.md
