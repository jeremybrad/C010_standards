# Project Documentation Template

**Use this template when documenting each project in the session files.**

---

## [PROJECT_CODE]: [Project Name]

**Status:** [Active/Prototype/Archived/Deprecated]
**Type:** [Core Infrastructure/Memory System/Application/Analytics/Creative/etc]
**Location:** `/Users/jeremybradford/SyncedProjects/[PROJECT_CODE]`
**Last Updated:** [Date of analysis]

### Purpose
[2-3 sentences explaining what problem this project solves and why it exists in the ecosystem]

### Key Capabilities
- **[Capability 1]:** [Brief description]
- **[Capability 2]:** [Brief description]
- **[Capability 3]:** [Brief description]
[Add more as needed]

### Dependencies

**Depends On:**
- `[PROJECT_CODE]` - [What it provides]
- `[LIBRARY/TOOL]` - [Why it's needed]

**Used By:**
- `[PROJECT_CODE]` - [How it's used]
- `[PROJECT_CODE]` - [How it's used]

### Technical Stack
- **Language:** [Python 3.x / Node.js / etc]
- **Key Libraries:**
  - `[library]` - [purpose]
  - `[library]` - [purpose]
- **Ports/Services:** [If applicable - e.g., "Port 3000: Web UI", "Port 8082: API server"]
- **Storage:** [Database/files/memory/etc]

### Integration Points

**File System:**
- Reads from: `[paths]`
- Writes to: `[paths]`
- Shared with: `[other projects]`

**Network:**
- APIs exposed: `[endpoints]`
- APIs consumed: `[external services]`

**Protocols:**
- `[Protocol name]` - [How it's used]

### Architecture Notes
[Any important architectural decisions, patterns, or design choices]

### Current Status

**Operational:** [Yes/No/Partial]
**Issues:** [Known bugs or limitations from docs]
**TODO Items:** [Documented future work]

### Connection Map
```
[Visual representation of how this connects to other projects]

Example:
P160 (This Project)
├── Depends on: Ollama (local LLM)
├── Depends on: C003_sadb_canonical (data source)
├── Integrates: P092_mirrorlab (memory)
└── Serves: All user interactions (port 3000)
```

### Discovery & Insights

**What I Learned:**
- [Key insight about architecture]
- [Interesting pattern or approach]
- [Unexpected connection]

**Questions/Uncertainties:**
- [Anything that needs clarification]
- [Conflicting information]
- [Areas that need deeper investigation]

**Recommendations:**
- [Potential improvements]
- [Documentation needs]
- [Consolidation opportunities]

### Files Analyzed
- `README.md` ✅
- `AGENTS.md` / `CLAUDE.md` ✅ / ⏭️
- `pyproject.toml` / `package.json` ✅ / ⏭️
- `[other key files]` ✅

---

**Next Project:** [PROJECT_CODE] - [Brief note about what to expect]

---

## Usage Notes for Claude Code

### When to use each section:

**Always include:**
- Purpose, Key Capabilities, Technical Stack, Current Status, Files Analyzed

**Include if applicable:**
- Dependencies (most projects will have some)
- Integration Points (if it connects to other projects)
- Connection Map (especially for infrastructure projects)
- Architecture Notes (if there are notable design decisions)

**Include Discovery & Insights for:**
- Projects with interesting patterns
- Projects that reveal ecosystem-wide themes
- Projects with consolidation opportunities
- Projects that are particularly critical or complex

### Quality checks:
- ✅ Can another engineer understand this project from the doc alone?
- ✅ Are connections to other projects clear?
- ✅ Is technical detail balanced with readability?
- ✅ Are paths and port numbers accurate?
- ✅ Did I note what's uncertain vs. what's confirmed?

---

**Remember:** Jeremy trusts you to be thorough. Take time to understand each project before documenting it. Save your work frequently!
