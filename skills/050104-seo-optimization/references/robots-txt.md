# Robots.txt Reference (RFC 9309)

## Robots Exclusion Protocol

The Robots Exclusion Protocol (RFC 9309) is a voluntary standard that service owners use to communicate with automated clients known as crawlers. Crawlers are expected to honor the rules defined in a file named `robots.txt`. These rules are not a form of access authorization.

## Protocol Definition

A robots.txt file consists of groups and rules:

- **Rule**: A line with a key-value pair that defines if a crawler may access a URI path.
- **Group**: One or more `User-agent` lines followed by one or more rules. A group is terminated by another `User-agent` line or end of file. The last group may have no rules, which implicitly allows everything.

### Formal Syntax (ABNF)

Simplified grammar based on RFC 9309:

```
robotstxt     = *(group / emptyline)
group         = startgroupline *(startgroupline / emptyline) *(rule / emptyline)
startgroupline = "user-agent" ":" product-token
rule          = ("allow" / "disallow") ":" path-pattern
product-token = identifier / "*"
path-pattern  = "/" *UTF8-char
identifier    = 1*( "-" / %x41-5A / "_" / %x61-7A )
```

## User-Agent Line

Crawlers identify themselves via a product token sent in the User-Agent header (for HTTP). The product token MUST contain only letters, underscores, and hyphens. Crawlers use case-insensitive matching to find the group that matches their product token.

### Group Merging

If multiple groups match the same product token, their rules MUST be merged into one:

```txt
# Two groups that match ExampleBot
user-agent: ExampleBot
disallow: /foo
disallow: /bar

user-agent: ExampleBot
disallow: /baz

# Merged into:
# user-agent: ExampleBot
# disallow: /foo
# disallow: /bar
# disallow: /baz
```

### Wildcard Fallback

If no matching group exists, crawlers MUST obey the group with `User-agent: *`, if present. If no group matches and there is no `*` group, no rules apply.

```txt
# ExampleBot has no explicit group — falls back to *
User-agent: *
Disallow: /private/

User-agent: BazBot
Disallow: /baz/
```

## Allow and Disallow Lines

### Matching Algorithm

1. Match paths in `allow` and `disallow` rules against the URI.
2. Matching SHOULD be case-sensitive.
3. The **most specific match** wins (the match with the most octets).
4. If an `allow` rule and a `disallow` rule are equivalent, `allow` SHOULD be used.
5. If no match is found or there are no rules, the URI is allowed.
6. The `/robots.txt` URI is implicitly allowed.

### Percent-Encoding

Octets outside the ASCII range and reserved URI characters MUST be percent-encoded before comparison. When comparing, percent-encoded unreserved characters SHOULD be unencoded first:

| Path in robots.txt | Encoded Path | Path to Match |
|---|---|---|
| `/foo/bar?baz=quz` | `/foo/bar?baz=quz` | `/foo/bar?baz=quz` |
| `/foo/bar/ツ` | `/foo/bar/%E3%83%84` | `/foo/bar/%E3%83%84` |
| `/foo/bar/%62%61%7A` | `/foo/bar/%62%61%7A` | `/foo/bar/baz` |

Rules that are not in any group (before the first `User-agent` line) SHOULD be ignored.

## Special Characters

| Character | Description | Example |
|---|---|---|
| `#` | Designates a line comment | `allow: / # comment` |
| `$` | Designates the end of the match pattern | `allow: /this/path/exactly$` |
| `*` | Designates 0 or more instances of any character | `allow: /this/*/exactly` |

To match literal `*` or `$` in a URI, use percent-encoding:

```txt
# Match literal * in path
Disallow: /path/file-with-a-%2A.html

# Match literal $ in path
Disallow: /path/foo-%24
```

## Other Records

Crawlers MAY interpret other records (e.g., `Sitemap`, `Crawl-delay`). These records MUST NOT interfere with the parsing of `User-agent`, `Allow`, and `Disallow` lines. For example, a `Sitemap` record MUST NOT terminate a group.

## Access Method

The rules MUST be accessible at `/robots.txt` (all lowercase) in the top-level path:

```
scheme:[//authority]/robots.txt
```

Examples:
- `https://www.example.com/robots.txt`
- `ftp://ftp.example.com/robots.txt`

The file MUST be UTF-8 encoded with media type `text/plain`.

## Access Results

### Successful Access

If the crawler successfully downloads the file, it MUST follow the parseable rules.

### Redirects

Crawlers SHOULD follow at least five consecutive redirects, even across authorities (e.g., different hosts). If reached within five redirects, rules apply to the initial authority. Beyond five, crawlers MAY assume the file is unavailable.

### Unavailable (4xx)

If the server responds with a 4xx status (e.g., 404, 403), the file is unavailable. Crawlers MAY access any resources on the server.

### Unreachable (5xx/Network Errors)

If the file is unreachable due to server or network errors (5xx status or connection failure), crawlers MUST assume complete disallow. After approximately 30 days, crawlers MAY treat it as unavailable or continue using a cached copy.

### Parsing Errors

Crawlers MUST try to parse each line individually. Any parseable lines MUST be followed. Unparseable lines are ignored.

## Caching

Crawlers MAY cache the fetched robots.txt contents. Standard cache control (RFC 9111) applies. Crawlers SHOULD NOT use a cached version for more than 24 hours, unless the file is unreachable.

## Limits

Crawlers SHOULD impose a parsing limit of at least 500 KiB to protect their systems. Files larger than this may be truncated for parsing.

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
Disallow: /sitemap.xml   # Not recommended — sitemaps should be accessible!
Disallow: /robots.txt    # Never block robots.txt itself
```

## Allow Exceptions

Use `Allow` to carve out exceptions from a broader `Disallow`:

```txt
User-agent: *
Disallow: /_next/
Allow: /_next/static/
Allow: /_next/static/css/
Allow: /_next/static/chunks/
```

## Sitemap Directive

The `Sitemap` directive is independent of any `User-agent` group. It can appear anywhere in the file:

```txt
Sitemap: https://example.com/sitemap.xml
Sitemap: https://example.com/sitemap-news.xml
```

Each must be a full, absolute URL.

## RFC 9309 Examples

### Simple Example (Multiple Crawlers)

```txt
User-Agent: *
Disallow: *.gif$
Disallow: /example/
Allow: /publications/

User-Agent: foobot
Disallow:/
Allow:/example/page.html
Allow:/example/allowed.gif

User-Agent: barbot
User-Agent: bazbot
Disallow: /example/page.html

User-Agent: quxbot
```

- `*`: Allows `/publications/`, blocks `/example/` and `.gif` files.
- `foobot`: Only allows two specific paths.
- `barbot` and `bazbot`: Share rules blocking one path.
- `quxbot`: Empty group — unrestricted access.

### Longest Match

```txt
User-Agent: foobot
Allow: /example/page/
Disallow: /example/page/disallowed.gif
```

For URI `/example/page/disallowed.gif`, `Disallow: /example/page/disallowed.gif` is longer and wins.

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
6. See which rule matches and whether access is allowed or blocked

## Security Considerations

### What Robots.txt Is NOT

- **Not a security mechanism** — it is a voluntary protocol. Malicious crawlers and scrapers ignore it completely.
- **Not a way to hide content** — paths listed in robots.txt are publicly visible to anyone who fetches the file. Listing a path draws attention to it.
- **Not an access control mechanism** — no authentication, no encryption, no compliance guarantee.

### What Robots.txt IS

- A signal to well-behaved crawlers about which paths to skip during crawling.
- A **crawl budget management** tool — helps crawlers focus on important content.
- A **sitemap discovery** mechanism via the `Sitemap` directive.

### Parser Hardening

Implementors should consider:

- **Memory management**: The 500 KiB parsing limit protects against out-of-memory scenarios.
- **Invalid characters**: Reject out-of-bounds characters to limit attack vectors.
- **Untrusted content**: Treat robots.txt content as untrusted per the application layer specification.

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

### Static File (`/robots.txt`)

```txt
User-agent: *
Disallow:

Sitemap: https://example.com/sitemap.xml
```

### Nginx

```nginx
location = /robots.txt {
    alias /var/www/static/robots.txt;
}
```

### Apache

```apache
<Files "robots.txt">
    Require all granted
</Files>
```

## File Format Rules

- **Location**: Always at root: `https://example.com/robots.txt`
- **Encoding**: UTF-8, media type `text/plain`
- **Line endings**: Unix (LF) or Windows (CRLF)
- **Blank lines**: Separate user-agent groups
- **Comments**: Lines starting with `#` are comments
- **Case**: Directives are case-insensitive (`user-agent`, `USER-AGENT`); paths are case-sensitive
- **Parsing limit**: Crawlers MUST support at least 500 KiB
- **Caching**: Crawlers SHOULD NOT cache for more than 24 hours
