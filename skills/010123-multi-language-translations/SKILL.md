---
name: 010123-multi-language-translations
description: Multi-language translations — per-entity translation tables, assembler pattern (fetch all, filter in-memory), cache invalidation, and slug per locale.
license: MIT
compatibility: PostgreSQL 16+ with Drizzle ORM or raw SQL
---

# Multi-Language Translations

## When to use

When building applications that need to display content in multiple languages without hardcoding translations or using third-party services.

## References

| Topic | File |
|---|---|
| Per-entity translation tables | `references/translation-tables.md` |
| Assembler pattern (fetch all, filter in-memory) | `references/assembler-pattern.md` |
| Cache invalidation across languages | `references/cache-invalidation.md` |
| Slug resolution per locale | `references/slug-resolution.md` |
| Direction from language table | `references/language-direction.md` |

## Quick checklist

- [ ] `sys_languages`: code PK, name, direction (ltr/rtl), isActive, isDefault
- [ ] Per-entity `{entity}_translations` tables with `UNIQUE(entity_id, language_code)`
- [ ] `UNIQUE(slug, language_code)` for per-language URL trees
- [ ] Assembler: SQL JOIN all translations → in-memory `.find(lang)` → fallback to first
- [ ] Cache: single key per entity (all languages bundled), tag-based invalidation
- [ ] Slug resolution: `getTranslationSlug(entity, slug, fromLang, toLang)`
- [ ] Direction: `sys_languages.direction` → `<html dir>` → DirectionProvider
- [ ] FK protection: `ON DELETE RESTRICT` on language_code FK
