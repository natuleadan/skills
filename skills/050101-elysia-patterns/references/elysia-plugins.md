# Elysia Plugin Patterns Reference

## Clean Architecture Placement

Elysia lives in the infrastructure layer:

```
infrastructure/elysia/
├── controllers/     ← Route handlers
├── plugins/         ← Middleware plugins
├── common/          ← Shared helpers (response, error)
├── models/          ← TypeBox schemas
└── support/         ← Auto-router, codegen
```

## Plugin Pipeline

Each plugin has a single responsibility and runs in declared order:

```typescript
const app = new Elysia({ prefix: "/api" })
  .use(corsPlugin)
  .use(errorHandler)
  .use(authPlugin)
  .use(openapiPlugin)
  .use(controllers)
  .use(xssSanitizer)
```

## Adding a New Controller

1. Create `controllers/{name}.ctrl.ts`
2. Run auto-router generator
3. Verify routes at `/openapi`

### Controller Template

```typescript
import { Elysia } from "elysia"
import { t } from "elysia"

export const itemsController = new Elysia({ prefix: "/items", name: "items" })
  .get("/", async () => {
    return await listItems()
  }, {
    detail: { summary: "List all items", tags: ["Items"] },
  })
  .post("/", async ({ body }) => {
    return await createItem(body)
  }, {
    body: t.Object({ name: t.String(), price: t.Number() }),
    detail: { summary: "Create item", tags: ["Items"] },
  })
```

## Error Handling Pattern

```typescript
app.onError(({ code, error }) => {
  if (code === "VALIDATION") {
    return { code: 0, msg: "Validation error", data: error }
  }
  console.error(error)
  return { code: 0, msg: "Internal error", data: null }
})
```

## Auth Identity Flow

```
Request comes in
  → Check session cookie
    → If valid: resolve user
  → Check Authorization: Bearer header
    → If valid: resolve user
  → Check x-api-key header
    → If valid: resolve mock session
  → No auth: user = null
```

## CORS

```typescript
cors({
  origin: allowedOrigins,
  methods: ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
  allowedHeaders: ["Content-Type", "Authorization"],
  credentials: true,
  maxAge: 86400, // 24h preflight cache
})
```

## Cookie Configuration

```typescript
{
  cookie: process.env.COOKIE_SECRET
    ? { secrets: [process.env.COOKIE_SECRET] }
    : undefined,
}
```
