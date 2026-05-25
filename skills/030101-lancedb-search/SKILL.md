---
name: 030101-lancedb-search
description: LanceDB vector search fundamentals — distance metrics, ANN indexing, embeddings, similarity search patterns, and performance tuning.
---

# Vector Search Core

## Overview

Core concepts for vector search with LanceDB: distance metrics, ANN indexing, embedding models, and search patterns.

## Quick Reference

### Distance Metrics

| Metric | Use Case | Behavior |
|--------|----------|----------|
| `l2` | General purpose | Smaller = more similar |
| `cosine` | Text/document similarity | Smaller = more similar |
| `dot` | Normalized vectors | Larger = more similar |
| `hamming` | Binary vectors | Smaller = more similar |

### Search Modes

- **Exact search**: Brute force, 100% recall, no index needed
- **ANN search**: Approximate, fast, requires index, configurable recall
- **Hybrid**: Vector + FTS combined with reranking

### Embedding Functions

- OpenAI: `text-embedding-ada-002`, `text-embedding-3-small`, `text-embedding-3-large`
- Sentence Transformers: local models via `sentence-transformers`
- Custom: create your own embedding function

## References

- [Vector Fundamentals](references/vector-fundamentals.md) — Distance metrics, ANN vs exact, nprobes
- [Vector Search Patterns](references/vector-search-patterns.md) — Prefiltering, binary search, batch, brute-force
- [Embeddings](references/embeddings.md) — Embedding function registry, dimension selection
