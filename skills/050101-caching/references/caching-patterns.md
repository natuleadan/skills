# Caching Patterns Reference

## Three-Tier Architecture

| Layer | Storage | Latency | Use Case |
|-------|---------|---------|----------|
| Browser/CDN | CDN edge nodes | ~10ms | Public pages, assets, API responses |
| Runtime | Regional server memory | ~1ms | Per-request data, SSR output |
| Distributed | Global KV store | ~5ms | Sessions, rate limits, shared state |

## Invalidation Strategies

| Strategy | When | How |
|----------|------|-----|
| TTL-based | Always | Set `expire` time on write |
| Tag-based | On data change | `revalidateTag("tag-name")` |
| Path-based | On page change | `revalidatePath("/url")` |
| Manual | On demand | `cache.del("key")` |

## Pipeline Batching

Group independent cache reads to reduce network round-trips:

```typescript
// Bad: N sequential requests
const a = await cache.get("a")
const b = await cache.get("b")

// Good: 1 batched request
const [a, b] = await execBatch([
  cache.get("a"),
  cache.get("b"),
])
```

## Atomic Transactions

Use `MULTI/EXEC` for operations that must execute as a unit:

```typescript
const tx = multi()
tx.decr("inventory:count")
tx.sadd("inventory:sold", itemId)
await tx.exec()
```

## Graceful Degradation

- Set timeouts on all cache operations
- Fall through to database when cache is unreachable
- Log cache failures for monitoring
- Never crash on cache miss

## Cache Strategy by Data Type

| Data | Recommended TTL | Layer | Invalidation |
|------|----------------|-------|-------------|
| User session | 5-15 min | Distributed | On logout |
| Rate limit | 10s-60min | Distributed | Automatic |
| Public API response | 5-60 min | CDN | TTL |
| SSR page output | 30-300s | Runtime | TTL + revalidation |
| Static assets | 1 year | CDN | Content hash |
| Health checks | 10-30s | Runtime | TTL |

## Common Pitfalls

1. **Stale data**: TTL too long → set shorter TTL or use tag-based invalidation
2. **Cache stampede**: High TTL + high traffic → use probabilistic early expiration
3. **No fallback**: Cache dead → app dead → always add fallback to source of truth
4. **Over-caching**: Everything cached → stale everywhere → be selective
5. **Missing Vary header**: User-specific data cached for wrong user → add `Vary: Cookie`
