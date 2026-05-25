# XML Sitemaps Protocol Reference

## Overview

The XML Sitemap protocol provides a standardized format for listing URLs on a website so search engines can discover and crawl them efficiently.

## Namespace

```
http://www.sitemaps.org/schemas/sitemap/0.9
```

## XML Examples

### Basic Sitemap — Single URL with All Optional Tags

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://example.com/</loc>
    <lastmod>2026-05-25</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>
</urlset>
```

### Multi-URL Sitemap with Entity Escaping

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://example.com/</loc>
    <lastmod>2026-05-25</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>https://example.com/products?category=books&amp;sort=price</loc>
    <lastmod>2026-05-24</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>https://example.com/search?q=John&amp;apos;s+guide</loc>
    <changefreq>monthly</changefreq>
    <priority>0.3</priority>
  </url>
</urlset>
```

### Sitemap Index File

```xml
<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <sitemap>
    <loc>https://example.com/sitemap-products.xml</loc>
    <lastmod>2026-05-25T12:00:00+00:00</lastmod>
  </sitemap>
  <sitemap>
    <loc>https://example.com/sitemap-articles.xml</loc>
    <lastmod>2026-05-24T18:30:00+00:00</lastmod>
  </sitemap>
  <sitemap>
    <loc>https://example.com/sitemap-static.xml</loc>
    <lastmod>2026-05-01T00:00:00+00:00</lastmod>
  </sitemap>
</sitemapindex>
```

### Schema Validation-Ready Sitemap

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset
  xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9
                      http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">
  <url>
    <loc>https://example.com/</loc>
    <lastmod>2026-05-25</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>https://example.com/about</loc>
    <lastmod>2026-05-20</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.5</priority>
  </url>
</urlset>
```

### Schema Validation-Ready Sitemap Index

```xml
<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex
  xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9
                      http://www.sitemaps.org/schemas/sitemap/0.9/siteindex.xsd">
  <sitemap>
    <loc>https://example.com/sitemap1.xml</loc>
    <lastmod>2026-05-25T12:00:00+00:00</lastmod>
  </sitemap>
  <sitemap>
    <loc>https://example.com/sitemap2.xml</loc>
    <lastmod>2026-05-24T00:00:00+00:00</lastmod>
  </sitemap>
</sitemapindex>
```

### Namespace Extension Example

Custom namespaces add additional metadata to sitemap entries:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset
  xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
  xmlns:image="http://www.google.com/schemas/sitemap-image/1.1"
  xmlns:video="http://www.google.com/schemas/sitemap-video/1.1">
  <url>
    <loc>https://example.com/product</loc>
    <image:image>
      <image:loc>https://example.com/product-image.jpg</image:loc>
      <image:title>Product Image Title</image:title>
    </image:image>
    <video:video>
      <video:content_loc>https://example.com/product-video.mp4</video:content_loc>
      <video:title>Product Video</video:title>
    </video:video>
  </url>
</urlset>
```

### Text File Format

```
https://example.com/
https://example.com/about
https://example.com/products
https://example.com/contact
https://example.com/blog
```

### RSS Feed as Sitemap

```xml
<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"
  xmlns:content="http://purl.org/rss/1.0/modules/content/"
  xmlns:wfw="http://wellformedweb.org/CommentAPI/"
  xmlns:dc="http://purl.org/dc/elements/1.1/">
  <channel>
    <title>Example Blog</title>
    <link>https://example.com/</link>
    <description>Latest articles from Example</description>
    <item>
      <title>SEO Optimization Guide</title>
      <link>https://example.com/blog/seo-guide</link>
      <pubDate>Mon, 25 May 2026 12:00:00 GMT</pubDate>
      <description>A comprehensive SEO guide.</description>
    </item>
    <item>
      <title>Web Performance Tips</title>
      <link>https://example.com/blog/performance</link>
      <pubDate>Fri, 22 May 2026 10:30:00 GMT</pubDate>
      <description>Tips for faster web performance.</description>
    </item>
  </channel>
</rss>
```

### Atom Feed as Sitemap

```xml
<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <title>Example Blog</title>
  <link href="https://example.com/"/>
  <updated>2026-05-25T12:00:00Z</updated>
  <entry>
    <title>SEO Optimization Guide</title>
    <link href="https://example.com/blog/seo-guide"/>
    <updated>2026-05-25T12:00:00Z</updated>
    <summary>A comprehensive SEO guide.</summary>
  </entry>
  <entry>
    <title>Web Performance Tips</title>
    <link href="https://example.com/blog/performance"/>
    <updated>2026-05-22T10:30:00Z</updated>
    <summary>Tips for faster web performance.</summary>
  </entry>
</feed>
```

## Entity Escaping

### XML Entity Escape Reference

| Character | Escape Code | Meaning |
|---|---|---|
| `&` | `&amp;` | Ampersand |
| `'` | `&apos;` | Apostrophe |
| `"` | `&quot;` | Quotation mark |
| `>` | `&gt;` | Greater than |
| `<` | `&lt;` | Less than |

### Python Entity Escaping Script

```python
#!/usr/bin/env python3
"""Escape URLs for sitemap XML."""

from xml.sax.saxutils import escape

def escape_url(url: str) -> str:
    """Apply XML entity escaping to a URL string."""
    return escape(url, {"'": "&apos;", "\"": "&quot;"})

# Example URLs with characters that need escaping
urls = [
    "https://example.com/search?q=John's+bar&sort=asc",
    "https://example.com/path?name=foo>bar&value=baz<qux",
    "https://example.com/?q=a&b=c\"d'e",
]

escaped = [escape_url(u) for u in urls]
for original, esc in zip(urls, escaped):
    print(f"Original: {original}")
    print(f"Escaped:  {esc}")
    print()
```

Output:

```
Original: https://example.com/search?q=John's+bar&sort=asc
Escaped:  https://example.com/search?q=John&apos;s+bar&amp;sort=asc

Original: https://example.com/path?name=foo>bar&value=baz<qux
Escaped:  https://example.com/path?name=foo&gt;bar&amp;value=baz&lt;qux

Original: https://example.com/?q=a&b=c"d'e
Escaped:  https://example.com/?q=a&amp;b=c&quot;d&apos;e
```

## URL Encoding Examples

### Three-Layer Encoding Chain

URLs in sitemaps go through three encoding layers:

**Layer 1 — Character Encoding (binary):**
Non-ASCII characters must be encoded to a byte sequence. ISO-8859-1 encodes each character as one byte. UTF-8 uses one to four bytes per character.

**Layer 2 — URL Percent-Encoding (RFC 3986):**
Special characters and non-ASCII bytes are percent-encoded as `%XX`.

**Layer 3 — XML Entity Escaping:**
The five XML special characters (&, ', ", <, >) are entity-escaped.

**Example with special characters:**

Original URL with special characters:
```
https://example.com/path?query=value&name=John's page
```

Step 1 — UTF-8 byte encoding (for non-ASCII, if any):
```
(Same ASCII bytes for this example)
```

Step 2 — URL percent-encoding:
```
https://example.com/path?query=value&name=John%27s%20page
```

Step 3 — XML entity escaping:
```
https://example.com/path?query=value&amp;name=John%27s%20page
```

**ISO-8859-1 vs UTF-8 example:**

URL with the character `ñ` (U+00F1):

ISO-8859-1: `%F1`
UTF-8: `%C3%B1`

```
ISO-8859-1: https://example.com/ma%F1ana
UTF-8:      https://example.com/ma%C3%B1ana
```

W3C Datetime format with timezone for lastmod:

```
2026-05-25
2026-05-25T14:30:00Z
2026-05-25T14:30:00+00:00
2026-05-25T14:30:00-05:00
```

## Cross-Submission Example

To submit sitemaps from one domain for URLs on another domain, use the `Sitemap` directive in `robots.txt` on the target domain pointing to the submitting domain.

**robots.txt on `https://cdn.example.com`:**

```txt
User-agent: *
Disallow:

Sitemap: https://www.example.com/sitemap-cdn.xml
```

**robots.txt on `https://images.example.com`:**

```txt
User-agent: *
Allow: /

Sitemap: https://www.example.com/sitemap-images.xml
```

This proves ownership of the target domains because only the domain owner can modify `robots.txt`.

## Tag Definitions

| Tag | Required | Description |
|---|---|---|
| `urlset` | Yes | Root element wrapping all URLs |
| `sitemapindex` | Yes | Root element wrapping sitemap references |
| `url` | Yes | Parent element for a single URL entry |
| `sitemap` | Yes | Parent element for a single sitemap reference |
| `loc` | Yes | Full URL (protocol + host + path) |
| `lastmod` | No | W3C Datetime of last modification |
| `changefreq` | No | Hint for change frequency |
| `priority` | No | Relative priority (0.0–1.0) |

## File Size Limits

| Item | Limit |
|---|---|
| URLs per sitemap | 50,000 |
| Uncompressed file size | 50 MB (52,428,800 bytes) |
| Sitemaps per index | 50,000 |
| Index file size | 50 MB |
| `loc` length | 2,048 characters |

## Location Rules

- Place at the **root directory** for widest coverage: `https://example.com/sitemap.xml`
- A sitemap under a subdirectory can only list URLs in that subdirectory:
  - `https://example.com/blog/sitemap.xml` can only list URLs starting with `https://example.com/blog/`
- All URLs in a sitemap must share the **same host** and **same protocol** (http vs https)
- If the site uses a non-standard port, all URLs must include that port
- Gzip compression is recommended (`sitemap.xml.gz`)
