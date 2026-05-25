---
name: 060102-zero-trust
description: Zero Trust authentication pattern — validate identity once at entry, propagate via userRole, never trust client-provided role data.
---

# Zero Trust Authentication

## Core Principle

> Identity is validated once at the entry point, then propagated downward through layers via userRole parameter. Never accept role from client.

## Architecture Flow

```
Entry Point (Server Action / Controller)
    ↓
Validate auth (session, API key, etc.)
    ↓
Extract userRole (admin | editor | user | public)
    ↓
Call Service with userRole
    ↓
Service propagates to Repository
    ↓
Repository applies security filters
```

## Role Types

| Role | Access Level |
|------|-------------|
| **admin** | Full access, no filters, can hard delete |
| **editor\_\*** | Own content access, can soft delete |
| **user** | Read-only access to own/public content |
| **public** | Unauthenticated — public content only |

## Security Rules

- [ ] Server Actions / Controllers must NEVER accept userRole from client
- [ ] Repository must receive userRole to apply security filters
- [ ] Service must propagate userRole from entry point to repository
- [ ] Role must be extracted from session, not from request body
- [ ] Default to lowest privilege when role is unknown

## Implementation Checklist

### Entry Points (Actions / Controllers)

- [ ] Validate session using auth provider
- [ ] Extract role from session or default to 'public'
- [ ] Pass userRole as parameter to service
- [ ] NEVER trust client-provided role

### Services

- [ ] Accept userRole as function parameter
- [ ] Propagate userRole to repository calls
- [ ] Implement role-based business logic

### Repositories

- [ ] Accept userRole in query methods
- [ ] Apply visibility filters based on role
- [ ] Apply soft-delete filters for non-admin roles

## Example

```typescript
// Action (entry point)
"use server"
export async function getItemsAction() {
  const session = await getSession()
  const userRole = session?.user?.role ?? "public"
  return getItemsService(userRole)
}

// Service
async function getItemsService(userRole: string) {
  const repo = createItemRepo()
  return repo.findAll(userRole)
}

// Repository
async function findAll(userRole: string) {
  if (userRole === "admin") return db.query("SELECT * FROM items")
  if (userRole === "editor") return db.query("SELECT * FROM items WHERE owner_id = $1 OR deleted_at IS NULL", [userId])
  return db.query("SELECT * FROM items WHERE deleted_at IS NULL")
}
```

## Quick Reference

```typescript
// Correct: extract role from session
const role = session?.user?.role ?? "public"

// WRONG: never do this
const role = request.body.role  // UNSAFE!
```
