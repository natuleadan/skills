---
name: 010116-i18n-patterns
description: Internationalization patterns — RTL support, safe translation access, language propagation, LangProvider, and database-driven language configuration.
license: MIT
---

# Internationalization (i18n)

## Overview

Patterns for building multilingual applications with RTL support, safe translation rendering, and server-side language detection.

## Quick Reference

### Language Detection
- Language determined server-side (middleware or database)
- Propagated to clients via `LangProvider` in layout
- Database `languages.direction` is source of truth for RTL

### Safe Translation
```typescript
const { getT } = useSafeTranslation(translations);
return <h1>{getT('page.title')}</h1>;
```

### RTL Support
- Automatic detection via `LangService`
- `dir="rtl"` on HTML element
- Tailwind respects RTL direction
- ARIA text in English unless translation key exists

## References

| Topic | File |
|---|---|
| RTL support, safe translations, LangProvider, language tables | [references/i18n-patterns.md](references/i18n-patterns.md) |
| CSS logical properties, DirectionProvider, icon rotation, RTL pitfalls | [references/rtl-css-patterns.md](references/rtl-css-patterns.md) |
