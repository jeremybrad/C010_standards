# Receipt: CI Compliance Gate Rollout

**Date:** 2026-01-01
**Repo:** C010_standards
**Scope:** GitHub Actions CI — Workspace Compliance Check
**Outcome:** ✅ Deployed + Verified (hard/soft gate behavior confirmed)

---

## Summary

Deployed a CI compliance gate that validates the workspace compliance tooling and enforces a **hard stop** on **unclassified violations** for push-to-main and manual runs (when `blocking=true`). The workflow runs successfully on GitHub and uploads artifacts for audit visibility.

This completes the "standards are observable + enforceable" leg of the rollout:
- **Observable:** compliance report + exceptions register are produced and uploaded as artifacts
- **Enforceable:** hard gate blocks main when STOP conditions exist
- **Diagnosable:** logs show explicit gate decision

---

## Deliverables

### Workflow file
- **Added:** `.github/workflows/compliance.yml`
- **Commit:** `2dd3681`
- **Behavior:**
  - Push to `main`: hard gate (fails on unclassified violations)
  - PRs: soft gate (report-only)
  - Weekly schedule: soft gate (report-only)
  - Manual (`workflow_dispatch`) with `blocking=true`: hard gate

### CI Artifact Outputs
- Compliance report (generated/parsed by workflow)
- Temporary exceptions register / exception inputs (uploaded for visibility)
- Retention: **30 days**

---

## Verification Evidence

### GitHub Actions run (proof of execution)
- **Workflow:** Workspace Compliance Check
- **Trigger:** push to `main`
- **Run ID:** `20645272892`
- **Run URL:** https://github.com/jeremybrad/C010_standards/actions/runs/20645272892
- **Result:** `completed / success`

### Key log lines (gate decision)
- `compliance-check  Gate decision  Gate passed: No unclassified violations`
- `has_stop_condition = false` (derived from report parsing)
- `Unclassified violations = 0`

### Local verification commands used
- `gh run list -R jeremybrad/C010_standards --workflow compliance.yml --branch main --limit 10`
- `gh run view 20645272892 -R jeremybrad/C010_standards --log`

---

## Gate Logic

### STOP condition
The workflow hard-fails (exit != 0) when:
- **Unclassified violations > 0**, meaning violations exist that are not categorized as:
  - compliant
  - permanent exception (justified)
  - temporary exception (in register with remediation gates)
  - excluded (external tool/vendor repo)

### Current graduation path
1) **Now:** Hard gate on push-to-main; soft gate on PRs/scheduled
2) **Next:** Enable PR hard gate (switch conditional)
3) **Later:** Enforce overdue review dates as a failing condition

---

## Notes / Known Constraints

- CI does **not** check out the full workspace; it validates:
  - audit script syntax
  - renderer syntax
  - compliance report parsing and STOP-condition detection
  - exception register structure and review-date monitoring logic

A full "clone-all-repos and audit reality" check remains a future enhancement.

---

## Follow-ups

- [ ] Decide when to graduate PR runs from soft gate to hard gate.
- [ ] Decide whether overdue review dates should fail scheduled runs or only fail blocking/manual runs.
- [ ] Optional: add a future full-workspace checkout mode (requires repo list + credentials policy).

---

## Final State

✅ CI compliance gate deployed
✅ CI run verified on GitHub Actions
✅ Hard/soft gate behavior confirmed
✅ Artifacts uploading successfully
✅ Main remains clean and protected against unclassified violations
