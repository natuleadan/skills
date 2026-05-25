# Caching Strategy

Next.js 16 uses `'use cache'` with tags for intelligent caching.

## Caching Directives

- **'use cache'** — make function/component cacheable
- **cacheTag()** — add one or more tags for invalidation
- **cacheLife()** — set TTL (time-to-live)

```tsx
'use cache'
import { cacheTag, cacheLife } from 'next/cache'

export async function getProduct(id: string) {
  cacheLife('hours')  // Cache for 1 hour
  cacheTag(`product:${id}`, 'products')

  return await db.products.findById(id)
}
```

## Invalidation

- **revalidateTag(tag)** — Standard SWR (stale-while-revalidate)
- **updateTag(tag)** — Immediate refresh in same request (read-your-writes)
- **revalidatePath(path)** — Invalidate entire path

```tsx
export async function updateProduct(id: string, data: any) {
  await db.products.update(id, data)

  // Update immediately
  updateTag(`product:${id}`)

  // Or soft refresh
  revalidateTag('products')
}
```

## Fetch Behavior

- **fetch is no-store by default** — not cached
- **unstable_cache** — for database/non-fetch queries with custom tags
- **cacheComponents: true** — enable in next.config.ts

## Rules

- [ ] **'use cache' at function top** — wraps all code below
- [ ] **cacheTag() before async work** — declare tags early
- [ ] **updateTag for mutations** — read-your-writes pattern
- [ ] **revalidateTag for soft updates** — stale-while-revalidate
- [ ] **Nested caches** — outer cache invalidates inner
