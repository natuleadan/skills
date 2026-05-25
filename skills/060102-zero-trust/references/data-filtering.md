# Data Filtering Patterns

Security patterns for filtering database queries at the repository layer based on role and data sensitivity.

## Column Conventions

### visibility

Classifies data sensitivity by role access:

| Value | Admin | Editor | User (auth) | Public |
|-------|-------|--------|-------------|--------|
| `public` | ✓ | ✓ | ✓ | ✓ |
| `private` | ✓ | ✓ | ✓ | ✗ |
| `confidential` | ✓ | ✗ | ✗ | ✗ |

```sql
ALTER TABLE items ADD COLUMN visibility TEXT NOT NULL DEFAULT 'private'
  CHECK (visibility IN ('public', 'private', 'confidential'));
```

### soft_delete

Logical deletion — rows remain in database but are hidden from non-admin users.

| Role | Sees deleted? |
|------|-------------|
| admin | ✓ (unless explicitly filtered) |
| editor | ✗ (own content only, non-deleted) |
| user | ✗ (non-deleted only) |

```sql
ALTER TABLE items ADD COLUMN is_deleted BOOLEAN NOT NULL DEFAULT false;
```

### user_id

Tracks record ownership for editor-level filtering.

```sql
ALTER TABLE items ADD COLUMN user_id UUID NOT NULL REFERENCES users(id);
```

## Repository-Level Filtering

### Always Re-Filter

Database-level security (e.g., RLS) is a defense-in-depth layer — it must never be the only enforcement. The repository must independently apply all applicable filters:

```typescript
async function getAllItems(userRole: string, userId?: string) {
  const conditions: string[] = [];

  if (userRole !== "admin") {
    conditions.push("is_deleted = false");
  }

  if (userRole === "user") {
    conditions.push("visibility = 'public'");
  }

  if (userRole === "editor" && userId) {
    conditions.push(`(visibility != 'confidential' AND user_id = '${userId}')`);
  }

  return db.query(`SELECT * FROM items WHERE ${conditions.join(" AND ")}`);
}
```

### Never Expose Storage Paths

Never return raw storage paths or bucket identifiers to the client. Use temporary access URLs or proxy endpoints:

```typescript
// ❌ WRONG: exposes internal paths
return { path: file.storage_path }

// ✅ RIGHT: generates temporary access URL
return { url: generateSignedUrl(file.storage_path, ttl) }
```

## Summary Checklist

- [ ] Repository independently applies visibility filters by role
- [ ] Repository excludes soft-deleted rows for non-admin roles
- [ ] Repository filters by user_id for editor-level roles
- [ ] Never expose raw storage paths to clients
- [ ] Role is never trusted from client input — always from session
- [ ] All queries go through repository layer (no direct table access from services)
- [ ] Assemblers sanitize fields by role before sending to client
