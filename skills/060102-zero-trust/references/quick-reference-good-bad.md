# Quick Reference: Correct vs Wrong

```typescript
// ✅ Correct: extract role from session
const role = session?.user?.role ?? "public"
getDataService(role)

// ❌ WRONG: never accept role from client
const role = request.body.role  // UNSAFE!
```

## Implementation Checklist

### Entry Points (Actions / Controllers)

- [ ] Validate session using auth provider
- [ ] Extract role from session or default to 'public'
- [ ] Pass userRole as parameter to service
- [ ] NEVER trust client-provided role

### Services

- [ ] Accept userRole as function parameter
- [ ] Propagate userRole to repository calls
- [ ] Implement role-based business logic

### Repositories

- [ ] Accept userRole in query methods
- [ ] Apply visibility filters based on role
- [ ] Apply soft-delete filters for non-admin roles
