# Test Setup and Auth Helpers

## Setup file pattern

```typescript
// tests/setup.ts — Global preload
import { beforeAll } from "bun:test"
import { Pool } from "pg"

beforeAll(async () => {
  process.env.DATABASE_URL = process.env.TEST_DATABASE_URL!
  const pool = new Pool({ connectionString: process.env.DATABASE_URL })
  await pool.execute("DELETE FROM prd_products WHERE name LIKE 'test-%'")
  await pool.end()
})
```

## Auth helper pattern

```typescript
// tests/helpers/auth.ts
export async function getAuthHeaders(role: string = "user") {
  const res = await fetch(`${HOST}/v1/test/auth/login`, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({ role }),
  })
  const data = await res.json()
  const cookie = extractCookie(res)
  return { cookie, userId: data.data?.user?.id }
}

function extractCookie(res: Response) {
  const setCookie = res.headers.getSetCookie()
  return setCookie.map(c => c.split(";")[0]).join("; ")
}
```

## describeIf guard

```typescript
// tests/helpers/skip-in-prod.ts
export const IS_PROD = process.env.NODE_ENV === "production"
export function describeIf(condition: boolean, ...args: Parameters<typeof describe>) {
  if (condition) return describe(...args)
  return describe.skip(...args)
}
```

## req() helper

```typescript
async function req(method: string, path: string, body?: unknown, useCookie = true) {
  const headers: Record<string, string> = { "content-type": "application/json" }
  if (useCookie) headers["cookie"] = cookie
  const opts: RequestInit = { method, headers }
  if (body) opts.body = JSON.stringify(body)
  const res = await fetch(`${HOST}${path}`, opts)
  const data = safeJson(res)
  return { status: res.status, data }
}
```
