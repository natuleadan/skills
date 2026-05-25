# Auth Macro

Identity resolution order: cookies → bearer token → API key.

```typescript
.get("/protected", ({ user }) => user, { auth: true })
```

The macro auto-detects the auth method and resolves the session/user in-process.
