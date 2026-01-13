# C010_standards Operations

**Last Updated**: 2026-01-12
**Version**: 1.0.0

Day-to-day operation of C010_standards.

## Operating Modes

### Reference Mode (Primary)

```bash
# Consult standards before starting work
cat protocols/betty_protocol.md
cat protocols/tier3_documentation_spec.md
```

Use when starting new projects or reviewing requirements.

### Validation Mode

```bash
# Run all Houston validators (from repo root)
python validators/run_all.py
```

Use for pre-commit checks, CI/CD, and periodic audits.

### Bootstrap Mode

```bash
# Apply Ruff config to a repo
./scripts/bootstrap_ruff.sh ~/SyncedProjects/P050_ableton-mcp

# Add cross-platform Claude support
./scripts/bootstrap_claude_crossplatform.sh ~/SyncedProjects/P050_ableton-mcp
```

Use when standardizing repos or setting up new projects.

### Governance Mode

```bash
# Update a protocol
vi protocols/betty_protocol.md

# Bump schema version
vi schemas/docmeta_v1.3.yaml  # Create new version
```

Use when evolving standards (requires careful review).

## Daily Workflows

### Session Startup (AI Agents)

1. Read `AGENT_START_HERE.md` (mandatory pre-flight)
2. Check `protocols/betty_protocol.md` for current governance
3. Verify Houston trust phase in `30_config/houston-features.json`

### Health Check

```bash
# Run validator suite
python validators/run_all.py --config 30_config/houston-features.json
```

| Result | Status |
|--------|--------|
| Exit 0 | All checks pass |
| Exit 1 | Validation failure - review output |
| Exit 2 | Config/parse error - check file syntax |

### Adding a New Protocol

1. Create protocol document in `protocols/`
2. Add reference in `README.md`
3. Create receipt in `20_receipts/`
4. Update CHANGELOG.md

```bash
# Example
vi protocols/new_protocol.md
echo "- Added new_protocol.md" >> CHANGELOG.md
```

### Updating a Taxonomy

1. Edit taxonomy file in `taxonomies/`
2. Validate against schema (if applicable)
3. Create change receipt

```bash
# Add term to topic taxonomy
vi taxonomies/topic_taxonomy.yaml
# Verify format
python -c "import yaml; yaml.safe_load(open('taxonomies/topic_taxonomy.yaml'))"
```

### Recovery from Validation Failure

When validator fails:

```bash
# 1. Read error output
python validators/check_houston_features.py --config 30_config/houston-features.json

# 2. Fix configuration
vi 30_config/houston-features.json

# 3. Re-run validation
python validators/check_houston_features.py --config 30_config/houston-features.json
```

## Common Operations

**Check repo compliance:**
```bash
python validators/check_repo_contract.py --repo ~/SyncedProjects/P050_ableton-mcp
```

**Validate README repo card:**
```bash
python scripts/validate_readme_repo_card.py ~/SyncedProjects/C001_mission-control/README.md
```

**List all projects:**
```bash
cat workspace/KNOWN_PROJECTS.md
```

**Check project relationships:**
```bash
cat workspace/PROJECT_RELATIONSHIPS.md
```

**Find a taxonomy term:**
```bash
grep -i "term" taxonomies/universal_terms.yaml
```

## Resource Management

### File Counts

| Category | Approximate Count |
|----------|-------------------|
| Protocols | 11 documents |
| Schemas | 3 versioned specs |
| Taxonomies | 8 files |
| Validators | 6 checkers |
| Receipts | 148+ entries |
| Registry entries | 66+ repos |

### Storage

- Repository size: ~5MB (excluding receipts archive)
- No external data dependencies
- No runtime services

## Troubleshooting Quick Reference

### Validation Issues

| Symptom | Fix |
|---------|-----|
| `ImportError: yaml` | Install PyYAML: `pip install pyyaml` |
| `ImportError: jsonschema` | Install: `pip install jsonschema` |
| Exit code 2 | Check YAML/JSON syntax in config file |
| Exit code 1 | Review validation errors in output |

### Schema Issues

| Symptom | Fix |
|---------|-----|
| Unknown field in DocMeta | Check `schemas/docmeta_v1.2.yaml` for valid fields |
| Invalid routing value | Must be: `internal`, `external`, or `all` |
| Missing required field | Check schema for required properties |

### Taxonomy Issues

| Symptom | Fix |
|---------|-----|
| Term not recognized | Check `taxonomies/universal_terms.yaml` for synonyms |
| Disambiguation needed | Consult `taxonomies/disambiguation_rules.yaml` |
| New term needed | Add to appropriate taxonomy file |

## Tool Categories

### Read-Only
- `cat protocols/*.md` - Read protocols
- `cat schemas/*.yaml` - Read schemas
- `python validators/*.py` - Run validators (no file changes)
- `grep` through taxonomies

### Modification
- Edit protocols (governance changes)
- Update schemas (version bumps)
- Add taxonomy terms
- Create receipts

### Administrative (Require Care)
- Schema version changes (affects all consumers)
- Protocol amendments (workspace-wide impact)
- Registry updates (project tracking)

## Log Locations

| Log | Location | Purpose |
|-----|----------|---------|
| Change receipts | `20_receipts/` | Audit trail |
| Validator output | stdout | Validation results |
| Nightly registry | `workspace/KNOWN_PROJECTS.md` | Project list |

## Upgrading Standards

### Minor Update (patch)

```bash
# 1. Make changes
vi protocols/betty_protocol.md

# 2. Update version in META.yaml
vi META.yaml  # version: 1.0.1

# 3. Create receipt
vi 20_receipts/$(date +%Y-%m-%d)_update_description.md

# 4. Commit
git add -A && git commit -m "chore: update betty protocol"
```

### Schema Version Bump

```bash
# 1. Create new version file
cp schemas/docmeta_v1.2.yaml schemas/docmeta_v1.3.yaml

# 2. Update version in new file
vi schemas/docmeta_v1.3.yaml

# 3. Update consumers (notify via CHANGELOG)
vi CHANGELOG.md

# 4. Create receipt documenting changes
```

## Related Documentation

- [QUICKSTART.md](QUICKSTART.md) - Initial setup
- [ARCHITECTURE.md](ARCHITECTURE.md) - System design
- [SECURITY_AND_PRIVACY.md](SECURITY_AND_PRIVACY.md) - Security model
