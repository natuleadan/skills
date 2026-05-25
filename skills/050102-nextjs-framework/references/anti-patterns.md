# Anti-Patterns

Common mistakes to avoid in Next.js 16.

## 1. Sync Request APIs

DON'T access without await:
```tsx
export function Page({ params }) {
  return <h1>{params.id}</h1>  // Error: params is a promise
}
```

DO always await:
```tsx
export async function Page(props) {
  const params = await props.params
  return <h1>{params.id}</h1>
}
```

## 2. Legacy Middleware

DON'T use `middleware.ts` for routing logic:
```tsx
// middleware.ts
```

DO use `proxy.ts` (Node.js runtime):
```tsx
// proxy.ts
```

## 3. Manual Memoization with Compiler

DON'T use useMemo/useCallback when Compiler is enabled:
```tsx
const memoized = useMemo(() => expensive(), [dep])
const callback = useCallback(() => {}, [dep])
```

DO let Compiler handle it:
```tsx
// Just write the code, Compiler optimizes
const result = expensive()
```

## 4. Missing Slot Defaults

DON'T leave parallel routes without default.tsx:
```
@modal/
└── page.tsx  // Missing default.tsx
```

DO always add default.tsx:
```
@modal/
├── default.tsx
└── page.tsx
```

## 5. Using `<a>` Instead of Link

DON'T use HTML anchor tag for navigation:
```tsx
<a href="/about">About</a>
```

DO use next/link:
```tsx
import Link from 'next/link'
<Link href="/about">About</Link>
```

## 6. Naked Database Calls

DON'T use direct database queries in components:
```tsx
const data = await db.query('SELECT * FROM table')
```

DO abstract in repository/service:
```tsx
const data = await productRepository.getAll()
```

## Rules Checklist

- [ ] **All Request APIs are awaited** — params, searchParams, cookies
- [ ] **Using proxy.ts, not middleware.ts**
- [ ] **No manual memo** — Compiler handles it
- [ ] **All slots have default.tsx**
- [ ] **Using Link, not `<a>`**
- [ ] **No naked API calls** — wrapped in services
- [ ] **'use cache' for caching** — not fetch cache directives
