# Price Table Design

## Schema

```typescript
const prices = pgTable("prd_prices", {
  id: id(),
  productId: text("productId").notNull().references(() => products.id, { onDelete: "cascade" }),
  variantId: text("variantId").references(() => variants.id, { onDelete: "cascade" }),
  currencyId: text("currencyId").notNull().references(() => currencies.code),
  price: numeric("price", { precision: 10, scale: 2 }).notNull(),
  compareAtPrice: numeric("compareAtPrice", { precision: 10, scale: 2 }),
  cost: numeric("cost", { precision: 10, scale: 2 }),
  isActive: boolean("isActive").default(true),
  validFrom: timestamp("validFrom").defaultNow(),
  validUntil: timestamp("validUntil"),
})
```

## Unique constraint

```sql
UNIQUE (product_id, variant_id, currency_id)
```

Use `NULLS NOT DISTINCT` for databases that support it (PostgreSQL 15+).

## Price resolution

```typescript
function resolvePrice(prices: Price[], currencyCode: string, variantId?: string) {
  // 1. Variant-specific price in requested currency
  if (variantId) {
    const vp = prices.find(p => p.currencyId === currencyCode && p.variantId === variantId)
    if (vp) return vp
  }
  // 2. Product-level price in requested currency
  return prices.find(p => p.currencyId === currencyCode && !p.variantId)
}
```
