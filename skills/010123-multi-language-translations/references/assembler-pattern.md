# Translation Assembler Pattern

## Strategy: Fetch all, filter in-memory

Instead of `WHERE language_code = ?` at query time, fetch ALL translations and find the matching one in code:

```typescript
async function getProductWithTranslations(productId: string, lang: string) {
  const product = await db.query.products.findFirst({
    where: eq(products.id, productId),
    with: { translations: true }
  })

  // Filter in-memory: find matching language or fallback
  const t = product.translations.find(t => t.languageCode === lang)
       ?? product.translations[0]

  return {
    id: product.id,
    name: t?.name ?? product.slug,
    description: t?.description ?? null,
    slug: t?.slug ?? product.slug,
    // ... translation fields
  }
}
```

## Cache: Single key per entity (all languages bundled)

```typescript
const cacheKey = `product:${productId}` // NO lang suffix!

await cache.set(cacheKey, enrichedProduct, ["products", `product:${productId}`])
```

Invalidation clears ALL language variants at once:

```typescript
await cache.invalidateTags(["products", `product:${productId}`])
```

## Why not per-language cache keys?

| Approach | Cache entries | Invalidation | Complexity |
|---|---|---|---|
| **Single key** (all languages) | 1 per entity | 1 tag removes all | Low |
| **Per-language key** (1 per lang) | N per entity | N tags to remove all | High |

Single key wins for small-N languages. Per-language keys only make sense for 20+ languages or when different languages have different update frequencies.
