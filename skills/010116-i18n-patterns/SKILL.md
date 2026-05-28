---
name: 010116-i18n-patterns
description: Internationalization — translation tables, RTL support, safe translations, LangProvider, locale detection, SEO hreflang, and language config.
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
| Per-entity translation table pattern (product_translations, etc.) | [references/per-entity-translations.md](references/per-entity-translations.md) |
| Translation assembler pattern (fetch all, filter in-memory) | [references/assembler-pattern.md](references/assembler-pattern.md) |
| Server-side locale detection in proxy.ts | [references/server-locale-detection.md](references/server-locale-detection.md) |
| SEO hreflang alternates for multi-language sites | [references/seo-hreflang.md](references/seo-hreflang.md) |
