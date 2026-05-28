# Table Conventions

## Prefixes

| Prefix | Domain | Example |
|---|---|---|
| `prd_` | Production data | `prd_products`, `prd_variants` |
| `sys_` | System internals | `sys_currencies`, `sys_cron_jobs` |
| `usr_` | Better Auth users | `usr_users`, `usr_sessions` |
| `tst_` | Test data only | `tst_vector_items` |

## Primary Keys

Use the `id()` helper from `_cuid.ts`:

```typescript
import { id } from "../_cuid"

export const products = pgTable("prd_products", {
  id: id(),  // text + UUID v4 + PK
  // ...
})
```

The `id()` helper generates a UUID v4 via `crypto.randomUUID()`.

## Timestamps

Use the `timestamps` spread:

```typescript
import { timestamps } from "../_timestamps"

export const products = pgTable("prd_products", {
  // ... fields
  ...timestamps,
  // → createdAt, updatedAt, deletedAt
})
```

## Slug

Use the `slug()` helper for SEO-friendly unique identifiers:

```typescript
slug: slug(),  // text + unique, 12-char UUID prefix
```

## Naming

- Columns: `camelCase` — Drizzle auto-converts to `snake_case` in SQL
- Tables: `snake_case` with `{prefix}_{name}` pattern
- Files: kebab-case matching the table name
