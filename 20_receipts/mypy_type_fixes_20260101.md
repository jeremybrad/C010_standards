# mypy Type Fixes - Closeout Receipt

**Date:** 2026-01-01
**Mission:** Resolve 12 mypy type errors in C010_standards validators
**Agent:** Claude Code (Opus 4.5)
**Session:** C010 Cloud Code Operator

---

## Summary

| Metric | Value |
|--------|-------|
| mypy errors fixed | 12 |
| Files modified | 7 |
| Commits | 2 |
| CI Status | All Green |

---

## Commits

| SHA | Description |
|-----|-------------|
| `567b69e` | fix(types): resolve 12 mypy errors in validators |
| `0e6bf93` | fix(types): remove unused type ignore (CI has stubs) |

---

## Error Categories Resolved

### 1. `no-any-return` (5 errors)
Functions returning `Any` instead of declared type from `json.loads()` / `yaml.safe_load()`.

**Fix:** Added `cast(dict[str, Any], data)` for explicit type narrowing.

**Files:**
- `validators/common.py` - `load_json_config()`
- `validators/check_houston_tools.py` - `load_json()`
- `validators/check_houston_models.py` - `load_json()`
- `validators/check_houston_docmeta.py` - `load_yaml_front_matter()`, `load_yaml_file()`

### 2. `var-annotated` (5 errors)
Missing type annotations on local variables assigned from generic returns.

**Fix:** Added explicit annotations like `errors: list[str] = []` and `suggestions: dict[str, list[str]] = {}`.

**Files:**
- `validators/common.py` - `suggestions` variable
- `validators/check_repo_contract.py` - `errors` variable
- `validators/check_houston_tools.py` - `errors` variable
- `validators/check_houston_docmeta.py` - `errors` variable
- `validators/check_houston_telemetry.py` - `entries` variable

### 3. `arg-type` (1 error)
Type mismatch in latencies list - `list[int | float | Any]` not assignable to `list[float]`.

**Fix:** Used explicit `float()` conversion in list comprehension:
```python
latencies: list[float] = [
    float(e["latency_ms"])
    for e in recent_entries
    if e.get("latency_ms") is not None
]
```

**File:** `validators/check_houston_telemetry.py`

### 4. Dynamic import cast (1 error)
`module.cli` returning `Any` instead of `ValidatorFn`.

**Fix:** Added `cast(ValidatorFn, module.cli)` in `load_validator()`.

**File:** `validators/__init__.py`

---

## Policy Decision: jsonschema type ignore

**Issue:** Local dev environment lacks `types-jsonschema` stubs, causing `import-untyped` error.

**Initial fix (567b69e):** Added `# type: ignore[import-untyped]` comment.

**CI Failure:** GitHub Actions has `types-jsonschema` installed, so the ignore became `unused-ignore` error.

**Final fix (0e6bf93):** Removed the type ignore entirely.

**Policy:** Let CI environment (with stubs) be authoritative. Local devs can:
- Install `types-jsonschema` locally, OR
- Run with `--ignore-missing-imports` for local iteration

---

## CI Verification

All workflows passing on commit `0e6bf93`:

| Workflow | Status |
|----------|--------|
| Lint with Ruff | Pass |
| Test Suite | Pass |
| Secret Detection | Pass |
| Run All Validators | Pass |
| Type Check with mypy | Pass |

---

## Reusable Patterns

### Pattern 1: Cast json/yaml returns
```python
from typing import Any, cast

def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text())
    return cast(dict[str, Any], data)
```

### Pattern 2: Annotate empty collections
```python
errors: list[str] = []
suggestions: dict[str, list[str]] = {}
```

### Pattern 3: Explicit numeric conversion
```python
values: list[float] = [float(x) for x in raw_values]
```

---

## Status: COMPLETE

All mypy errors resolved. CI is green. Ready for future validator development.
