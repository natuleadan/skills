# Code Examples

## Type Safety Fundamentals

### Union Types with Type Guards

```typescript
type User = { type: 'user'; name: string }
type Admin = { type: 'admin'; permissions: string[] }
type Person = User | Admin

function describe(person: Person): string {
  if (person.type === 'admin') {
    return `Admin with ${person.permissions.length} permissions`
  }
  return `User: ${person.name}`
}
```

### Result Type for Error Handling

```typescript
type Result<T, E = Error> =
  | { ok: true; value: T }
  | { ok: false; error: E }

async function fetchUser(id: string): Promise<Result<User>> {
  try {
    const response = await fetch(`/api/users/${id}`)
    const data = await response.json()
    return { ok: true, value: data }
  } catch (error) {
    return { ok: false, error: error as Error }
  }
}

// Usage
const result = await fetchUser('123')
if (result.ok) {
  console.log(result.value.name)
} else {
  console.error(result.error.message)
}
```

## Advanced Type Patterns

### Generic Repository

```typescript
interface Repository<T, ID = string> {
  findById(id: ID): Promise<T | null>
  findAll(): Promise<T[]>
  save(entity: T): Promise<T>
  delete(id: ID): Promise<boolean>
}

class UserRepository implements Repository<User> {
  async findById(id: string): Promise<User | null> {
    const response = await fetch(`/api/users/${id}`)
    return response.ok ? response.json() : null
  }

  async findAll(): Promise<User[]> {
    const response = await fetch('/api/users')
    return response.json()
  }

  async save(entity: User): Promise<User> {
    const response = await fetch('/api/users', {
      method: 'POST',
      body: JSON.stringify(entity)
    })
    return response.json()
  }

  async delete(id: string): Promise<boolean> {
    const response = await fetch(`/api/users/${id}`, {
      method: 'DELETE'
    })
    return response.ok
  }
}
```

### Mapped Types for API DTOs

```typescript
// Define domain model
interface User {
  id: string
  name: string
  email: string
  password: string
  createdAt: Date
}

// Create DTO (exclude sensitive fields)
type UserDTO = Omit<User, 'password'>

// Create form input (all optional except id)
type UpdateUserForm = Partial<Omit<User, 'id' | 'createdAt'>>

// Make all properties readonly
type ReadonlyUser = Readonly<User>

// Create getters
type UserGetters = {
  [K in keyof User as `get${Capitalize<string & K>}`]: () => User[K]
}
```

### Conditional Types for Type Extraction

```typescript
// Extract array element type
type ArrayElement<T> = T extends (infer E)[] ? E : T

type StringArray = ArrayElement<string[]>  // string
type SingleNumber = ArrayElement<number>   // number

// Unwrap Promise
type Awaited<T> = T extends Promise<infer R> ? R : T

type PromiseUser = Awaited<Promise<User>>  // User
type DirectString = Awaited<string>        // string
```

## Validation with Zod

```typescript
import { z } from 'zod'

// Define schema
const CreateUserSchema = z.object({
  name: z.string().min(1).max(100),
  email: z.string().email(),
  role: z.enum(['user', 'admin']).default('user'),
  age: z.number().min(0).max(150).optional()
})

// Infer type from schema
type CreateUserInput = z.infer<typeof CreateUserSchema>

// Parse and validate
function createUser(data: unknown): CreateUserInput {
  return CreateUserSchema.parse(data)  // Throws if invalid
}

// Safe parsing
const result = CreateUserSchema.safeParse(data)
if (result.success) {
  console.log(result.data)  // Typed as CreateUserInput
} else {
  console.error(result.error.issues)
}
```

## No Non-Null Assertions

### ❌ Bad Pattern

```typescript
const user = getUser()!
console.log(user.name)  // Crashes if null
```

### ✅ Good Pattern

```typescript
const user = getUser()

if (!user) {
  throw new Error('User not found')
}

console.log(user.name)  // Type-safe
```

### ✅ Better with Guards

```typescript
function ensureUser(user: User | null): User {
  if (!user) {
    throw new Error('User not found')
  }
  return user
}

const user = ensureUser(getUser())
console.log(user.name)  // Always defined
```

## Avoid Enums

### ❌ Bad: Enum (generates runtime code)

```typescript
enum Status {
  PENDING = 'pending',
  APPROVED = 'approved',
  REJECTED = 'rejected'
}

const status: Status = Status.PENDING
```

### ✅ Good: Union Type

```typescript
type Status = 'pending' | 'approved' | 'rejected'

const status: Status = 'pending'
```

### ✅ Better: Constants + Type

```typescript
const Status = {
  PENDING: 'pending',
  APPROVED: 'approved',
  REJECTED: 'rejected'
} as const

type Status = typeof Status[keyof typeof Status]

const status: Status = Status.PENDING
```

## Type Inference vs Annotation

### ❌ Over-Annotated

```typescript
const name: string = 'Alice'
const age: number = 30
const active: boolean = true
const items: string[] = ['a', 'b', 'c']
```

### ✅ Let TypeScript Infer

```typescript
const name = 'Alice'      // string
const age = 30            // number
const active = true       // boolean
const items = ['a', 'b']  // string[]
```

### ✅ Annotate Complex Types

```typescript
interface User {
  id: string
  name: string
}

// Inferred: User
const user = { id: '1', name: 'Alice' }

// Annotated: When needed
const config: Record<string, unknown> = loadConfig()
const callback: (e: Event) => void = handleClick
```

## Type-Only Imports

### ✅ Good

```typescript
import type { User, Role } from './types'
import { getUserById, createUser } from './api'

export type { User }
export { createUser }
```

### Properties on Type Imports

```typescript
// Multiple imports at once
import type { User, Role, Permission } from './types'

// From different modules
import type { User } from './users'
import type { Post } from './posts'

// With values
import { API_URL } from './config'
import type { Config } from './config'
```
