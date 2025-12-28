# Houston Validators

Production-ready validation suite for Houston configuration and document compliance. All validators are fully implemented and exit with proper status codes for CI integration.

**Exit Codes**:
- `0` - Validation passed
- `1` - Validation failed (issues found)
- `2` - Configuration/parse error (file not found, invalid JSON/YAML)

## Available Validators

| Target | Module | Purpose |
|--------|--------|---------|
| `houston_docmeta` | `check_houston_docmeta.py` | Enforce DocMeta routing tags, projects, and taxonomy alignment for Houston memories. |
| `houston_features` | `check_houston_features.py` | Validate feature toggle config against JSON schema and trust phases. |
| `houston_tools` | `check_houston_tools.py` | Confirm tool pipelines, phase gates, and capability flags are consistent. |
| `houston_models` | `check_houston_models.py` | Check model fallback chains and config parity across files. |
| `houston_telemetry` | `check_houston_telemetry.py` | Ensure telemetry feeds are fresh and contain required metrics. |

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

## Platform Compatibility

Validators work on Windows, macOS, and Linux. Unicode characters (checkmarks, etc.) automatically fall back to ASCII equivalents on Windows consoles that don't support UTF-8.

## Dependencies

Optional but recommended:
```bash
pip install pyyaml jsonschema
```

Validators will function without these (with warnings), but full validation requires PyYAML for DocMeta and jsonschema for features validation.
