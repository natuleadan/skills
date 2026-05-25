# Service Layering

Three-layer architecture: Repository → Service → Action

## Layer Responsibilities

### Repository (.repository.ts)

- Lowest layer: raw database queries
- Receives `userRole` for security filtering
- Applies `visibility` and `soft_delete` filters
- Returns unprocessed database rows

### Service (.service.ts)

- Middle layer: business logic orchestration
- Receives `userRole` from action
- Calls repository methods
- Transforms data, applies business rules
- Sanitizes sensitive fields per role

### Action (.actions.ts)

- Highest layer: entry point
- Validates auth via auth service
- Extracts `userRole` from session
- Calls service methods with role
- Returns final response

## Flow Example

```
Action: loginUser()
  → Auth service gets session context
  → Extract userRole
  → Call Service.getUserProfile(userId, userRole)
    → Service calls Repository.getUser(userId, userRole)
      → Repository filters: SELECT * WHERE id = ? AND visibility != 'confidential'
    → Service sanitizes response per userRole
  → Return to client
```

## Rules

- [ ] **Action** determines identity & role once
- [ ] **Service** orchestrates and enforces business rules
- [ ] **Repository** applies data-layer security filters
- [ ] **Never bypass** any layer for "efficiency"
- [ ] **userRole parameter** is mandatory in all three layers
