# Per-Entity Translation Tables

## Pattern

Each entity that requires multi-language content gets its own `_translations` table:

```sql
CREATE TABLE product_translations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  product_id UUID NOT NULL REFERENCES products(id) ON DELETE CASCADE,
  language_code TEXT NOT NULL REFERENCES languages(code) ON DELETE RESTRICT,
  name TEXT NOT NULL,
  description TEXT,
  slug TEXT NOT NULL,
  -- entity-specific fields
  shipping_info TEXT,
  warranty_info TEXT,
  UNIQUE (product_id, language_code),
  UNIQUE (slug, language_code)
);
```

Same pattern for categories, variants, ratings, storehouses — each with their own field set.

## Key design decisions

| Decision | Rationale |
|---|---|
| One table per entity | Different entities have different translatable fields. A unified table would be sparse and hard to maintain. |
| Composite `UNIQUE(entity_id, language_code)` | Prevents duplicate translations per language. |
| `slug` is per-translation | Each language has its own URL tree. `UNIQUE(slug, language_code)` avoids cross-language collisions. |
| `ON DELETE RESTRICT` on `language_code` | Prevents deleting a language that has active translations. |
| No JSONB for translations | Typed columns give better type safety, queryability, and validation. JSONB is reserved for truly dynamic data. |

## Language table

```sql
CREATE TABLE languages (
  code TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  direction TEXT NOT NULL DEFAULT 'ltr' CHECK (direction IN ('ltr', 'rtl')),
  is_active BOOLEAN DEFAULT false,
  is_default BOOLEAN DEFAULT false
);
```

The `languages` table is the single source of truth for available languages and their text direction.
