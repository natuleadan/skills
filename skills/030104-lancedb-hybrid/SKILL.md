---
name: 030104-lancedb-hybrid
description: LanceDB hybrid search (vector + FTS with RRF), multivector search (ColBERT late interaction), and metadata filtering patterns.
---

# Hybrid & Multivector Search

## Overview

Advanced search patterns combining vector and text search, multi-embedding late interaction models (ColBERT), and metadata filtering.

## Quick Reference

### Hybrid Search

```
vector search + FTS → RRF fusion → reranked results
```

```typescript
const results = await table.search("query")
  .vector(queryVector)
  .text("search terms")
  .reranker(new RRFReranker(100))
  .toArray()
```

### Multivector (ColBERT)

- Late interaction: query tokens ↔ document tokens
- MaxSim scoring for relevance
- IVF_PQ index with cosine metric for multivector columns

### Filtering

| Approach | When | Performance |
|----------|------|-------------|
| Pre-filter | Before ANN | Fast with scalar indexes |
| Post-filter | After ANN | May lose results |
| Push-down | SQL pushdown | Most efficient |

## References

- [Hybrid Search](references/hybrid-search.md) — Vector + FTS combination, RRF reranking
- [Multivector Search](references/multivector-search.md) — ColBERT, late interaction, MaxSim scoring
- [Filtering](references/filtering.md) — Pre/post filtering, SQL expressions, scalar indexes
