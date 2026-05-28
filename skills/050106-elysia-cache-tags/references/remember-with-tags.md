# Cache-Aside with Tags

## Basic operations

```typescript
import * as cache from "@/app/lib/service/cache"

// Store value + associate with tags
await cache.setWithTags("key", data, [cache.tagProducts, cache.tagCatalog], 30)

// Cache-aside read-through with tags
const data = await cache.rememberWithTags(
  "key",
  () => fetchExpensiveData(),
  [cache.tagProducts, cache.tagCatalog],
  30
)

// Invalidation
await cache.invalidateTags([
  cache.tagProducts,
  cache.tagCatalog,
  cache.tagProduct(productId),
])
```

## Implementation

```typescript
export async function setWithTags<T>(key, data, tags, ttl = 30) {
  await kv.send("SET", [key, JSON.stringify(data), "EX", String(ttl)])
  for (const tag of tags) {
    await kv.send("SADD", [tag, key])
    await kv.send("EXPIRE", [tag, String(ttl * 2)])
  }
}

export async function invalidateTag(tag) {
  const members = await kv.send("SMEMBERS", [tag])
  if (members?.length) await kv.send("DEL", [tag, ...members])
}
```
