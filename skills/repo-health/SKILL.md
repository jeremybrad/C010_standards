---
name: repo-health
description: >
  Deep repository health scan with drift detection.
  Triggers: "repo health", "drift scan", "check repo health",
  "structure audit", "deep scan", "repo cleanup".
---

# /repo-health

Run the Repo Drift Detector against the current repository (or a specified target).

## What it does

The detector performs tiered drift analysis:

- **Level 1** (fast): Directory inventory, canonical scope globs, stale path patterns, repo contract
- **Level 2** (medium): Cross-doc consistency, internal link validation, META.yaml drift, generator staleness
- **Level 3** (deep): Reference graph, orphan/archive candidates, misplaced artifact detection

The detector auto-profiles the target repo and skips checks that would produce false positives (e.g. validator inventory on repos without `validators/`). Rules are resolved in order: `--rules` flag, then `<repo>/30_config/drift_rules.yaml`, then universal defaults.

## Invocation

```bash
# From within the target repo (uses C010_STANDARDS env var)
python "$C10_STANDARDS/scripts/repo_drift_detector.py" --repo "$(pwd)" --level 2 --verbose

# From within C010_standards itself
python scripts/repo_drift_detector.py --level 2 --verbose

# Scan a different repo
python scripts/repo_drift_detector.py --repo /path/to/target --level 2 --verbose

# With explicit rules file
python scripts/repo_drift_detector.py --repo /path/to/target --rules /path/to/drift_rules.yaml --level 2
```

Set `C10_STANDARDS` to point at the C010_standards repo root for cross-repo use.

## Output

- **Console**: Summary table of findings by severity (CRITICAL / MAJOR / MINOR / INFO)
- **Markdown report**: Written to `70_evidence/drift/<repo_name>/` if that directory exists
- **JSON report**: Same location, with `--format json` or `--format both`
- If the target repo has no `70_evidence/` directory, output is console-only

## Exit codes

| Code | Meaning |
|------|---------|
| 0 | Success (default) or no CRITICAL findings (`--strict`) |
| 1 | CRITICAL findings detected (`--strict` mode only) |
| 2 | Configuration or parse error |

## Interpreting results

- **CRITICAL**: Broken links, inventory mismatches between ground truth and docs — fix immediately
- **MAJOR**: Cross-doc contradictions, stale generators — fix soon
- **MINOR**: Stale path patterns, empty directories — fix at convenience
- **INFO**: Observations, orphan candidates — review when time permits

## Repo profiling

The detector auto-detects:

| Flag | Condition |
|------|-----------|
| `has_validators` | `validators/` with `__init__.py` |
| `has_schemas` | `schemas/` directory exists |
| `has_taxonomies` | `taxonomies/` directory exists |
| `has_meta_yaml` | `META.yaml` at repo root |
| `has_project_primer` | `PROJECT_PRIMER.md` at repo root |
| `has_drift_rules` | `30_config/drift_rules.yaml` exists |

Checks that depend on missing capabilities are skipped with a verbose-mode log message.
