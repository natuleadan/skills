---
name: 060103-better-auth
description: Better Auth integration for Next.js — setup, API endpoints, client SDK, React Context provider, and Organization plugin for multi-tenant auth.
license: MIT
---

# Better Auth

## Overview

Better Auth is an authentication library for Next.js. It provides a complete auth system with email/password, session management, React hooks, and an Organization plugin for multi-tenant access control.

## Quick Start

```bash
npm add better-auth
npx auth@latest secret
```

Set `BETTER_AUTH_SECRET`, `BETTER_AUTH_URL`, `NEXT_PUBLIC_APP_URL` in `.env`.

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
│   └── organizationClient()       ← org plugin (optional)
│
└── Auth Provider (optional)       ← React Context wrapper
    └── useAuth() hook
```

## Quick Reference

```typescript
import { auth } from "@/lib/auth"
import { authClient } from "@/lib/auth-client"
const { signIn, signUp, signOut, useSession } = authClient

// Sign in
const result = await signIn.email({ email, password })
if (result.error) { /* handle */ }

// Session
const { data: session, isPending } = useSession()
```

## Organization Plugin

See [references/organization-plugin.md](references/organization-plugin.md) for full setup.

```typescript
// Client hooks
const { data: orgs } = authClient.useListOrganizations()
const { data: activeOrg } = authClient.useActiveOrganization()

// Mutations
await authClient.organization.setActive({ organizationId: orgId })
await authClient.organization.inviteMember({ email, role: "member", organizationId: orgId })
```

## Key Files

| File | Purpose |
|------|---------|
| `src/lib/auth.ts` | Better Auth server config |
| `src/app/api/auth/[...all]/route.ts` | Catch-all API route |
| `src/lib/auth-client.ts` | Browser client |
| `src/components/auth/auth-provider.tsx` | React Context provider (optional) |
| `references/organization-plugin.md` | Org plugin config, teams, dynamic AC |
