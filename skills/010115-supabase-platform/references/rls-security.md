# RLS Security Lesson

Row Level Security (RLS) is mandatory for all public tables. Policies control row-level access based on user identity.

## Mandatory RLS Setup

- Enable RLS immediately when creating tables
- Create separate policies for SELECT, INSERT, UPDATE, DELETE
- Never use `FOR ALL` — be specific about operation

```sql
alter table public.posts enable row level security;

create policy "Users can view published posts"
on public.posts
for select
to authenticated
using (published = true OR user_id = (SELECT auth.uid()));
```

## Null Safety

`auth.uid()` returns NULL if unauthenticated. Always check explicitly:

```sql
-- ❌ WRONG - silent failure if not authenticated
where user_id = auth.uid()

-- ✅ RIGHT - explicit null check
where (auth.uid() IS NOT NULL AND user_id = (SELECT auth.uid()))
```

## Policy Best Practices

- **Index FK columns** — columns used in `USING` must be indexed
- **Avoid joins** — joins in RLS are slow; denormalize or use security definer functions carefully
- **Use custom claims** — inject roles into JWT via access token hook instead of DB queries in policies
- **Separate operations** — `FOR SELECT`, `FOR INSERT`, `FOR UPDATE`, `FOR DELETE`

## Custom Access Token Hook (RBAC)

Inject roles into JWT claims to avoid database queries inside RLS:

```sql
-- JWT includes { role: "admin", org_id: "123" }
-- Use in policy: (current_setting('request.jwt.claims')::jsonb ->> 'role') = 'admin'
```

## Rules

- [ ] **RLS enabled** on all public tables
- [ ] **Separate policies** for each operation (SELECT/INSERT/UPDATE/DELETE)
- [ ] **Null safety** in auth checks — explicit `IS NOT NULL`
- [ ] **Indexes on FK columns** used in policies
- [ ] **Custom claims** for role-based access (not DB queries)
