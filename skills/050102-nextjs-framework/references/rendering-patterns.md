# Rendering Patterns

Server Components are the default. Only use Client Components when necessary.

## Server Components (Default)

- Run only on server
- Access databases, APIs, secrets directly
- No state, hooks, or event listeners
- Streamed to client automatically
- Optimal for data fetching

```tsx
// Server Component (no 'use client')
export default async function ProductList() {
  const products = await db.products.findAll()
  return (
    <ul>
      {products.map(p => <li key={p.id}>{p.name}</li>)}
    </ul>
  )
}
```

## Client Components ('use client')

- Mark with `'use client'` directive
- Run in browser
- Use hooks, state, effects
- Keep at leaf nodes (as deep as possible)
- Receive data from Server Components as props

```tsx
// Client Component pushed down the tree
'use client'

export function ProductFilter({ products }) {
  const [filtered, setFiltered] = useState(products)
  return <input onChange={() => /* filter */} />
}
```

## React 19 & Compiler

- **Compiler enabled** → automatic memoization (no manual useMemo/useCallback)
- **Suspense boundaries** → stream parts of page as ready
- **Use transitions** → non-blocking state updates

## Rules

- [ ] **Default to Server** — only add 'use client' when needed
- [ ] **Push 'use client' down** — keep as close to leaves as possible
- [ ] **No manual memo** — React Compiler handles memoization
- [ ] **Async by default** — Server Components are async
