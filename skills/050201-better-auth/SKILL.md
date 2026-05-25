---
name: 050201-better-auth
description: Better Auth integration for Next.js — setup, API endpoints, client SDK, and React Context provider for session management.
---

# Better Auth

## Overview

Better Auth is an authentication library for Next.js. It provides a complete auth system with email/password, session management, and React hooks.

## Quick Start

```bash
# Install
npm add better-auth
npx auth@latest secret

# Set env vars (in .env)
BETTER_AUTH_SECRET="your-generated-secret"
BETTER_AUTH_URL="http://localhost:3000"
NEXT_PUBLIC_APP_URL="http://localhost:3000"
```

## Architecture

```
Next.js App
├── API Route: /api/auth/[...all]  ← toNextJsHandler(auth)
│   ├── POST /api/auth/sign-in     ← Login
│   ├── POST /api/auth/sign-up     ← Register
│   ├── POST /api/auth/sign-out    ← Logout
│   └── GET  /api/auth/get-session ← Current session
│
├── Auth Config: src/lib/auth.ts   ← betterAuth({ ... })
│
├── Auth Client: src/lib/auth-client.ts  ← createAuthClient()
│   ├── signIn.email()
│   ├── signUp.email()
│   ├── signOut()
│   └── useSession()
│
└── Auth Provider (optional)       ← React Context wrapper
    └── useAuth() hook
```

## Key Files

| File | Purpose |
|------|---------|
| `src/lib/auth.ts` | Better Auth server config |
| `src/app/api/auth/[...all]/route.ts` | Catch-all API route |
| `src/lib/auth-client.ts` | Browser client |
| `src/components/auth/auth-provider.tsx` | React Context provider (optional) |

## Quick Reference

```typescript
// Server
import { auth } from "@/lib/auth"

// Client
import { authClient } from "@/lib/auth-client"
const { signIn, signUp, signOut, useSession } = authClient

// Sign in
const result = await signIn.email({ email, password })
if (result.error) { /* handle */ }

// Sign up
const result = await signUp.email({ name, email, password })

// Session
const { data: session, isPending } = useSession()

// Sign out
await signOut()
```

See reference docs for full setup and provider patterns.
