# SEO hreflang Alternates

## Pattern

Generate `<link rel="alternate" hreflang="{lang}">` tags for all supported languages.

```typescript
export function getAlternateLanguages(
  currentLang: string,
  path: string,
  availableLanguages: string[],
  baseUrl: string,
): Record<string, string> {
  const alternates: Record<string, string> = {}
  const cleanPath = path.startsWith("/") ? path : `/${path}`

  for (const lang of availableLanguages) {
    alternates[lang] = `${baseUrl}/${lang}${cleanPath}`
  }

  // x-default points to the default language
  const defaultLang = currentLang || availableLanguages[0]
  alternates["x-default"] = `${baseUrl}/${defaultLang}${cleanPath}`

  return alternates
}
```

## Usage in Next.js metadata

```typescript
export async function generateMetadata({ params }): Promise<Metadata> {
  const { lang } = await params
  const languages = await getAvailableLanguages()

  return {
    alternates: {
      languages: getAlternateLanguages(lang, "/products", languages, baseUrl),
      canonical: `${baseUrl}/${lang}/products`,
    },
  }
}
```

## SEO locale map

For proper locale formatting (e.g., `en-US`, `es-ES`):

```typescript
const SEO_LOCALE_MAP: Record<string, string> = {
  en: "en-US", es: "es-ES", ar: "ar-SA",
  fr: "fr-FR", de: "de-DE", pt: "pt-BR",
}
```

Use the full locale code (with country) in hreflang tags for better SEO targeting.
