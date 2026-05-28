# Signed URL Caching

## Problem

Signed URLs have a limited TTL (usually 3600s). Generating one on every request is wasteful.

## Solution

Cache the signed URL for slightly less than its TTL, renewing before expiry.

```typescript
const SIGNED_URL_TTL = 3600  // 1 hour
const CACHE_TTL = SIGNED_URL_TTL - 100  // 3500s

async function resolveMediaUrl(media: any) {
  if (!media.filePath) return { ...media, signedUrl: null }

  const cacheKey = `media:signed:${media.id}`
  const cached = await cache.get<{ signedUrl: string }>(cacheKey)
  if (cached) return { ...media, signedUrl: cached.signedUrl }

  const signedUrl = await createSignedGetUrl(media.filePath, SIGNED_URL_TTL)
  if (signedUrl) {
    await cache.set(cacheKey, { signedUrl }, CACHE_TTL)
    return { ...media, signedUrl }
  }
  return { ...media, signedUrl: null }
}
```

## Cache invalidation on update

When the underlying media changes, invalidate the cached signed URL:

```typescript
await cache.del(`media:signed:${id}`)
```
