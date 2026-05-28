# Vector Columns and HNSW Indexes

## Table definition

```typescript
import { vector, index } from "drizzle-orm/pg-core"

export const prdEmbeddings = pgTable("prd_embeddings", {
  id: text("id").primaryKey().default(sql`gen_random_uuid()::text`),
  embedding: vector({ dimensions: 384 }),
  entityType: text("entity_type").notNull(),
  entityId: text("entity_id").notNull(),
}, (table) => [
  index("prd_embedding_hnsw_idx")
    .using("hnsw", table.embedding.op("vector_cosine_ops")),
])
```

## Inserting vectors

```typescript
// Using raw SQL cast (required by pgvector)
const vector = [0.023, -0.456, /* ...384 values */]
const vecStr = sql`${`[${vector.join(",")}]`}::vector`

await db.insert(table).values({ embedding: vecStr } as any)
```

## Similarity search

```typescript
const vector = await generateEmbedding(query)
const vecStr = `[${vector.join(",")}]`

const result = await db.execute(sql`
  SELECT p.id, p.name, 1 - (e.embedding <=> ${vecStr}::vector) AS similarity
  FROM prd_embeddings e
  JOIN prd_products p ON p.id = e.entity_id
  WHERE e.entity_type = 'product'
    AND 1 - (e.embedding <=> ${vecStr}::vector) > ${threshold}
  ORDER BY similarity DESC
  LIMIT ${limit}
`)
```

## Distance metrics

| Operator | Metric | Use case |
|---|---|---|
| `<=>` | Cosine similarity | Text embeddings, semantic search |
| `<->` | L2 (Euclidean) | Image embeddings |
| `<#>` | Inner product | Normalized vectors |
| `<+>` | L1 (Manhattan) | Sparser vectors |
