# Implementation Examples

Full Action→Service→Repository flow with TypeScript:

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

## Dual Auth Methods

Both JWT session and API key authentication follow the same propagate-never-trust pattern.
