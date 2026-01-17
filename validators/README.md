# Houston Validators

Production-ready validation suite for Houston configuration and document compliance. All validators are fully implemented and exit with proper status codes for CI integration.

**Exit Codes**:
- `0` - Validation passed
- `1` - Validation failed (issues found) / Error for `repo_contract`
- `2` - Configuration/parse error (file not found, invalid JSON/YAML) / Contract violations for `repo_contract`

## Available Validators

| Target | Module | Purpose |
|--------|--------|---------|
| `houston_docmeta` | `check_houston_docmeta.py` | Enforce DocMeta routing tags, projects, and taxonomy alignment for Houston memories. |
| `houston_features` | `check_houston_features.py` | Validate feature toggle config against JSON schema and trust phases. |
| `houston_tools` | `check_houston_tools.py` | Confirm tool pipelines, phase gates, and capability flags are consistent. |
| `houston_models` | `check_houston_models.py` | Check model fallback chains and config parity across files. |
| `houston_telemetry` | `check_houston_telemetry.py` | Ensure telemetry feeds are fresh and contain required metrics. |
| `repo_contract` | `check_repo_contract.py` | Validate repository structure (README, .gitignore, receipts, markers). |
| `capsulemeta` | `check_capsulemeta.py` | Validate capsule frontmatter (c010.capsule.v1) in markdown files. |

## Usage

Run all validators:
```bash
python validators/run_all.py
```

Run specific validators:
```bash
python validators/run_all.py --targets houston_docmeta houston_features
```

Run with verbose output:
```bash
python validators/run_all.py --pass-args --verbose
```

### Repo Contract Validator

The `repo_contract` validator checks general repository structure:

```bash
# Validate current repo (auto-discovers git root)
python validators/check_repo_contract.py

# Validate specific repo
python validators/check_repo_contract.py --repo-root /path/to/repo

# Set default via environment variable
export REPO_CONTRACT_ROOT=/path/to/repo
python validators/check_repo_contract.py
```

**Required** (fails if missing):
- `README.md`
- `.gitignore`
- `20_receipts/` directory

**Recommended** (warns if missing):
- `CLAUDE.md`
- `.gitattributes`

**Marker integrity**: If README contains `<!-- BOT:repo_card:start -->`, it must also contain `<!-- BOT:repo_card:end -->`.

## Platform Compatibility

Validators work on Windows, macOS, and Linux. Unicode characters (checkmarks, etc.) automatically fall back to ASCII equivalents on Windows consoles that don't support UTF-8.

See [`protocols/cross_platform_hooks.md`](../protocols/cross_platform_hooks.md) for enforcement and hook guidance.

## Dependencies

Optional but recommended:
```bash
pip install pyyaml jsonschema
```

Validators will function without these (with warnings), but full validation requires PyYAML for DocMeta and jsonschema for features validation.

## Execution Contexts

### Running in C010_standards (full suite)

When running validators inside C010_standards, all validators work because required config files (`30_config/houston-features.json`, etc.) are present:

```bash
cd ~/SyncedProjects/C010_standards
python validators/run_all.py
```

### Running from consumer repos (via submodule)

Consumer repos (like C001_mission-control) consume C010 as a git submodule. The Houston-specific validators (`houston_features`, `houston_tools`, etc.) require config files that only exist in C010, so running `run_all.py` without targets will fail.

**Use `--targets` to run only applicable validators:**

```bash
cd ~/SyncedProjects/C001_mission-control
python external/standards/validators/run_all.py --targets repo_contract capsulemeta
```

**Portable validators** (work in any repo):
- `repo_contract` - Checks repository structure
- `capsulemeta` - Validates capsule frontmatter
- `constitution` - Guardrail compliance

**C010-context validators** (require `30_config/`):
- `houston_docmeta`, `houston_features`, `houston_tools`, `houston_models`, `houston_telemetry`
