# i18n Patterns Lesson

Language is determined server-side and propagated to clients. RTL languages (Arabic, Hebrew) are handled automatically.

## Safe Translation Access

**Never** access translations with dot notation directly in JSX:

```tsx
// ❌ WRONG
return <span>{translations["key.with.dots"]}</span>
```

**Always** use a helper or hook:

```tsx
// ✅ RIGHT
const { getT } = useSafeTranslation(translations)
return <span>{getT("key.with.dots")}</span>
```

## Language Source

- **Server-side** — middleware or database determines language
- **Database** → `set_languages.direction` is source of truth for RTL support
- **Propagation** → LangProvider in layout.tsx sends lang to all client components
- **Client** → `useLangContext()` reads language (no URL parsing)

## RTL Support (Arabic, Hebrew)

- **Automatic detection** — LangService checks if language is RTL
- **Direction attribute** → `dir="rtl"` applied to HTML/layouts
- **Styling** — Tailwind and component styles respect RTL automatically
- **ARIA text** — always in English unless translation key exists
- **Database enum** — check `set_languages` table for language direction metadata

## Rules

- [ ] **Safe Prop Lifting** — extract translations to constants before JSX
- [ ] **Fallback handling** — i18n always returns a string (never undefined)
- [ ] **ARIA in English** — unless specific translation key for accessibility text
- [ ] **RTL opt-in** — no magic; only activate when language direction is RTL
