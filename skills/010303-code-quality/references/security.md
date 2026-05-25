# Security Lesson

Secure code prevents data breaches, injection attacks, credential theft, and log manipulation.

## No Hardcoded Secrets

```typescript
// ✅ GOOD: Environment variables
const apiKey = process.env.NEXT_PUBLIC_API_KEY;
const dbUrl = process.env.DATABASE_URL;

// ❌ BAD: Hardcoded in source
const apiKey = 'sk-1234567890abcdef';
const dbUrl = 'postgresql://user:pass@localhost';
```

- Public values → `NEXT_PUBLIC_*`
- Secrets → `.env` (git-ignored, never committed)
- Production → Platform environment variables

## Input Validation at Boundaries

```typescript
import { z } from 'zod';

const Schema = z.object({
  email: z.string().email(),
  age: z.number().min(0).max(150)
});

// ✅ GOOD: Validate before processing
export async function updateUser(input: unknown) {
  const validated = Schema.parse(input);
  return db.users.update(validated);
}

// ❌ BAD: Trust unvalidated input
export async function updateUser(input: any) {
  return db.users.update(input);
}
```

## SQL Injection Prevention

```typescript
// ✅ GOOD: Parameterized query
const user = await db.query(
  'SELECT * FROM users WHERE email = $1',
  [userEmail]
);

// ❌ BAD: String concatenation (SQL injection!)
const user = await db.query(
  `SELECT * FROM users WHERE email = '${userEmail}'`
);
// If userEmail = "'; DROP TABLE users; --" → catastrophic
```

## Open Redirect Prevention

Validate redirect URLs before navigating:

```typescript
export function isLocalUrl(url: string): boolean {
  if (!url.startsWith('/') || url.startsWith('//')) return false;
  try { new URL(url, 'http://localhost'); return true; }
  catch { return false; }
}

// ✅ GOOD: Validate before redirect
const redirectUrl = searchParams.get('redirect');
if (redirectUrl && isLocalUrl(redirectUrl)) {
  router.push(redirectUrl);
}

// ❌ BAD: Open redirect
router.push(searchParams.get('redirect') ?? '/');
// Attacker sends: ?redirect=https://evil.com/phishing
```

## Log Injection Prevention

Sanitize user input before logging:

```typescript
export function sanitizeLog(input: unknown, maxLength = 256): string {
  return String(input)
    .replace(/[\x00-\x1F\x7F]/g, '')  // Remove control characters
    .slice(0, maxLength);
}

// ✅ GOOD: Sanitize before logging
console.error('Failed for:', sanitizeLog(userInput), error.code);

// ❌ BAD: Raw input in logs
console.error('Failed for:', userInput);
// Attacker sends: "x\nINFO: Admin logged in successfully"
```

## CORS Configuration

```typescript
// ✅ GOOD: Restrict to known origins
res.setHeader('Access-Control-Allow-Origin', 'https://myapp.com');

// ❌ BAD: Allow all origins
res.setHeader('Access-Control-Allow-Origin', '*');
```

## Authentication & Authorization

Validate identity and permissions server-side:

```typescript
// ✅ GOOD: Validate on server
export async function deleteUser(userId: string) {
  const currentUser = await auth(); // Resolved server-side
  if (!currentUser) throw new UnauthorizedError();
  if (currentUser.role !== 'admin') throw new ForbiddenError();
  return db.users.delete(userId);
}

// ❌ BAD: Trust client-provided role
export async function deleteUser(userId: string, role: string) {
  if (role !== 'admin') throw new Error('Not admin');
  // Client can send role='admin' — bypassed!
  return db.users.delete(userId);
}
```

## Anti-Patterns

| ❌ WRONG | ✅ RIGHT |
|---------|---------|
| Hardcode secrets | Use env vars |
| Trust user input | Validate with Zod |
| String-concat SQL | Parameterized queries |
| `router.push(anyUrl)` | `isLocalUrl(url)` check |
| Raw user input in logs | `sanitizeLog(input)` |
| Allow all CORS | Restrict to known origins |
| Trust client roles | Validate server-side |

## Security Checklist

- ✅ No hardcoded secrets
- ✅ All user input validated at boundaries
- ✅ SQL uses parameterized queries
- ✅ Redirect URLs validated with `isLocalUrl()`
- ✅ User input sanitized before logging
- ✅ CORS restricted to known origins
- ✅ Auth/permissions enforced server-side
