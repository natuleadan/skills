# Zero Trust Authentication

Identity is validated **once at entry** (Server Actions or Middleware), then propagated downward through layers via `userRole` parameter.

## Architecture

- **Entry Point**: Server Actions / Middleware validate auth via the auth provider
- **Propagation**: userRole (admin, editor, user) flows downward → Service → Repository
- **Security Filter**: Repository applies visibility & soft_delete filters based on role

## Role Types

- `admin` — full access, no filters, can hard delete
- `editor` — access own content, can soft delete
- `user` — read-only public content

## Rules

- [ ] **Server Actions** must NEVER accept userRole from client
- [ ] **Repository** must receive userRole to apply security filters (visibility, soft_delete)
- [ ] **Service** must propagate userRole from action to repository
- [ ] **Assemblers** (transformers) must sanitize fields based on role before sending to client
- [ ] **Exceptions**: Functions like `invalidateUserCache(userId)` can accept external IDs if they immediately validate against AuthService

## Dual Auth Methods

- **JWT via cookies** — respects database-level security, created by auth provider
- **x-api-key header** — validated by API key verification, bypasses database-level security, uses admin client

Both require role-based filtering at repository level.
