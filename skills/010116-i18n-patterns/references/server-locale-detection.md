# Server-Side Locale Detection (proxy.ts)

## Architecture

Uses Next.js 16 `proxy.ts` (replaces `middleware.ts`) to detect the user's language from the URL or `Accept-Language` header, then redirects to `/{lang}/...`.

## Detection pipeline

```
1. URL path first segment → /es/products → "es"
2. Not found → Accept-Language header → parse + match
3. Not found → cookie (NEXT_LOCALE or similar)
4. Not found → default locale
```

## Implementation (no external library)

```typescript
// proxy.ts
const SUPPORTED_LOCALES = ["en", "es", "ar"]
const DEFAULT_LOCALE = "en"

export async function proxy(request: NextRequest) {
  const { pathname } = request.nextUrl
  if (isStaticRoute(pathname)) return

  const firstSegment = pathname.split("/").filter(Boolean)[0]

  // Skip if already localized
  if (SUPPORTED_LOCALES.includes(firstSegment)) return

  // Detect locale
  const locale = await detectLocale(request)

  // Redirect
  const url = request.nextUrl.clone()
  url.pathname = `/${locale}${pathname}`
  const response = NextResponse.redirect(url)
  response.cookies.set("NEXT_LOCALE", locale, {
    maxAge: 31536000, path: "/", sameSite: "lax"
  })
  return response
}

function detectLocale(request: NextRequest): string {
  // 1. Cookie
  const cookie = request.cookies.get("NEXT_LOCALE")?.value
  if (cookie && SUPPORTED_LOCALES.includes(cookie)) return cookie

  // 2. Accept-Language (no Negotiator)
  const accept = request.headers.get("accept-language") || ""
  const lang = accept.split(",")[0]?.split("-")[0]?.toLowerCase()
  if (lang && SUPPORTED_LOCALES.includes(lang)) return lang

  // 3. Default
  return DEFAULT_LOCALE
}
```

## Module-level cache (for DB-backed languages)

```typescript
let _langCache: { codes: string[]; exp: number } | null = null
const CACHE_TTL = 5 * 60 * 1000

async function getCachedLanguages(): Promise<string[]> {
  if (_langCache && _langCache.exp > Date.now()) return _langCache.codes
  const langs = await db.query.languages.findMany({ where: eq(languages.isActive, true) })
  _langCache = { codes: langs.map(l => l.code), exp: Date.now() + CACHE_TTL }
  return _langCache.codes
}
```
