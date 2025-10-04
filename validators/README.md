# Validator Scaffolding

Phase 2 tooling will populate these scripts with real checks. For now they:
- parse basic CLI arguments,
- verify referenced files exist and are valid JSON (where applicable), and
- exit with status `99` to flag unimplemented logic.

## Available Validators
| Target | Module | Purpose |
|--------|--------|---------|
| `houston_docmeta` | `check_houston_docmeta.py` | Enforce DocMeta routing tags, projects, and taxonomy alignment for Houston memories. |
| `houston_features` | `check_houston_features.py` | Validate feature toggle config against JSON schema and trust phases. |
| `houston_tools` | `check_houston_tools.py` | Confirm tool pipelines, phase gates, and capability flags are consistent. |
| `houston_models` | `check_houston_models.py` | Check model fallback chains and config parity across files. |
| `houston_telemetry` | `check_houston_telemetry.py` | Ensure telemetry feeds are fresh and contain required metrics. |

Run via:
```bash
python validators/run_all.py
```
or target specific validators:
```bash
python validators/run_all.py --targets houston_docmeta houston_features
```

As implementations land, adjust exit codes to `0` on success and propagate
meaningful failure codes for CI integration.
