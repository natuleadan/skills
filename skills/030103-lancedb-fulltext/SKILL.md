---
name: 030103-lancedb-fulltext
description: LanceDB full-text search — BM25 indexing, FTS querying, fuzzy search, phrase queries, field boosting, and boolean search.
license: MIT
compatibility: Requires Python 3.10+ with lancedb and tantivy
---

# Full-Text Search

## Overview

Full-text search with LanceDB using BM25 indexing. Covers FTS index creation, query patterns, fuzzy search, and advanced filtering.

## Quick Reference

### FTS Index

```python
table.create_fts_index("text_column", replace=True)
```

### Basic Query

```typescript
const results = await table.search("search terms", queryType="fts").toArray()
```

### FTS Features

| Feature | API | Description |
|---------|-----|-------------|
| Phrase | `"exact phrase"` | Exact phrase matching |
| Fuzzy | `term~1` | Levenshtein distance |
| Field boost | `field:term^2` | Weighted field scoring |
| Boolean | Must/Should | AND/OR term combinations |
| Filtering | `.filter(sql)` | Metadata pre-filtering |

## References

- [FTS Index](references/fts-index.md) — Index creation, BM25 configuration, tokenization
- [FTS Querying](references/fts-querying.md) — Query patterns, phrase search, index usage
- [FTS Advanced](references/fts-advanced.md) — Fuzzy, boosting, boolean, array fields, filtering
