# Cross-Platform Hooks Policy

**Status:** Active
**Created:** 2025-12-28

## Principle

Hooks should be **platform-agnostic or advisory only**. Enforcement should live in **Python entrypoints** (validators) and **CI**, not shell scripts that assume macOS paths.

## Rationale

This workspace syncs between macOS and Windows via Syncthing. Shell-based pre-commit hooks configured on one platform often fail on the other due to:

- Hardcoded paths (e.g., `/Users/...` vs `C:\Users\...`)
- Missing tools (e.g., `pre-commit` installed in a macOS-only virtualenv)
- Shell incompatibilities (bash vs PowerShell)

When hooks fail silently or block commits on one platform, developers bypass them with `--no-verify`, defeating their purpose.

## Policy

### 1. Enforcement lives in Python and CI

- **Validators** (`validators/*.py`) are the source of truth for code standards
- **CI workflows** run validators on every push/PR
- Exit codes are meaningful: `0`=pass, non-zero=fail

### 2. Hooks are advisory

- Pre-commit hooks MAY exist but MUST NOT be the only enforcement point
- Hooks SHOULD call Python entrypoints (e.g., `python validators/run_all.py`)
- Hooks SHOULD gracefully degrade if tools are missing

### 3. Platform-agnostic hook template

If a repo uses pre-commit hooks, prefer this pattern:

```bash
#!/usr/bin/env bash
# .git/hooks/pre-commit

# Advisory: runs validators if Python available, warns otherwise
if command -v python &> /dev/null; then
    python validators/run_all.py
    exit $?
else
    echo "[WARN] Python not found, skipping pre-commit validation"
    echo "[WARN] CI will enforce standards on push"
    exit 0
fi
```

### 4. No hardcoded paths

Hooks MUST NOT contain:
- Absolute paths to user directories
- Platform-specific tool locations
- Virtualenv activations that assume a specific path

## Migration

Repos with macOS-only hooks should:

1. Keep the hook but make it advisory (exit 0 on missing tools)
2. Add equivalent CI enforcement
3. Document in repo README that `--no-verify` is acceptable if validators pass manually

## See Also

- `validators/README.md` - validator suite documentation
- `protocols/cross_platform_claude_md.md` - cross-platform CLAUDE.md standard
