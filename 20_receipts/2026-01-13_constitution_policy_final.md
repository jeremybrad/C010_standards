# Constitution Guardrail Policy Finalization

**Date**: 2026-01-13
**Operation**: Finalize and document constitution guardrail enforcement policy
**Operator**: Claude Code (Opus 4.5)

## Summary

Finalized the C010 constitution guardrail policy with:
- Fail-only enforcement (no WARN tier)
- NOTICE reporting for observability of contextual exceptions
- Tightened prose check for exit-code definitions missing code 2

## Constitution Truths (Locked)

These are now machine-enforced via `validators/check_constitution.py`:

| # | Rule | Enforcement |
|---|------|-------------|
| 1 | Repo identity is C010_standards only | FAIL if C000_info-center outside 70_evidence/ |
| 2 | Validator exit codes are 0/1/2 only | FAIL if exit code 99 mentioned (unless in "removed/no longer" context) |
| 3 | Canonical invocation from repo root | FAIL if `cd validators` recommended (unless in "wrong/incorrect" example) |
| 4 | Python minimum is 3.11+ | FAIL if lower version stated |
| 5 | KNOWN_PROJECTS path uses 70_evidence/ prefix | FAIL if workspace/KNOWN_PROJECTS.md without prefix |
| 6 | Exit code prose must include code 2 | FAIL if "Exit 0 on pass, 1 on fail" omits code 2 |

## Severity Model

**Fail-only (no WARN tier)**:
- All constitution breaches result in exit code 1
- CI gates on any breach
- No "soft" warnings that could be ignored

**Exit Codes**:
- `0` - All checks passed
- `1` - Validation failure (constitution breach)
- `2` - Configuration/parse/setup error

## Contextual Exceptions

Two patterns are allowed **only** in specific contexts:

| Pattern | Allowed Context | Effect |
|---------|-----------------|--------|
| "exit code 99" | "removed" or "no longer" | Not an error; generates NOTICE |
| "cd validators" | "wrong" or "incorrect" example | Not an error; generates NOTICE |

**Why**: Teaching by contrast and historical documentation should not trigger false positives. The validator recognizes these patterns and records them as notices for observability without failing.

## NOTICE Reporting

When contextual exceptions are detected:
- **Not added to errors** (exit code remains 0 if no other issues)
- **Printed at end** with count and details
- **Provides visibility** into allowed-but-notable patterns

Example output:
```
📋 NOTICES (1 contextual exception(s) detected):
   • 10_docs/notes/TROUBLESHOOTING.md:532: 'cd validators' in 'wrong/incorrect' example (allowed)
✅ Constitution guardrail validation passed
```

## Exit Code Prose Check

Added check for prose patterns like:
- "Exit 0 on pass, 1 on fail" (FAILS if no mention of code 2)
- "exits 0 on pass, 1 on validation failure" (FAILS if code 2 missing)

This closes the drift vector where structured tables show 0/1/2 but inline prose omits code 2.

## Changes Made

| File | Change |
|------|--------|
| `validators/check_constitution.py` | Added NOTICE reporting, prose exit-code check, fixed multiline pattern |
| `20_receipts/2026-01-12_constitution_guardrail.md` | Fixed "Warns" → "Fails" wording |
| `CLAUDE.md` | Fixed "Exit 0 on pass, 1 on fail" → added code 2 |
| `PROJECT_PRIMER.md` | Regenerated (sha256:6f952b67d4a1) |

## Excluded Directories

The following directories are excluded from constitution scanning:
- `70_evidence/` - Historical artifacts and workspace exports
- `20_receipts/` - Change receipts (meta-documentation)
- `.git/`, `venv/`, `.venv/`, `node_modules/` - Infrastructure

## Verification

### Validators Passed (7/7)
```
$ python validators/run_all.py
▶ Running houston_docmeta (check_houston_docmeta)
✅ DocMeta validation passed (0 docs)
✔ houston_docmeta passed
▶ Running houston_features (check_houston_features)
✅ Houston features validation passed
✔ houston_features passed
▶ Running houston_tools (check_houston_tools)
✅ Houston tools validation passed
✔ houston_tools passed
▶ Running houston_models (check_houston_models)
✅ Houston models validation passed
✔ houston_models passed
▶ Running houston_telemetry (check_houston_telemetry)
✅ Houston telemetry validation passed (no telemetry to validate)
✔ houston_telemetry passed
▶ Running repo_contract (check_repo_contract)
[OK] Repo contract validation passed
✔ repo_contract passed
▶ Running constitution (check_constitution)
📋 NOTICES (1 contextual exception(s) detected):
   • 10_docs/notes/TROUBLESHOOTING.md:532: 'cd validators' in 'wrong/incorrect' example (allowed)
✅ Constitution guardrail validation passed
✔ constitution passed
```

### Primer Owner Verified
```
$ generate-project-primer C010_standards
...
| **Owner** | Jeremy Bradford |
...
Hash: sha256:6f952b67d4a1
```

## Acceptance Criteria Status

- [x] Constitution enforcement remains hard FAIL for real breaches
- [x] Exceptions remain narrowly scoped (only in specific contexts)
- [x] Exceptions produce visible NOTICE output without failing CI
- [x] Any "0/1 only" phrasing that omits exit code 2 is caught and fails
- [x] Receipts/docs accurately describe behavior (fail-only; no WARN tier)
- [x] Primer owner displays correctly

---

*Receipt generated by Claude Code (Opus 4.5)*
*Verified by running validators and checking primer output*
