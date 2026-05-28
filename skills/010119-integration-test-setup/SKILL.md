---
name: 010119-integration-test-setup
description: Backend API test patterns — describeIf guards, getAuthHeaders, test-% cleanup, req() helper, KV isolation, sub-resource tests, and permissions matrix.
license: MIT
---

# Integration Test Setup

## When to use

When writing HTTP integration tests against a live backend server with PostgreSQL, Redis, and S3 services.

## References

| Topic | File |
|---|---|
| Test setup and auth helpers | `references/test-setup.md` |
| Data cleanup patterns | `references/data-cleanup.md` |
| Sub-resource test pattern | `references/sub-resource-tests.md` |
| Permissions matrix test | `references/permissions-matrix.md` |

## Quick checklist

- [ ] Guard tests with `describeIf(!IS_PROD, ...)` to skip in production
- [ ] Use `getAuthHeaders(role)` to create users and get session cookies
- [ ] Clean up test data with `WHERE name LIKE 'test-%'` patterns
- [ ] Never use `FLUSHALL` on Redis — use targeted key deletion
- [ ] Test auth: 401 without auth, 403 without permission, 200 with permission
- [ ] For sub-resources: test CRUD + auth in the same describe block
- [ ] Clean up sub-resource tables with `WHERE productId IN (SELECT id FROM prd_products WHERE name LIKE 'test-%')`
