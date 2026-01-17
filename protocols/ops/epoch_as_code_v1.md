# Epoch-as-Code Specification v1

**Version**: 1.0
**Status**: Active
**Effective Date**: 2026-01-17

## Purpose

Epoch-as-Code provides a machine-readable repo state snapshot (`00_admin/EPOCH.yaml`) that tracks git HEAD, derived artifact checksums (e.g., PROJECT_PRIMER.md), and optional standards submodule state. This enables:

- **Staleness detection**: Quickly determine if derived artifacts need regeneration
- **Reproducibility**: Record exact repo state at a point in time
- **Audit trails**: Track when snapshots were generated and by what tool
- **Submodule tracking**: For consumer repos, record which version of C010_standards is in use

## Terminology

| Term | Definition |
|------|------------|
| **Epoch** | A point-in-time snapshot of repo state captured in EPOCH.yaml |
| **Derived artifact** | A file generated from repo content (e.g., PROJECT_PRIMER.md) |
| **Primer** | The PROJECT_PRIMER.md file, a common derived artifact |
| **Standards submodule** | C010_standards consumed as git submodule in consumer repos |

## Document Structure

EPOCH.yaml lives at `00_admin/EPOCH.yaml` and contains YAML frontmatter:

```yaml
# Required fields
epoch_schema: "c010.epoch.v1"           # Exact match required
repo_id: "C001_mission-control"         # Non-empty repo identifier
repo_head: "a1b2c3d"                     # 7-40 hex characters (git SHA)
generated_at_utc: "2026-01-17T14:30:00Z" # ISO 8601 datetime

# Conditional (required if PROJECT_PRIMER.md exists)
primer:
  sha256: "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"  # pragma: allowlist secret
  path: "PROJECT_PRIMER.md"              # Default, customizable

# Optional (for consumer repos with C010 submodule)
standards:
  submodule_path: "external/standards"
  commit: "abc1234"

# Optional metadata
generator:
  tool: "claude-code"
  version: "1.0.0"

# Extension point
custom: {}
```

## Required Fields

| Field | Type | Description | Validation |
|-------|------|-------------|------------|
| `epoch_schema` | string | Specification version identifier | Must equal `"c010.epoch.v1"` |
| `repo_id` | string | Repository identifier | Non-empty string |
| `repo_head` | string | Git commit SHA at snapshot time | Matches `^[a-f0-9]{7,40}$` |
| `generated_at_utc` | string | When snapshot was generated | Valid ISO 8601 datetime |

## Conditional Fields

| Field | Condition | Description |
|-------|-----------|-------------|
| `primer` | PROJECT_PRIMER.md exists | Block with SHA256 and path of primer file |
| `primer.sha256` | primer block present | SHA256 hash of primer file content |
| `primer.path` | primer block present | Path to primer file (default: `PROJECT_PRIMER.md`) |

## Optional Fields

| Field | Type | Description |
|-------|------|-------------|
| `standards.submodule_path` | string | Path to C010_standards submodule |
| `standards.commit` | string | Commit SHA of standards submodule |
| `generator.tool` | string | Tool that generated this epoch |
| `generator.version` | string | Version of the generating tool |
| `custom` | object | Extension point for tool-specific metadata |

## Validation Rules

### Rule Summary

| Rule | Mode | Description |
|------|------|-------------|
| R1 | Required | `epoch_schema` must equal `"c010.epoch.v1"` |
| R2 | Required | `repo_id` must be non-empty string |
| R3 | Required | `repo_head` must match `^[a-f0-9]{7,40}$` |
| R4 | Required | `generated_at_utc` must be valid ISO 8601 |
| R5 | Conditional | If PROJECT_PRIMER.md exists, primer block is required |
| R6 | Conditional | `primer.sha256` must match actual file content |
| R7 | Strict | `repo_head` must equal current git HEAD |
| R8 | Default | Unknown fields generate warnings |
| R9 | Strict | Unknown fields cause validation failure |
| R10 | Require/Strict | Missing EPOCH.yaml causes exit 1 |

### Standard Mode (Default)

1. **R1 - Schema Check**: `epoch_schema` must exactly equal `"c010.epoch.v1"`
2. **R2 - Repo ID**: `repo_id` must be present and non-empty
3. **R3 - Git Hash**: `repo_head` must be 7-40 lowercase hex characters
4. **R4 - Timestamp**: `generated_at_utc` must be valid ISO 8601 format
5. **R5 - Primer Required**: If `PROJECT_PRIMER.md` exists in repo root, `primer` block required
6. **R6 - Primer Sync**: `primer.sha256` must match SHA256 of actual primer file content
7. **R8 - Unknown Fields**: Unknown top-level fields generate **warnings** but do not cause failure

### Strict Mode (`--strict`)

All standard mode rules apply, plus:

8. **R7 - Head Freshness**: `repo_head` must equal current `git rev-parse HEAD`
9. **R9 - Unknown Fields**: Unknown top-level fields cause validation **failure** (exit 1)
10. **R10 - File Required**: Missing EPOCH.yaml causes exit 1 (implied by `--strict`)

### Missing EPOCH.yaml Behavior

| Mode | Behavior |
|------|----------|
| Default | Warn + exit 0 (allows gradual adoption) |
| `--require` | Exit 1 (enforces epoch tracking) |
| `--strict` | Exit 1 (implies `--require`) |

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | All validations passed (or no EPOCH.yaml in default mode) |
| 1 | Validation failure (missing required field, invalid value, unknown field in strict, missing file when required) |
| 2 | Parse/config error (invalid YAML, file read error) |

## Use Cases

### Staleness Detection

Compare `repo_head` with current git HEAD to determine if derived artifacts may be stale:

```bash
current_head=$(git rev-parse HEAD)
epoch_head=$(grep repo_head 00_admin/EPOCH.yaml | cut -d'"' -f2)

if [ "$current_head" != "$epoch_head" ]; then
    echo "Warning: Epoch is stale, derived artifacts may need regeneration"
fi
```

### Primer Verification

Verify PROJECT_PRIMER.md hasn't been manually edited since epoch generation:

```bash
expected_sha=$(grep -A1 primer 00_admin/EPOCH.yaml | grep sha256 | cut -d'"' -f2)
actual_sha=$(sha256sum PROJECT_PRIMER.md | cut -d' ' -f1)

if [ "$expected_sha" != "$actual_sha" ]; then
    echo "Warning: PROJECT_PRIMER.md has changed since epoch generation"
fi
```

### CI Integration

Use `--strict` mode in CI to enforce epoch freshness:

```yaml
# .github/workflows/epoch.yml
- name: Validate epoch freshness
  run: python validators/check_epoch.py --strict
```

## Versioning Policy

### What Constitutes a Breaking Change (v1 -> v2)

- Adding a new **required** field
- Removing or renaming an existing required field
- Changing the type of a required field
- Changing the `epoch_schema` identifier format
- Changing validation behavior for existing rules

### Non-Breaking Changes (patch versions)

- Adding new **optional** fields
- Relaxing validation rules
- Clarifying documentation
- Adding new validator modes/flags

## Unknown Field Handling

Per the Betty Protocol's extensibility principle:

> "Ignore unknown fields unless explicitly disallowed"

By default, unknown top-level fields in EPOCH.yaml are:
- **Logged as warnings** in verbose mode
- **Ignored** for validation purposes (exit 0)

In `--strict` mode, unknown fields cause validation failure (exit 1) to enforce schema compliance.

## Examples

### Minimal EPOCH.yaml

```yaml
epoch_schema: "c010.epoch.v1"
repo_id: "C010_standards"
repo_head: "abc1234"
generated_at_utc: "2026-01-17T14:30:00Z"
```

### Full EPOCH.yaml with Primer

```yaml
epoch_schema: "c010.epoch.v1"
repo_id: "C001_mission-control"
repo_head: "a1b2c3d4e5f6"  # pragma: allowlist secret
generated_at_utc: "2026-01-17T14:30:00Z"

primer:
  sha256: "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"  # pragma: allowlist secret
  path: "PROJECT_PRIMER.md"

standards:
  submodule_path: "external/standards"
  commit: "def7890"

generator:
  tool: "claude-code"
  version: "1.0.0"

custom:
  last_full_build: "2026-01-16T08:00:00Z"
```

## Validator

Validate EPOCH.yaml using:

```bash
# Default mode: warn if missing, exit 0
python validators/check_epoch.py

# Require mode: exit 1 if missing
python validators/check_epoch.py --require

# Strict mode: require file + verify repo_head matches git HEAD
python validators/check_epoch.py --strict

# Validate specific path(s)
python validators/check_epoch.py /path/to/repo --verbose

# JSON output for CI
python validators/check_epoch.py --json-output results.json
```

## Integration Points

### Consumers

- **CI/CD pipelines**: Verify epoch freshness before deployment
- **Documentation generators**: Check if primer needs regeneration
- **Build systems**: Invalidate caches when epoch changes

### Producers

- **claude-code**: Generate epoch after completing tasks
- **Make/build scripts**: Update epoch after artifact generation
- **Pre-commit hooks**: Warn if epoch is stale

## Related Documents

- [Project Primer Protocol](../project_primer_protocol.md) - Derived artifact standard
- [Betty Protocol](../betty_protocol.md) - Workspace governance standards
- [Capsule Specification](../capsules/capsule_spec_v1.md) - Related metadata standard
