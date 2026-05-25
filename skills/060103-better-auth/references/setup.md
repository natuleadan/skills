# Better Auth Integration Rules

## Installation

- [ ] Install: `npm add better-auth`
- [ ] Generate secret: `npm dlx auth@latest secret`
- [ ] Add to .env: `BETTER_AUTH_SECRET` and `BETTER_AUTH_URL`

## Configuration

Create `src/infrastructure/external/auth.ts`:

```typescript
import { betterAuth } from "better-auth";
import { prismaAdapter } from "better-auth/adapters/prisma";
import { PrismaPg } from "@prisma/adapter-pg";
import { PrismaClient } from "../../../generated/prisma/client";

const adapter = new PrismaPg({ connectionString: process.env.DATABASE_URL });
const prisma = new PrismaClient({ adapter });

export const auth = betterAuth({
  database: prismaAdapter(prisma, { provider: "postgresql" }),
  emailAndPassword: { enabled: true, requireEmailVerification: false },
  session: { expiresIn: 60 * 60 * 24 * 7, updateAge: 60 * 60 * 24 },
});
```

## Configuration Checklist

- [ ] Use prismaAdapter with provider "postgresql"
- [ ] Enable emailAndPassword for login/signup
- [ ] Configure session expiry (7 days default)
- [ ] Add trustedOrigins if using non-standard ports

## API Route

Create `src/app/api/auth/[...all]/route.ts`:

```typescript
import { auth } from "@/infrastructure/external/auth";
import { toNextJsHandler } from "better-auth/next-js";

export const { GET, POST } = toNextJsHandler(auth);
```

## Client Setup

Create `src/lib/auth-client.ts`:

```typescript
import { createAuthClient } from "better-auth/react";

export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_APP_URL || "http://localhost:3000",
});

export const { signIn, signUp, signOut, useSession } = authClient;
```

## Usage in Components

- [ ] Use `signUp.email()` for registration
- [ ] Use `signIn.email()` for login
- [ ] Use `signOut()` for logout
- [ ] Use `useSession()` hook for session state

---

> [!important]
> Always use baseURL in createAuthClient for proper cookie handling.
