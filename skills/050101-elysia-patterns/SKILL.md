---
name: 050101-elysia-patterns
description: Elysia API framework patterns — plugin pipeline, controller conventions, auto-routing, auth macro, TypeBox models, and multi-tier API keys.
---

# Elysia API Patterns

## Plugin Pipeline (Execution Order)

```
cors → error handling → auth → OpenAPI → controllers → XSS
```

Common plugin roles:

| Plugin | Purpose |
|--------|---------|
| `cors` | Cross-origin request handling |
| `error` | Structured error handling + logging |
| `auth` | Session/API key resolution |
| `openapi` | OpenAPI spec generation + Swagger UI |
| `controllers` | Route registration (auto or manual) |
| `xss` | Input sanitization |

## Controller Pattern

One file per resource, auto-registered:

```typescript
// controllers/products.ctrl.ts
import { Elysia } from "elysia"

export const productsController = new Elysia({ prefix: "/products", name: "products" })
  .get("/", async () => {
    return await getProducts()
  }, {
    detail: { summary: "List products", tags: ["Products"] },
  })
  .get("/:id", async ({ params: { id } }) => {
    return await getProduct(id)
  }, {
    detail: { summary: "Get product by ID", tags: ["Products"] },
  })
```

### Controller Conventions

- **File name**: `kebab-case.ctrl.ts`
- **Export name**: `{name}Controller` (camelCase)
- **Prefix**: Matches resource name
- **Tags**: OpenAPI grouping via `detail.tags`
- **Response**: Return raw data (wrapper at top level)

## Auto-Router

Scan `controllers/` for `*.ctrl.ts` files and auto-generate route registration:

```bash
# Regenerate after adding/changing controllers
node scripts/generate-routes.ts
```

## Response Format

Standard envelope:

```typescript
return { code: 1, msg: "ok", data: result }
return { code: 0, msg: "Not found", data: null }
```

## Auth Macro

Identity resolution order: cookies → bearer token → API key.

```typescript
.get("/protected", ({ user }) => user, { auth: true })
```

The macro auto-detects the auth method and resolves the session/user in-process.

## TypeBox Models

Define reusable schemas:

```typescript
import { t } from "elysia"

export const ProductSchema = t.Object({
  id: t.Number(),
  name: t.String(),
  price: t.Number(),
})
```

## CORS Configuration

```typescript
cors({
  origin: [process.env.APP_URL || "http://localhost:3000"],
  methods: ["GET", "POST", "PUT", "PATCH", "DELETE"],
  credentials: true,
  maxAge: 86400,
})
```

## Quick Reference

```bash
bun run dev           # Start development server
bun run test          # Run tests
open http://localhost:3000/swagger  # API docs
```
