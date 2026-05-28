# Foreign Keys

## Basic FK

```typescript
import { products } from "./products"

export const variants = pgTable("prd_variants", {
  productId: text("productId")
    .notNull()
    .references(() => products.id, { onDelete: "cascade" }),
})
```

## Self-referencing FK

```typescript
export const categories = pgTable("prd_categories", {
  parentId: text("parentId").references(() => categories.id, {
    onDelete: "set null",
  }),
})
```

## onDelete options

| Value | Behavior |
|---|---|
| `cascade` | Delete the child rows when parent is deleted |
| `set null` | Set FK column to NULL when parent is deleted (column must be nullable) |
| `restrict` | Prevent deletion if any child rows exist |
| `no action` | Default — same as restrict but checked at end of transaction |

## Must have FK for every xxxId column

Every column named `{entity}Id` should have a `.references()` declaration:

```typescript
// GOOD — has FK
countryId: text("countryId").references(() => countries.id)

// BAD — no FK, orphaned data possible
countryId: text("countryId")
```
