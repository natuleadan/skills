# TypeScript Reference

## Environment

- **TypeScript:** 5.7.0+
- **Node.js:** 22.0.0+
- **Strict Mode:** Always enabled
- **Module:** ESNext (ESM)

## Type System Quick Reference

### Primitives

```typescript
string, number, boolean, bigint, symbol, undefined, null
```

### Collections

```typescript
T[]              // Array of T
Array<T>         // Alternative syntax
[T, U, V]        // Tuple (fixed length, specific types)
Record<K, V>     // Object with keys K, values V
Map<K, V>        // Map type
Set<T>           // Set type
```

### Control Flow

```typescript
T | U            // Union (T or U)
T & U            // Intersection (T and U)
T extends U      // Conditional type
T extends Promise<infer R> ? R : never  // Type extraction
```

## Strict Mode Checklist

- [ ] `strict: true`
- [ ] `noImplicitAny: true`
- [ ] `strictNullChecks: true`
- [ ] `strictFunctionTypes: true`
- [ ] `strictBindCallApply: true`
- [ ] `strictPropertyInitialization: true`
- [ ] `noImplicitThis: true`
- [ ] `alwaysStrict: true`
- [ ] `noUncheckedIndexedAccess: true`
- [ ] `exactOptionalPropertyTypes: true`
- [ ] `noImplicitReturns: true`
- [ ] `noFallthroughCasesInSwitch: true`
- [ ] `noImplicitOverride: true`

## Declaration Patterns

### Function Types

```typescript
type Fn<T, R> = (arg: T) => R
type Predicate<T> = (value: T) => boolean
type Reducer<T, U> = (acc: T, value: U) => T
```

### Object Types

```typescript
interface User {
  id: string
  name: string
  email: string
}

type UserWithTimestamp = User & {
  createdAt: Date
  updatedAt: Date
}
```

### Generic Constraints

```typescript
<T extends string>           // Must be string type
<T extends { length: number }> // Must have length property
<T extends U>                // T must be assignable to U
<T extends keyof U>          // T must be a key of U
```

## Utility Types

| Name | Purpose |
|------|---------|
| `Partial<T>` | All properties optional |
| `Required<T>` | All properties required |
| `Readonly<T>` | All properties readonly |
| `Pick<T, K>` | Select specific keys |
| `Omit<T, K>` | Exclude specific keys |
| `Record<K, V>` | Object with keys K |
| `Exclude<T, U>` | Remove U from T |
| `Extract<T, U>` | Keep only U in T |
| `NonNullable<T>` | Remove null/undefined |
| `Parameters<F>` | Function params as tuple |
| `ReturnType<F>` | Function return type |
| `InstanceType<C>` | Constructor instance type |

## Keywords

- `type` — declare type alias
- `interface` — declare object shape
- `enum` — ❌ AVOID (use unions)
- `class` — object constructor
- `extends` — inheritance or constraint
- `implements` — satisfy interface
- `as const` — make literal type
- `satisfies` — validate conformance
- `keyof` — keys of an object type
- `typeof` — type of a value
- `infer` — extract type in conditional

## Rules Summary

✅ **DO:**
- Use strict mode
- Validate at boundaries (Zod)
- Use union types over enums
- Type narrowing with guards
- Leverage type inference

❌ **DON'T:**
- Use `any` type
- Non-null assertions (`!`)
- Enums (use unions)
- Implicit `any`
- Dynamic type access
