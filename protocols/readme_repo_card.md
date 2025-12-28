# README Repo Card Standard

**Version:** 1.0.0
**Date:** 2025-12-28
**Status:** Active

## Purpose

Define a deterministic, extractable "repo card" block within README.md files that provides structured context for LLM primers. This enables automated extraction of repository summaries without parsing free-form markdown.

## Specification

### Marker Format

Every compliant README.md must contain exactly one repo card block:

```markdown
<!-- BOT:repo_card:start -->
... structured content ...
<!-- BOT:repo_card:end -->
```

- Markers are HTML comments (invisible in rendered markdown)
- Exactly one block per README (duplicates are invalid)
- Block must contain all 10 required headings

### Required Headings (10 total)

The following H2 headings must appear inside the repo card block, in any order:

| # | Heading | Purpose |
|---|---------|---------|
| 1 | `## What this repo is` | Purpose and key capabilities |
| 2 | `## What it is not` | Explicit scope boundaries |
| 3 | `## When to use it` | Use case to entry point mapping |
| 4 | `## Entry points` | Key files and directories |
| 5 | `## Core architecture` | System design, diagrams |
| 6 | `## Interfaces and contracts` | APIs, protocols, schemas |
| 7 | `## Common workflows` | CLI commands, typical tasks |
| 8 | `## Footguns and gotchas` | Known issues, workarounds |
| 9 | `## Related repos` | Ecosystem connections |
| 10 | `## Provenance` | Version, date, git SHA |

### Content Guidelines

- **Accuracy over brevity** - Cover all major subsystems
- **Tables for structured data** - Entry points, use cases, interfaces
- **Code blocks for commands** - Copy-paste ready
- **Provenance includes git SHA** - Update on significant changes

### Provenance Section

The `## Provenance` section must include:

```markdown
## Provenance

- **Version**: X.Y.Z
- **Last Updated**: YYYY-MM-DD
- **Git SHA**: abc1234 (or full SHA)
- **Receipts**: 20_receipts/
```

## Validation

### Using the Validator

```bash
# Basic validation
python scripts/validate_readme_repo_card.py /path/to/repo

# Strict mode (exits 1 on any warning)
python scripts/validate_readme_repo_card.py /path/to/repo --strict

# Verbose output
python scripts/validate_readme_repo_card.py /path/to/repo --verbose
```

### Validation Checks

| Check | Severity | Description |
|-------|----------|-------------|
| README exists | ERROR | README.md must exist at repo root |
| Single block | ERROR | Exactly one `BOT:repo_card` block |
| Required headings | ERROR | All 10 headings present |
| Provenance present | WARNING | `## Provenance` contains version info |

### Exit Codes

- `0`: All checks pass
- `1`: One or more errors (or warnings in strict mode)

## Extraction

### Programmatic Access

```python
from brain_on_tap.sources.external_standards import extract_between_markers

readme_text = Path("README.md").read_text()
repo_card = extract_between_markers(
    readme_text,
    "<!-- BOT:repo_card:start -->",
    "<!-- BOT:repo_card:end -->"
)
```

### Error Handling

If markers are missing, extraction returns an actionable error message:

```
[ERROR: No repo card block found. Add <!-- BOT:repo_card:start --> and <!-- BOT:repo_card:end --> markers to README.md]
```

## Example

See `C017_brain-on-tap/README.md` for the gold standard implementation.

## Related Standards

- `betty_protocol.md` - Receipts and evidence requirements
- `META_YAML_SPEC.md` - Project metadata format
- `session_closeout_protocol.md` - Session tracking

## Changelog

- **1.0.0** (2025-12-28): Initial release
