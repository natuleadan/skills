# Next.js 16+ Reference

## Environment Requirements

- **Node.js:** 22.0.0+ or 20.11.0+ (18 deprecated)
- **TypeScript:** 5.7.0+
- **React:** 19.2+

## Build & Config

- **Bundler:** Turbopack (default, stable)
- **React Compiler:** Enable in next.config.ts
- **Caching:** `cacheComponents: true`

## Request APIs

All are async (must await):
- `params` — route parameters
- `searchParams` — query string
- `cookies()` — request cookies
- `headers()` — request headers
- `draftMode()` — preview mode

## Rendering

| Type | Best For | Async |
|------|----------|-------|
| Server Component | Data fetching, secrets | Yes |
| Client Component | State, hooks, interactivity | No |
| Suspense | Streaming, progressive rendering | N/A |

## Caching

- **'use cache'** — mark function as cacheable
- **cacheTag()** — add invalidation tags
- **cacheLife()** — set TTL
- **revalidateTag()** — SWR invalidation
- **updateTag()** — immediate refresh
- **unstable_cache()** — for non-fetch queries

## Routing Files

| File | Purpose |
|------|---------|
| layout.tsx | Wrapper |
| page.tsx | Route content |
| loading.tsx | Suspense fallback |
| error.tsx | Error boundary |
| not-found.tsx | 404 page |
| proxy.ts | Request interceptor |
| @slot/ | Parallel route |
| _folder/ | Private (non-routable) |

## Key Patterns

- **Default to Server Components** — add 'use client' only when needed
- **Await all Request APIs** — params, cookies, headers, searchParams
- **Use proxy.ts** — not middleware.ts
- **Enable React Compiler** — automatic memoization
- **Tag-based caching** — for invalidation control
- **Parallel routes** — @slot with default.tsx required
