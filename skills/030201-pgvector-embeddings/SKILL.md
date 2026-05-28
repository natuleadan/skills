---
name: 030201-pgvector-embeddings
description: Vector search with pgvector — embedding generation (OpenAI or hash), HNSW indexing, cosine similarity search, and enriched product JOIN queries.
license: MIT
compatibility: PostgreSQL 16+ with pgvector 0.8+
---

# pgvector Embeddings

## When to use

When implementing semantic search, recommendation systems, or any feature requiring vector similarity in PostgreSQL.

## References

| Topic | File |
|---|---|
| Embedding generation | `references/embedding-generation.md` |
| HNSW index setup | `references/hnsw-index.md` |
| Cosine similarity search | `references/similarity-search.md` |
| Hybrid search patterns | `references/hybrid-search.md` |

## Quick checklist

- [ ] Install pgvector extension: `CREATE EXTENSION vector;`
- [ ] Define columns with `vector({ dimensions: 384 })` or 1536 for OpenAI
- [ ] Create HNSW index for fast approximate search
- [ ] Use cosine similarity (`<=>`) for text embeddings
- [ ] Generate embeddings with OpenAI or deterministic hash fallback
- [ ] Search with `WHERE 1 - (embedding <=> $vector) > threshold`
- [ ] JOIN with entities for enriched results
