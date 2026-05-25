---
name: 050102-nextjs-compiler
description: Next.js SWC compiler optimization options — removeConsole, optimizePackageImports, styled-components, relay, module transpilation, and build-time defines.
---

# Next.js Compiler Optimization

## Overview

Next.js uses the SWC compiler under the hood. Several configuration options in `next.config` can reduce bundle size and improve production performance.

## Common Optimizations

### removeConsole

Removes `console.*` calls from production builds.

```javascript
// next.config.js
const nextConfig = {
  compiler: {
    removeConsole: process.env.NODE_ENV === "production",
  },
}
```

- Keeps `console.error` and `console.warn` by default
- Reduces bundle size
- Should only run in production

### optimizePackageImports

Tree-shakes barrel imports from specific packages.

```javascript
compiler: {
  optimizePackageImports: [
    "@tabler/icons-react",
    "recharts",
    "date-fns",
    "lodash-es",
  ],
}
```

## Other Available Options

### Styled Components

```javascript
compiler: { styledComponents: true }
```

### Relay

```javascript
compiler: {
  relay: {
    src: "./src",
    artifactDirectory: "./src/__generated__",
    language: "typescript",
  },
}
```

### React Remove Properties

```javascript
compiler: { reactRemoveProperties: true }

// With custom regex
compiler: {
  reactRemoveProperties: { properties: ["^data-testid$"] },
}
```

### Module Transpilation

```javascript
transpilePackages: ["@acme/ui", "some-esm-package"]
```

### Build-time Variables (Define)

```javascript
compiler: {
  define: {
    "process.env.BUILD_TIME": JSON.stringify(new Date().toISOString()),
  },
}
```

## Optimization Checklist

- [ ] `removeConsole` active only in production
- [ ] `optimizePackageImports` for heavy icon/utility libraries
- [ ] `output: "standalone"` for Docker/server deployments
- [ ] React Remove Properties for test-only attributes
- [ ] Transpile ESM-only packages if needed

## Quick Reference

```bash
# Check current config
cat next.config.{js,mjs}

# Build with optimizations
npm run build

# Analyze bundle
ANALYZE=true npm run build
```
