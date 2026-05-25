# Async APIs

Next.js 16 requires `await` for all Request APIs.

## APIs That Must Be Awaited

- `params` — route parameters
- `searchParams` — query strings
- `cookies()` — request cookies
- `headers()` — request headers
- `draftMode()` — draft mode status

## Pattern

```tsx
// WRONG
export async function Page({ params }) {
  const id = params.id  // Error in v16
}

// RIGHT
export async function Page(props) {
  const params = await props.params
  const id = params.id
}
```

## Usage in Metadata, Sitemaps, Icons

- `generateMetadata` receives props with `params`, `searchParams` as promises
- `sitemap()`, `opengraph-image.tsx` must await `params`
- `icon.tsx` must await `params` for dynamic icons

## Rules

- [ ] **Always await** params, searchParams, cookies, headers
- [ ] **In generateMetadata** — both params and searchParams are promises
- [ ] **In dynamic routes** — params.id, params.slug must be awaited
- [ ] **Type safety** — use TypeScript to catch missed awaits at build time
