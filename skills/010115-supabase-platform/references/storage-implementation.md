# Storage Implementation Lesson

Supabase Storage manages file uploads with RLS and signed URLs.

## Buckets & Access Control

- **Private by default** — files require signed URL access
- **Public buckets** — readable by anyone (use sparingly)
- **RLS on storage.objects** — control who can upload/read

```sql
-- Policy: Users upload only to their own folder
create policy "Upload to own folder"
on storage.objects
for insert
to authenticated
with check (
  bucket_id = 'avatars' and
  (storage.foldername(name))[1] = (select auth.uid()::text)
);
```

## Signed URLs

Generate temporary access URLs for private files:

```typescript
const { data } = await supabase.storage
  .from('avatars')
  .createSignedUrl('user-123/avatar.png', 3600) // 1 hour

// Returns: { signedUrl: "https://..." }
```

## Resumable Uploads (TUS)

For files > 6MB, use resumable upload:

```typescript
// Use TUS-compatible client library
// Supabase supports resumable uploads out of the box
```

## Anti-Patterns

- ❌ **Upsert** — CDN propagation delays; use unique filenames
- ❌ **Direct paths** — always use signed URLs for private files
- ❌ **No RLS** — define policies on storage.objects

## Rules

- [ ] **RLS on storage.objects** — control access
- [ ] **Signed URLs** for private files (use short TTL)
- [ ] **Unique filenames** — avoid upsert issues
- [ ] **TUS for large files** — > 6MB
- [ ] **Public buckets** only when necessary
