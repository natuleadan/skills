---
name: 060102-zero-trust
description: Zero Trust authentication pattern — validate identity once at entry, propagate via userRole, never trust client-provided role data.
---

# Zero Trust Authentication

Zero Trust authentication pattern: validate identity at the entry point, propagate via `userRole` parameter, never accept role data from the client.

## References

| Topic | File |
|---|---|
| Core principle, architecture flow, role types, security rules | [references/zero-trust.md](references/zero-trust.md) |
| Identity propagation through layers | [references/role-propagation.md](references/role-propagation.md) |
| Data filtering, visibility, soft-delete, ownership conventions | [references/data-filtering.md](references/data-filtering.md) |
| Full Action→Service→Repository code example | [references/implementation-examples.md](references/implementation-examples.md) |
| Correct vs wrong patterns, implementation checklist | [references/quick-reference-good-bad.md](references/quick-reference-good-bad.md) |
