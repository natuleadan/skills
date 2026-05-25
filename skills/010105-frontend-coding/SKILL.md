---
name: 010105-frontend-coding
description: React best practices, web accessibility (ARIA, keyboard nav, semantic HTML), and frontend performance (N+1, lazy loading, memoization, caching).
license: MIT
---

# Frontend Coding Standards

## Overview

Best practices for React, accessibility, and performance in web applications.

## Quick Reference

### React

- Prefer Server Components by default; use `"use client"` only for interactivity
- Hooks at top level only (no conditions/loops)
- List keys must be stable unique IDs, not array index
- Client Components should be leaf-level only (push interactivity down)

### Accessibility

- Use semantic HTML (`<button>`, `<nav>`, `<main>`) over `<div>` with ARIA
- `aria-label` for icon-only controls, `aria-hidden="true"` for decorative elements
- Keyboard navigation: `tabIndex`, `onKeyDown` handlers
- Color is never the only indicator (add text or icons)

### Performance

- Avoid N+1 queries: batch with joins or `Promise.all`
- Lazy load via dynamic imports and image lazyloading
- Memoize expensive computations with `useMemo` or cache maps
- Use pagination or virtualized lists for large datasets

## References

- [React Patterns](references/react-patterns.md)
- [Accessibility](references/accessibility.md)
- [Performance](references/performance.md)
