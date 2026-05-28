# Sub-Resource Test Pattern

## Structure

Each sub-resource test follows the same pattern:
1. Create parent resource
2. CRUD sub-resource
3. Verify auth (401, 403, 200)

## Example: product variants

```typescript
let productId = ""
let variantId = ""

test("POST creates variant", async () => {
  const { data } = await req("POST", "/v1/products", {
    name: "test-product-variant", price: 10
  })
  productId = data.data.id
  expect(data.code).toBe(1)
})

test("POST creates variant for product", async () => {
  const { data } = await req("POST", `/v1/products/${productId}/variants`, {
    name: "test-variant-red", sku: "TEST-RED", price: 12
  })
  variantId = data.data.id
  expect(data.code).toBe(1)
})

test("GET returns variants", async () => {
  const { data } = await req("GET", `/v1/products/${productId}/variants`)
  expect(data.code).toBe(1)
  expect(data.data.length).toBeGreaterThan(0)
})

test("GET 401 without auth", async () => {
  const { status } = await req("GET", `/v1/products/${productId}/variants`, undefined, false)
  expect(status).toBe(401)
})

test("DELETE variant", async () => {
  const { data } = await req("DELETE", `/v1/products/${productId}/variants/${variantId}`)
  expect(data.code).toBe(1)
})
```

## Auth test matrix for each sub-resource

```typescript
test("403 with wrong role", async () => {
  // Login as user without permission
  const userCookie = await getAuthHeaders("user")
  const { status } = await fetch(`${HOST}/v1/products/${productId}/media`, {
    method: "POST",
    headers: { cookie: userCookie.cookie, "content-type": "application/json" },
    body: JSON.stringify({ url: "...", type: "image" }),
  })
  expect(status).toBe(403)
})
```
