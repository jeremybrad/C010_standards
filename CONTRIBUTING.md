# Contributing to C010_standards

Thank you for your interest in contributing to C010_standards! This document provides guidelines for contributing to the canonical metadata standards, schemas, and validation tooling for the workspace ecosystem.

## Table of Contents

- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Adding New Validators](#adding-new-validators)
- [Modifying Schemas](#modifying-schemas)
- [Updating Taxonomies](#updating-taxonomies)
- [Testing](#testing)
- [Code Style](#code-style)
- [Pull Request Process](#pull-request-process)
- [Versioning Policy](#versioning-policy)

## Getting Started

C010_standards serves as the single source of truth for:
- Metadata schemas (DocMeta, CodeMeta)
- Taxonomies (topics, content types, emotions)
- Houston agent configuration and validation
- Workspace-wide Python standards (Ruff config)

Changes here affect multiple downstream projects, so please follow these guidelines carefully.

## Development Setup

### Prerequisites

- Python 3.11 or higher
- Git
- pip or pipx for package management

### Installation

```bash
# Clone the repository
git clone https://github.com/jeremybrad/C010_standards.git
cd C010_standards

# Install dependencies
pip install -r requirements.txt -r requirements-dev.txt

# Install pre-commit hooks (optional but recommended)
pre-commit install
```

### Verify Setup

```bash
# Run all validators
python validators/run_all.py

# Run tests
pytest tests/ -v

# Run linter
ruff check validators/

# Run type checker
mypy validators/ --check-untyped-defs
```

All should pass with no errors.

## Making Changes

### Branch Naming

Use descriptive branch names:
- `feature/add-new-taxonomy`
- `fix/docmeta-validation-bug`
- `docs/update-readme`
- `refactor/extract-common-code`

### Commit Messages

Follow conventional commit format:

```
type(scope): brief description

Detailed explanation of changes, motivation, and impact.

- List specific changes
- Reference related issues
- Note breaking changes
```

**Types:**
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `refactor:` Code restructuring
- `test:` Adding or updating tests
- `chore:` Maintenance tasks

**Examples:**
```
feat(validators): add JSON output option to houston_docmeta

Added --json-output flag to enable CI integration. Output includes
pass/fail status and detailed error information.

- Added json output parameter to CLI
- Updated report_validation_results to support JSON
- Added tests for JSON output format
```

## Adding New Validators

### Validator Structure

All validators should follow this pattern:

```python
#!/usr/bin/env python3
"""Validator for [purpose].

[Detailed description of what this validates and why.]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import List

# Import common utilities
sys.path.insert(0, str(Path(__file__).parent.parent))
from validators.common import load_json_config, report_validation_results, verbose_check

DEFAULT_CONFIG = Path("path/to/config.json")


def parse_args(argv: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate [thing]")
    parser.add_argument("--config", default=DEFAULT_CONFIG, type=Path)
    parser.add_argument("--verbose", "-v", action="store_true")
    return parser.parse_args(argv)


def validate_rule_1(config: dict, verbose: bool = False) -> list[str]:
    """Check [specific rule]. Returns list of errors."""
    errors = []
    # Validation logic here
    verbose_check(condition, "Rule 1 passed", verbose)
    return errors


def cli(argv: List[str] | None = None) -> int:
    args = parse_args(argv or [])

    # Load config
    try:
        config = load_json_config(args.config)
    except Exception as e:
        print(f"ERROR: Failed to load config: {e}")
        return 2

    # Run validations
    all_errors: list[str] = []
    all_errors.extend(validate_rule_1(config, args.verbose))
    # Add more validation rules...

    # Build suggestions
    suggestions = {}
    if any("keyword" in e.lower() for e in all_errors):
        suggestions["category"] = ["Remediation step 1", "Remediation step 2"]

    # Report results
    return report_validation_results("Validator name", all_errors, suggestions, args.verbose)


if __name__ == "__main__":
    raise SystemExit(cli())
```

### Register the Validator

Add to `validators/__init__.py`:

```python
AVAILABLE_VALIDATORS: Dict[str, str] = {
    # ... existing validators ...
    "your_validator": "check_your_validator",
}
```

### Add Tests

Create `tests/test_check_your_validator.py`:

```python
"""Tests for check_your_validator."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))
from validators.check_your_validator import validate_rule_1


class TestValidateRule1:
    """Tests for validate_rule_1 function."""

    def test_valid_config(self):
        """Test with valid configuration."""
        config = {"key": "value"}
        errors = validate_rule_1(config)
        assert errors == []

    def test_invalid_config(self):
        """Test with invalid configuration."""
        config = {"wrong": "value"}
        errors = validate_rule_1(config)
        assert len(errors) == 1
        assert "expected" in errors[0].lower()
```

### Exit Codes

Validators must use these exit codes:
- `0`: All validations passed
- `1`: Validation failures found
- `2`: Configuration or parsing errors

## Modifying Schemas

### Schema Files

Schemas live in `schemas/`:
- `docmeta_v1.2.yaml` - Document metadata
- `codemeta_v1.0.yaml` - Code artifact metadata
- `houston_features.schema.json` - Houston features config

### Making Schema Changes

1. **Determine impact**: Is this breaking or non-breaking?
   - **Breaking**: Requires existing documents to be updated
   - **Non-breaking**: Optional additions, clarifications

2. **Update the schema file** with clear comments

3. **Update documentation** in corresponding `.md` file

4. **Update validators** that enforce the schema

5. **Add migration guide** in `notes/CHANGELOG.md` if breaking

6. **Update consuming projects** listed in `notes/SCHEMA_CONSUMERS.md`

### Example

```yaml
# schemas/docmeta_v1.2.yaml
doc:
  # ... existing fields ...
  new_field: "<optional description>"  # Added 2025-11-08: enables X feature
```

Update `notes/CHANGELOG.md`:

```markdown
## 2025-11-08
- **DocMeta v1.2 Enhancement**: Added optional `doc.new_field` for X feature
- Non-breaking change, backward compatible
- Consuming projects: C001_mission-control, C002_sadb
```

## Updating Taxonomies

### Taxonomy Files

Located in `taxonomies/`:
- `topic_taxonomy.yaml` - Technical topics
- `content_taxonomy.yaml` - Document types
- `emotion_taxonomy.yaml` - Emotional tags

### Taxonomy Change Process

**⚠️ WARNING**: Taxonomy changes are potentially breaking changes!

1. **Check usage** across consuming projects first
2. **Add new terms** to the appropriate taxonomy file
3. **Document reason** in comments
4. **Run validators** to ensure no documents break
5. **Communicate changes** to project maintainers

### Example

```yaml
# taxonomies/topic_taxonomy.yaml
topics:
  - monitoring
  - deployment
  - new_topic  # Added 2025-11-08: covers XYZ use case
```

**Then validate:**

```bash
python validators/check_houston_docmeta.py --taxonomy taxonomies/topic_taxonomy.yaml --verbose
```

## Testing

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=validators --cov-report=term

# Run specific test file
pytest tests/test_common.py -v

# Run specific test
pytest tests/test_common.py::TestLoadJsonConfig::test_load_valid_json -v
```

### Test Requirements

- All new validators MUST have tests
- All new functions in `common.py` MUST have tests
- Aim for >80% code coverage
- Test both success and failure cases
- Test edge cases and error handling

### Test Fixtures

Place test data in `tests/fixtures/`:

```
tests/fixtures/
├── valid_houston_features.json
├── invalid_houston_features.json
└── sample_docmeta.yaml
```

## Code Style

### Python Style

We use **Ruff** for linting and formatting:

```bash
# Check code
ruff check validators/

# Format code
ruff format validators/

# Both in one command
ruff check --fix validators/ && ruff format validators/
```

### Type Hints

Use type hints for all function signatures:

```python
def validate_something(config: dict[str, Any], verbose: bool = False) -> list[str]:
    """Validate something and return errors."""
    ...
```

Run type checking:

```bash
mypy validators/ --check-untyped-defs
```

### Docstrings

Use Google-style docstrings:

```python
def my_function(arg1: str, arg2: int = 0) -> bool:
    """Brief description.

    Longer description explaining behavior, assumptions, and side effects.

    Args:
        arg1: Description of arg1
        arg2: Description of arg2, defaults to 0

    Returns:
        True if success, False otherwise

    Raises:
        ValueError: If arg1 is empty
    """
```

## Pull Request Process

### Before Submitting

- [ ] All tests pass (`pytest tests/ -v`)
- [ ] All validators pass (`python validators/run_all.py`)
- [ ] Code is linted (`ruff check validators/`)
- [ ] Code is formatted (`ruff format validators/`)
- [ ] Type checks pass (`mypy validators/ --check-untyped-defs`)
- [ ] Documentation is updated
- [ ] CHANGELOG.md is updated (if applicable)

### PR Template

```markdown
## Description
[What does this PR do?]

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Changes Made
- [List specific changes]
- [Be detailed]

## Testing
- [How was this tested?]
- [What test cases were added?]

## Impact
- [ ] Affects consuming projects (list which ones)
- [ ] Requires schema migration
- [ ] Requires taxonomy updates
- [ ] Breaking change (requires major version bump)

## Checklist
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] All CI checks pass
```

### Review Process

1. Submit PR with clear description
2. Ensure all CI checks pass
3. Address reviewer feedback
4. Squash commits if requested
5. Maintainer will merge when approved

## Versioning Policy

### Schema Versioning

We use semantic versioning for schemas: `MAJOR.MINOR`

- **MAJOR**: Breaking changes (requires document migration)
- **MINOR**: Non-breaking additions or clarifications

Examples:
- `docmeta_v1.2.yaml` → `docmeta_v1.3.yaml` (add optional field)
- `docmeta_v1.2.yaml` → `docmeta_v2.0.yaml` (breaking change)

### Repository Versioning

Git tags for significant milestones:
- `v1.0.0` - Initial Phase 1 consolidation complete
- `v2.0.0` - Phase 2 validators complete
- `v2.1.0` - Added Houston features validator

## Questions?

- Check existing issues: https://github.com/jeremybrad/C010_standards/issues
- Review documentation in `notes/`
- See `CLAUDE.md` for project-specific Claude Code guidance

## License

All contributions will be under the same license as the project (internal use).

---

**Thank you for contributing to C010_standards!** 🎉
