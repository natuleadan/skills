# Cache Keys & Revalidation

Cache layer with tag-based revalidation.

## Cache Keys

Hierarchical format: `domain:entity:params[:lang][:currency]`

Examples:
- `products:list:all`
- `products:list:all:en`
- `products:list:all:en:usd`
- `products:detail:product-id-123`
- `users:profile:user-id-456`

### Language and currency in cache keys

In multi-lingual, multi-currency applications, cache keys MUST include language and currency to prevent serving the wrong content:

```typescript
function buildCacheKey(domain: string, id: string, lang: string, currency: string) {
  return `${domain}:${id}:${lang}:${currency}`
}

// Example: "products:detail:abc123:en:usd"
// Example: "products:detail:abc123:es:eur"
```

Tags should NOT include lang/currency since invalidation should clear across all languages:

## Tags vs Cache Keys

| Concept | Includes lang/currency? | Purpose |
|---|---|---|
| **Cache key** | ✅ Yes (`products:detail:abc:en`) | Uniquely identifies a cached response |
| **Tag** | ❌ No (`products`, `categories`) | Groups related entries for bulk invalidation |

Tags are always language-agnostic. Invalidating tag `products` clears cache for ALL languages:

```typescript
// Cache a product with language+currency key
await cache.set(`products:detail:${id}:${lang}:${currency}`, data, ["products", "catalog"])

// Invalidation clears ALL language variants
await cache.invalidateTags(["products", "catalog"])
```

## Tag-Based Revalidation

- **Tags per entity** — `products`, `users`, `categories`, etc.
- **Unique tags** — prevent cache pollution across domains
- **TTL configurable** — set per use case (short for dynamic, long for static)

## Mutation Pattern

**Every POST/PUT/PATCH/DELETE must call:**

```
revalidateDomain(domain)
```

Examples:
- Create product → `revalidateDomain('products')`
- Update user → `revalidateDomain('users')`
- Delete course → `revalidateDomain('courses')`

## Integration Layers

- **Repository** — reads from cache first
- **Service** — wraps repository, handles business logic
- **Action** — calls service, triggers revalidation on mutation

## Rules

- [ ] **Cache reads** only in Repository layer
- [ ] **Revalidation** happens after every mutation (POST/PUT/PATCH/DELETE)
- [ ] **Tags are domain-scoped** — no cross-domain cache sharing
- [ ] **TTL is configurable** — set per cache instance
- [ ] **Never bypass** cache for "fresh" data — use revalidation instead
