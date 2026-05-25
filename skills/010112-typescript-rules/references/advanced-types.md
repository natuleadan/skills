# Advanced Types Lesson

Type-level programming for complex scenarios.

## Generics

Reusable types that work with any type parameter:

```typescript
// Generic function
function first<T>(items: T[]): T | undefined {
  return items[0]
}

// Constrained generic
function logLength<T extends { length: number }>(item: T): T {
  console.log(item.length)
  return item
}

// Generic interface
interface Repository<T, ID = string> {
  findById(id: ID): Promise<T | null>
  save(entity: T): Promise<T>
}
```

## Mapped Types

Transform existing types:

```typescript
// Make all properties readonly
type Immutable<T> = { readonly [K in keyof T]: T[K] }

// Make all properties optional
type Partial<T> = { [K in keyof T]?: T[K] }

// Create getters for each property
type Getters<T> = {
  [K in keyof T as `get${Capitalize<string & K>}`]: () => T[K]
}
```

## Conditional Types

Type depends on another type:

```typescript
// Basic: check if T extends string
type IsString<T> = T extends string ? true : false

// Extract array element type
type ArrayElement<T> = T extends (infer E)[] ? E : never

// Unwrap Promise
type Awaited<T> = T extends Promise<infer R> ? R : T
```

## The `satisfies` Operator (TS 5.0+)

Validate type conformance without losing inference:

```typescript
// ❌ as loses literal type information
const colors = { red: "#ff0000" } as Record<string, string>
colors.red // string, not "#ff0000"

// ✅ satisfies preserves inference
const colors = { red: "#ff0000" } satisfies Record<string, string>
colors.red // "#ff0000" (literal type preserved)
```

## Utility Types

| Type | Purpose |
|------|---------|
| `Partial<T>` | All properties optional |
| `Required<T>` | All properties required |
| `Pick<T, K>` | Select specific properties |
| `Omit<T, K>` | Exclude specific properties |
| `Record<K, V>` | Object with typed keys/values |
| `Extract<T, U>` | Types in T assignable to U |
| `Exclude<T, U>` | Types in T not assignable to U |
| `ReturnType<F>` | Function return type |
| `Parameters<F>` | Function parameter types |

## Rules

- [ ] **Use generics** — avoid repeating type logic
- [ ] **Mapped types** — for object transformations
- [ ] **Conditional types** — for type-level decisions
- [ ] **satisfies** — validate without losing inference
- [ ] **Utility types** — leverage built-in type helpers
