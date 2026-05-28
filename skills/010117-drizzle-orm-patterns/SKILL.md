---
name: 010117-drizzle-orm-patterns
description: Drizzle ORM schema patterns — domain factories, prd_/sys_/tst_ prefixes, FK constraints, vector+HNSW, JSONB+GIN, raw SQL, and the as any bridge.
license: MIT
compatibility: Requires Drizzle ORM 0.38+ with PostgreSQL
---

# Drizzle ORM Patterns

## When to use

When building PostgreSQL schemas with Drizzle ORM. Covers table conventions, constraints, vector search, and domain factories.

## References

| Topic | File |
|---|---|
| Table naming, prefixes, timestamps | `references/table-conventions.md` |
| FK constraints and cascade rules | `references/foreign-keys.md` |
| Vector columns and HNSW indexes | `references/vector-columns.md` |
| JSONB columns and GIN indexes | `references/jsonb-gin.md` |
| Raw SQL with `sql\`\`` | `references/raw-sql.md` |
| Domain factory pattern | `references/domain-factories.md` |

## Quick checklist

- [ ] Prefix tables: `prd_` (prod), `sys_` (system), `tst_` (test)
- [ ] Use `id()` from `_cuid.ts` for UUID PKs
- [ ] Use `.references(()=>Table.id, {onDelete: "cascade"|"set null"})` for FKs
- [ ] Declare all `xxxId` columns as `.references()` — never leave implicit
- [ ] Wrap domain logic in factory functions: `createXxxRepo(table)`
- [ ] Use `as any` to bridge Drizzle's complex types in factories
- [ ] For vector search: `vector({ dimensions: 384 })` + HNSW index
- [ ] For JSONB search: `jsonb()` + GIN `@>` index
- [ ] For timestamps: use the `timestamps` spread (`createdAt`, `updatedAt`, `deletedAt`)
