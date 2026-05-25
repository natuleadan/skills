# Cache Keys & Revalidation

Cache layer with tag-based revalidation.

## Cache Keys

Hierarchical format: `domain:entity:params`

Examples:
- `products:list:all`
- `products:detail:product-id-123`
- `users:profile:user-id-456`

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
