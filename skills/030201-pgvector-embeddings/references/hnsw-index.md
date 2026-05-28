# HNSW Index Setup

## What is HNSW?

Hierarchical Navigable Small World — an approximate nearest neighbor (ANN) index that provides fast vector similarity search with configurable recall vs. speed trade-offs.

## Drizzle definition

```typescript
import { vector } from "drizzle-orm/pg-core"

export const prdEmbeddings = pgTable("prd_embeddings", {
  id: id().primaryKey(),
  entityType: text("entity_type").notNull(),
  entityId: text("entity_id").notNull(),
  embedding: vector("embedding", { dimensions: 384 }).notNull(),
})
```

## SQL index creation

```sql
CREATE INDEX idx_prd_embeddings_hnsw ON prd_embeddings
USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 200);
```

## Parameters

| Parameter | Default | Range | Effect |
|---|---|---|---|
| `m` | 16 | 2–100 | Max connections per node (higher = better recall, slower build) |
| `ef_construction` | 200 | 4–1000 | Build-time search width (higher = better recall, slower build) |

## Search-time `ef`

```sql
SET hnsw.ef_search = 100;  -- per-session (default: 40)
```

Higher `ef_search` = better recall, slower query.

## Production considerations

- HNSW builds in memory first, then writes to disk — ensure sufficient RAM
- Index build is single-threaded per index — build during low traffic
- For 384-dim vectors with 10k rows, HNSW is ~100x faster than exact search
- Monitor with `EXPLAIN ANALYZE` to verify index usage
