# Routing Conventions

App Router uses file-based routing with strict conventions.

## File Conventions

- **layout.tsx** — Wrapper, persistent across routes
- **page.tsx** — Route page content
- **loading.tsx** — Suspense fallback while loading
- **error.tsx** — Error boundary for route segment
- **not-found.tsx** — 404 custom page
- **proxy.ts** — Request interceptor (replaces middleware)
- **_folder/** — Private (excluded from routing)

## Proxy.ts (Modern Middleware)

`proxy.ts` runs at Node.js runtime (full access to Node APIs):

```tsx
// src/proxy.ts (at project root, same level as app/)
import { next } from 'next/server'

export function middleware(request: Request) {
  // Routing logic, auth checks, redirects
  return next(request)
}

export const config = {
  matcher: ['/((?!_next|static).*)']
}
```

## Parallel Routes (@slot)

Every `@slot` must have a `default.tsx`:

```
app/
├── layout.tsx
├── page.tsx
├── @sidebar/
│   ├── default.tsx
│   └── page.tsx
└── @modal/
    └── default.tsx
```

## Colocation

Use `_` prefix to exclude folders from routing:

```
app/
├── page.tsx
└── _components/
    ├── Header.tsx
    └── Footer.tsx
```

## Rules

- [ ] **Use App Router only** — Pages Router is legacy
- [ ] **Proxy.ts for routing logic** — not middleware.ts
- [ ] **All slots have default.tsx** — required for parallel routes
- [ ] **Colocate with _prefix** — keep logic near where it's used
- [ ] **No naked API calls** — wrap in actions or handlers
