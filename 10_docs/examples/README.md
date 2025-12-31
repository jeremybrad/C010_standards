# C010_standards Examples

This directory contains example configurations and metadata templates to help you use C010_standards effectively.

## Houston Configuration Examples

### Phase 1 - Observation Mode
**File**: `houston_phase1_observation.json`

Initial trust-building phase with minimal agency. Houston operates in supervisory mode:
- Can notify and suggest
- Cannot execute actions without confirmation
- Basic monitoring only
- No deployment permissions

**Use when**: First setting up Houston, establishing baseline behavior.

### Phase 2 - Collaboration Mode
**File**: `houston_phase2_collaboration.json`

Enhanced collaboration with IDE integration:
- Advisory agency level
- Can execute with confirmation
- Can restart services
- Proactive alerts enabled
- Full memory integration

**Use when**: Trust is established, ready for Houston to actively assist.

### Phase 3 - Partnership Mode
**File**: `houston_phase3_partnership.json`

Full autonomous partnership with emergency protocols:
- Autonomous agency level
- Can execute without confirmation (with safety controls)
- Can deploy updates
- Emergency protocols enabled
- Full system management

**Use when**: Houston has proven reliable, full automation desired.

## Metadata Examples

### DocMeta Template
**File**: `docmeta_example.yaml`

Complete DocMeta v1.2 example showing:
- Required and optional fields
- Proper routing tags for Houston
- Taxonomy-compliant topic tags
- Entity tracking
- Governance flags

**Use for**: Tagging documents for Houston retrieval, SADB indexing.

### CodeMeta Template
**File**: `codemeta_example.yaml`

CodeMeta v1.0 example showing:
- Repository metadata
- Dependency tracking
- License information
- Build/deployment details

**Use for**: Tagging code repositories, scripts, libraries.

### Houston-Targeted Document
**File**: `houston_document_example.md`

Markdown document with DocMeta front matter configured for Houston agent:
- Required routing tags (`agent:houston`, `sensitivity:internal`)
- Project tags (`Mission Control`, `C010`)
- Valid topics from taxonomy
- Related documentation links

**Use for**: Creating Houston-retrievable documentation.

## Tool Configuration Examples

### Houston Tools - Phase 1
**File**: `houston_tools_phase1.json`

Minimal tool access for observation:
- Read-only filesystem access
- Process monitoring (no control)
- Basic network checks
- No dangerous operations

### Houston Tools - Phase 2
**File**: `houston_tools_phase2.json`

Enhanced tool access for collaboration:
- Read/write filesystem access
- Service restart capability
- Full deployment pipeline
- VPS integration (optional)

## Usage

### Copy and Customize

```bash
# Copy Houston config for your phase
cp examples/houston_phase1_observation.json 30_config/houston-features.json

# Customize for your environment
vim 30_config/houston-features.json

# Validate
python validators/check_houston_features.py --verbose
```

### Apply DocMeta Template

```bash
# Copy template
cp examples/docmeta_example.yaml my_document_meta.yaml

# Fill in your document details
vim my_document_meta.yaml

# Validate against taxonomy
python validators/check_houston_docmeta.py my_document_meta.yaml --verbose
```

### Use as Starting Point

All examples are fully validated and working configurations. Use them as:
- **Reference**: See what a complete, valid config looks like
- **Template**: Copy and customize for your needs
- **Testing**: Use in your own validation scripts

## Validation

All example files have been validated against their respective schemas and validators:

```bash
# Validate Houston configs
python validators/check_houston_features.py --config examples/houston_phase1_observation.json
python validators/check_houston_features.py --config examples/houston_phase2_collaboration.json
python validators/check_houston_features.py --config examples/houston_phase3_partnership.json

# Validate metadata examples
python validators/check_houston_docmeta.py examples/
```

## Notes

- **Phase progression**: Always start with Phase 1 and advance gradually
- **Taxonomy compliance**: Topic tags must exist in `taxonomies/topic_taxonomy.yaml`
- **Schema versions**: Check schema version numbers in comments
- **Customization**: Examples are starting points - adapt to your needs

## See Also

- [CONTRIBUTING.md](../CONTRIBUTING.md) - Guidelines for modifying schemas
- [schemas/](../schemas/) - Full schema definitions
- [taxonomies/](../taxonomies/) - Valid taxonomy values
- [validators/README.md](../validators/README.md) - Validation tool documentation
