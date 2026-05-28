# Role Definitions

## Using createAccessControl

```typescript
import { createAccessControl } from "better-auth/plugins/access"

const statement = {
  products: ["create", "read", "read_private", /* ... */] as const,
  admin: ["manage_system"] as const,
}
const ac = createAccessControl(statement)
```

## Role creation

```typescript
const roles = {
  admin: ac.newRole({
    products: ["*"],
    admin: ["*"],
  }),
  "products:editor": ac.newRole({
    products: ["create", "read", "read_private", "update",
               "publish", "archive", "set_visibility",
               "softdelete", "manage_categories", "manage_variants",
               "manage_prices", "manage_medias", "manage_ratings"],
  }),
  "products:operator": ac.newRole({
    products: ["create", "read", "read_private", "update",
               "manage_inventory", "manage_storehouses"],
  }),
  "products:manager": ac.newRole({
    products: ["create", "read", "read_private", "update",
               "delete", "publish", "archive"],
  }),
  "users:editor": ac.newRole({
    users: ["create", "read", "read_private", "update", "delete"],
  }),
  user: ac.newRole({}),  // no permissions
}
```

## Checking at runtime

```typescript
const userRole = session.user.role as keyof typeof roles
if (userRole === "admin") return  // bypass

const roleObj = roles[userRole]
if (!roleObj) throw error(403, "Unknown role")

const result = roleObj.authorize({ products: ["create"] })
if (result.error) throw error(403, result.error)
```

## Role hint on login

The `metadata` field in Better Auth stores role as a string:

```typescript
// backend/app/lib/auth/config.ts
const auth = betterAuth({
  databaseHooks: {
    user: {
      create: {
        before: async (user) => ({ ...user, role: "user" }),
      },
    },
  },
})
```
