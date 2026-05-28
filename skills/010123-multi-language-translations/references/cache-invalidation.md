# Cache Invalidation Across Languages

## Principle

Invalidate ALL languages when any translation changes. Don't maintain per-language cache entries.

## Tags

```typescript
const tags = {
  detail: (id: string) => [`${entity}:${id}`],
  list: () => [`${entity}:list`],
  catalog: () => ["catalog"],
}
```

## Invalidation chain

```typescript
// When a product translation is updated:
async function onTranslationUpdate(productId: string) {
  await invalidateCache([
    `product:${productId}`,     // detail page (all languages)
    `products:list`,            // listing pages
    `catalog`,                  // cross-domain catalog
  ])
}

// When a category translation is updated:
async function onCategoryTranslationUpdate(categoryId: string) {
  await invalidateCache([
    `category:${categoryId}`,   // category detail
    `categories:list`,          // category listing
    `catalog`,                  // cross-domain catalog
  ])
}
```

## No per-language invalidation

Avoid patterns like `invalidateAllForLang("es")`. If you need to invalidate only one language, you have separate cache keys per language, which means more complex cache code and more keys to manage.
