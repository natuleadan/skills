# Metadata & Open Graph Reference

## Title Tag

The HTML `<title>` element is the most important on-page SEO factor.

### Best Practices

| Aspect | Guideline |
|---|---|
| Length | 50–60 characters |
| Position | Primary keywords first |
| Brand | Include brand name, ideally at the end |
| Uniqueness | Every page must have a unique title |

### Examples

**Good titles:**
```html
<title>Technical SEO Guide — Best Practices | Example</title>
<title>Buy Organic Coffee Beans Online | Example Store</title>
<title>About Us | Example Inc.</title>
```

**Bad titles:**
```html
<title>Home</title>
<title>Product 1 | Product 2 | Product 3 | Example Store</title>
<title></title>
```

## Meta Description

The meta description is the snippet shown below the title in search results.

### Best Practices

| Aspect | Guideline |
|---|---|
| Length | 150–160 characters |
| Content | Compelling summary with keywords naturally integrated |
| CTA | End with a call to action |
| Uniqueness | Every page needs a unique description |

### Examples

```html
<meta name="description" content="Master technical SEO with our comprehensive guide covering sitemaps, robots.txt, structured data, and performance optimization. Includes code examples and best practices." />
```

## Open Graph Protocol

Open Graph enables rich social sharing previews. Defined in `<meta property="og:*" content="...">` tags.

### Core Properties

| Property | Description | Required | Example |
|---|---|---|---|
| `og:title` | Title of the content | Yes | `"Technical SEO Guide"` |
| `og:description` | 1–2 sentence description | Recommended | `"Master technical SEO..."` |
| `og:image` | Preview image URL | Yes | `"https://example.com/og.jpg"` |
| `og:url` | Canonical URL | Yes | `"https://example.com/guide"` |
| `og:type` | Content type | Yes | `"article"`, `"website"`, `"product"` |
| `og:site_name` | Site name | Recommended | `"Example"` |
| `og:locale` | Locale | Recommended | `"en_US"` |

### Image Guidelines

- **Recommended size**: 1200 × 630 pixels (1.9:1 aspect ratio)
- **Min size**: 200 × 200 pixels
- **Max size**: 5 MB
- **Format**: PNG or JPEG
- **Content**: Should be distinct and representative of the page

### Complete Example

```html
<meta property="og:title" content="Technical SEO Guide — Best Practices" />
<meta property="og:description" content="Master technical SEO with our comprehensive guide covering sitemaps, robots.txt, structured data, and more." />
<meta property="og:image" content="https://example.com/images/og-seo-guide.jpg" />
<meta property="og:url" content="https://example.com/guides/seo" />
<meta property="og:type" content="article" />
<meta property="og:site_name" content="Example" />
<meta property="og:locale" content="en_US" />
```

### Additional OG Properties

```html
<!-- Article-specific -->
<meta property="article:published_time" content="2026-01-15T10:00:00Z" />
<meta property="article:modified_time" content="2026-05-25T14:30:00Z" />
<meta property="article:author" content="https://example.com/authors/john-doe" />
<meta property="article:section" content="Technology" />
<meta property="article:tag" content="SEO" />
<meta property="article:tag" content="Web Development" />

<!-- Product-specific -->
<meta property="product:price:amount" content="29.99" />
<meta property="product:price:currency" content="USD" />
<meta property="product:availability" content="in stock" />

<!-- Video-specific -->
<meta property="og:video" content="https://example.com/video.mp4" />
<meta property="og:video:width" content="1920" />
<meta property="og:video:height" content="1080" />
<meta property="og:video:type" content="video/mp4" />
```

## Twitter Cards

Twitter Cards control how content appears when shared on Twitter/X.

### Card Types

| Card Type | Description |
|---|---|
| `summary` | Title, description, small thumbnail image |
| `summary_large_image` | Title, description, large prominent image |
| `app` | Deep link to a mobile app |
| `player` | Video/audio player experience |

### Properties

| Property | Description | Example |
|---|---|---|
| `twitter:card` | Card type | `"summary_large_image"` |
| `twitter:site` | Site Twitter account | `"@example"` |
| `twitter:creator` | Author Twitter account | `"@author"` |
| `twitter:title` | Card title (≤ 70 chars) | `"Technical SEO Guide"` |
| `twitter:description` | Card description (≤ 200 chars) | `"Master technical SEO..."` |
| `twitter:image` | Image URL | `"https://example.com/og.jpg"` |
| `twitter:image:alt` | Image alt text | `"SEO Guide cover image"` |

### Complete Example

```html
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:site" content="@example" />
<meta name="twitter:creator" content="@author" />
<meta name="twitter:title" content="Technical SEO Guide — Best Practices" />
<meta name="twitter:description" content="Master technical SEO with our comprehensive guide." />
<meta name="twitter:image" content="https://example.com/images/twitter-card.jpg" />
<meta name="twitter:image:alt" content="Technical SEO Guide cover image" />
```

## Canonical URLs

The `rel="canonical"` tag tells search engines which URL is the preferred version when duplicate or similar content exists.

### Syntax

```html
<link rel="canonical" href="https://example.com/preferred-url" />
```

### Best Practices

**Self-referencing canonicals** — every page links to itself:

```html
<link rel="canonical" href="https://example.com/current-page" />
```

**Cross-domain canonicals** — for syndicated content:

```html
<!-- On syndicated copy at https://other-site.com/article -->
<link rel="canonical" href="https://example.com/original-article" />
```

**Handle URL parameters** — canonical to the clean URL:

```html
<!-- Page: https://example.com/products?sort=price&page=2 -->
<link rel="canonical" href="https://example.com/products" />

<!-- With pagination, canonical to the specific page -->
<link rel="canonical" href="https://example.com/products?page=2" />
```

### Rules

- Use **absolute** URLs, not relative
- Only **one** canonical per page
- Canonical target must be indexable (no noindex)
- Cross-domain canonicals are valid (indicates original source)
- HTTP → HTTPS canonicals are valid (preferred for migration)

## Hreflang Tags

For international or multilingual sites, hreflang tells search engines which language/region version to serve.

### Syntax

```html
<link rel="alternate" hreflang="en" href="https://example.com/en/page" />
<link rel="alternate" hreflang="es" href="https://example.com/es/pagina" />
<link rel="alternate" hreflang="fr" href="https://example.com/fr/page" />
<link rel="alternate" hreflang="x-default" href="https://example.com/en/page" />
```

### Language Codes

- ISO 639-1 language code (e.g., `en`, `es`, `fr`, `de`, `ja`)
- Optional ISO 3166-1 alpha-2 region code (e.g., `en-US`, `en-GB`, `pt-BR`, `pt-PT`)

### Rules

- Each language variant must link back to ALL other variants
- Include `x-default` for the fallback (no language match)
- Use in `<head>`, HTTP headers, or sitemaps

### Complete Example

```html
<link rel="alternate" hreflang="en-US" href="https://example.com/" />
<link rel="alternate" hreflang="en-GB" href="https://example.com/uk/" />
<link rel="alternate" hreflang="es" href="https://example.com/es/" />
<link rel="alternate" hreflang="fr" href="https://example.com/fr/" />
<link rel="alternate" hreflang="de" href="https://example.com/de/" />
<link rel="alternate" hreflang="x-default" href="https://example.com/" />
```

Hreflang can also be specified in sitemaps:

```xml
<url>
  <loc>https://example.com/</loc>
  <xhtml:link rel="alternate" hreflang="es" href="https://example.com/es/" />
  <xhtml:link rel="alternate" hreflang="fr" href="https://example.com/fr/" />
  <xhtml:link rel="alternate" hreflang="x-default" href="https://example.com/" />
</url>
```

## Meta Robots Tags

Control how search engines index individual pages.

### Values

| Value | Description |
|---|---|
| `index` | Allow indexing (default) |
| `noindex` | Prevent indexing |
| `follow` | Follow links on this page (default) |
| `nofollow` | Do not follow links on this page |
| `noarchive` | Do not show cached version in SERPs |
| `nosnippet` | Do not show snippet/preview in SERPs |
| `notranslate` | Do not offer translation |
| `noimageindex` | Do not index images on this page |
| `unavailable_after: [date]` | Remove from index after date |
| `max-snippet: [num]` | Max characters for snippet |
| `max-image-preview: [size]` | Max size for image preview |
| `max-video-preview: [num]` | Max seconds for video preview |

### Page-Level Example

```html
<meta name="robots" content="noindex, nofollow" />
<meta name="googlebot" content="noindex, nofollow, noarchive" />
<meta name="bingbot" content="noindex, nofollow" />
```

### Site-Wide via X-Robots-Tag Header

**Nginx:**

```nginx
add_header X-Robots-Tag "noindex, nofollow";
```

**Apache:**

```apache
Header set X-Robots-Tag "noindex, nofollow"
```

**Elysia/Bun:**

```typescript
app.onBeforeHandle(({ set }) => {
  set.headers["X-Robots-Tag"] = "noindex, nofollow"
})
```

**Next.js middleware (`proxy.ts`):**

```typescript
export function middleware(request: NextRequest) {
  const response = NextResponse.next()
  if (request.nextUrl.pathname.startsWith("/admin")) {
    response.headers.set("X-Robots-Tag", "noindex, nofollow")
  }
  return response
}
```

## Other Meta Tags

### Viewport

```html
<meta name="viewport" content="width=device-width, initial-scale=1" />
```

### Theme Color

```html
<meta name="theme-color" content="#ff0000" />
```

### Referrer

```html
<meta name="referrer" content="strict-origin-when-cross-origin" />
```

### Format Detection

```html
<meta name="format-detection" content="telephone=no" />
```

## Framework Examples

### Next.js Layout Metadata API

```typescript
// app/layout.tsx
import type { Metadata } from "next"

export const metadata: Metadata = {
  title: {
    default: "Example",
    template: "%s | Example",
  },
  description: "Example website description for search engines.",
  openGraph: {
    title: "Example",
    description: "Example website description for social sharing.",
    url: "https://example.com",
    siteName: "Example",
    images: [
      {
        url: "https://example.com/og.png",
        width: 1200,
        height: 630,
        alt: "Example",
      },
    ],
    locale: "en_US",
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    site: "@example",
    creator: "@author",
    images: ["https://example.com/og.png"],
  },
  robots: {
    index: true,
    follow: true,
    nocache: false,
  },
  alternates: {
    canonical: "https://example.com",
    languages: {
      "en-US": "https://example.com/",
      "es": "https://example.com/es/",
    },
  },
}
```

### Next.js Per-Page Metadata

```typescript
// app/products/[slug]/page.tsx
import type { Metadata } from "next"
import { getProduct } from "@/lib/products"

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const product = await getProduct(params.slug)

  return {
    title: product.name,
    description: product.description,
    openGraph: {
      title: product.name,
      description: product.description,
      images: [{ url: product.image, width: 1200, height: 630 }],
    },
    alternates: {
      canonical: `https://example.com/products/${product.slug}`,
    },
  }
}
```

### Static HTML Template

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />

  <!-- Standard SEO -->
  <title>Technical SEO Guide — Best Practices | Example</title>
  <meta name="description" content="Master technical SEO with our comprehensive guide covering sitemaps, robots.txt, structured data, and more." />
  <link rel="canonical" href="https://example.com/guides/seo" />

  <!-- Open Graph -->
  <meta property="og:title" content="Technical SEO Guide — Best Practices" />
  <meta property="og:description" content="Master technical SEO with our comprehensive guide." />
  <meta property="og:image" content="https://example.com/og.jpg" />
  <meta property="og:url" content="https://example.com/guides/seo" />
  <meta property="og:type" content="article" />
  <meta property="og:site_name" content="Example" />

  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:site" content="@example" />
  <meta name="twitter:creator" content="@author" />
  <meta name="twitter:image" content="https://example.com/twitter-card.jpg" />

  <!-- Robots -->
  <meta name="robots" content="index, follow, max-image-preview:large" />

  <!-- Hreflang -->
  <link rel="alternate" hreflang="en" href="https://example.com/guides/seo" />
  <link rel="alternate" hreflang="es" href="https://example.com/es/guias/seo" />
  <link rel="alternate" hreflang="x-default" href="https://example.com/guides/seo" />
</head>
<body>
  <!-- Page content -->
</body>
</html>
```
