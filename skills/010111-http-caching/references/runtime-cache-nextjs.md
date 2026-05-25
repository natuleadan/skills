# Runtime Cache (Next.js)

The runtime cache stores function outputs within the same region using Next.js cache APIs.

## Scope & Behavior

- **Scope**: Regional, per-project, per-environment
- **Persistence**: Ephemeral (LRU eviction)
- **Invalidation**: TTL, `revalidateTag()`, `revalidatePath()`

## Usage

```typescript
import { cacheLife, cacheTag } from "next/cache"

async function getData() {
  "use cache"
  cacheTag("my-tag")
  cacheLife({ expire: 3600 })
  return await fetch("https://api.example.com/data").then(r => r.json())
}
```

## Invalidation

```typescript
import { revalidateTag, revalidatePath } from "next/cache"

// Invalidate by tag
revalidateTag("my-tag")

// Invalidate by path
revalidatePath("/products")
```
