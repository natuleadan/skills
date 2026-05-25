---
name: 010111-http-caching
description: Three-tier caching architecture — browser, runtime, and distributed cache. Pipeline batching, atomic transactions, invalidation patterns.
---

# Caching Strategies

## Overview

Three caching layers, each with different scope and purpose:

```
Browser Cache         ← Cache-Control headers (CDN edge)
  ↓
Runtime Cache         ← "use cache" + cacheLife/cacheTag (regional, ephemeral)
  ↓
Distributed Cache     ← KV store (global, persistent)
  ↓
Database              ← Source of truth
```

## Layer 1: Runtime Cache (Regional)

Stores function outputs within the same region.

- **Scope**: Regional, per-project, per-environment
- **Persistence**: Ephemeral (LRU eviction)
- **Invalidation**: TTL, `revalidateTag()`, `revalidatePath()`

```typescript
import { cacheLife, cacheTag } from "next/cache"

async function getData() {
  "use cache"
  cacheTag("my-tag")
  cacheLife({ expire: 3600 })
  return await fetch("https://api.example.com/data").then(r => r.json())
}
```

```typescript
import { revalidateTag, revalidatePath } from "next/cache"
revalidateTag("my-tag")
revalidatePath("/products")
```

## Layer 2: Distributed Cache (Global)

Shared across all regions, persistent, TTL-based.

### Features

- Auto-pipelining (batch multiple commands into one HTTP request)
- Per-key TTL
- Global across all regions
- Falls back silently when credentials are missing
- Batch helper for multi-key operations

### Pipeline Strategy

```typescript
// Sequential — N requests (one per await)
const a = await cache.get("foo")
const b = await cache.get("bar")

// Batch — 1 request (Promise.all triggers pipeline)
const [a, b] = await execBatch([
  cache.get("foo"),
  cache.get("bar"),
])
```

### Atomic Transactions

For commands that must execute atomically, use `multi()`:

```typescript
const tx = multi()
tx.set("inventory:item:1", JSON.stringify({ qty: 5 }))
tx.incr("inventory:reserved")
const [setRes, incrRes] = await tx.exec()
```

`multi()` wraps `MULTI/EXEC` — guarantees atomic execution.

## Layer 3: CDN Cache (Browser/Edge)

Cache-Control headers, `s-maxage`, `stale-while-revalidate` at the edge/CDN layer.

## Principles

1. **Runtime Cache first** for regional data (faster, no network call)
2. **Distributed cache** for global/stateful data
3. **CDN Cache** for HTTP responses same for all users
4. **Never cache user-specific data** without `Vary` header
5. **Tag-based invalidation** over TTL for predictable updates
6. **TTL fallback** ensures stale data is eventually refreshed

## Quick Reference

| Layer | Scope | TTL | Invalidation |
|-------|-------|-----|-------------|
| Browser/CDN | Global | hours-days | `Cache-Control`, redeploy |
| Runtime | Regional | seconds-hours | `revalidateTag`, `revalidatePath` |
| Distributed | Global | minutes-hours | TTL, manual delete |

## References

- [Caching Patterns](references/caching-patterns.md)
- [Cache Keys & Revalidation](references/cache-keys-revalidation.md) — Hierarchical cache keys, domain-scoped tags, mutation-triggered invalidation
