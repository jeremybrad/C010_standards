# Receipt: Testing Standards Infrastructure

**Date**: 2025-11-28
**Author**: Claude (Opus 4.5)
**Task**: Implement workspace-wide testing standards

## Summary

Created comprehensive testing infrastructure templates and applied them to C-series core projects.

## Files Created

### Templates (policy/testing/)
| File | Purpose |
|------|---------|
| `pytest.ini.template` | Python test config with 70% coverage threshold |
| `jest.config.js.template` | Node.js test config with 70% coverage threshold |
| `Makefile.testing.template` | Standard test targets (test, test-fast, coverage) |
| `github-actions-test.yml.template` | CI/CD workflow for GitHub Actions |
| `README.md` | Testing standards documentation |

### Scripts
| File | Purpose |
|------|---------|
| `scripts/bootstrap_testing.sh` | Automated application of testing standards |

## Projects Updated

| Project | pytest.ini | jest.config.js | Notes |
|---------|------------|----------------|-------|
| C001_mission-control | Created | Created | Full stack |
| C002_sadb | Created | - | Custom config for legacy tests |
| C009_mcp-memory-http | Created | Skipped | Already had Jest coverage |
| C010_standards | Created | - | Self-referential |
| C011_agents | Created | - | |
| C016_prompt-engine | - | Created | Node.js only |
| C017_brain-on-tap | Created | - | |
| C020_pavlok | Created | - | Betty Protocol paths |
| C004_star-extraction | Skipped | - | Already 70% coverage |
| C008_CBFS | Skipped | - | Already 80% coverage |

## Standards Established

### Coverage Thresholds
- **Minimum**: 70% (workspace default)
- **Standard**: 80% (active development)
- **Strict**: 90% (critical infrastructure)

### Standard Markers (pytest)
```python
@pytest.mark.unit        # Fast, no I/O
@pytest.mark.integration # End-to-end with I/O
@pytest.mark.slow        # Takes > 1 second
@pytest.mark.network     # Requires network access
@pytest.mark.smoke       # Quick sanity checks
```

### Makefile Targets
```makefile
make test       # Full suite with coverage
make test-fast  # Skip slow/network tests
make test-unit  # Unit tests only
make coverage   # Generate HTML report
make test-ci    # Strict CI mode
```

## Documentation Updated

- `C010_standards/README.md` - Added Section 6: Testing Standards
- `C010_standards/policy/testing/README.md` - Full testing documentation

## Verification Commands

```bash
# Check coverage threshold applied
grep "cov-fail-under" ~/SyncedProjects/C001_mission-control/pytest.ini

# Run bootstrap on additional projects
./scripts/bootstrap_testing.sh --dry-run ~/SyncedProjects/P030_ai-services

# List all projects with pytest.ini
ls ~/SyncedProjects/*/pytest.ini 2>/dev/null | wc -l
```

## Next Steps

1. Apply to P-series critical projects (P030_ai-services)
2. Add GitHub Actions workflows to C-series repos
3. Refactor C002_sadb ad-hoc tests to pytest format
4. Set up pre-commit hooks for test enforcement
