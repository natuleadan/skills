# Hybrid Search

## What is hybrid search?

Combines vector similarity (semantic) with keyword matching (lexical) for better results. The vector search finds conceptually related items; keyword search filters by exact terms.

## PostgreSQL hybrid approach

```typescript
const vector = await generateEmbedding(query)
const vecStr = `[${vector.join(",")}]`
const term = `%${query}%`

const result: any = await db.execute(sql`
  SELECT p.id, p.name, p.description,
    1 - (e.embedding <=> ${vecStr}::vector) AS vector_score
  FROM prd_embeddings e
  JOIN prd_products p ON p.id = e.entity_id
  WHERE e.entity_type = 'product'
    AND (
      p.name ILIKE ${term}
      OR p.description ILIKE ${term}
      OR 1 - (e.embedding <=> ${vecStr}::vector) > 0.5
    )
  ORDER BY
    CASE
      WHEN p.name ILIKE ${term} THEN 1
      WHEN p.description ILIKE ${term} THEN 2
      ELSE 3
    END,
    vector_score DESC NULLS LAST
  LIMIT ${limit}
`)
```

## Weighted hybrid approach

```typescript
SELECT
  p.*,
  (0.7 * (1 - (e.embedding <=> ${vecStr}::vector))
   + 0.3 * ts_rank(p.search_vector, query)) AS combined_score
FROM prd_embeddings e
JOIN prd_products p ON p.id = e.entity_id
, plainto_tsquery('english', ${query}) AS query
WHERE e.entity_type = 'product'
  AND (
    1 - (e.embedding <=> ${vecStr}::vector) > 0.5
    OR p.search_vector @@ query
  )
ORDER BY combined_score DESC
LIMIT ${limit}
```

## Full-text search vector setup

```sql
ALTER TABLE prd_products ADD COLUMN search_vector tsvector
  GENERATED ALWAYS AS (
    to_tsvector('english', coalesce(name, '') || ' ' || coalesce(description, ''))
  ) STORED;

CREATE INDEX idx_products_fts ON prd_products USING GIN (search_vector);
```

## When to use each

| Mode | Best for |
|---|---|
| Pure vector | Concept/topic search ("sustainable outdoor gear") |
| Pure FTS | Exact term search ("red hiking boots size 10") |
| Hybrid | General product search in e-commerce |
