# Permission Statements

## Define statements

```typescript
const customStatements = {
  products: [
    "create", "read", "read_private", "read_confidential",
    "update", "delete", "publish", "archive",
    "set_visibility", "softdelete",
    "manage_categories", "manage_variants", "manage_prices",
    "manage_inventory", "manage_medias", "manage_ratings",
    "manage_coupons", "manage_storehouses",
  ] as const,
  admin: ["manage_system"] as const,
  orders: ["create", "read", "update", "delete", "refund", "ship", "cancel"] as const,
} as const

const statement = { ...defaultStatements, ...customStatements }
const ac = createAccessControl(statement)
```

## Role definitions

```typescript
const admin = ac.newRole({
  products: [...productsFull],
  admin: ["manage_system"],
})

const user = ac.newRole({})  // empty = no permissions
```

## Checking permissions

```typescript
const roleObj = roles[user.role]
if (!roleObj) return 403

const result = roleObj.authorize({ products: ["create"] })
if (!result.success) return 403
```

## Admin bypass

```typescript
if (user.role === "admin") return { ok: true }  // admin always passes
```
