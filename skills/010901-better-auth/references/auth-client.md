# Auth Client Configuration Rules

## Overview

The auth client is the main interface for authentication operations in the browser. It provides methods for sign in, sign up, sign out, and session management.

## Implementation

File: `src/lib/auth-client.ts`

```typescript
import { createAuthClient } from "better-auth/react"

export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_APP_URL || "http://localhost:3000",
})

export const { signIn, signUp, signOut, useSession } = authClient
```

## Configuration Options

### baseURL (Required)

- [ ] Must match your application URL
- [ ] Development: `http://localhost:3000`
- [ ] Production: `https://your-domain.com`
- [ ] Used for cookie configuration and redirects

### Exported Methods

- [ ] **signIn** - Sign in with email/password or OAuth
- [ ] **signUp** - Create new account
- [ ] **signOut** - End current session
- [ ] **useSession** - React hook for session state

## Usage Examples

### Sign In with Email

```typescript
const result = await signIn.email({
  email: "user@example.com",
  password: "password123",
})

if (result.error) {
  console.error(result.error.message)
} else {
  // Success - redirect or update UI
}
```

### Sign Up with Email

```typescript
const result = await signUp.email({
  name: "John Doe",
  email: "john@example.com",
  password: "password123",
})
```

### Sign Out

```typescript
await signOut()
```

### Get Session (Hook)

```typescript
const { data: session, isPending } = useSession()

if (isPending) {
  return <Loading />
}

if (session) {
  return <Dashboard user={session.user} />
}

return <LoginPrompt />
```

## Checklist

- [ ] createAuthClient called with baseURL
- [ ] Methods destructured and exported
- [ ] baseURL matches BETTER_AUTH_URL
- [ ] Environment variable NEXT_PUBLIC_APP_URL set

## TypeScript Types

The client provides typed responses:

- [ ] `signIn.email()` returns `Promise<{ data?: { user, session }, error?: { message } }>`
- [ ] `useSession()` returns `{ data: { user, session } | null, isPending: boolean }`

---

> [!important]
> Always set baseURL correctly for cookies to work in production.
