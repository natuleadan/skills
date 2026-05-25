# Robots.txt Reference

## Robots Exclusion Standard

The Robots Exclusion Standard is a voluntary protocol that webmasters use to communicate with web crawlers. It is not a security mechanism.

## Syntax Format

A `robots.txt` file consists of one or more groups (defined by `User-agent` lines), followed by rules and directives.

### Directives

| Directive | Format | Description |
|---|---|---|
| `User-agent` | `User-agent: [name]` | Specifies the crawler this group applies to |
| `Disallow` | `Disallow: [path-prefix]` | Path crawlers must not access |
| `Allow` | `Allow: [path-prefix]` | Overrides Disallow for a more specific path |
| `Crawl-delay` | `Crawl-delay: [seconds]` | Seconds between consecutive requests |
| `Sitemap` | `Sitemap: [full-url]` | Location of a sitemap |

### Wildcard Patterns

| Pattern | Description |
|---|---|
| `*` | Matches any sequence of characters |
| `$` | Matches the end of the URL |

**Examples:**

```txt
# Block everything under /private/ with a query parameter
Disallow: /private/*?*

# Block any path ending in .pdf
Disallow: /*.pdf$

# Block all paths containing /tmp/ anywhere
Disallow: */tmp/
```

## Group Ordering

Crawlers select the most specific matching `User-agent` group. Groups are evaluated in order of specificity, not order in the file (though order is used as a tiebreaker for equally specific agents).

```txt
# Googlebot gets its own rules
User-agent: Googlebot
Disallow: /admin/

# All other crawlers get these rules
User-agent: *
Disallow: /private/
```

## Common Disallow Patterns

```txt
# Block admin/management areas
User-agent: *
Disallow: /admin/
Disallow: /wp-admin/
Disallow: /dashboard/
Disallow: /manage/

# Block API endpoints
User-agent: *
Disallow: /api/
Disallow: /graphql
Disallow: /rest/
Disallow: /v1/

# Block private/temporary areas
User-agent: *
Disallow: /private/
Disallow: /tmp/
Disallow: /draft/
Disallow: /staging/

# Block dynamic content that causes infinite crawl
Disallow: /search?*
Disallow: /tag/*?page=*
Disallow: */sort=
Disallow: */order=

# Block system paths
User-agent: *
Disallow: /_next/
Disallow: /_static/
Disallow: /includes/
Disallow: /vendor/

# Block file types (for some frameworks)
Disallow: /*.json$
Disallow: /*.env$

# Block specific files
Disallow: /sitemap.xml   # <-- Not recommended — sitemaps should be accessible!
Disallow: /robots.txt    # <-- Never block robots.txt itself
```

## Allow Exceptions

Use `Allow` to carve out exceptions from a broader `Disallow`:

```txt
User-agent: *
Disallow: /_next/
Allow: /_next/static/     # Allow static assets for rendering
Allow: /_next/static/css/ # Allow CSS for render-quality indexing
Allow: /_next/static/chunks/ # Allow JS for render-quality indexing
```

## Sitemap Directive

The `Sitemap` directive is independent of any `User-agent` group. It can appear anywhere in the file and multiple directives are allowed:

```txt
Sitemap: https://example.com/sitemap.xml
Sitemap: https://example.com/sitemap-news.xml
Sitemap: https://example.com/sitemap-images.xml
Sitemap: https://example.com/sitemap-video.xml
```

Each must be a full, absolute URL. The `Sitemap` directive is supported by Google, Bing, Yandex, and other major search engines.

## Complete Examples

### Allow All (No Restrictions)

```txt
User-agent: *
Disallow:
```

### Production Site

```txt
User-agent: *
Disallow: /admin/
Disallow: /api/
Disallow: /_next/
Allow: /_next/static/

Sitemap: https://example.com/sitemap.xml
```

### Block AI/LLM Crawlers

```txt
User-agent: GPTBot
Disallow: /

User-agent: ChatGPT-User
Disallow: /

User-agent: anthropic-ai
Disallow: /

User-agent: Google-Extended
Disallow: /
```

### Polite Crawling with Delay

```txt
User-agent: *
Disallow: /admin/
Disallow: /api/
Crawl-delay: 10
Sitemap: https://example.com/sitemap.xml
```

### Staging Environment (Block All)

```txt
User-agent: *
Disallow: /
```

## Testing

### Google Search Console Robots.txt Tester

1. Open Google Search Console
2. Select your property
3. Go to **Settings** → **Crawling** → **robots.txt Tester**
4. Paste or edit your robots.txt
5. Enter a URL to test against the rules
6. See which rule matches and whether access is allowed/blocked

## Security Considerations

### What Robots.txt Is NOT

- **Not a security mechanism** — it is a voluntary protocol. Malicious crawlers and scrapers ignore it completely.
- **Not a way to hide content** — paths listed in robots.txt are publicly visible to anyone who fetches the file. If you add a sensitive path, you are drawing attention to it.
- **Not an access control mechanism** — there is no authentication, no encryption, no guarantee of compliance.

### What Robots.txt IS

- A signal to **well-behaved** crawlers about which paths to skip during crawling
- A **crawl budget management** tool — helps crawlers focus on important content
- A **sitemap discovery** mechanism via the `Sitemap` directive

### Best Practice

Use authentication (password, IP whitelist, session tokens) to protect sensitive areas. Use `robots.txt` only for crawl optimization, not security.

## Framework Examples

### Next.js (`app/robots.ts`)

```typescript
import type { MetadataRoute } from "next"

export default function robots(): MetadataRoute.Robots {
  return {
    rules: [
      {
        userAgent: "*",
        allow: "/",
        disallow: ["/admin/", "/api/", "/_next/"],
      },
      {
        userAgent: "GPTBot",
        disallow: "/",
      },
    ],
    sitemap: [
      "https://example.com/sitemap.xml",
      "https://example.com/sitemap-products.xml",
    ],
  }
}
```

### Static HTML (`/robots.txt`)

```txt
User-agent: *
Disallow:

Sitemap: https://example.com/sitemap.xml
```

### Nginx Serving Custom robots.txt

```nginx
location = /robots.txt {
    alias /var/www/static/robots.txt;
}
```

### Apache Serving Custom robots.txt

```apache
<Files "robots.txt">
    Require all granted
</Files>
```

## File Format Rules

- **Location**: Always at the root: `https://example.com/robots.txt`
- **Encoding**: UTF-8
- **Line endings**: Unix (LF) or Windows (CRLF)
- **Blank lines**: Separate user-agent groups
- **Comments**: Lines starting with `#` are comments
- **Case**: Directives are case-insensitive (`user-agent`, `USER-AGENT`), but path values are case-sensitive
- **Size limit**: Max 500 KiB (Google ignores larger files)
