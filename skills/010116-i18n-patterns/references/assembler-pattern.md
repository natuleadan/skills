# Translation Assembler Pattern

## Strategy: Fetch all, filter in-memory

Instead of filtering translations at query time with `WHERE language_code = ?`, fetch ALL translations for an entity and filter in-memory:

```typescript
async function getProduct(productId: string, lang: string) {
  // Single query joins ALL translations (no language filter)
  const result = await db.query.products.findBy({
    id: productId,
    with: { translations: true }
  })

  // Filter in-memory: find matching language or fallback
  const translation = result.translations.find(t => t.language_code === lang)
    ?? result.translations[0]

  return {
    id: result.id,
    name: translation?.name ?? result.slug,
    description: translation?.description ?? null,
    slug: translation?.slug ?? result.slug,
    // ...
  }
}
```

## Why?

| Approach | Pros | Cons |
|---|---|---|
| **SQL filter** (`WHERE lang = ?`) | Less data transferred | Cache miss per language, complex pagination |
| **In-memory filter** (all translations) | Single cache entry, simpler code | More data per query |

The in-memory approach:
- Caches once for all languages
- Avoids N cache keys per entity
- Fallback to first available translation is trivial
- Works well for small-N languages (under 20)

## Translation cache invalidation

```typescript
// On translation update:
await invalidateCache([
  `entity:${entityId}`,
  `entities:list`,
  `entities:list:${categoryId}`,
])
```

Cache keys should NOT include the language code since all languages are bundled in one cache entry.
