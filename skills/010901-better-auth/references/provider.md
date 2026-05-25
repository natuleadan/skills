# Auth Provider Rules

## Overview

The Auth Provider provides authentication state to all components in the application. It wraps the app and exposes session state via React Context.

## Implementation Location

- [ ] Provider: `src/components/auth/auth-provider.tsx`
- [ ] Hook: `useAuth()` exported from provider
- [ ] Client: `src/lib/auth-client.ts` for Better Auth client

## AuthProvider Component

```typescript
// src/components/auth/auth-provider.tsx
"use client"

import { createContext, useContext, useState, useEffect, ReactNode } from "react"
import { authClient } from "@/lib/auth-client"

interface AuthState {
  user: AuthUser | null
  isLoading: boolean
  signIn: (email: string, password: string) => Promise<void>
  signUp: (name: string, email: string, password: string) => Promise<void>
  signOut: () => Promise<void>
  refreshSession: () => void
}

const AuthContext = createContext<AuthState>(/* ... */)

export function useAuth() {
  return useContext(AuthContext)
}

export function AuthProvider({ children }: { children: ReactNode }) {
  // Implementation
}
```

## Auth State Interface

```typescript
interface AuthUser {
  id: string
  name: string | null
  email: string
  emailVerified: boolean
  image: string | null | undefined
  createdAt: Date
  updatedAt: Date
}
```

## useAuth Hook Usage

```typescript
// In any component
const { user, isLoading, signIn, signUp, signOut } = useAuth()

// Check if user is logged in
if (user) {
  console.log("Logged in as:", user.email)
}
```

## Provider Setup in Pages

Wrap pages that need auth:

```typescript
// src/app/login/page.tsx
export default function LoginPage() {
  return (
    <AuthProvider>
      <LoginForm />
    </AuthProvider>
  )
}
```

## Checklist

- [ ] AuthProvider wraps auth-required pages
- [ ] useAuth provides user, isLoading, signIn, signUp, signOut
- [ ] Session persists across page navigation
- [ ] User state updates on auth changes

## Integration with Better Auth Client

The provider uses `authClient` from `src/lib/auth-client.ts`:

- [ ] `signIn.email()` - Login with email/password
- [ ] `signUp.email()` - Register with email/password
- [ ] `signOut()` - Logout
- [ ] `authClient.getSession()` - Get current session

---

> [!note]
> For simpler cases, direct use of createAuthClient hooks (signIn, signUp, signOut, useSession) is sufficient without custom provider.
