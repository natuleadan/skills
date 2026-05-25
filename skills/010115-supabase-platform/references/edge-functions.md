# Edge Functions Lesson

Supabase Edge Functions run on Deno (serverless). Use Web APIs and npm packages.

## Runtime & Imports

- **Deno Runtime** — Web-standard APIs (fetch, Response, Headers)
- **npm: specifier** — import npm packages with `npm:` prefix
- **No bare specifiers** — always use `npm:` for packages
- **Avoid deno.land** — prefer npm equivalents

```typescript
import { serve } from "npm:@hono/node-server"
import { Hono } from "npm:hono"
```

## Basic Structure

```typescript
// supabase/functions/my-func/index.ts
Deno.serve(async (req) => {
  return new Response(JSON.stringify({ message: "Hello" }), {
    headers: { "Content-Type": "application/json" }
  })
})
```

## Supabase Client in Edge Functions

Use `SUPABASE_SERVICE_ROLE_KEY` (admin) for privileged operations:

```typescript
import { createClient } from "npm:@supabase/supabase-js@2"

const supabase = createClient(
  Deno.env.get("SUPABASE_URL"),
  Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")
)
```

## Hono Framework (Recommended)

Router and middleware pattern for multiple routes:

```typescript
import { Hono } from "npm:hono"

const app = new Hono()

app.get("/", (c) => c.json({ message: "GET /" }))
app.post("/", (c) => c.json({ message: "POST /" }))

Deno.serve(app.fetch)
```

## Rules

- [ ] **Use Deno** — not Node.js
- [ ] **npm: imports** — never bare specifiers
- [ ] **Service role key** in env, never expose to client
- [ ] **Hono for routing** — clean, performant
- [ ] **Web APIs** — fetch, Response, Headers
