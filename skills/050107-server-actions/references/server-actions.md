# Server Actions Reference

## Common Patterns

### Form Action

```typescript
"use server"

export async function createItem(formData: FormData) {
  const title = formData.get("title") as string
  const price = Number(formData.get("price"))

  // Validate
  if (!title || price <= 0) {
    return { error: "Invalid input" }
  }

  // Process
  const item = await db.insert({ title, price })

  // Revalidate cache
  revalidatePath("/items")

  // Return result (don't redirect if form is on same page)
  return { success: true, id: item.id }
}
```

### Server Action with useActionState

```tsx
"use client"
import { useActionState } from "react"
import { createItem } from "@/actions/items"

export function CreateItemForm() {
  const [state, formAction, pending] = useActionState(createItem, null)

  return (
    <form action={formAction}>
      <input name="title" required />
      <input name="price" type="number" required />
      <button disabled={pending}>
        {pending ? "Saving..." : "Create"}
      </button>
      {state?.error && <p className="error">{state.error}</p>}
    </form>
  )
}
```

### Typed Return

Always return a consistent shape:

```typescript
type ActionResult<T = void> =
  | { success: true; data: T }
  | { success: false; error: string }

export async function action(): Promise<ActionResult<{ id: string }>> {
  // ...
}
```

### Revalidation

```typescript
import { revalidatePath, revalidateTag } from "next/cache"

// Revalidate a specific page
revalidatePath("/dashboard")

// Revalidate by tag
revalidateTag("products")
```

## Security

| Rule | Rationale |
|------|-----------|
| Validate auth at action start | Prevents unauthorized access |
| Never trust client-provided roles | Client can be tampered |
| Validate all input | Prevents injection |
| Use redirects, not client navigation | Ensures URL consistency |
| Return errors, don't throw | Better UX handling |

## Best Practices

1. One action file per domain (`actions/products.ts`, `actions/users.ts`)
2. Keep actions thin — delegate to services
3. Always handle errors, never let them bubble to client
4. Use `revalidatePath`/`revalidateTag` instead of full page reloads
5. Prefer `useActionState` over manual `startTransition`
