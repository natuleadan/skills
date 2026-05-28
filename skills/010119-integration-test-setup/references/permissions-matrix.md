# Permissions Matrix Test

## Purpose

Verify each role can only perform its authorized operations. Test the full matrix of role × action.

## Matrix layout

```typescript
const matrix = [
  { role: "admin",       create: true,  read: true,  read_private: true,  update: true,  delete: true,  publish: true },
  { role: "editor",      create: true,  read: true,  read_private: true,  update: true,  delete: false, publish: true },
  { role: "operator",    create: true,  read: true,  read_private: true,  update: true,  delete: false, publish: false },
  { role: "user",        create: false, read: true,  read_private: false, update: false, delete: false, publish: false },
  { role: "none",        create: false, read: false, read_private: false, update: false, delete: false, publish: false },
] as const
```

## Test generator

```typescript
describeIf(!IS_PROD, "products permissions matrix", () => {
  let productId = ""

  beforeAll(async () => {
    const auth = await getAuthHeaders("admin")
    const res = await req("POST", "/v1/products", { name: "test-perm" })
    productId = res.data.data.id
  })

  for (const { role, create, read, update, delete: canDelete } of matrix) {
    test(`${role}: create = ${create}`, async () => {
      const { cookie: roleCookie } = await getAuthHeaders(role)
      const { status } = await fetch(`${HOST}/v1/products`, {
        method: "POST", headers: { cookie: roleCookie, "content-type": "application/json" },
        body: JSON.stringify({ name: "test-perm-{role}" }),
      })
      expect(status).toBe(create ? 200 : 403)
    })

    test(`${role}: read = ${read}`, async () => {
      const { cookie: roleCookie } = await getAuthHeaders(role)
      const { status } = await fetch(`${HOST}/v1/products/${productId}`, {
        headers: { cookie: roleCookie },
      })
      expect(status).toBe(read ? 200 : 403)
    })
  }
})
```
