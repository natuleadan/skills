---
name: 050106-elysia-cache-tags
description: Tag-based cache invalidation for Elysia — 3-level tags (entity/domain/cross) via Redis Sets, cache-aside, invalidation chains, and signed URL caching.
license: MIT
compatibility: Requires Redis-compatible KV (Valkey, DragonflyDB, Redis) + Bun RedisClient
---

# Elysia Cache Tags

## When to use

When you need fine-grained cache invalidation beyond simple key-based TTL. Tags let you invalidate related cache entries in bulk.

## References

| Topic | File |
|---|---|
| 3-level tag system | `references/tag-levels.md` |
| Cache-aside with tags | `references/remember-with-tags.md` |
| Invalidation chains | `references/invalidation-chains.md` |
| Signed URL caching | `references/signed-url-cache.md` |

## Quick checklist

- [ ] Level 1: entity-specific tag (`cache:tags:{domain}:{entityId}`)
- [ ] Level 2: domain collection tag (`cache:tags:{domain}`)
- [ ] Level 3: cross-domain tag (`cache:tags:cross:{scope}`)
- [ ] Use `setWithTags(key, data, tags, ttl)` when storing cached values
- [ ] Use `invalidateTags([tag1, tag2, ...])` to batch-invalidate
- [ ] Tag sets TTL = 2x value TTL (ensures tags outlive their members)
- [ ] For signed URLs, cache the URL for 3500s (just under the 3600s expiry)
