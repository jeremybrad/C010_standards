# Universal Claude Standards v1.0

**Sources:**
- `/Users/jeremybradford/SyncedProjects/P001_bettymirror/CLAUDE.md`
- `/Users/jeremybradford/SyncedProjects/Infrastructure/CLAUDE.md`

**Last Upstream Update:** 2025-08-19 (per template header)
**Consolidated into P210:** 2025-09-21

The section below mirrors the canonical Universal Claude Standards block shared across repositories. Project-specific guidance has been intentionally omitted.

<!-- BEGIN: UNIVERSAL_CLAUDE_STANDARDS v1.0 -->

## 🚨 BETTY Protocol (MANDATORY)

**Canonical:** **BETTY Protocol** — *Betty's Evidence-Driven Integrity (BEDI)*.  
**Why:** Trust via verification; continuity via documentation.

**Non-negotiables**
1. **Receipts first.** Every non-trivial action produces evidence (log, diff, artifact, screenshot) with **exact paths** in `receipts/` or `70_evidence/`.  
2. **No self-certification.** Work is **Pending Approval** until a human/lead ACKs.  
3. **Keep README accurate.** Update when behavior/setup/decisions change.  
4. **Verify before "done."** Run tests/linters and attach outputs. Show results, not assertions.  
5. **Honesty over impressiveness.** If blocked/unknown, say so; propose a plan.  
6. **Continuity.** Leave next steps and handoff notes.

**ACK flow**: generate receipt → (optional) create **Pending Approval** symlink (TTL, tracked in `symlinks.json`) → send ACK request via `~/bin/ack_receipt.sh` with Drive link from `~/bin/gdrive_share_ttl.py` → close only after explicit ACK.

---

## 🪞 Workspace Standards (BettyMirror)

- **Naming:** `P###_<slug>` (zero-padded). Keep `project_registry.yaml` in sync.  
- **Structure:** prefer `docs/`, `src/`, `tests/`, `receipts/` (or `70_evidence/`), `30_config/`.  
- **Symlinks:** compatibility symlinks get TTL; record in `30_config/symlinks.json`.  
- **Archives:** move stale receipts (>30d) to an archive with index.  
- **File casing:** use `CLAUDE.md` (uppercase).

---

## 🔧 Available Tools & Capabilities

**Claude Desktop — MCP servers**  
filesystem · git · fetch · memory · sequentialthinking · time · everything · gmail · notionhq · mcp-spotify-search · dj-claude

**Claude Code — native**  
File ops · Shell (bash/ls/grep/glob) · WebFetch/WebSearch · NotebookEdit · TodoWrite

**Environment integrations**  
Google Drive sharing (`gdrive_share_ttl.py`) · Betty Bridge (`ack_receipt.sh`) · BettyLint · LaunchAgents · (optional) Ollama on :11434

> If a listed tool isn't active in this repo's runtime, state "not_active_here" rather than deleting it.

---

## 🧩 Data & Formatting Standards

**YAML frontmatter**
```yaml
title: "…"
date: "YYYY-MM-DD"
project_id: "P###_<slug>"
topics: ["…"]
people: ["…"]        # see people.yaml
mood: "neutral|positive|…"
status: "draft|final|deprecated"
confidentiality: "public|internal|private"
tags: ["…"]
```

**Terminology:** BETTY Protocol · Memory Cathedral · SADB (future canonical truth) · Betty Bridge · BettyMirror (workspace standards)

---

## 🎯 Autonomous Operations & Behavior

- **You CAN and SHOULD:** use tools · run tests/linters · write scripts · update README · generate receipts · request ACK
- **Recovery:** attempt fixes · log failures with receipts · escalate with options
- **Boundaries:** never leak secrets · never fabricate outputs

---

## 🧭 Mission & Philosophy (Co-evolution)

Rules are runways, not cages. We use rigor so we can go faster together. Share insights, propose improvements, keep evidence so trust compounds.

---

## ✅ Completion Checklist

- [ ] Receipts saved (exact paths)
- [ ] README/docs updated
- [ ] Tests/linters run; outputs attached
- [ ] Pending Approval + ACK requested (if needed)
- [ ] Next steps / handoff notes

<!-- END: UNIVERSAL_CLAUDE_STANDARDS -->
