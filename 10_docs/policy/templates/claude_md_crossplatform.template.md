## Platform Compatibility

This workspace syncs between macOS and Windows via Syncthing. Commands are provided in cross-platform format where possible.

**Environment**:
- **macOS/Linux**: `~/SyncedProjects` paths, bash/zsh shells
- **Windows**: `C:\Users\jerem\SyncedProjects` paths, PowerShell (primary) or Git Bash

**Path Conventions**:
- Python and most modern tools accept forward slashes (`/`) on all platforms
- Examples use forward slashes by default - works on Windows PowerShell and macOS/Linux
- Backslash (`\`) alternatives noted only when specifically required

**Command Compatibility**:
- Use `python` (not `python3`) - works cross-platform
- Prefer `python -m module.command` for tool execution
- Shell scripts (`.sh`) require bash - native on macOS/Linux, needs Git Bash on Windows
- PowerShell scripts (`.ps1`) are Windows-only

**Virtual Environments**:
```bash
# Create (cross-platform)
python -m venv venv

# Activate (platform-specific)
source venv/bin/activate              # macOS/Linux/Git Bash
venv\Scripts\Activate.ps1             # Windows PowerShell
```

**Common Paths**:
```bash
# Project root (absolute)
~/SyncedProjects/{PROJECT_NAME}           # macOS/Linux/Git Bash
C:\Users\jerem\SyncedProjects\{PROJECT_NAME}  # Windows PowerShell

# Prefer relative paths when already in workspace:
cd {PROJECT_NAME}                     # Works everywhere from workspace root
```

**Tool Preferences**:
- File operations: Use Claude Code built-in tools (Read/Edit/Write) rather than shell commands (cat/sed/echo)
- Search: Use Grep tool rather than grep/rg commands
- Find files: Use Glob tool rather than find command

**Service Management**:
```bash
# Docker (cross-platform)
docker ps
docker start service-name

# Process inspection (platform-specific)
ps aux | grep name                    # macOS/Linux
Get-Process | Where-Object {$_.Name -like "*name*"}  # PowerShell
```

---
**Note**: This project follows the [Cross-Platform CLAUDE.md Standard](https://github.com/yourusername/C010_standards/blob/main/protocols/cross_platform_claude_md.md) from C010_standards.
