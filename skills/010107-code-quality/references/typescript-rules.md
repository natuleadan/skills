# TypeScript Rules Lesson

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

## `import type` / `export type`

```typescript
// ❌ BAD: Runtime import of type-only value
import { User } from './types'; // Included in bundle unnecessarily

// ✅ GOOD: Type-only import (erased at compile time)
import type { User } from './types';
export type { User };
```

## Code Complexity

Keep functions focused and short:

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

// ✅ GOOD: Nullish check shorthand
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
