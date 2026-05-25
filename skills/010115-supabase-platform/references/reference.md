# Supabase & PostgreSQL Reference

## Critical Security Rules

1. **RLS is mandatory** — enable on all public tables immediately
2. **Secure SQL execution** — use `SECURITY INVOKER` and `SET search_path = ''`
3. **Dual authentication** — JWT for users, API Keys for services
4. **Realtime scalability** — prefer broadcast over postgres_changes

## Core Concepts

| Concept | Purpose | Key Point |
|---------|---------|-----------|
| **RLS Policies** | Row-level access control | Separate policies per operation (SELECT/INSERT/UPDATE/DELETE) |
| **Signed URLs** | Temporary file access | Required for private storage |
| **Broadcast** | High-frequency events | Transient, better scalability |
| **Postgres_changes** | DB change stream | Persistent, limited scalability |
| **Edge Functions** | Serverless compute | Deno runtime, npm packages |
| **Custom Claims** | RBAC in JWT | Avoid DB queries in RLS |

## Table Creation Pattern

```sql
create table public.{name} (
  id uuid primary key default gen_random_uuid(),
  column_name type constraints,
  created_at timestamptz default now()
);

alter table public.{name} enable row level security;
comment on table public.{name} is 'Description';
```

## RLS Policy Pattern

```sql
create policy "Policy Name"
on table_name
for operation  -- select, insert, update, delete
to role
using (condition);
```

## Realtime Channel Pattern

```typescript
supabase.channel('scope:entity:id', {
  config: { private: true }
})
.on('broadcast', { event: 'event_name' }, callback)
.subscribe()
```

## Storage Pattern

- Create bucket → add RLS policy → use signed URLs
- Private by default
- TUS for resumable uploads (>6MB)

## Edge Function Pattern

```typescript
Deno.serve(async (req) => {
  // Handle request
  return new Response(json, { headers })
})
```

## Key Rules Summary

- ✅ RLS enabled + separate policies per operation
- ✅ Broadcast for high-frequency, postgres_changes for persistence
- ✅ Signed URLs for private files
- ✅ Deno + npm packages in Edge Functions
- ✅ Indexes on FK columns
- ✅ Null safety in auth checks
