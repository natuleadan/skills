---
name: 050402-index-optimization
description: LanceDB vector index types (IVF, HNSW, PQ, RQ), quantization techniques, reindexing strategies, and performance tuning.
---

# Vector Indexing & Optimization

## Overview

Index types, quantization, and reindexing strategies for LanceDB vector search performance.

## Quick Reference

### Index Types

| Index | Best For | Quantization |
|-------|----------|-------------|
| IVF_PQ | General purpose | Product Quantization |
| IVF_HNSW_SQ | High recall | Scalar Quantization |
| IVF_HNSW_PQ | Large datasets | Product Quantization |
| IVF_FLAT | Small datasets, 100% recall | None |
| IVF_RQ | Binary vectors | RaBitQ (1 bit/dim) |

### Quantization

| Type | Bits/Dim | Compression | Recall Impact |
|------|----------|-------------|---------------|
| None | 32 | 1x | None |
| SQ | 8 | 4x | Minimal |
| PQ | 4-8 | 4-8x | Moderate |
| RQ (RaBitQ) | 1 | 32x | Low-moderate |

### Reindexing

```python
table.optimize()  # Compaction + cleanup + index update
```

## References

- [Vector Index Types](references/vector-index.md) — IVF, HNSW, PQ, RQ index selection and tuning
- [Indexing Concepts](references/indexing.md) — Internal mechanics, disk-based indexing
- [Quantization](references/quantization.md) — Compression techniques, accuracy tradeoffs
- [Reindexing](references/reindex.md) — Incremental updates, compaction, optimization
