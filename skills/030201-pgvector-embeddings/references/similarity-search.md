# Similarity Search

## Basic vector search

```typescript
const vector = await generateEmbedding(query)
const vecStr = `[${vector.join(",")}]`

const result: any = await db.execute(sql`
  SELECT id, name, 1 - (embedding <=> ${vecStr}::vector) AS similarity
  FROM prd_embeddings
  WHERE 1 - (embedding <=> ${vecStr}::vector) > ${threshold}
  ORDER BY similarity DESC
  LIMIT ${limit}
`)
```

## Search with entity JOIN

```typescript
const result: any = await db.execute(sql`
  SELECT p.id, p.name, p.price, p.image,
    1 - (e.embedding <=> ${vecStr}::vector) AS similarity
  FROM prd_embeddings e
  JOIN prd_products p ON p.id = e.entity_id
  WHERE e.entity_type = 'product'
    AND 1 - (e.embedding <=> ${vecStr}::vector) > ${threshold}
  ORDER BY similarity DESC
  LIMIT ${limit}
`)
```

## Distance metrics

| Metric | Operator | pgvector function | Use case |
|---|---|---|---|
| Cosine | `<=>` | `cosineDistance()` | Text embeddings |
| L2 | `<->` | `l2Distance()` | Image embeddings |
| Inner product | `<#>` | `innerProduct()` | Normalized vectors |
| L1 | `<+>` | `l1Distance()` | Sparse vectors |
