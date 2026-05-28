---
name: 060104-better-auth-rbac
description: Role-based access control with Better Auth — permission statements, createAccessControl, authorize() checks, dual auth, and frontend permission sync.
license: MIT
compatibility: Requires better-auth 1.6.x
---

# Better Auth RBAC

## When to use

When implementing granular role-based permissions beyond Better Auth's built-in admin plugin roles.

## References

| Topic | File |
|---|---|
| Permission statements | `references/permission-statements.md` |
| Role definitions | `references/role-definitions.md` |
| Dual auth (API key + session) | `references/dual-auth.md` |
| Frontend permissions sync | `references/frontend-sync.md` |

## Quick checklist

- [ ] Define all permission actions in `customStatements` with `as const`
- [ ] Create roles with `ac.newRole({})` mapping statements to actions
- [ ] Check permissions with `roleObj.authorize(permissions)`
- [ ] Admin role always passes (short-circuit before authorize)
- [ ] Use `requireApiKeyOrSession()` for dual auth (Bearer or cookie)
- [ ] Frontend: keep `permissions.ts` in sync with backend role definitions
