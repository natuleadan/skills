---
name: 010118-repository-factories
description: Domain repository factory — functions accepting Drizzle tables to create reusable CRUD for test (tst_) and production (prd_/sys_) tables.
license: MIT
---

# Repository Factories

## When to use

When building data access layers that need to work with different table schemas (test vs production) without duplicating code.

## References

| Topic | File |
|---|---|
| Factory pattern overview | `references/factory-pattern.md` |
| Service dual-mode (index + test) | `references/service-dual-mode.md` |
| Generic admin system factory | `references/admin-sys-factory.md` |

## Quick checklist

- [ ] Create one factory per domain, accepting tables as parameters
- [ ] Return an object with CRUD methods
- [ ] Use a type alias for the accepted table shape
- [ ] Cast with `as any` at the call site, not inside the factory
- [ ] Create paired services: `index.ts` (sys_*) and `test.ts` (tst_*)
- [ ] For simple CRUD tables, use the generic `createSysRepo()` factory
