# JSONB Columns and GIN Indexes

## Table definition

```typescript
import { jsonb, index } from "drizzle-orm/pg-core"

export const prdFields = pgTable("prd_fields", {
  field: jsonb("field").notNull().default({}).$type<Record<string, unknown>>(),
  tags: jsonb("tags").notNull().default([]).$type<string[]>(),
  entityType: text("entity_type").notNull(),
  entityId: text("entity_id").notNull(),
}, (table) => [
  index("prd_field_gin_idx").using("gin", table.field),
  index("prd_field_tags_gin_idx").using("gin", table.tags),
])
```

## Polymorphic entity pattern

Use `entityType` + `entityId` to reference any entity type without a fixed FK:

```typescript
// Query fields for a product
const rows = await db.execute(sql`
  SELECT * FROM prd_fields
  WHERE entity_type = 'product' AND entity_id = ${productId}
`)
```

## Search with containment (`@>`)

The GIN index enables efficient JSON containment queries:

```typescript
const result = await db.execute(sql`
  SELECT * FROM prd_fields
  WHERE field @> ${JSON.stringify({ formato: "SVG" })}::jsonb
`)
```

## Search by tags

```typescript
// Single tag
WHERE tags ? 'react'

// Any of multiple tags  
WHERE tags ?| ${["react", "nextjs"]}::text[]

// All of multiple tags
WHERE tags ?& ${["react", "typescript"]}::text[]
```

## When to use JSONB vs columns

| Use JSONB when | Use columns when |
|---|---|
| Fields vary by category | Fields are known at design time |
| Schema is unpredictable | Need NOT NULL or FK constraints |
| Deeply nested data | Need indexes on individual fields |
| Attaching metadata | Accessed frequently in queries |
