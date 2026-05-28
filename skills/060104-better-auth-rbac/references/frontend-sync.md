# Frontend Permissions Sync

## Backend defines, frontend mirrors

```typescript
// frontend/src/lib/permissions.ts
export function hasProductPerm(role: string, action: string): boolean {
  const rolePerms = {
    admin: ["create", "read", "read_private", /* ...all 18 actions */],
    "products:editor": ["create", "read", "read_private", "update", "publish", /* ... */],
    "products:operator": ["create", "read", "read_private", "update"],
  }
  return rolePerms[role]?.includes(action) ?? false
}
```

## UI gating

```typescript
const role = session?.user?.role as string
const canPublish = hasProductPerm(role, "publish")
const canDelete = hasProductPerm(role, "delete")
```

## High-level permissions

```typescript
const ALLOWED = {
  manageProducts: ["admin", "products:operator", "products:editor", "products:manager"],
  viewAdmin: ["admin", "users:editor"],
} as const
```

## Backend is the gate

The frontend only controls UI visibility (show/hide buttons). The API always validates permissions server-side and returns 401/403 if missing.
