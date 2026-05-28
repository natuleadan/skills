# Raw SQL with `sql\`\``

## When to use raw SQL

Drizzle's query builder handles most cases, but raw `sql\`\`` is needed for:

- Calling PostgreSQL functions (`gen_random_uuid()`, `to_tsvector()`)
- Using pgvector operators (`<=>`, `<->`)
- JSONB containment (`@>`) with GIN indexes
- `EXPLAIN ANALYZE` queries
- Dynamic table names (via `sql.raw()`)
- Complex JOINs with custom filtering

## Basic patterns

```typescript
import { sql } from "drizzle-orm"

// Parameter binding (safe from injection)
const result = await db.execute(sql`
  SELECT * FROM users WHERE email = ${email}
`)

// Raw identifiers (use with caution)
const result = await db.execute(sql`
  EXPLAIN ANALYZE SELECT * FROM ${sql.raw(tableName)}
`)

// JSONB operation
sql`field @> ${JSON.stringify(query)}::jsonb`

// Vector distance
sql`1 - (e.embedding <=> ${vecStr}::vector) AS similarity`
```

## Return type

`db.execute(sql\`...\`)` returns `{ rows: T[], rowCount: number, fields: any[] }`. Access rows via `.rows`:

```typescript
const result: any = await db.execute(sql`SELECT * FROM items`)
return (result?.rows ?? []) as Item[]
```

## `sql.raw()` warning

Never use `sql.raw()` with user-supplied values — it bypasses parameter binding and creates SQL injection risk. Only use with hardcoded table names or column identifiers.
