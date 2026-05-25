# TypeScript Rules & Anti-Patterns

Strict TypeScript conventions to prevent bugs and ensure maintainability.

## No `any` — Ever

```typescript
// ❌ BAD: any loses all type safety
function process(data: any) {
  return data.name; // No error even if name doesn't exist
}

// ✅ GOOD: Use generics
function process<T extends { name: string }>(data: T): string {
  return data.name;
}

// ✅ GOOD: Use unknown with type guard
function process(data: unknown): string {
  if (typeof data === 'object' && data !== null && 'name' in data) {
    return String((data as { name: unknown }).name);
  }
  throw new Error('Invalid data shape');
}

// ✅ GOOD: Use Record<string, unknown> for dynamic objects
function process(data: Record<string, unknown>): void {
  // Explicit shape, keys checked at runtime
}
```

## No Enums — Use Union Literals

```typescript
// ❌ BAD: TypeScript enum (generates extra JS, not tree-shakeable)
enum Status {
  Active = 'active',
  Inactive = 'inactive',
}

// ✅ GOOD: Union literal type
type Status = 'active' | 'inactive';

// ✅ GOOD: as const object (also gives you an iterable)
const STATUS = {
  Active: 'active',
  Inactive: 'inactive',
} as const;

type Status = typeof STATUS[keyof typeof STATUS];

// ✅ GOOD: Use in function params
function updateStatus(status: Status) {
  // TypeScript ensures only valid values
}
```

## No Non-Null Assertion `!`

```typescript
// ❌ BAD: Runtime crash if element is null
const el = document.getElementById('root')!;
el.style.color = 'red';

// ✅ GOOD: Explicit null check
const el = document.getElementById('root');
if (!el) throw new Error('Root element not found');
el.style.color = 'red';

// ✅ GOOD: Optional chaining
const color = el?.style?.color ?? 'default';
```

## `import type` / `export type`

```typescript
// ❌ BAD: Runtime import of type-only value
import { User } from './types'; // Included in bundle unnecessarily

// ✅ GOOD: Type-only import (erased at compile time)
import type { User } from './types';
export type { User };

// ✅ GOOD: Separate type and value imports
import type { User, Role } from './types';
import { getUserById } from './api';

export type { User };
export { createUser };

// ✅ GOOD: Multiple type imports
import type { User, Role, Permission } from './types';

// ✅ GOOD: With values from same module
import { API_URL } from './config';
import type { Config } from './config';
```

## No `@ts-ignore`

```typescript
// ❌ BAD: Silences TypeScript, hides real bugs
// @ts-ignore
const result = badlyTypedLib.doThing();

// ✅ GOOD: Fix the type properly
const result = (badlyTypedLib as LibWithDoThing).doThing();

// ✅ GOOD: Use @ts-expect-error only if intentionally testing a type error
// @ts-expect-error Testing invalid input
expectError(null);
```

## Zod Validation at Boundaries

Validate external data (API, user input) using Zod:

```typescript
import { z } from 'zod';

const UserSchema = z.object({
  id: z.string().uuid(),
  name: z.string().min(1),
  email: z.string().email(),
});

type User = z.infer<typeof UserSchema>;

function parseUser(data: unknown): User {
  return UserSchema.parse(data); // Throws ZodError if invalid
}

// Safe parsing without throwing
const result = UserSchema.safeParse(data);
if (result.success) {
  console.log(result.data); // Typed as User
} else {
  console.error(result.error.issues);
}
```

## Discriminated Unions / Result Pattern

Use tagged unions for type-safe error handling:

```typescript
type Result<T, E = Error> =
  | { ok: true; value: T }
  | { ok: false; error: E }

async function fetchUser(id: string): Promise<Result<User>> {
  try {
    const response = await fetch(`/api/users/${id}`);
    const data = await response.json();
    return { ok: true, value: data };
  } catch (error) {
    return { ok: false, error: error as Error };
  }
}

// Usage — TypeScript narrows based on `ok` discriminant
const result = await fetchUser('123');
if (result.ok) {
  console.log(result.value.name);  // User
} else {
  console.error(result.error.message); // Error
}
```

## Avoid Redundant Type Annotations

Let TypeScript infer types when obvious:

```typescript
// ❌ BAD: Redundant annotations
const name: string = 'Alice';
const age: number = 30;
const active: boolean = true;

// ✅ GOOD: Let TypeScript infer
const name = 'Alice';      // string
const age = 30;            // number
const active = true;       // boolean

// ✅ GOOD: Annotate when inference is insufficient
const config: Record<string, unknown> = loadConfig();
const callback: (e: Event) => void = handleClick;
```

## Code Complexity

Keep functions focused and short — early returns reduce nesting:

```typescript
// ❌ BAD: High complexity (many branches)
function processOrder(order: Order) {
  if (order.status === 'active') {
    if (order.items.length > 0) {
      for (const item of order.items) {
        if (item.available) {
          if (item.price > 0) {
            // ... more nesting
          }
        }
      }
    }
  }
}

// ✅ GOOD: Early returns reduce nesting
function processOrder(order: Order) {
  if (order.status !== 'active') return;
  if (order.items.length === 0) return;

  const availableItems = order.items.filter(i => i.available && i.price > 0);
  return availableItems.map(processItem);
}
```

## Prefer `for...of` over `forEach`

```typescript
// ❌ BAD: forEach (no break, async issues)
items.forEach(async (item) => {
  await process(item); // Won't await properly!
});

// ✅ GOOD: for...of (awaitable, breakable)
for (const item of items) {
  await process(item);
}

// ✅ ALSO GOOD: map/filter for transformations
const processed = await Promise.all(items.map(process));
```

## No Unnecessary Optionals

```typescript
// ❌ BAD: Everything optional (hides missing data)
interface User {
  id?: string;
  name?: string;
  email?: string;
}

// ✅ GOOD: Required fields explicit, optional only when truly optional
interface User {
  id: string;
  name: string;
  email: string;
  avatar?: string; // Genuinely optional
}
```

## Template Literals over Concatenation

```typescript
// ❌ BAD
const msg = 'Hello ' + name + ', you have ' + count + ' messages';

// ✅ GOOD
const msg = `Hello ${name}, you have ${count} messages`;
```

## Strict Equality

```typescript
// ❌ BAD: Loose equality (coerces types)
if (value == null) {}   // matches null AND undefined
if (count == '0') {}    // matches number 0 and string '0'

// ✅ GOOD: Strict equality
if (value === null || value === undefined) {}
if (count === 0) {}

// ✅ GOOD: Nullish check shorthand (only acceptable for this)
if (value == null) {} // Only acceptable for null + undefined check together
```

## `const` by Default

```typescript
// ❌ BAD: let when never reassigned
let name = 'John';
let items = [1, 2, 3];

// ✅ GOOD: const (signals immutability)
const name = 'John';
const items = [1, 2, 3]; // Array content can change, reference cannot
```

## Anti-Patterns Reference

| ❌ WRONG | ✅ RIGHT |
|---------|---------|
| `any` type | Generic `<T>` or `unknown` + guard |
| `enum Status {}` | `type Status = 'a' \| 'b'` |
| Non-null `value!` | Null check + guard |
| `@ts-ignore` | Fix the type |
| `import { Type }` | `import type { Type }` |
| `forEach` with async | `for...of` loop |
| `let x = 'fixed'` | `const x = 'fixed'` |
| `'a' + b + 'c'` | `` `a${b}c` `` |
| `==` | `===` |
| Deep nesting | Early returns + extract functions |
| Untrusted `unknown` data | Zod schema validation |
| `throw` in catch blocks | `Result<T, E>` discriminated union |
