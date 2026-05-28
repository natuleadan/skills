# Slug Resolution Per Locale

## Pattern

Each language has its own slug namespace. `UNIQUE(slug, language_code)` allows the same slug in different languages.

```typescript
async function resolveSlug(slug: string, lang: string): Promise<Product | null> {
  const translation = await db.query.productTranslations.findFirst({
    where: and(
      eq(productTranslations.slug, slug),
      eq(productTranslations.languageCode, lang)
    ),
    with: { product: true }
  })
  return translation?.product ?? null
}
```

## Cross-language slug redirect

When a user visits a slug in the wrong language:

```typescript
async function resolveWithFallback(slug: string, lang: string) {
  // Try requested language first
  const product = await resolveSlug(slug, lang)
  if (product) return { product, locale: lang }

  // Fall through to other languages
  for (const alt of availableLanguages) {
    if (alt === lang) continue
    const found = await resolveSlug(slug, alt)
    if (found) {
      redirect(`/${alt}/${slug}`) // redirect to the language that has this slug
    }
  }

  notFound()
}
```

## Language switcher with slug mapping

```typescript
async function switchLanguage(currentSlug: string, fromLang: string, toLang: string) {
  const translation = await db.query.productTranslations.findFirst({
    where: and(
      eq(productTranslations.slug, currentSlug),
      eq(productTranslations.languageCode, fromLang)
    ),
    with: {
      product: {
        with: {
          translations: {
            where: eq(productTranslations.languageCode, toLang)
          }
        }
      }
    }
  })

  const targetSlug = translation?.product?.translations?.[0]?.slug
  return targetSlug ?? currentSlug // fallback to same slug
}
```
