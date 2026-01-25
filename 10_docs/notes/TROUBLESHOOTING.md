# C010_standards Troubleshooting Guide

## Overview

This guide helps you diagnose and resolve common issues when using C010_standards validators, schemas, and tooling.

## Quick Diagnosis

Use this flowchart to quickly identify your issue category:

```
Is the problem related to...
├─ Running validators? → Go to Section 1
├─ Schema validation errors? → Go to Section 2
├─ Taxonomy issues? → Go to Section 3
├─ Houston configuration? → Go to Section 4
├─ Git submodule? → Go to Section 5
└─ CI/CD integration? → Go to Section 6
```

---

## 1. Validator Execution Issues

### Problem: "ModuleNotFoundError: No module named 'validators'"

**Symptoms:**
```
Traceback (most recent call last):
  File "validators/check_houston_features.py", line 12
    from validators.common import load_json_config
ModuleNotFoundError: No module named 'validators'
```

**Cause:** Python can't find the validators package

**Solutions:**

1. **Run from repository root:**
   ```bash
   cd /path/to/C010_standards
   python validators/check_houston_features.py
   ```

2. **Add to Python path:**
   ```bash
   export PYTHONPATH=/path/to/C010_standards:$PYTHONPATH
   python validators/check_houston_features.py
   ```

3. **Use absolute path:**
   ```bash
   python /path/to/C010_standards/validators/check_houston_features.py
   ```

### Problem: "ERROR: PyYAML library not installed"

**Symptoms:**
```
ERROR: PyYAML library not installed. Install with: pip install pyyaml
```

**Cause:** Required dependencies not installed

**Solution:**
```bash
# Install production dependencies
pip install -r requirements.txt

# Or install specific package
pip install PyYAML jsonschema
```

### Problem: Validator returns unexpected exit code

**Symptoms:**
Validator exits with a code you don't recognize

**Exit Code Reference:**
- **0**: All checks passed
- **1**: Validation failure (check output for specific errors)
- **2**: Configuration/parse error (file not found, invalid JSON/YAML)

**Solution:**
```bash
# Check for latest version
git pull origin main

# Run with verbose output to see details
python validators/run_all.py --pass-args --verbose
```

### Problem: "Permission denied" when running validator

**Symptoms:**
```
bash: ./validators/check_houston_features.py: Permission denied
```

**Cause:** File not executable

**Solution:**
```bash
# Make executable
chmod +x validators/check_houston_features.py

# Or run with python explicitly
python validators/check_houston_features.py
```

---

## 2. Schema Validation Errors

### Problem: "Schema validation error: Missing required field"

**Symptoms:**
```
❌ Houston features validation FAILED (1 issues):
  1. Schema validation error at features.agency_levels: Missing required field
```

**Diagnosis:**
Check which field is missing in the JSON schema

**Solution:**
```bash
# Validate JSON structure
python -m json.tool 30_config/houston-features.json

# Compare against schema
diff <(jq -S . 30_config/houston-features.json) \
     <(jq -S . schemas/houston_features.schema.json)
```

### Problem: "Invalid editors in supported_editors"

**Symptoms:**
```
❌ Houston features validation FAILED (1 issues):
  1. Invalid editors in supported_editors: {'sublime'}. Allowed: {'cursor', 'vscode', 'jetbrains'}
```

**Cause:** Using unsupported editor name

**Solution:**
Update config to use allowed editors only:
```json
{
  "features": {
    "ide_integration": {
      "supported_editors": ["cursor", "vscode", "jetbrains"]
    }
  }
}
```

### Problem: "CRITICAL: autonomous mode misconfigured"

**Symptoms:**
```
CRITICAL: agency_levels.current_level is 'autonomous' but
safety_controls.destructive_actions.require_password is false.
Must be true for autonomous mode.
```

**Cause:** Safety controls not enabled for autonomous mode

**Solution:**
```json
{
  "features": {
    "agency_levels": {
      "current_level": "autonomous"
    }
  },
  "safety_controls": {
    "destructive_actions": {
      "require_password": true  // Must be true
    }
  }
}
```

### Problem: "can_deploy_updates requires phase >= 3"

**Symptoms:**
```
CRITICAL: can_deploy_updates is true but current_phase is 1.
Deployment permission requires phase >= 3.
```

**Cause:** Deployment enabled too early in trust phases

**Solution:**
Either:
1. Disable deployment:
   ```json
   {"autonomous": {"can_deploy_updates": false}}
   ```

2. OR advance to phase 3:
   ```json
   {"gradual_trust_building": {"current_phase": 3}}
   ```
   (And update agency_level to "autonomous")

---

## 3. Taxonomy Issues

### Problem: "Invalid topics not in taxonomy"

**Symptoms:**
```
❌ DocMeta validation FAILED (1 issues):
  1. docs/guide.yaml: Invalid topics not in taxonomy: {'containerization'}.
     See taxonomies/topic_taxonomy.yaml
```

**Diagnosis:**
Topic used in document doesn't exist in taxonomy

**Solutions:**

1. **Use existing similar topic:**
   ```bash
   # Check available topics
   cat taxonomies/topic_taxonomy.yaml | grep -A 100 "^topics:"

   # Use 'deployment' instead of 'containerization'
   ```

2. **Request new topic:**
   - Open PR to C010_standards
   - Add topic to `taxonomies/topic_taxonomy.yaml`
   - Include justification

3. **Temporary: Skip taxonomy validation:**
   ```bash
   # For testing only - don't use in production
   python validators/check_houston_docmeta.py docs/ --taxonomy /dev/null
   ```

### Problem: "Topic stoplist violation"

**Symptoms:**
Document uses topic from stoplist (too generic/deprecated)

**Solution:**
Replace with more specific topic:
```yaml
# DON'T USE:
topics:
  - "general"
  - "misc"

# USE SPECIFIC TOPICS:
topics:
  - "monitoring"
  - "deployment"
```

---

## 4. Houston Configuration Issues

### Problem: "Phase consistency check failed"

**Symptoms:**
```
Tools phase_settings.current_phase (3) exceeds
features gradual_trust_building.current_phase (1).
Tool permissions cannot exceed trust phase.
```

**Cause:** Tools config has higher phase than features config

**Solution:**
Align phases:
```json
// houston-features.json
{"gradual_trust_building": {"current_phase": 3}}

// houston-tools.json
{"phase_settings": {"current_phase": 3}}
```

### Problem: "WARNING: auto_advance is false but no changelog entry"

**Symptoms:**
```
WARNING: auto_advance is false and current_phase is 2, but no
'Phase 2 activated' entry found in CHANGELOG.md.
```

**Cause:** Manual phase advancement not documented

**Solution:**
Add entry to `CHANGELOG.md`:
```markdown
## 2025-11-08
- **Houston Phase 2 activated**: Transitioned to Collaboration mode
  with advisory agency level. IDE integration and proactive alerts enabled.
```

### Problem: "VPS tools enabled with placeholder endpoint"

**Symptoms:**
```
WARNING: vps_tools.enabled is true but endpoint is placeholder ('example.com').
Provide real VPS endpoint before enabling.
```

**Solution:**
Either disable VPS tools or provide real endpoint:
```json
{
  "tool_access": {
    "vps_tools": {
      "enabled": true,
      "endpoint": "https://real-server.example.com"  // Real endpoint
    }
  }
}
```

---

## 5. Git Submodule Issues

### Problem: "Submodule not initialized"

**Symptoms:**
```bash
$ ls external/standards
# Empty directory
```

**Solution:**
```bash
# Initialize submodule
git submodule init
git submodule update

# Or do both at once
git submodule update --init --recursive
```

### Problem: "Submodule detached HEAD"

**Symptoms:**
```bash
$ cd external/standards
$ git branch
* (HEAD detached at abc123)
```

**Explanation:** This is normal for git submodules

**Solution:**
If you need to work on submodule:
```bash
cd external/standards
git checkout main
git pull
# Make changes
cd ../..
git add external/standards
git commit -m "Update submodule"
```

### Problem: "Submodule points to wrong commit"

**Solution:**
```bash
# Update to latest
cd external/standards
git fetch origin
git checkout main
git pull
cd ../..
git add external/standards
git commit -m "Update C010_standards to latest"

# Or update to specific version
cd external/standards
git checkout schema/docmeta/v1.2
cd ../..
git add external/standards
git commit -m "Pin to DocMeta v1.2"
```

---

## 6. CI/CD Integration Issues

### Problem: "Validators fail in CI but pass locally"

**Diagnosis:**
```bash
# Check Python version
python --version  # Local
python3 --version  # CI might use python3

# Check dependencies
pip list | grep -E "PyYAML|jsonschema"
```

**Common Causes:**

1. **Different Python version:**
   ```yaml
   # .github/workflows/ci.yml
   - uses: actions/setup-python@v5
     with:
       python-version: '3.11'  # Match local version
   ```

2. **Missing dependencies:**
   ```yaml
   - name: Install dependencies
     run: pip install -r requirements.txt
   ```

3. **Working directory:**
   ```yaml
   - name: Run validators
     run: python validators/run_all.py
     working-directory: ./  # Ensure correct directory
   ```

### Problem: "Submodule not checked out in CI"

**Symptoms:**
```
ERROR: Required file not found: external/standards/validators/...
```

**Solution:**
```yaml
# .github/workflows/ci.yml
- uses: actions/checkout@v4
  with:
    submodules: true  # Add this
    # Or:
    submodules: recursive
```

### Problem: "Validators timeout in CI"

**Symptoms:**
```
Error: The operation was canceled.
```

**Solutions:**

1. **Increase timeout:**
   ```yaml
   - name: Run validators
     run: python validators/run_all.py
     timeout-minutes: 10  # Default is 5
   ```

2. **Run validators in parallel:**
   ```yaml
   - name: Validate features
     run: python validators/check_houston_features.py &

   - name: Validate tools
     run: python validators/check_houston_tools.py &

   - wait  # Wait for all background jobs
   ```

---

## 7. Performance Issues

### Problem: "Validators are slow"

**Diagnosis:**
```bash
# Time validator execution
time python validators/run_all.py
```

**Optimization strategies:**

1. **Run specific validators only:**
   ```bash
   # Instead of all validators
   python validators/run_all.py --targets houston_features houston_tools
   ```

2. **Skip verbose output:**
   ```bash
   # Verbose mode is slower
   python validators/run_all.py  # Without --verbose
   ```

3. **Cache dependencies:**
   ```yaml
   # In CI
   - uses: actions/cache@v3
     with:
       path: ~/.cache/pip
       key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
   ```

### Problem: "Large number of files to validate"

**Solution:**
```bash
# Validate only changed files
git diff --name-only --diff-filter=AM | grep ".yaml$" | \
  xargs python validators/check_houston_docmeta.py

# Or validate specific directory
python validators/check_houston_docmeta.py docs/houston/
```

---

## 8. Common Mistakes

### Mistake: Running validators from wrong directory

**Wrong:**
```bash
cd validators
python check_houston_features.py  # ModuleNotFoundError
```

**Right:**
```bash
cd /path/to/C010_standards
python validators/check_houston_features.py  # Works
```

### Mistake: Editing schemas directly instead of via PR

**Impact:** Changes will be overwritten on next update

**Right approach:**
1. Fork C010_standards
2. Make changes in your fork
3. Open PR
4. Wait for approval
5. Update submodule after merge

### Mistake: Using wrong schema version

**Problem:**
```yaml
schema: "DocMeta.v1.3"  # Doesn't exist yet
```

**Solution:**
Check available versions:
```bash
ls schemas/docmeta_*.yaml
# Use existing version: DocMeta.v1.2
```

### Mistake: Not updating submodule after schema changes

**Impact:** Using old validators with new schema

**Solution:**
```bash
# Always update submodule after pull
git pull
git submodule update --remote
```

---

## 9. Debugging Tools

### Enable Verbose Mode

```bash
# All validators support --verbose
python validators/check_houston_features.py --verbose

# Shows detailed validation steps
✓ JSON schema validation passed
✓ Supported editors valid: {'cursor', 'vscode'}
✓ Autonomous safety check passed (level=supervisory, require_password=True)
```

### Validate JSON Structure

```bash
# Check if JSON is valid
python -m json.tool config.json

# Pretty print
jq . config.json

# Validate against schema manually
python -c "import json, jsonschema
config = json.load(open('config.json'))
schema = json.load(open('schema.json'))
jsonschema.validate(config, schema)
print('Valid')"
```

### Check YAML Syntax

```bash
# Parse YAML
python -c "import yaml; yaml.safe_load(open('file.yaml'))"

# Pretty print
python -c "import yaml; print(yaml.dump(yaml.safe_load(open('file.yaml'))))"
```

### Trace Validation Errors

```bash
# Run with Python debugger
python -m pdb validators/check_houston_features.py

# Add breakpoint in code
import pdb; pdb.set_trace()
```

---

## 10. Getting Help

### Self-Service

1. **Check this guide** - Most common issues covered
2. **Read documentation** - Check CLAUDE.md, README.md, CONTRIBUTING.md
3. **Review examples** - See `examples/` directory
4. **Check tests** - See `tests/` for usage patterns

### Community Support

1. **Search issues** - https://github.com/jeremybrad/C010_standards/issues
2. **Ask in Slack** - #dev-standards channel
3. **Open issue** - With minimal reproduction case

### Issue Template

When opening an issue, include:

```markdown
## Problem
Brief description of issue

## Environment
- OS: macOS 14.1
- Python: 3.11.6
- C010_standards version: commit abc123

## Steps to Reproduce
1. Run `python validators/...`
2. See error

## Expected Behavior
Should validate successfully

## Actual Behavior
```
Error message here
```

## Additional Context
- Running as git submodule: Yes/No
- CI or local: Local
- Config file: [attach or inline]
```

---

## 11. FAQ

**Q: Can I skip validation in CI temporarily?**

A: Yes, but use environment variable:
```yaml
- name: Validate
  if: env.SKIP_VALIDATION != 'true'
  run: python validators/run_all.py
```

**Q: Which Python version is required?**

A: Python 3.11+ required. Validators use modern type hints.

**Q: Can I use validators without adopting schemas?**

A: Yes! See [MIGRATION_CHECKLIST.md](MIGRATION_CHECKLIST.md) Section 4.

**Q: How often should I update submodule?**

A: Monthly recommended. Check for breaking changes before updating.

**Q: Can I modify validators for my project?**

A: Yes, but prefer:
1. Contributing changes upstream (benefits everyone)
2. Using validator arguments/config options
3. Only fork as last resort

---

## 12. Emergency Procedures

### Validation Blocking Production Deploy

If validators block critical deploy:

1. **Quick fix if possible:**
   ```bash
   # Fix the actual issue
   vim 30_config/houston-features.json
   python validators/run_all.py  # Verify fix
   ```

2. **Bypass in emergency:**
   ```bash
   # Document why
   echo "Emergency bypass: [TICKET-123] explanation" > validation_bypass.txt

   # Skip validation (emergency only)
   git commit --no-verify
   ```

3. **Follow up:**
   - Create ticket to fix properly
   - Don't make bypassing a habit

### Submodule Broken in Production

If submodule update breaks production:

```bash
# Revert to last known good commit
cd external/standards
git checkout <previous-working-commit>
cd ../..
git add external/standards
git commit -m "Revert standards to working version"
git push

# Then investigate issue
```

---

**Last updated:** 2025-11-08
**Need more help?** Open an issue: https://github.com/jeremybrad/C010_standards/issues
