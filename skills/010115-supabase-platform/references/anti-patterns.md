# Anti-Patterns Lesson

Common mistakes to avoid in Supabase.

## 1. RLS Without Null Safety

❌ **DON'T:** Direct auth.uid() comparison
```sql
where user_id = auth.uid()  -- Fails silently if NULL
```

✅ **DO:** Explicit null check
```sql
where (auth.uid() IS NOT NULL AND user_id = (SELECT auth.uid()))
```

## 2. Joins in RLS Policies

❌ **DON'T:** Complex joins in policies
```sql
where exists (select 1 from orgs where orgs.id = posts.org_id and orgs.user_id = auth.uid())
```

✅ **DO:** Denormalize or use security definer
```sql
where org_id = any(select org_ids from auth_metadata)
```

## 3. Missing Search Path in Security Definer

❌ **DON'T:** SECURITY DEFINER without search_path
```sql
create function fn() security definer as $$ ... $$
```

✅ **DO:** Always set search_path
```sql
create function fn() security definer set search_path = '' as $$ ... $$
```

## 4. Generic Realtime Event Names

❌ **DON'T:** Use generic names
```typescript
.on('broadcast', { event: 'update' }, ...)
```

✅ **DO:** Specific snake_case
```typescript
.on('broadcast', { event: 'message_created' }, ...)
```

## 5. Logic in Triggers

❌ **DON'T:** Complex business logic in triggers
```sql
create trigger update_stats after insert on posts
for each row execute function complex_business_logic()
```

✅ **DO:** Use Edge Functions or webhooks
```sql
-- Trigger calls edge function via webhook
```

## Rules Checklist

- [ ] **Null safety** in RLS policies
- [ ] **No joins** in RLS — denormalize instead
- [ ] **Search path = ''** in security definer functions
- [ ] **Specific event names** for realtime
- [ ] **Simple triggers** — logic in functions/webhooks
- [ ] **No GRANT/REVOKE** on columns — use RLS
