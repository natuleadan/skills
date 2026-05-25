# Code Examples — SQL

## RLS Policy — Secure Select

```sql
-- Enable RLS
alter table public.posts enable row level security;

-- Policy: Users see published OR their own posts
create policy "View posts"
on public.posts
for select
to authenticated
using (
  published = true
  OR user_id = (SELECT auth.uid())
);

-- IMPORTANT: Index user_id for performance
create index idx_posts_user_id on public.posts(user_id);
```

## RLS Policy — Insert with Authorization

```sql
create policy "Users create own posts"
on public.posts
for insert
to authenticated
with check (
  user_id = (SELECT auth.uid())
);
```

## RLS Policy — Update Own Data

```sql
create policy "Users update own posts"
on public.posts
for update
to authenticated
using (user_id = (SELECT auth.uid()))
with check (user_id = (SELECT auth.uid()));
```

## Storage RLS Policy

```sql
-- Users upload to their own folder
create policy "Upload to own folder"
on storage.objects
for insert
to authenticated
with check (
  bucket_id = 'avatars' and
  (storage.foldername(name))[1] = (select auth.uid()::text)
);

-- Users view their own files
create policy "View own files"
on storage.objects
for select
to authenticated
using (
  bucket_id = 'avatars' and
  (storage.foldername(name))[1] = (select auth.uid()::text)
);
```

## Realtime — Database Trigger for Broadcast

```sql
-- Trigger to broadcast room changes without client `postgres_changes`
create or replace function broadcast_room_update()
returns trigger as $$
begin
  perform realtime.broadcast(
    'room:' || new.id,
    'room_updated',
    jsonb_build_object('room_id', new.id, 'name', new.name)
  );
  return new;
end;
$$ language plpgsql;

create trigger room_broadcast_trigger
after update on rooms
for each row
execute function broadcast_room_update();
```

## Schema — ENUMs Definition

```sql
-- Define custom types
create type visibility_type as enum ('public', 'private', 'confidential');
create type user_role as enum ('user', 'editor', 'admin');
create type post_status as enum ('draft', 'published', 'archived');

-- Now tables can use these enums for type safety
```

## Schema — Complete Table with Enums, Constraints, Soft Delete

```sql
-- Idempotent creation
do $$
begin
  if not exists (select 1 from pg_tables where tablename = 'posts') then
    create table public.posts (
      id uuid primary key default gen_random_uuid(),
      user_id uuid not null references public.users(id) on delete cascade,
      title text not null,
      content text,
      status post_status default 'draft',
      visibility visibility_type default 'public',
      soft_delete boolean default false,
      metadata jsonb default '{"views": 0, "likes": 0}'::jsonb,
      created_at timestamptz default now(),
      updated_at timestamptz default now(),

      -- Constraints
      constraint uq_posts_title_user unique (title, user_id),
      constraint ck_soft_delete check (soft_delete in (true, false)),
      constraint ck_status check (status in ('draft', 'published', 'archived')),
      constraint ck_visibility check (visibility in ('public', 'private', 'confidential'))
    );
  end if;
end $$;

-- Enable RLS
alter table public.posts enable row level security;

-- Add indexes
create index idx_posts_user_id on public.posts(user_id);
create index idx_posts_visibility on public.posts(visibility);
create index idx_posts_soft_delete on public.posts(soft_delete) where soft_delete = false;
create index idx_posts_created on public.posts(created_at desc);
create index idx_posts_metadata on public.posts using gin(metadata);

-- Document
comment on table public.posts is 'User blog posts with soft delete and visibility control';
comment on column public.posts.soft_delete is 'Logical deletion flag (true = deleted, false = active)';
comment on column public.posts.visibility is 'Access control: public, private (owner only), confidential (admin only)';
comment on column public.posts.metadata is 'Additional post data (views, likes, etc)';
```

## RLS Policy with Visibility & Soft Delete

```sql
-- Policy: Users see public posts OR their own (not deleted)
create policy "View posts"
on public.posts
for select
to authenticated
using (
  (soft_delete = false)
  and (
    visibility = 'public'
    OR (visibility = 'private' and user_id = (SELECT auth.uid()))
    OR (SELECT auth.uid())::text = 'admin-user-id'  -- Admins see all
  )
);

-- Policy: Users create own posts
create policy "Create posts"
on public.posts
for insert
to authenticated
with check (user_id = (SELECT auth.uid()));

-- Policy: Users soft-delete own posts
create policy "Soft delete own posts"
on public.posts
for update
to authenticated
using (user_id = (SELECT auth.uid()))
with check (user_id = (SELECT auth.uid()) and soft_delete in (true, false));
```

## Security Definer Function (Careful!)

```sql
-- ✅ CORRECT: With search_path set to empty
create or replace function get_user_stats(user_id uuid)
returns json as $$
declare
  post_count int;
  follower_count int;
begin
  select count(*) into post_count from public.posts where posts.user_id = get_user_stats.user_id;
  select count(*) into follower_count from public.followers where followers.user_id = get_user_stats.user_id;

  return json_build_object('posts', post_count, 'followers', follower_count);
end;
$$ language plpgsql security definer set search_path = '';
```
