---
name: 050107-server-actions
description: Next.js Server Actions patterns — form handling, auth validation, typed returns, redirects, error handling, and client component usage.
---

# Server Actions

## Definition

Server Actions are functions that run on the server but can be called from the client. They are the entry point for mutations in a Next.js application.

## Basic Pattern

```typescript
// actions/submit.ts
"use server"
import { redirect } from "next/navigation"

export async function submitAction(formData: FormData) {
  const name = formData.get("name") as string
  const email = formData.get("email") as string

  // Validate
  if (!name || !email) {
    return { error: "Name and email are required" }
  }

  // Process
  await saveToDatabase({ name, email })

  // Redirect on success
  redirect("/success")
}
```

## With Auth Validation

```typescript
"use server"
import { auth } from "@/lib/auth"
import { headers } from "next/headers"

export async function protectedAction(formData: FormData) {
  const hdrs = await headers()
  const session = await auth.api.getSession({ headers: hdrs })

  if (!session) {
    return { error: "Unauthorized" }
  }

  // Proceed with authenticated user
  const { user } = session
  // ...
}
```

## Client Component Usage

```tsx
"use client"
import { submitAction } from "@/actions/submit"

export function MyForm() {
  return (
    <form action={submitAction}>
      <input name="name" required />
      <input name="email" type="email" required />
      <button type="submit">Submit</button>
    </form>
  )
}
```

## Error Handling Pattern

```typescript
"use server"

export async function safeAction(data: FormData) {
  try {
    const result = await processData(data)
    return { success: true, data: result }
  } catch (error) {
    console.error("Action failed:", error)
    return { error: "Failed to process request" }
  }
}
```

## Rules Checklist

- [ ] Add `"use server"` directive at top of action file
- [ ] Export async function
- [ ] Validate input before processing
- [ ] Return typed objects with success/error
- [ ] Use `redirect()` for navigation after success
- [ ] Validate auth before sensitive operations
- [ ] NEVER trust client-provided role/auth data

## Quick Reference

```typescript
// Form action
<form action={myAction}>
  <input name="field" />
</form>

// Programmatic call
const result = await myAction(new FormData(formElement))

// With button formAction
<button formAction={otherAction}>Submit</button>
```
