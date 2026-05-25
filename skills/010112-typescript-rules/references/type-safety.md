# Type Safety Lesson

Core principles for leveraging TypeScript's type system.

## Strict Mode

Enable all strict options in tsconfig.json:

- `strict: true` — enables strictNullChecks, strictFunctionTypes, and more
- `noUncheckedIndexedAccess: true` — array/object access returns T | undefined
- `exactOptionalPropertyTypes: true` — optional properties cannot be undefined
- `noImplicitAny: true` — reject implicit any types
- `useUnknownInCatchVariables: true` — catch errors as unknown, not any

## Avoiding `any`

Never use `any` — it defeats type safety.

**❌ DON'T:**
```typescript
const value: any = getUserData()  // Type info lost
value.nonexistent.method()        // No error, crashes at runtime
```

**✅ DO:**
```typescript
const value: unknown = getUserData()
if (typeof value === 'object' && value !== null) {
  // Narrowed type
}
```

## No Non-Null Assertions (`!`)

Don't force TypeScript to ignore null/undefined.

**❌ DON'T:**
```typescript
const user = getUser()!  // Trusting it's not null
console.log(user.name)   // Crashes if null
```

**✅ DO:**
```typescript
const user = getUser()
if (user) {
  console.log(user.name)
}
```

## Union & Discriminated Unions

Use tagged unions for type-safe handling:

```typescript
type Result<T> =
  | { success: true; data: T }
  | { success: false; error: string }

function handle<T>(result: Result<T>) {
  if (result.success) {
    console.log(result.data)  // T, not Result<T>
  } else {
    console.log(result.error) // string
  }
}
```

## Type Guards

Narrow types with explicit checks:

```typescript
// typeof guard
if (typeof value === 'string') { }

// instanceof guard
if (error instanceof ValidationError) { }

// Custom guard
function isUser(obj: any): obj is User {
  return obj && 'id' in obj && 'name' in obj
}
```

## Rules

- [ ] **Enable strict mode** — all strict flags in tsconfig
- [ ] **Never use any** — prefer unknown
- [ ] **No non-null assertions** — use guards instead
- [ ] **Discriminated unions** — for type-safe control flow
- [ ] **Type guards** — narrow types explicitly
- [ ] **Infer over annotate** — let TypeScript infer when obvious
