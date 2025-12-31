# Migration Checklist for Consuming Projects

## Overview

This checklist guides projects through adopting C010_standards schemas, taxonomies, and validation tooling. Follow this step-by-step guide to ensure smooth integration.

## Target Audience

- Project leads integrating C010_standards
- Developers adding metadata to documentation
- DevOps engineers setting up validation in CI
- Teams migrating from custom metadata formats

## Prerequisites

Before starting migration:

- [ ] Review [CONTRIBUTING.md](../CONTRIBUTING.md) for contribution guidelines
- [ ] Review [VERSIONING_POLICY.md](VERSIONING_POLICY.md) for schema versions
- [ ] Understand your project's metadata needs
- [ ] Have write access to target repository
- [ ] Coordinate with team on migration timeline

## Migration Paths

Choose your migration path based on current state:

### Path A: New Project (No Existing Metadata)
Start from scratch with C010_standards → Go to [Section 1](#1-initial-setup)

### Path B: Existing Custom Metadata
Migrate from custom format to C010_standards → Go to [Section 2](#2-schema-migration)

### Path C: Git Submodule Integration
Integrate C010_standards as submodule → Go to [Section 3](#3-git-submodule-integration)

### Path D: Validator Integration Only
Add validators without adopting schemas → Go to [Section 4](#4-validator-only-integration)

---

## 1. Initial Setup

### 1.1 Install Dependencies

```bash
# Clone or access C010_standards
cd /path/to/your/project

# Option A: Git submodule (recommended for core projects)
git submodule add https://github.com/jeremybrad/C010_standards.git external/standards
git submodule update --init --recursive

# Option B: Direct dependency
pip install -r https://raw.githubusercontent.com/jeremybrad/C010_standards/main/requirements.txt
```

**Checklist:**
- [ ] C010_standards accessible in project
- [ ] Dependencies installed (PyYAML, jsonschema)
- [ ] Validators can be run

### 1.2 Choose Schemas

Select which schemas your project needs:

- [ ] **DocMeta v1.2** - For documentation, reports, specs
- [ ] **CodeMeta v1.0** - For code repositories, scripts, libraries
- [ ] **Houston Features** - For Mission Control agent configuration
- [ ] **Taxonomies** - For controlled vocabularies

### 1.3 Create Examples

```bash
# Copy example files to your project
cp external/standards/examples/docmeta_example.yaml docs/metadata_template.yaml
cp external/standards/examples/codemeta_example.yaml .codemeta.yaml

# Customize for your project
vim docs/metadata_template.yaml
```

**Checklist:**
- [ ] Example files copied
- [ ] Templates customized for your project
- [ ] Team trained on metadata format

---

## 2. Schema Migration

### 2.1 Audit Existing Metadata

```bash
# Find all files with metadata
find . -name "*.md" -exec grep -l "^---" {} \;
find . -name "*.yaml" -type f

# Document current format
```

**Checklist:**
- [ ] Inventory of files with metadata
- [ ] Current schema documented
- [ ] Gap analysis: Current → Target schema

### 2.2 Map Fields

Create mapping from your schema to C010_standards:

| Your Field | DocMeta Field | Notes |
|------------|---------------|-------|
| `author` | `doc.authors[]` | Convert to array |
| `tags` | `doc.topics[]` | Validate against taxonomy |
| `created_date` | `doc.created` | Format as YYYY-MM-DD |
| `category` | `doc.type` | Map to allowed types |

**Checklist:**
- [ ] Field mapping table created
- [ ] Data transformations identified
- [ ] Edge cases documented

### 2.3 Write Migration Script

```python
#!/usr/bin/env python3
"""Migrate custom metadata to DocMeta v1.2."""

import yaml
from pathlib import Path

def migrate_file(input_path: Path, output_path: Path):
    """Migrate one file."""
    with open(input_path) as f:
        old_metadata = yaml.safe_load(f)

    # Transform to DocMeta format
    new_metadata = {
        "schema": "DocMeta.v1.2",
        "doc": {
            "title": old_metadata.get("title", ""),
            "authors": [old_metadata.get("author", "")],
            "created": old_metadata.get("created_date", ""),
            "topics": old_metadata.get("tags", []),
            # ... map other fields
        }
    }

    with open(output_path, 'w') as f:
        yaml.dump(new_metadata, f)

# Run migration
for md_file in Path(".").rglob("*.md"):
    migrate_file(md_file, md_file)
```

**Checklist:**
- [ ] Migration script written
- [ ] Script tested on sample files
- [ ] Backup of original files created

### 2.4 Validate Migrated Files

```bash
# Run DocMeta validator
python external/standards/validators/check_houston_docmeta.py docs/ --verbose

# Fix any validation errors
# Re-run until all pass
```

**Checklist:**
- [ ] All files validate successfully
- [ ] No taxonomy violations
- [ ] Required fields present

---

## 3. Git Submodule Integration

### 3.1 Add Submodule

```bash
# Add C010_standards as submodule
git submodule add https://github.com/jeremybrad/C010_standards.git external/standards

# Initialize submodule
git submodule update --init --recursive

# Commit
git add .gitmodules external/standards
git commit -m "Add C010_standards as git submodule"
```

**Checklist:**
- [ ] Submodule added successfully
- [ ] `.gitmodules` file created
- [ ] Submodule committed

### 3.2 Pin to Specific Version

```bash
# Pin to stable release tag
cd external/standards
git fetch --tags
git checkout schema/docmeta/v1.2  # or specific version
cd ../..
git add external/standards
git commit -m "Pin C010_standards to DocMeta v1.2"
```

**Checklist:**
- [ ] Submodule pinned to stable version
- [ ] Version documented in README
- [ ] Team knows how to update

### 3.3 Setup Update Workflow

```bash
# Update submodule to latest
cd external/standards
git fetch origin
git checkout main
git pull
cd ../..
git add external/standards
git commit -m "Update C010_standards submodule"
```

**Documentation:**
Add to your project's README:

```markdown
## Updating Standards

Update C010_standards to latest version:

```bash
git submodule update --remote external/standards
git add external/standards
git commit -m "Update standards to latest"
```
```

**Checklist:**
- [ ] Update procedure documented
- [ ] Team knows how to update submodule
- [ ] Update schedule established (e.g., monthly)

---

## 4. Validator-Only Integration

### 4.1 Setup Validator Access

```bash
# Option A: Copy validators to your project
cp -r /path/to/C010_standards/validators ./tools/validators
cp /path/to/C010_standards/requirements.txt ./tools/validators/

# Option B: Run from submodule
# (Validators already accessible at external/standards/validators/)
```

**Checklist:**
- [ ] Validators accessible
- [ ] Dependencies installed
- [ ] Can run validators manually

### 4.2 Add to Development Workflow

Add to `Makefile`:

```makefile
.PHONY: validate

validate:
	@echo "Running metadata validation..."
	python external/standards/validators/check_houston_docmeta.py docs/ --verbose
	python external/standards/validators/check_houston_features.py --verbose
```

**Checklist:**
- [ ] Validation added to Makefile/scripts
- [ ] Developers know how to run validation
- [ ] Validation passes on current codebase

### 4.3 Add to CI Pipeline

**.github/workflows/validate-metadata.yml:**

```yaml
name: Validate Metadata

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          submodules: true

      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: pip install -r external/standards/requirements.txt

      - name: Validate DocMeta
        run: |
          python external/standards/validators/check_houston_docmeta.py docs/ --verbose

      - name: Validate Houston configs
        if: -f 30_config/houston-features.json
        run: |
          python external/standards/validators/check_houston_features.py --verbose
```

**Checklist:**
- [ ] CI workflow created
- [ ] CI runs on every PR
- [ ] Validation failures block merge

---

## 5. Taxonomy Adoption

### 5.1 Review Available Taxonomies

```bash
# View topic taxonomy
cat external/standards/taxonomies/topic_taxonomy.yaml

# View content taxonomy
cat external/standards/taxonomies/content_taxonomy.yaml
```

**Checklist:**
- [ ] Reviewed all relevant taxonomies
- [ ] Identified missing terms for your domain
- [ ] Documented custom taxonomy needs

### 5.2 Request Taxonomy Additions

If you need new taxonomy terms:

1. **Check if term already exists** in similar form
2. **Open PR to C010_standards** with taxonomy addition
3. **Include justification** and usage examples
4. **Wait for approval** before using in production

**Template PR description:**

```markdown
## Add New Topic: "container_orchestration"

### Justification
Our team manages Kubernetes clusters and needs to tag documentation
related to container orchestration. This is distinct from existing
"deployment" and "infra" topics.

### Usage Examples
- K8s troubleshooting guides
- Helm chart documentation
- Container security policies

### Related Terms
- deployment (existing)
- infra (existing)
```

**Checklist:**
- [ ] PR opened for new terms
- [ ] Approval received
- [ ] New terms added to local copy

### 5.3 Validate Against Taxonomy

```bash
# Validate all docs use approved topics
python external/standards/validators/check_houston_docmeta.py docs/ \
  --taxonomy external/standards/taxonomies/topic_taxonomy.yaml \
  --verbose
```

**Checklist:**
- [ ] All topic tags validated
- [ ] No unapproved terms used
- [ ] Validation passes

---

## 6. Houston Integration (Mission Control Projects Only)

### 6.1 Add Houston Routing Tags

For documents that should be retrievable by Houston:

```yaml
# Add to document front matter
routing:
  tags:
    - "agent:houston"
    - "sensitivity:internal"

doc:
  projects:
    - "Mission Control"
    - "YourProject"
```

**Checklist:**
- [ ] Houston tags added to relevant docs
- [ ] Project tags include "Mission Control"
- [ ] Sensitivity level appropriate

### 6.2 Configure Houston Features

```bash
# Copy appropriate phase template
cp external/standards/examples/houston_phase1_observation.json \
   30_config/houston-features.json

# Customize for your environment
vim 30_config/houston-features.json
```

**Checklist:**
- [ ] Houston config file created
- [ ] Phase appropriate for trust level
- [ ] Safety controls enabled

### 6.3 Validate Houston Config

```bash
# Validate features config
python external/standards/validators/check_houston_features.py --verbose

# Validate tools config
python external/standards/validators/check_houston_tools.py --verbose
```

**Checklist:**
- [ ] Features config validates
- [ ] Tools config validates
- [ ] Phase consistency verified

---

## 7. Documentation Updates

### 7.1 Update Project README

Add section to README.md:

```markdown
## Metadata Standards

This project follows [C010_standards](https://github.com/jeremybrad/C010_standards)
for metadata schemas and validation.

### Schemas Used
- DocMeta v1.2 for documentation
- CodeMeta v1.0 for code artifacts

### Adding Metadata
See [docs/metadata_template.yaml](docs/metadata_template.yaml) for template.

### Validation
```bash
make validate  # Run metadata validation
```
```

**Checklist:**
- [ ] README updated with standards reference
- [ ] Schemas documented
- [ ] Validation instructions added

### 7.2 Add Developer Documentation

Create `docs/METADATA.md`:

```markdown
# Metadata Guide

## Overview
This project uses standardized metadata schemas...

## Adding Metadata to Documents

### DocMeta Example
```yaml
---
schema: "DocMeta.v1.2"
doc:
  title: "Your Document Title"
  # ... see template
---
```

## Validation
Run `make validate` before committing.

## Taxonomy
Use only approved topics from:
- monitoring
- deployment
- [see full list](../external/standards/taxonomies/topic_taxonomy.yaml)
```

**Checklist:**
- [ ] Developer guide created
- [ ] Examples provided
- [ ] Linked from main README

---

## 8. Testing & Validation

### 8.1 Test Migration

```bash
# Create test branch
git checkout -b test-metadata-migration

# Run full validation
python external/standards/validators/run_all.py

# Run tests (if applicable)
pytest tests/
```

**Checklist:**
- [ ] All validators pass
- [ ] No validation errors
- [ ] Tests pass

### 8.2 Peer Review

```bash
# Create PR for team review
git push -u origin test-metadata-migration

# Open PR with checklist:
```

**PR Checklist Template:**
```markdown
## Metadata Migration

- [ ] All files validate against schemas
- [ ] Taxonomy terms approved
- [ ] CI validation passing
- [ ] Documentation updated
- [ ] Team trained on new format
```

**Checklist:**
- [ ] PR created
- [ ] Peer review completed
- [ ] Feedback addressed

### 8.3 Staged Rollout

For large migrations:

1. **Week 1:** Migrate 10% of files
2. **Week 2:** Migrate 50% of files
3. **Week 3:** Migrate remaining files
4. **Week 4:** Remove old format support

**Checklist:**
- [ ] Rollout plan created
- [ ] Progress tracked
- [ ] Team informed of timeline

---

## 9. Maintenance & Updates

### 9.1 Monitor for Schema Updates

Subscribe to C010_standards updates:

```bash
# Watch repository on GitHub
# OR set up notification for new releases
```

**Checklist:**
- [ ] Team member assigned to monitor updates
- [ ] Update schedule established
- [ ] Notification system configured

### 9.2 Update Workflow

When new schema version released:

1. Review [VERSIONING_POLICY.md](VERSIONING_POLICY.md)
2. Check if MAJOR (breaking) or MINOR (compatible)
3. Review migration guide (if MAJOR)
4. Test in development branch
5. Update production

**Checklist:**
- [ ] Update procedure documented
- [ ] Testing requirements defined
- [ ] Rollback plan exists

### 9.3 Contribute Back

Contribute improvements to C010_standards:

- New taxonomy terms
- Schema clarifications
- Bug fixes in validators
- Additional examples

**Checklist:**
- [ ] Contributing guidelines reviewed
- [ ] PRs welcomed and encouraged
- [ ] Team knows how to contribute

---

## 10. Troubleshooting

### Common Issues

**Issue:** Validator not found
**Solution:** Check Python path and submodule init

**Issue:** Taxonomy validation fails
**Solution:** Use only terms from approved taxonomy, or submit PR for new terms

**Issue:** Schema version mismatch
**Solution:** Check which version you're using vs which validator expects

See [TROUBLESHOOTING.md](./TROUBLESHOOTING.md) for full guide.

---

## Completion Checklist

Use this final checklist to confirm migration is complete:

### Schema Adoption
- [ ] Schemas selected and documented
- [ ] Example files created
- [ ] Team trained on metadata format

### Validation
- [ ] Validators integrated
- [ ] Make/script commands added
- [ ] CI pipeline configured
- [ ] All validations passing

### Documentation
- [ ] README updated
- [ ] Developer guide created
- [ ] Examples provided
- [ ] Taxonomy documented

### Maintenance
- [ ] Update procedure defined
- [ ] Team member monitoring updates
- [ ] Contribution workflow established

---

## Support

For help with migration:

1. **Review documentation** in C010_standards
2. **Check examples** in `examples/` directory
3. **Open issue** in C010_standards repository
4. **Contact** project maintainers

**Estimated Timeline:**
- Simple project (validators only): 1-2 days
- Medium project (schema adoption): 1-2 weeks
- Complex project (full migration): 2-4 weeks

Good luck with your migration! 🎉
