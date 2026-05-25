# Performance & Compiler

React Compiler and Turbopack provide automatic optimizations.

## React Compiler

Enable in `next.config.ts`:

```js
const config = {
  experimental: {
    reactCompiler: true
  }
}
```

**Benefits:**
- Automatic memoization (no useMemo/useCallback needed)
- Fine-grained reactivity
- Reduced boilerplate

## Turbopack

Default bundler (v16). Faster than Webpack:

- **`next dev`** uses Turbopack by default
- **`next build`** uses Turbopack by default
- **`--webpack` flag** — fallback to Webpack if needed

Benefits:
- <100ms HMR (Hot Module Reload)
- Instant startup
- Lazy compilation

## Code Splitting

- **Dynamic imports** — `React.lazy` / `dynamic()`
- **Route-based** — automatic per page
- **Component-based** — manual with dynamic()

```tsx
import dynamic from 'next/dynamic'

const HeavyComponent = dynamic(() => import('./Heavy'), {
  loading: () => <div>Loading...</div>
})

export default function Page() {
  return <HeavyComponent />
}
```

## Bundle Analysis

```bash
ANALYZE=true npm run build
```

## Rules

- [ ] **Enable reactCompiler** — in next.config.ts
- [ ] **No manual memoization** — Compiler handles it
- [ ] **Use dynamic() for large components** — lazy load when safe
- [ ] **Keep bundle lean** — monitor with ANALYZE
- [ ] **Test with Turbopack** — report webpack-only issues
