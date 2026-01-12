# CI Gate Graduation Policy Update

**Date**: 2026-01-12
**Repo**: C010_standards
**Scope**: `.github/workflows/compliance.yml`
**Outcome**: Policy implemented

---

## Summary

Updated the compliance workflow with a graduated gate policy following the 2026-01-11 compliance sweep that achieved 98% workspace compliance (61/62 repos).

---

## Policy Decisions

### 1. PR Hard Gate Graduation

**Decision**: PRs will graduate from soft gate to hard gate on **2026-01-25** (2 weeks after achieving 98% compliance).

**Rationale**:
- Allows time for any remaining edge cases to surface
- Gives developers notice before enforcement begins
- Date is configurable via `PR_GRADUATION_DATE` env var

### 2. Overdue Exception Reviews

**Decision**: Overdue reviews emit **warnings only** for now. Hard fail available via `fail_on_overdue` input.

**Rationale**:
- Exception review process is new
- Avoid blocking legitimate work while process matures
- Hard fail planned for Phase 4 after review cadence is established

---

## Changes Made

### Workflow Updates

1. **Added policy documentation** at top of workflow file
2. **Added `fail_on_overdue` input** for manual override
3. **Added `PR_GRADUATION_DATE` env var** for configurable graduation
4. **Added `Determine gate mode` step** with graduation logic
5. **Updated `Gate decision` step** with:
   - Graduation date check for PRs
   - Overdue review handling (warn vs fail)
   - Summary table in GitHub Step Summary

### Gate Behavior Matrix

| Trigger | Before 2026-01-25 | After 2026-01-25 |
|---------|-------------------|------------------|
| Push to main | Hard gate | Hard gate |
| PR | Soft gate | Hard gate |
| Scheduled | Soft gate | Soft gate |
| Manual (blocking=true) | Hard gate | Hard gate |
| Manual (fail_on_overdue=true) | + Fail on overdue | + Fail on overdue |

---

## Verification

- [ ] Workflow syntax valid (will verify on push)
- [ ] Gate logic handles all trigger types
- [ ] Graduation date configurable
- [ ] Overdue handling respects input flag

---

## Follow-ups

- [ ] Monitor first PR run after this push
- [ ] Review graduation effectiveness on 2026-01-25
- [ ] Evaluate overdue hard fail for Phase 4

---

## Related

- `20_receipts/receipt_ci_compliance_gate_rollout_2026-01-01.md` - Original gate deployment
- `20_receipts/compliance_sweep_20260111.md` - Compliance sweep that triggered graduation
