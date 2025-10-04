# Taxonomy Packages

Canonical taxonomy assets consolidated from SADB repositories. Each file retains original attribution via header comments and preserves upstream structure.

## Coverage
- `content_taxonomy.yaml` — derived from `../P002_sadb/30_config/CONTENT_TAXONOMY.yaml` (July 7, 2025 cross-corpus analysis). Replaces legacy fixtures under `30_taxonomy/`.
- `emotion_taxonomy.yaml` — full emotional register (work + sacred/poetic) from `../P002_sadb/30_config/EMOTION_TAXONOMY.yaml`. Supersedes empty placeholder in `30_taxonomy/`.
- `topic_taxonomy.yaml` — active topic list from `../P002_sadb/30_taxonomy/topic_taxonomy_actual.yaml`. Test stub `topic_taxonomy.yaml` kept only in source repo.
- `metadata_taxonomy.yaml` — workspace tagging defaults (speakers, types, primary/secondary categories) from `../P002_sadb/30_config/taxonomy.yaml`.
- `universal_terms.yaml` — synonym registry with Claude/Betty register context from `../P002_sadb/30_config/UNIVERSAL_TERMS.yaml`.
- `disambiguation_rules.yaml` — contextual rules for interpreting shared vocabulary (Claude vs Betty usage) from `../P002_sadb/30_config/DISAMBIGUATION_RULES.yaml`.
- `topic_stoplist.yaml` — stopword list for topic extraction from `../P002_sadb/30_config/TOPIC_STOPLIST.yaml`.
- `taxonomy_additions_cross_corpus.yaml` — archived July 7, 2025 expansion package (never implemented). Includes proposed new emotions/content types, register disambiguation cues, and universal term extensions.

## Notes on Duplicates & Gaps
- `30_taxonomy/` contained truncated fixtures used for testing; canonical copies here point back to the richer `30_config/` sources.
- The additions archive documents discoveries not yet merged into production taxonomies; keep separate until validated.
- Any divergence or updates should be logged in `notes/CHANGELOG.md` and cross-referenced here for adoption planning.
