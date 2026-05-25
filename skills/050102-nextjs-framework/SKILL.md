---
name: 050102-nextjs-framework
description: Next.js 16 framework patterns — async APIs, server components, React Compiler, routing conventions, caching strategy, metadata SEO, performance optimization, and anti-patterns checklist.
---

# Next.js 16 Framework

## Overview

Next.js 16 patterns covering async Request APIs, Server/Client Components, React Compiler, App Router conventions, caching with `'use cache'`, metadata and SEO, SWC compiler optimization, Server Actions, and common anti-patterns.

## Quick Reference

### Async APIs

All Request APIs must be awaited in Next.js 16: `params`, `searchParams`, `cookies()`, `headers()`, `draftMode()`.

### Rendering

Server Components by default. `'use client'` only for interactivity, pushed to leaf components.

### Caching

```typescript
'use cache'
cacheTag('products')
cacheLife({ expire: 3600 })
```

Invalidation: `revalidateTag()`, `updateTag()` (read-your-writes), `revalidatePath()`.

### Routing

App Router files: `layout.tsx`, `page.tsx`, `loading.tsx`, `error.tsx`, `not-found.tsx`, `proxy.ts` (replaces middleware.ts in Next.js 16).

### React Compiler

```typescript
// next.config.ts
experimental: { reactCompiler: true }
```

Auto-memoization, fine-grained reactivity. Turbopack is the default bundler.

### Server Actions

```typescript
'use server'
import { revalidateTag } from 'next/cache'

export async function updateAction(data) {
  await db.update(data)
  revalidateTag('products')
}
```

## References

- [Async APIs](references/async-apis.md) — Awaitable Request APIs pattern
- [Rendering Patterns](references/rendering-patterns.md) — Server vs Client Components
- [Caching Strategy](references/caching-strategy.md) — `'use cache'`, cacheTag, invalidation
- [Routing Conventions](references/routing-conventions.md) — App Router files, proxy.ts, slots
- [Performance Compiler](references/performance-compiler.md) — React Compiler + Turbopack
- [Metadata SEO](references/metadata-seo.md) — generateMetadata, OG images, JSON-LD
- [Anti-Patterns](references/anti-patterns.md) — 6 common Next.js 16 mistakes
- [Compiler Options](references/compiler-options.md) — SWC optimization, removeConsole, tree-shaking
- [Server Actions](references/server-actions.md) — Server Actions patterns, auth, redirects
- [Code Examples](references/code-examples.md) — Full working examples
- [Quick Reference](references/quick-reference.md) — Architecture overview card
