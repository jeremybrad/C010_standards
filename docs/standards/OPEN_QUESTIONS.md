# C010_standards Open Questions

**Last Updated**: 2026-01-12
**Version**: 1.0.0

Unresolved decisions, known limitations, and future considerations.

## Architecture Questions

### Schema Versioning Strategy

**Current State**: Schemas use simple version suffixes (docmeta_v1.2.yaml, codemeta_v1.0.yaml)

**Question**: Should we adopt semantic versioning with breaking change indicators?

| Option | Pros | Cons |
|--------|------|------|
| Keep current (v1.2) | Simple, familiar | No breaking change signal |
| SemVer (1.2.0) | Industry standard | More complex filenames |
| Date-based (2026-01) | Clear timeline | Less intuitive |

**Resolution**: Pending - current approach works for now

### Validator Orchestration

**Current State**: `run_all.py` stops on first failure

**Question**: Should validators continue and report all failures?

| Option | Pros | Cons |
|--------|------|------|
| Stop on first | Fast feedback | May hide other issues |
| Run all, report all | Complete picture | Slower, more output |
| Configurable | Flexible | More complex |

**Resolution**: Pending - may add `--continue-on-error` flag

## Known Limitations

### Protocol Limitations

| Limitation | Impact | Workaround |
|------------|--------|------------|
| No protocol inheritance | Each protocol standalone | Copy shared sections |
| Manual sync to consumers | Standards drift possible | CI/CD checks |
| No protocol deprecation process | Old protocols linger | Manual cleanup |

### Taxonomy Limitations

| Limitation | Impact | Workaround |
|------------|--------|------------|
| Flat hierarchy only | No nested topics | Use compound terms |
| No multilingual support | English only | N/A |
| No versioned taxonomies | Breaking changes risky | Careful additions |

### Validator Limitations

| Limitation | Impact | Workaround |
|------------|--------|------------|
| Python 3.11+ required | Older environments fail | Specify version |
| No parallel execution | Slower for many repos | Run selectively |
| Console output only | No structured reports | Pipe to file |

## Security Considerations

### Houston Trust Phase Automation

**Question**: Should trust phase advancement be automated based on metrics?

**Current Approach**: Manual phase changes only

**Potential Improvements**:
- Auto-advance after N successful operations
- Auto-demote on validation failures
- Configurable thresholds

**Resolution**: Manual preferred for safety

### Taxonomy Injection Prevention

**Question**: How to prevent malicious taxonomy entries?

**Current Approach**: Git review + protected branches

**Potential Improvements**:
- Automated term validation
- Blocklist for dangerous patterns
- Schema-based constraints

**Resolution**: Current approach sufficient for internal use

## Feature Roadmap Questions

### Multi-Workspace Support

**Current State**: Single workspace (SyncedProjects) assumed

**Question**: Should standards support multiple independent workspaces?

**Considerations**:
- Paths currently hardcoded to `~/SyncedProjects`
- Registry assumes single workspace
- Would require configuration layer

**Resolution**: Not planned - single workspace sufficient

### Protocol Testing Framework

**Current State**: No automated protocol testing

**Question**: Should we add tests that verify protocol compliance?

**Considerations**:
- Protocols are documentation, not code
- Validators partially cover this
- Would need example repos

**Resolution**: Partial coverage via validators; full framework not planned

### Taxonomy API

**Current State**: Taxonomies are static YAML files

**Question**: Should we provide a lookup API?

**Considerations**:
- Would enable runtime validation
- Adds service dependency
- Current grep-based lookup works

**Resolution**: Not planned - YAML files sufficient

## Integration Questions

### NotebookLM Sync Frequency

**Current State**: Manual sync via MCP tools

**Question**: Should Tier 3 docs auto-sync on commit?

**Considerations**:
- Requires webhook or CI/CD integration
- NotebookLM API rate limits apply
- Manual control preferred for now

**Resolution**: Manual sync preferred

### Cross-Repo Validation

**Current State**: Validators run per-repo

**Question**: Should we validate cross-repo relationships?

**Considerations**:
- Registry contains relationship data
- Would catch broken references
- Requires workspace-wide scan

**Resolution**: Partial - registry validates relationships

## Performance Questions

### Large Registry Performance

**Current State**: 66+ repos in single repos.yaml

**Question**: Will performance degrade at 200+ repos?

**Current Approach**: Simple YAML load

**Potential Improvements**:
- Index by project ID
- Split by series (C/P/W)
- Database backend

**Resolution**: Not yet an issue - monitor as workspace grows

### Validator Parallelization

**Current State**: Sequential validator execution

**Question**: Should validators run in parallel?

**Considerations**:
- Python GIL limits threading benefit
- Multiprocessing adds complexity
- Current runtime acceptable (~5s)

**Resolution**: Not planned unless runtime becomes problematic

## Resolved Questions

| Question | Resolution | Date |
|----------|------------|------|
| DocMeta version | v1.2 adopted as standard | 2025-12 |
| Houston validator suite | All 5 validators complete | 2025-12 |
| Tier 3 doc structure | 7 docs standard adopted | 2026-01 |
| Receipt format | Markdown with standard headers | 2025-10 |
| Taxonomy format | YAML with flat structure | 2025-09 |

## Contributing Questions

If you encounter an unresolved question:

1. Check existing issues on GitHub
2. Add question to this document with context
3. Propose options if you have ideas
4. Reference related code or protocol behavior

## Related Documentation

- [ARCHITECTURE.md](ARCHITECTURE.md) - System design context
- [SECURITY_AND_PRIVACY.md](SECURITY_AND_PRIVACY.md) - Security decisions
- [OPERATIONS.md](OPERATIONS.md) - Operational context
