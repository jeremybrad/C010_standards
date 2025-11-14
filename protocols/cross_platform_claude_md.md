# Cross-Platform CLAUDE.md Standard

## Purpose

This protocol defines how to write CLAUDE.md files that work seamlessly across macOS and Windows platforms in a Syncthing-synchronized workspace. It ensures that AI assistants (Claude Code, etc.) receive appropriate guidance regardless of which machine the user is currently working on.

## Problem Statement

Jeremy's SyncedProjects workspace syncs between multiple machines via Syncthing:
- **macOS** (Mac Mini, MacBook): Unix environment, bash/zsh shells, forward-slash paths
- **Windows** (Desktop PC): Windows environment, PowerShell/Git Bash, backslash paths

Previously, using WSL (Windows Subsystem for Linux) on Windows provided Unix-like consistency. However, native Windows usage (PowerShell) requires explicit cross-platform awareness in all documentation and command examples.

**The Goal**: Write CLAUDE.md files once that work correctly on both platforms without manual edits when switching machines.

## Core Principles

### 1. **Platform Agnostic by Default**

Prefer commands and patterns that work identically on both platforms:

✅ **Good (Platform Agnostic)**:
```bash
python script.py
python -m module.command
npm install
git status
```

❌ **Avoid (Platform Specific)**:
```bash
source venv/bin/activate        # macOS only
venv\Scripts\activate.bat       # Windows only
cat file.txt                    # Use Read tool instead
```

### 2. **Explicit When Platform-Specific Required**

When platform-specific commands are necessary, provide **both versions** with clear labels:

✅ **Good**:
```bash
# Activate virtual environment
source venv/bin/activate              # macOS/Linux/Git Bash
venv\Scripts\activate.ps1             # Windows PowerShell
# Or use: python -m venv venv && python -m pip install ...
```

❌ **Avoid**:
```bash
# Activate virtual environment
source venv/bin/activate
```

### 3. **Paths: Forward Slashes First**

Python and most modern tools accept forward slashes on Windows. Use them in examples:

✅ **Good**:
```bash
python validators/run_all.py          # Works on all platforms
cd ~/SyncedProjects/P###_project      # macOS/Linux/Git Bash
```

✅ **Also Acceptable** (when showing Windows alternative):
```bash
# Platform-agnostic (recommended)
python validators/run_all.py

# Windows PowerShell (also works)
python validators\run_all.py
```

### 4. **Home Directory References**

Show both home directory conventions when referencing absolute paths:

✅ **Good**:
```bash
# macOS/Linux/Git Bash
cd ~/SyncedProjects/C010_standards

# Windows PowerShell
cd C:\Users\jerem\SyncedProjects\C010_standards
```

Or use relative paths when possible:
```bash
cd ../C010_standards                   # Works everywhere
```

## Command Patterns

### Virtual Environments

**Creating**:
```bash
# Cross-platform
python -m venv venv
```

**Activating**:
```bash
# macOS/Linux/Git Bash
source venv/bin/activate

# Windows PowerShell
venv\Scripts\Activate.ps1

# Windows cmd
venv\Scripts\activate.bat

# Alternative: Skip activation, use full path
python -m pip install -r requirements.txt
```

**Best Practice**: In CLAUDE.md, note that Claude Code should use `python` directly rather than relying on shell activation.

### Running Python Scripts

✅ **Recommended Patterns**:
```bash
python script.py                       # Direct execution
python -m package.module               # Module execution
python -m pytest tests/                # Tool execution
```

❌ **Avoid**:
```bash
./script.py                            # Requires shebang + chmod (Unix only)
python3 script.py                      # May not exist on Windows
```

### Running Shell Scripts

**Bash Scripts** (`.sh` files):
```bash
# macOS/Linux
bash script.sh

# Windows (requires Git Bash)
bash script.sh

# Note in CLAUDE.md:
"Requires bash - macOS/Linux native, Windows needs Git Bash installed"
```

**PowerShell Scripts** (`.ps1` files):
```powershell
# Windows PowerShell only
.\script.ps1

# Note in CLAUDE.md:
"Windows PowerShell only - macOS users use equivalent bash script"
```

**Best Practice**: Provide both `.sh` and `.ps1` versions for critical scripts, or use Python for cross-platform scripts.

### File Operations

**Prefer Claude Code tools over shell commands**:

✅ **Good** (Claude Code tools):
- Read files: Use `Read` tool (not `cat`)
- Edit files: Use `Edit` tool (not `sed`)
- Write files: Use `Write` tool (not `echo >` or `cat <<EOF`)
- Search files: Use `Grep` tool (not `grep` or `rg`)
- Find files: Use `Glob` tool (not `find`)

**Reason**: Claude Code tools are platform-agnostic and work identically everywhere.

### Service Management

**Docker**:
```bash
# Cross-platform
docker ps
docker start container-name
docker-compose up -d
```

**Process Management**:
```bash
# macOS/Linux
ps aux | grep process-name
kill -9 PID
lsof -i :8080

# Windows PowerShell
Get-Process | Where-Object {$_.Name -like "*process*"}
Stop-Process -Id PID -Force
Get-NetTCPConnection | Where-Object {$_.LocalPort -eq 8080}

# Note both in CLAUDE.md when process management is needed
```

## Shell Detection and Adaptation

When writing scripts that need platform detection:

**Bash/Shell Script**:
```bash
#!/usr/bin/env bash

# Detect platform
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "macOS"
    PLATFORM="mac"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "Linux"
    PLATFORM="linux"
elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    echo "Windows (Git Bash)"
    PLATFORM="windows"
else
    echo "Unknown platform"
    PLATFORM="unknown"
fi
```

**Python Script**:
```python
import platform
import sys

system = platform.system()
if system == "Darwin":
    print("macOS")
elif system == "Linux":
    print("Linux")
elif system == "Windows":
    print("Windows")
```

**PowerShell**:
```powershell
if ($IsWindows) {
    Write-Host "Windows"
} elseif ($IsMacOS) {
    Write-Host "macOS"
} elseif ($IsLinux) {
    Write-Host "Linux"
}
```

## CLAUDE.md Template Sections

### Recommended Section: Platform Compatibility

Every CLAUDE.md should include a section like this:

```markdown
## Platform Compatibility

This workspace syncs between macOS and Windows via Syncthing. Commands are provided in cross-platform format where possible.

**Platform Detection**:
- **macOS/Linux**: `~/SyncedProjects` paths, bash/zsh shells
- **Windows**: `C:\Users\jerem\SyncedProjects` paths, PowerShell (native) or Git Bash

**Path Conventions**:
- Forward slashes (`/`) work in Python and most tools on all platforms
- Backslashes (`\`) required only in native Windows PowerShell for some commands
- When in doubt, use forward slashes

**Shell Commands**:
- Use `python` (not `python3`) for cross-platform compatibility
- Prefer module execution: `python -m package.module`
- Bash scripts (`.sh`) require Git Bash on Windows
- PowerShell scripts (`.ps1`) are Windows-only
```

### Recommended Section: Common Commands

When documenting commands, use this pattern:

```markdown
## Common Commands

### Setup Virtual Environment

# Cross-platform creation
python -m venv venv

# Activation (platform-specific)
source venv/bin/activate              # macOS/Linux/Git Bash
venv\Scripts\Activate.ps1             # Windows PowerShell

# Install dependencies (works after activation on any platform)
pip install -r requirements.txt
```

## Common Pitfalls

### ❌ Pitfall: Assuming Unix Environment

**Problem**:
```markdown
## Setup
1. Run `chmod +x script.sh`
2. Execute `./script.sh`
```

**Solution**:
```markdown
## Setup
# macOS/Linux
chmod +x script.sh && ./script.sh

# All platforms
bash script.sh
```

### ❌ Pitfall: Hardcoded Absolute Paths

**Problem**:
```markdown
cd ~/SyncedProjects/P002_sadb
python 40_src/main.py
```

**Solution**:
```markdown
# Navigate to project root
cd ~/SyncedProjects/P002_sadb           # macOS/Linux/Git Bash
cd C:\Users\jerem\SyncedProjects\P002_sadb  # Windows PowerShell

# Run from project root (works on all platforms)
python 40_src/main.py
```

Or better:
```markdown
# From workspace root, use relative path
cd P002_sadb
python 40_src/main.py
```

### ❌ Pitfall: Shell-Specific Features

**Problem**:
```bash
export VARIABLE=value
source .env
cat file.txt | grep pattern
```

**Solution**:
```bash
# Environment variables (show both)
export VARIABLE=value                  # bash/zsh
$env:VARIABLE="value"                 # PowerShell

# Loading .env (use cross-platform tool)
python-dotenv run command             # Works everywhere
# Or document both shell methods

# File operations (use Claude Code tools)
# Instead of: cat file.txt | grep pattern
# Claude should use: Grep tool with pattern
```

## Testing Cross-Platform Compatibility

When writing or updating CLAUDE.md:

1. **Test commands on both platforms** (if possible)
2. **Verify paths work with forward slashes on Windows**
3. **Check that Python scripts use `python` not `python3`**
4. **Ensure no hardcoded Unix-only commands** (chmod, ln -s, etc.)
5. **Provide alternatives for platform-specific operations**

## Bootstrap Integration

C010_standards provides `scripts/bootstrap_claude_crossplatform.sh` to automatically add cross-platform awareness to existing CLAUDE.md files across the workspace.

**Usage**:
```bash
# Add cross-platform section to all CLAUDE.md files
bash scripts/bootstrap_claude_crossplatform.sh

# Dry-run (show what would change)
bash scripts/bootstrap_claude_crossplatform.sh --dry-run
```

## References

- **Cross-platform Python**: https://docs.python.org/3/library/os.html
- **PowerShell cross-platform**: https://learn.microsoft.com/en-us/powershell/
- **Git Bash on Windows**: https://gitforwindows.org/
- **C010_standards Ruff bootstrap**: `scripts/bootstrap_ruff.sh` (similar pattern)

## Version History

- **v1.0** (2025-10-18): Initial cross-platform protocol established
  - Defined core principles and command patterns
  - Created template sections for CLAUDE.md files
  - Established path conventions and shell compatibility guidelines
