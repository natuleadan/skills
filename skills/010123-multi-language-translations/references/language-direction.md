# Direction from Language Table

## Pattern

The `sys_languages` table stores text direction per language:

```typescript
const languages = pgTable("sys_languages", {
  code: text().primaryKey(),
  name: text().notNull(),
  direction: text().notNull().default("ltr"), // "ltr" | "rtl"
  isActive: boolean("isActive").default(false),
  isDefault: boolean("isDefault").default(false),
})

// Seed data
{ code: "en", name: "English",  direction: "ltr" }
{ code: "es", name: "Español",  direction: "ltr" }
{ code: "ar", name: "العربية",  direction: "rtl" }
{ code: "he", name: "עברית",    direction: "rtl" }
```

## Provider chain

```typescript
// Server: [lang]/layout.tsx
const lang = await params.lang
const langData = await db.query.languages.findFirst({
  where: eq(languages.code, lang)
})
const direction = langData?.direction ?? "ltr"

return (
  <LangProvider lang={lang} direction={direction}>
    <DirectionProvider direction={direction}>
      <div dir={direction}>
        {children}
      </div>
    </DirectionProvider>
  </LangProvider>
)
```

## Client hook

```typescript
function useLangDirection(): "ltr" | "rtl" {
  const context = useContext(LangContext)
  return context?.direction || "ltr"
}
```

CSS logical properties (`margin-inline-start`, `padding-inline-end`) automatically respect the `dir` attribute — no need for separate LTR/RTL stylesheets.
