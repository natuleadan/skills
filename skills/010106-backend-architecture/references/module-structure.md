# Module Structure Lesson

Organize code in layers: service, repository, actions, hooks. One module per domain.

## Module File Layout

Each domain module follows this structure:

```
src/lib/{domain}/
├── types.ts                  # TypeScript interfaces
├── schemas.ts                # Zod validation schemas
├── constants.ts              # Cache keys, limits, config
├── repository.ts             # Re-exports all DB operations
├── repository.queries.ts     # Read operations only
├── repository.mutations.ts   # Write operations only
├── service.base.ts           # Shared base logic
├── service.admin.ts          # Admin-only (extends base)
├── service.ts                # Main orchestrator (extends admin)
├── actions.ts                # Server Actions (entry points)
├── hooks.ts                  # React hooks (client-side)
├── assemblers.ts             # Data transform for UI layer
└── utils.ts                  # Domain utilities
```

## Service Layer Hierarchy

Three levels: base → admin → public:

```typescript
// service.base.ts — shared logic
class ProductBaseService {
  protected async validateExists(id: string) {
    const product = await ProductRepository.findById(id);
    if (!product) throw new NotFoundError('product');
    return product;
  }
}

// service.admin.ts — admin-only
class ProductAdminService extends ProductBaseService {
  async hardDelete(id: string) {
    await this.validateExists(id);
    return ProductRepository.delete(id);
  }
}

// service.ts — public API
class ProductService extends ProductAdminService {
  async getPublic(id: string) {
    const product = await this.validateExists(id);
    if (product.visibility !== 'public') throw new ForbiddenError();
    return product;
  }
}
```

## Repository Split

Separate reads from writes:

```typescript
// repository.queries.ts — reads only
export async function findById(id: string) {
  return db.from('products').select('*').eq('id', id).single();
}

// repository.mutations.ts — writes only
export async function softDelete(id: string) {
  return db.from('products').update({ soft_delete: true }).eq('id', id);
}

// repository.ts — re-export both
export * from './repository.queries';
export * from './repository.mutations';
```

## Actions — Server Entry Points

```typescript
'use server';
export async function createProductAction(input: unknown) {
  const user = await auth();
  if (!user) throw new UnauthorizedError();

  const validated = CreateProductSchema.parse(input);
  const product = await ProductService.create(validated, user.role);

  revalidateTag('products');
  return { success: true, data: product };
}
```

## Centralized Environment Config

Never access `process.env` directly outside `env.ts`:

```typescript
// lib/config/env.ts
function requireEnv(key: string): string {
  const value = process.env[key];
  if (!value) throw new Error(`Missing env var: ${key}`);
  return value;
}

export const env = {
  databaseUrl: requireEnv('DATABASE_URL'),
  apiUrl: requireEnv('API_URL'),
  apiSecret: requireEnv('API_SECRET'),
} as const;

// Usage anywhere — never process.env directly
import { env } from '@/lib/config/env';
// Database client setup
```

## Log Sanitization

Sanitize user input before logging to prevent log injection:

```typescript
// utils/log.ts
export function sanitizeLog(input: unknown, maxLength = 256): string {
  return String(input)
    .replace(/[\x00-\x1F\x7F]/g, '')   // Remove control characters
    .slice(0, maxLength);
}

// ✅ GOOD: Sanitize before logging
console.error('Failed for user:', sanitizeLog(userInput), error.code);

// ❌ BAD: Raw user input in logs (log injection attack)
console.error('Failed for user:', userInput);
```

## Security Utilities

```typescript
// Prevent open redirects
export function isLocalUrl(url: string): boolean {
  if (!url.startsWith('/') || url.startsWith('//')) return false;
  try {
    new URL(url, 'http://localhost');
    return true;
  } catch {
    return false;
  }
}

// Safe JSON-LD for structured data (prevents script injection)
export function safeJsonLd(data: unknown): string {
  return JSON.stringify(data)
    .replace(/</g, '\\u003c')
    .replace(/>/g, '\\u003e')
    .replace(/&/g, '\\u0026');
}

// ✅ GOOD: Validate redirect URLs
const redirectUrl = searchParams.get('redirect');
if (redirectUrl && isLocalUrl(redirectUrl)) {
  router.push(redirectUrl);
}

// ❌ BAD: Open redirect vulnerability
router.push(searchParams.get('redirect') ?? '/');
```

## Anti-Patterns

| ❌ WRONG | ✅ RIGHT |
|---------|---------|
| Business logic in UI components | Put in `service.ts` |
| DB queries in Server Actions | Put in `repository.ts` |
| `process.env.X` scattered | Centralize in `env.ts` |
| User input directly in logs | `sanitizeLog(input)` first |
| `router.push(anyUrl)` | `isLocalUrl(url)` check first |
| One giant `service.ts` | Split base/admin/main layers |
