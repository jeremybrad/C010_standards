---
capsule_spec: "c010.capsule.v1"
capsule_id: "ba28730a-bec6-4602-bcad-58dd4211443d"
created_at: "2026-01-17T04:15:00Z"
kind: "handoff"
producer:
  tool: "claude-code"
  agent: "standards-editor"
title: "Handoff: Capsule Standard v1 shipped + C001 submodule updated"
summary: "CapsuleMeta v1 spec/schema/validator/examples/tests shipped in C010; META updated; C001 submodule advanced to include validator; consumer guidance clarified."
provenance:
  repo_id: "C010_standards"
  commits:
    - "ceea72e"
    - "758a097"
  consumer_rollout:
    - repo_id: "C001_mission-control"
      commit: "8d3f6e2"
custom:
  role: "operator"
  key_points:
    - "Validator: validators/check_capsulemeta.py; strict mode supported; exit codes 0/1/2."
    - "Examples live at 10_docs/examples/capsules/."
    - "Consumers should run capsulemeta via submodule path or pin validator in tooling."
  next_steps:
    - "C017 PR B: emit capsule_spec in Memory Lab exports + add explicit handoff emitter; update capsule inventory to read custom.role."
    - "Decide policy: how consumer repos should run run_all (targets vs full suite)."
---

## What changed

- Implemented Capsule Standard v1 (`c010.capsule.v1`) with protocol + schema template + validator + examples + tests.
- Registered validator as `capsulemeta` and added docs + changelog entry.
- Updated META.yaml to include new capsule files.

## Files created

| Path | Purpose |
|------|---------|
| `protocols/capsules/capsule_spec_v1.md` | Protocol specification |
| `schemas/capsulemeta_v1.0.yaml` | YAML schema template |
| `validators/check_capsulemeta.py` | Validator (37 tests) |
| `10_docs/examples/capsules/` | handoff, memory_export, activity examples |
| `tests/test_check_capsulemeta.py` | Comprehensive test suite |

## Verification

```bash
# Validate examples
python validators/check_capsulemeta.py 10_docs/examples/capsules/ --verbose
# Expected: exit 0, 3 capsules pass

# Run full suite in C010
python validators/run_all.py
# Expected: exit 0, all 8 validators pass

# From C001 consumer context
cd ~/SyncedProjects/C001_mission-control
python external/standards/validators/run_all.py --targets repo_contract capsulemeta
# Expected: exit 0
```

## Notes

- Running `validators/run_all.py` from a consumer repo fails Houston validators if consumer lacks `30_config/`; consumers should use `--targets repo_contract capsulemeta` or run the suite inside C010.
- Strict mode (`--strict`) treats unknown fields as errors; default mode warns but exits 0.
- Paths are repo-relative by default; use `--absolute-paths` for full paths.
