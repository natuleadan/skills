# Invalidation Chains

## Concept

When entity A changes, entities B and C that depend on A must also be invalidated. Chains define these relationships.

## Product change chain

```
prd_products:updated
  → invalidate products:123 (L1 — product detail)
  → invalidate products     (L2 — product list)
  → invalidate cross:catalog (L3 — catalog pages)
  → invalidate cross:admin   (L3 — admin dashboard)
```

## Variant creation chain

```
prd_variants:created (productId=123)
  → invalidate products:123 (L1 — product detail includes variants)
  → invalidate variants:456 (L1 — variant detail)
  → invalidate products     (L2 — product list shows prices with variants)
  → invalidate cross:catalog (L3 — storefront)
```

## Implementation

```typescript
export async function invalidateProductChain(productId: string) {
  await cache.invalidateTags([
    `cache:tags:products:${productId}`,
    "cache:tags:products",
    "cache:tags:cross:catalog",
  ])
}

export async function invalidatePriceChain(productId: string) {
  await cache.invalidateTags([
    `cache:tags:products:${productId}`,
    "cache:tags:prices",
    "cache:tags:products",
    "cache:tags:cross:catalog",
  ])
}
```

## Invalidation map

| Event | Tags invalidated |
|---|---|
| Product updated | product:{id}, products, cross:catalog, cross:admin |
| Variant created | product:{id}, variants, products, cross:catalog |
| Price changed | product:{id}, prices, products, cross:catalog |
| Media added | product:{id}, medias, products, cross:catalog |
| Rating submitted | product:{id}, ratings, products, cross:catalog |
| Inventory changed | product:{id}, inventory, products |
| Coupon created | coupons, cross:checkout |
| Category changed | categories, products, cross:catalog |
