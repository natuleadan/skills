# Zero Trust Auth Reference

## Core Principle

Zero Trust in application architecture means:
1. **Verify explicitly** — always validate identity at the entry point
2. **Least privilege** — default to lowest access level
3. **Assume breach** — never trust client-provided identity data

## Flow Diagram

```
┌─────────────────┐
│  Client Request  │
│  (no role sent)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Entry Point   │  ← Validates auth here
│  (Action/Route) │
└────────┬────────┘
         │ userRole extracted from session
         ▼
┌─────────────────┐
│    Service      │  ← Receives userRole as param
└────────┬────────┘
         │ userRole propagated
         ▼
┌─────────────────┐
│   Repository    │  ← Applies security filters by role
└─────────────────┘
```

## Role Propagation Contract

```typescript
// Domain
type Role = "admin" | "editor" | "user" | "public"

// Repository interface
interface ItemRepository {
  findAll(role: Role): Promise<Item[]>
  findById(id: string, role: Role): Promise<Item | null>
  softDelete(id: string, role: Role): Promise<void>
  hardDelete(id: string, role: Role): Promise<void>
}
```

## Security Filter Examples

### Visibility Filter (read)

| Role | Can see |
|------|---------|
| admin | All items (including deleted) |
| editor | Own items + non-deleted items |
| user | Non-deleted items |
| public | Non-deleted items marked public |

### Mutation Filter (write)

| Role | Can do |
|------|--------|
| admin | Create, update, hard delete |
| editor | Create, update own, soft delete own |
| user | Create own only |
| public | Nothing |

## Common Violations

| Violation | Risk | Fix |
|-----------|------|-----|
| Accepting role from request body | Privilege escalation | Extract from session |
| Skipping role propagation to repo | Data leak | Add role param to all queries |
| Defaulting to admin | Overprivilege | Default to public/user |
| Checking role in UI only | Bypassable | Always check server-side |
