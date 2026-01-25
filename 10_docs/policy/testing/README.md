# Testing Standards

Standard test configurations for all SyncedProjects repositories.

## Quick Start

### Python Projects (pytest)

```bash
# Copy pytest configuration
cp policy/testing/pytest.ini.template /path/to/your/project/pytest.ini

# Edit paths for your project structure
# - testpaths: tests/, 90_tests/, or 40_src/tests/
# - --cov=: 40_src/, src/, or your source directory
```

### Node.js Projects (Jest)

```bash
# Copy Jest configuration
cp policy/testing/jest.config.js.template /path/to/your/project/jest.config.js
```

### Adding Test Targets to Makefile

```bash
# Option 1: Include the template
echo 'include path/to/Makefile.testing.template' >> Makefile

# Option 2: Copy specific targets you need
```

### GitHub Actions CI

```bash
# Create workflow directory and copy template
mkdir -p /path/to/your/project/.github/workflows
cp policy/testing/github-actions-test.yml.template \
   /path/to/your/project/.github/workflows/test.yml
```

## Workspace Standards

### Coverage Thresholds

| Level | Threshold | Use Case |
|-------|-----------|----------|
| Minimum | 70% | New projects, maintenance mode |
| Standard | 80% | Active development |
| Strict | 90% | Critical infrastructure |

Current workspace default: **70%**

### Standard Markers (pytest)

All Python projects should use these markers consistently:

| Marker | Description | Example |
|--------|-------------|---------|
| `@pytest.mark.unit` | Fast, no I/O | Pure function tests |
| `@pytest.mark.integration` | End-to-end with I/O | API tests, DB tests |
| `@pytest.mark.slow` | Takes > 1 second | Large dataset tests |
| `@pytest.mark.network` | Requires network | External API tests |
| `@pytest.mark.smoke` | Quick sanity check | Basic functionality |
| `@pytest.mark.requires_ollama` | Needs Ollama running | LLM integration tests |

### Test Organization

Follow Betty Protocol directory structure:

```
project/
├── 40_src/           # Source code
├── 90_tests/         # Test files (preferred)
│   ├── unit/
│   ├── integration/
│   └── conftest.py
├── pytest.ini        # Test configuration
└── Makefile          # With test targets
```

Alternative (non-Betty): `tests/` directory in project root.

## Templates

| File | Purpose |
|------|---------|
| `pytest.ini.template` | Python test configuration |
| `jest.config.js.template` | Node.js test configuration |
| `Makefile.testing.template` | Standard test targets |
| `github-actions-test.yml.template` | CI/CD workflow |

## Common Commands

```bash
# Run all tests
make test

# Run fast tests only (skip slow/network)
make test-fast

# Run unit tests only
make test-unit

# Generate coverage report
make coverage

# Run tests in watch mode
make test-watch

# CI mode (strict, quiet)
make test-ci
```

## Bootstrap Script

To apply testing standards to multiple projects:

```bash
# From C010_standards directory
bash scripts/bootstrap_testing.sh --dry-run  # Preview changes
bash scripts/bootstrap_testing.sh            # Apply changes
```

## Projects Without Coverage

Projects that need test infrastructure:

- P030_ai-services (1 ad-hoc test)
- P052_n8n-mcp-setup (0 tests)
- P168_velvet-console (1 test, no config)

Priority: C-series (core infrastructure) first.

## See Also

- [Betty Protocol](../../../protocols/betty_protocol.md) - Workspace governance
- [Python Standards](../python/) - Ruff configuration
- [Project Template](../../../PROJECT_TEMPLATE.md) - New project setup
