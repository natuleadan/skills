# Authentication API Endpoints Rules

## Endpoint Overview

The catch-all route `/api/auth/[...all]` automatically creates all authentication endpoints.

## Available Endpoints

### Sign Up

- [ ] **POST** `/api/auth/sign-up` - Create new account
- [ ] Request body: `{ name, email, password }`
- [ ] Response: User object and session

### Sign In

- [ ] **POST** `/api/auth/sign-in` - Login with email/password
- [ ] Request body: `{ email, password }`
- [ ] Response: User object and session

### Sign Out

- [ ] **POST** `/api/auth/sign-out` - End current session
- [ ] Requires authentication cookie

### Get Session

- [ ] **GET** `/api/auth/get-session` - Retrieve current session
- [ ] Returns user data if authenticated
- [ ] Returns null if not logged in

### OAuth (Future)

- [ ] **GET** `/api/auth/oauth/*` - OAuth providers (Google, GitHub, etc.)
- [ ] Requires provider configuration in auth.ts

## Client-Side Usage

Better Auth client provides typed methods:

```typescript
// Sign up
const res = await signUp.email({ name, email, password });

// Sign in
const res = await signIn.email({ email, password });

// Sign out
await signOut();

// Get session
const { data: session } = useSession();
```

## Error Handling

- [ ] Check `res.error` on signIn/signUp responses
- [ ] Handle specific error codes from Better Auth
- [ ] Redirect on successful auth

## Security Headers

- [ ] Cookie configured with httpOnly, secure in production
- [ ] SameSite policy set appropriately
- [ ] CORS configured via trustedOrigins

---

> [!note]
> Server Actions can wrap these endpoints for additional validation.
