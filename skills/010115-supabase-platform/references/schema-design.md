# Schema Design Lesson

PostgreSQL schema conventions for Supabase.

## Naming Conventions

- **snake_case** — all table and column names
- **Plural table names** — `users`, `posts`, `comments`
- **Comments** — document tables and complex columns

## Primary Keys

- **UUID v4 by default** — use `uuid` type with `gen_random_uuid()`
- **No bigint** — deprecated in new tables
- **Generated identity** — `generated always as identity` for auto-increment

```sql
create table public.users (
  id uuid primary key default gen_random_uuid(),
  email text not null unique,
  created_at timestamptz default now()
);

comment on table public.users is 'User accounts';
```

## ENUMS (Custom Types)

Define domain-specific enums for type safety:

```sql
create type user_role as enum ('user', 'editor', 'admin');
create type visibility_type as enum ('public', 'private', 'confidential');
create type movement_type as enum ('in', 'out', 'transfer', 'adjustment');
```

Usage in tables:

```sql
create table public.posts (
  id uuid primary key,
  user_role user_role not null,
  visibility visibility_type default 'public',
  ...
);
```

## Constraints

### Primary & Unique

```sql
constraint pk_users primary key (id)
constraint uq_email unique (email)
constraint uq_code_name unique (code, name)  -- Composite unique
```

### Foreign Keys with ON DELETE/UPDATE

```sql
constraint fk_posts_user foreign key (user_id)
  references public.users(id) on delete cascade  -- Delete posts when user deleted
constraint fk_posts_org foreign key (org_id)
  references public.orgs(id) on delete restrict  -- Prevent org deletion if posts exist
constraint fk_comment_post foreign key (post_id)
  references public.posts(id) on delete cascade on update cascade
```

### CHECK Constraints

```sql
constraint ck_price check (price > 0)
constraint ck_direction check (direction in ('ltr', 'rtl'))
constraint ck_soft_delete check (soft_delete in (true, false))
```

## Common Table Patterns

### Soft Delete Pattern

Add `soft_delete` boolean column instead of actual deletion:

```sql
create table public.posts (
  id uuid primary key,
  ...,
  soft_delete boolean default false
);

-- In RLS or queries, filter: where soft_delete = false
```

### Visibility Pattern

Control access with enum:

```sql
create table public.posts (
  ...,
  visibility visibility_type default 'public'  -- public, private, confidential
);

-- RLS: SELECT where visibility = 'public' OR user_id = auth.uid()
```

### Audit Columns

Standard timestamps:

```sql
created_at timestamptz default now(),
updated_at timestamptz default now()
```

### JSON Metadata

Flexible data with defaults:

```sql
meta_data jsonb default '{"views": 0, "likes": 0}'::jsonb,
signed_url text,
signed_url_expires_at timestamptz
```

## Indexes & Performance

- **Index FK columns** — used in WHERE or JOIN
- **JSONB indexes** — `gin` index if querying JSON keys
- **Partial indexes** — for frequent WHERE conditions

```sql
create index idx_users_email on public.users(email);
create index idx_posts_user_id on public.posts(user_id);
create index idx_metadata on public.posts using gin(meta_data);
create index idx_active_posts on public.posts(created_at) where soft_delete = false;
```

## Sequences

For custom auto-increment (rarely needed with UUID):

```sql
create sequence product_order_seq start with 1;
```

## Idempotent Schema Creation

Always use IF NOT EXISTS and DO blocks:

```sql
do $$
begin
  if not exists (select 1 from pg_tables where tablename = 'posts') then
    create table public.posts (
      id uuid primary key default gen_random_uuid(),
      ...
    );
  end if;
end $$;
```

## JSONB vs JSON

- **JSONB** — indexed, faster, preferred
- **JSON** — slower, avoid unless needed

## Migrations

Naming: `YYYYMMDDHHmmss_description.sql` (UTC)

- Idempotent — can run multiple times safely
- Transactional — wrapped in BEGIN/COMMIT

## Rules

- [ ] **UUID** for all primary keys (new tables)
- [ ] **snake_case** naming
- [ ] **Plural table names**
- [ ] **ENUMS** for domain types (role, status, visibility)
- [ ] **CHECK constraints** for valid values
- [ ] **Composite UNIQUE** for multi-column uniqueness
- [ ] **ON DELETE/UPDATE** strategy defined (CASCADE, RESTRICT, SET NULL)
- [ ] **Index FK columns** used in WHERE/JOIN
- [ ] **JSONB** for unstructured data with defaults
- [ ] **Soft delete** pattern (soft_delete boolean)
- [ ] **Visibility** enum for access control
- [ ] **Comments** on tables and columns
- [ ] **IF NOT EXISTS** + DO blocks for idempotent creation
