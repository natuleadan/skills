# Proxy Locale Detection (Next.js 16)

## Pattern

Use `proxy.ts` (replaces `middleware.ts` in Next.js 16) to detect the user's locale from URL, header, or cookie, then redirect to `/{locale}/...`.

## File: `src/proxy.ts`

```typescript
import { type NextRequest, NextResponse } from "next/server"

const SUPPORTED = ["en", "es", "ar"] as const
const DEFAULT = "en"

function isStatic(path: string) {
  return (
    path.startsWith("/_next") ||
    path.startsWith("/api") ||
    /\.(jpg|png|svg|ico|webp|woff2?)$/i.test(path)
  )
}

export async function proxy(request: NextRequest) {
  const { pathname } = request.nextUrl
  if (isStatic(pathname)) return

  const segs = pathname.split("/").filter(Boolean)
  const first = segs[0]

  // Already localized
  if (SUPPORTED.includes(first as any)) return

  // Detect locale
  const cookie = request.cookies.get("NEXT_LOCALE")?.value
  const accept = request.headers.get("accept-language")?.split(",")[0]?.split("-")[0]
  const locale =
    SUPPORTED.find(l => l === cookie) ??
    SUPPORTED.find(l => l === accept) ??
    DEFAULT

  // Redirect
  const url = request.nextUrl.clone()
  url.pathname = `/${locale}${pathname}`
  const res = NextResponse.redirect(url)
  res.cookies.set("NEXT_LOCALE", locale, {
    maxAge: 31536000, path: "/", sameSite: "lax",
  })
  return res
}
```

## Route groups

Use route groups to separate public from admin:

```
src/app/
├── [lang]/           ← public pages (with locale)
│   ├── layout.tsx    ← LangProvider, direction, header/footer
│   ├── store/
│   └── ...
├── (dashboard)/      ← admin pages (no locale)
│   └── admin/
│       └── ...
```

## Layout pattern

```typescript
// [lang]/layout.tsx
export default async function LangLayout({
  children, params,
}: { children: React.ReactNode; params: Promise<{ lang: string }> }) {
  const { lang } = await params

  return (
    <LangProvider lang={lang} dir={getDir(lang)}>
      <div dir={getDir(lang)}>
        {children}
      </div>
    </LangProvider>
  )
}
```
