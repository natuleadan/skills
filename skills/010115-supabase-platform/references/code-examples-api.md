# Code Examples — API & Edge Functions

## Edge Function — Basic Handler

```typescript
// supabase/functions/hello/index.ts
Deno.serve(async (req) => {
  const { name } = await req.json()

  return new Response(
    JSON.stringify({ message: `Hello, ${name}!` }),
    { headers: { 'Content-Type': 'application/json' } }
  )
})
```

## Edge Function — With Hono Router

```typescript
// supabase/functions/api/index.ts
import { Hono } from "npm:hono"

const app = new Hono()

app.get("/users/:id", async (c) => {
  const id = c.req.param("id")
  return c.json({ id })
})

app.post("/users", async (c) => {
  const body = await c.req.json()
  return c.json({ created: true, ...body })
})

Deno.serve(app.fetch)
```

## Edge Function — Supabase Client

```typescript
import { createClient } from "npm:@supabase/supabase-js@2"

Deno.serve(async (req) => {
  const supabase = createClient(
    Deno.env.get("SUPABASE_URL")!,
    Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!
  )

  const { data, error } = await supabase
    .from("posts")
    .select("*")
    .eq("published", true)

  return new Response(JSON.stringify(data), {
    headers: { "Content-Type": "application/json" }
  })
})
```

## Realtime — Broadcast Client

```typescript
// Subscribe to high-frequency events (no DB persistence needed)
const channel = supabase.channel('room:123', {
  config: { private: true }
})

channel
  .on('broadcast', { event: 'cursor_moved' }, (payload) => {
    console.log("Cursor:", payload.payload)
  })
  .subscribe()

// Send event
channel.send({
  type: 'broadcast',
  event: 'cursor_moved',
  payload: { x: 100, y: 200 }
})
```

## Realtime — Postgres Changes

```typescript
// Listen to actual database changes (with persistence)
supabase
  .channel('public:posts')
  .on(
    'postgres_changes',
    { event: '*', schema: 'public', table: 'posts' },
    (payload) => {
      console.log("Change received:", payload.eventType, payload.new)
    }
  )
  .subscribe()
```

## Storage — Generate Signed URL

```typescript
const { data, error } = await supabase.storage
  .from('avatars')
  .createSignedUrl(`${userId}/avatar.png`, 3600) // 1 hour

if (error) {
  console.error('Error:', error)
} else {
  console.log('Signed URL:', data.signedUrl)
}
```
