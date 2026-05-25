# Next.js Compiler Options Reference

## Standard Options

| Option | Type | Purpose |
|--------|------|---------|
| `removeConsole` | `boolean \| object` | Strip `console.*` in production |
| `optimizePackageImports` | `string[]` | Tree-shake barrel imports |
| `styledComponents` | `boolean` | Enable SWC-based styled-components |
| `relay` | `object` | Relay compiler configuration |
| `reactRemoveProperties` | `boolean \| object` | Remove `data-*` attributes |
| `define` | `object` | Build-time variable injection |

## Detailed Configuration

### removeConsole

```javascript
// Remove all console.*
compiler: { removeConsole: true }

// Remove all except error/warn
compiler: { removeConsole: true }
// (this is the default behavior)

// Explicitly keep specific methods
compiler: {
  removeConsole: {
    exclude: ["error", "warn", "info"],
  },
}
```

### optimizePackageImports

Executed at the SWC level — tree-shakes imports so only used exports are bundled.

Works best with:
- Icon libraries (`@tabler/icons-react`, `lucide-react`)
- Utility libraries (`date-fns`, `lodash-es`)
- Chart libraries (`recharts`, `chart.js`)

### Define

Injects values at compile time, similar to `@babel/plugin-transform-define`:

```javascript
compiler: {
  define: {
    "process.env.API_VERSION": JSON.stringify("v2"),
    "process.env.BUILD_DATE": JSON.stringify(new Date().toISOString()),
    __CUSTOM_FLAG__: "true",
  },
}
```

## Best Practices

1. Enable `removeConsole` only in production (use env var check)
2. List only packages with heavy barrel exports in `optimizePackageImports`
3. Use `reactRemoveProperties` for `data-testid` removal in production builds
4. Prefer `output: "standalone"` for Docker deployment
5. Combine with `compression: true` in production

## Full Example

```javascript
const nextConfig = {
  output: "standalone",
  compiler: {
    removeConsole: process.env.NODE_ENV === "production",
    optimizePackageImports: ["@tabler/icons-react", "recharts", "date-fns"],
    reactRemoveProperties: process.env.NODE_ENV === "production",
  },
  transpilePackages: [],
}

export default nextConfig
```
