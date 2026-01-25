# C010 Standards CLI Reference

**Last Updated**: 2026-01-24
**Version**: 1.0.0

Command-line interface for C010_standards development and validation workflows.

## Quick Reference

| I want to... | Run... |
|--------------|--------|
| Run all validators | `make validate` |
| Run tests | `make test` |
| Lint and format code | `make lint-fix format` |
| Full CI check | `make ci` |
| Bootstrap Ruff to workspace | `make bootstrap-ruff` |

## Makefile Targets

### Development Setup

```bash
# Install dependencies
make install

# Install with dev dependencies
make install-dev
```

### Testing

```bash
# Run tests
make test

# Run tests with coverage
make test-cov
```

### Code Quality

```bash
# Lint code (check only)
make lint

# Lint and auto-fix
make lint-fix

# Format code
make format

# Check formatting without changes
make format-check

# Type checking
make typecheck
```

### Validation

```bash
# Run all validators
make validate

# Run specific validators
make validate-features    # Houston features config
make validate-tools       # Houston tools config
make validate-docmeta     # Document metadata
```

### CI/CD

```bash
# Full CI pipeline (lint, format, typecheck, test, validate)
make ci

# Same as ci
make all

# Quick check (lint-fix + test with coverage)
make quick
```

### Workspace Operations

```bash
# Bootstrap Ruff config to all workspace repos
make bootstrap-ruff

# Generate documentation
make docs

# Clean build artifacts
make clean
```

## Validators CLI

Individual validators can be run directly with Python:

```bash
# Run all validators
python validators/run_all.py

# Run specific validators
python validators/run_all.py --targets houston_docmeta houston_features

# Individual validator with verbose output
python validators/check_houston_features.py --verbose

# Output to JSON for CI integration
python validators/check_houston_docmeta.py --json-output results.json
```

### Available Validators

| Validator | Command | Purpose |
|-----------|---------|---------|
| `houston_docmeta` | `python validators/check_houston_docmeta.py` | Document metadata validation |
| `houston_features` | `python validators/check_houston_features.py` | Feature configuration validation |
| `houston_tools` | `python validators/check_houston_tools.py` | Tool pipeline validation |
| `houston_models` | `python validators/check_houston_models.py` | Model deployment validation |
| `houston_telemetry` | `python validators/check_houston_telemetry.py` | Telemetry health validation |
| `capsulemeta` | `python validators/check_capsulemeta.py` | Capsule frontmatter validation |
| `epoch` | `python validators/check_epoch.py` | Epoch-as-code validation |
| `windows_filename` | `python validators/check_windows_filename.py` | Windows filename compatibility |

### Exit Codes

All validators follow consistent exit codes:

| Code | Meaning |
|------|---------|
| 0 | Validation passed |
| 1 | Validation failed (issues found) |
| 2 | Configuration/parse error |

## Related Documentation

- [OPERATIONS.md](OPERATIONS.md) - Day-to-day workflows
- [QUICKSTART.md](QUICKSTART.md) - Initial setup
- [SCHEMAS.md](SCHEMAS.md) - Schema documentation
