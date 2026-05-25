# Search Engine Submission Reference

## Overview

Once a sitemap is created, it must be submitted to search engines so they know about it. This reference covers all submission methods, monitoring, and incremental update strategies.

## Submission Methods

### Method 1: Web Interface

#### Google Search Console

1. Go to `https://search.google.com/search-console`
2. Add a property:
   - **Domain**: Requires DNS TXT record verification
   - **URL prefix**: Requires DNS TXT, HTML file upload, HTML meta tag, Google Analytics, or Google Tag Manager
3. Navigate to **Indexing → Sitemaps**
4. Enter the sitemap URL (e.g., `https://example.com/sitemap.xml`)
5. Click Submit

#### Property Verification Methods

| Method | How | Best For |
|---|---|---|
| DNS TXT Record | Add TXT record to DNS zone | Domain properties (covers all subdomains) |
| HTML File | Upload Google-provided file to site root | Quick setup |
| HTML Meta Tag | Add `<meta name="google-site-verification" content="...">` to `<head>` | When you can edit HTML but not DNS or filesystem |
| Google Analytics | Same account as GA4 property | Already have GA4 set up |
| Google Tag Manager | Same account as GTM container | Already have GTM set up |

#### Bing Webmaster Tools

1. Go to `https://www.bing.com/webmasters`
2. Add a site
3. Verify ownership (import from Google Search Console or use DNS/HTML meta tag)
4. Go to **Sitemaps** → enter sitemap URL → Submit

### Method 2: robots.txt Directive

Add a `Sitemap` line anywhere in `robots.txt`. This directive is independent of any specific `User-agent` and can appear multiple times.

```txt
User-agent: *
Disallow:

Sitemap: https://example.com/sitemap.xml
Sitemap: https://example.com/sitemap-products.xml
Sitemap: https://example.com/sitemap-articles.xml
```

**Rules:**
- The URL must be absolute (include protocol and full path)
- Multiple `Sitemap` directives are allowed
- Placement is arbitrary — not tied to any user-agent group
- Supported by Google, Bing, Yandex, DuckDuckGo, and other major search engines

### Method 3: HTTP Ping

Send an HTTP GET request to the search engine's ping endpoint. The sitemap URL must be URL-encoded.

#### Ping Endpoints

| Search Engine | Ping URL |
|---|---|
| Google | `https://www.google.com/ping?sitemap=<url_encoded_sitemap_url>` |
| Bing | `https://www.bing.com/ping?sitemap=<url_encoded_sitemap_url>` |

#### curl Examples

```bash
# Manual ping
curl "https://www.google.com/ping?sitemap=https%3A%2F%2Fexample.com%2Fsitemap.xml"
curl "https://www.bing.com/ping?sitemap=https%3A%2F%2Fexample.com%2Fsitemap.xml"

# With URL encoding
SITEMAP="https://example.com/sitemap.xml"
ENCODED=$(python3 -c "import urllib.parse; print(urllib.parse.quote('$SITEMAP'))")
curl -s "https://www.google.com/ping?sitemap=$ENCODED"
curl -s "https://www.bing.com/ping?sitemap=$ENCODED"
```

#### Automated Ping via Cron

```bash
#!/bin/bash
# /usr/local/bin/ping-searchengines.sh

SITEMAP_URL="${1:-https://example.com/sitemap.xml}"
ENCODED_URL=$(python3 -c "import urllib.parse; print(urllib.parse.quote('${SITEMAP_URL}'))")

echo "Pinging Google..."
curl -s -o /dev/null -w "%{http_code}" "https://www.google.com/ping?sitemap=${ENCODED_URL}"

echo "Pinging Bing..."
curl -s -o /dev/null -w "%{http_code}" "https://www.bing.com/ping?sitemap=${ENCODED_URL}"
```

**Crontab entry:**

```cron
# Every day at 6 AM
0 6 * * * /usr/local/bin/ping-searchengines.sh

# After sitemap regeneration
30 3 * * * /path/to/regenerate-sitemap.sh && /usr/local/bin/ping-searchengines.sh
```

#### Ping Response

HTTP `200 OK` means the sitemap was received. It does NOT mean the sitemap is valid or that URLs were added to the index. Search engines process the sitemap asynchronously.

### Automated Submission via CI/CD

**GitHub Actions:**

```yaml
# .github/workflows/submit-sitemap.yml
name: Submit Sitemap
on:
  schedule:
    - cron: "0 6 * * *"  # Daily at 6 AM

jobs:
  submit:
    runs-on: ubuntu-latest
    steps:
      - name: Ping Google
        run: |
          SITEMAP="https://example.com/sitemap.xml"
          ENCODED=$(python3 -c "import urllib.parse; print(urllib.parse.quote('$SITEMAP'))")
          curl -s "https://www.google.com/ping?sitemap=$ENCODED"
      - name: Ping Bing
        run: |
          SITEMAP="https://example.com/sitemap.xml"
          ENCODED=$(python3 -c "import urllib.parse; print(urllib.parse.quote('$SITEMAP'))")
          curl -s "https://www.bing.com/ping?sitemap=$ENCODED"
```

## Monitoring

### Google Search Console

After submission, monitor the following sections:

**Sitemaps (Indexing → Sitemaps):**
- Sitemap processing status (Success, Has errors, Couldn't fetch)
- Number of URLs discovered
- Number of URLs indexed
- Processing errors with details

**URL Inspection (Indexing → URL Inspection):**
- Test individual URLs against the live index
- See when a URL was last crawled
- Check if a URL is indexed and why (or why not)
- Request manual indexing

**Index Coverage (Indexing → Pages):**
- Total indexed pages
- Errors, valid with warnings, valid, excluded
- Reasons for exclusion (crawled but not indexed, redirect, not found, blocked by robots.txt, etc.)

**Crawl Stats (Settings → Crawl Stats):**
- Total crawl requests per day
- Total download size
- Average response time
- Crawl host status

**Enhancements (various sections):**
- Structured data errors, warnings, and valid items
- Mobile usability issues
- Core Web Vitals reports
- Sitelinks search box status

### Bing Webmaster Tools

Similar reporting:

- **Sitemaps**: Status, URLs submitted, URLs indexed
- **Index**: Pages indexed, crawl errors, blocked pages
- **SEO Reports**: Structured data, mobile usability
- **Crawl Control**: Crawl rate, crawl configuration

## Incremental Sitemap Strategy

### For Large Sites (Millions of URLs)

**Principle:** Separate frequently-changing URLs from stable content. Use `lastmod` in the sitemap index to signal which sitemaps have changed.

**Strategy:**

```mermaid
sitemap-index.xml
├── sitemap-products-daily.xml   ← Frequently updated products (lastmod: today)
├── sitemap-products-hourly.xml  ← Hot/trending products (lastmod: 1 hour ago)
├── sitemap-articles-daily.xml   ← Blog posts (lastmod: today)
├── sitemap-categories-weekly.xml ← Category pages (lastmod: this week)
├── sitemap-static-monthly.xml   ← About, Contact, FAQ (lastmod: this month)
└── sitemap-archives.xml        ← Archived content (lastmod: last year, rarely changes)
```

**Implementation Patterns:**

| Content Type | Sitemap | Update Frequency | Sitemap lastmod | Priority |
|---|---|---|---|---|
| Trending products | `sitemap-hot.xml` | Every hour | Current hour | 0.9 |
| Active products | `sitemap-products-1..N.xml` | Daily | Today | 0.8 |
| Blog articles | `sitemap-articles-1..N.xml` | Daily | Today | 0.7 |
| Categories | `sitemap-categories.xml` | Weekly | This week | 0.6 |
| Static pages | `sitemap-static.xml` | Monthly | This month | 0.5 |
| Archived | `sitemap-archive.xml` | Rarely | Static date | 0.3 |

**Incremental crawling benefit:** If only 2 of 10 sitemaps changed today, crawlers fetch those 2 instead of all 10. For a site with 10 sitemaps of 50k URLs each, this saves 400k URL fetches per day.

### Sitemap Regeneration Script

```python
#!/usr/bin/env python3
"""regenerate_sitemaps.py — Generate sitemaps with incremental strategy."""

import datetime
import os
import json
from xml.sax.saxutils import escape

SITEMAP_DIR = "public"
BASE_URL = "https://example.com"
MAX_URLS = 50000

def write_sitemap(filename: str, urls: list[dict]) -> str:
    """Write a sitemap XML file and return the path."""
    filepath = os.path.join(SITEMAP_DIR, filename)
    lines = ['<?xml version="1.0" encoding="UTF-8"?>']
    lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    for url in urls:
        lines.append("  <url>")
        lines.append(f"    <loc>{escape(url['loc'])}</loc>")
        if "lastmod" in url:
            lines.append(f"    <lastmod>{url['lastmod']}</lastmod>")
        if "changefreq" in url:
            lines.append(f"    <changefreq>{url['changefreq']}</changefreq>")
        if "priority" in url:
            lines.append(f"    <priority>{url['priority']}</priority>")
        lines.append("  </url>")
    lines.append("</urlset>")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return filepath


def generate_sitemap_index(sitemaps: list[dict]) -> str:
    """Generate sitemap index XML."""
    lines = ['<?xml version="1.0" encoding="UTF-8"?>']
    lines.append('<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    for sitemap in sitemaps:
        lines.append("  <sitemap>")
        lines.append(f"    <loc>{escape(sitemap['loc'])}</loc>")
        if "lastmod" in sitemap:
            lines.append(f"    <lastmod>{sitemap['lastmod']}</lastmod>")
        lines.append("  </sitemap>")
    lines.append("</sitemapindex>")
    index_path = os.path.join(SITEMAP_DIR, "sitemap.xml")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return index_path


def main():
    today = datetime.date.today().isoformat()
    now = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S+00:00")

    # Fetch data from API
    products = json.loads(os.popen("curl -s https://api.example.com/v1/products?limit=50000").read())
    articles = json.loads(os.popen("curl -s https://api.example.com/v1/articles?limit=50000").read())

    sitemap_entries = []

    # Products (split into multiple sitemaps if > 50k)
    product_chunks = [products[i:i + MAX_URLS] for i in range(0, len(products), MAX_URLS)]
    for i, chunk in enumerate(product_chunks, 1):
        urls = []
        for p in chunk:
            urls.append({
                "loc": f"{BASE_URL}/products/{p['slug']}",
                "lastmod": p.get("updated_at", today),
                "changefreq": "weekly",
                "priority": "0.8",
            })
        filename = f"sitemap-products-{i}.xml"
        write_sitemap(filename, urls)
        sitemap_entries.append({
            "loc": f"{BASE_URL}/{filename}",
            "lastmod": now,
        })

    # Articles
    article_chunks = [articles[i:i + MAX_URLS] for i in range(0, len(articles), MAX_URLS)]
    for i, chunk in enumerate(article_chunks, 1):
        urls = []
        for a in chunk:
            urls.append({
                "loc": f"{BASE_URL}/blog/{a['slug']}",
                "lastmod": a.get("published_at", today),
                "changefreq": "monthly",
                "priority": "0.7",
            })
        filename = f"sitemap-articles-{i}.xml"
        write_sitemap(filename, urls)
        sitemap_entries.append({
            "loc": f"{BASE_URL}/{filename}",
            "lastmod": now,
        })

    # Static pages
    static_urls = [
        {"loc": f"{BASE_URL}/", "lastmod": today, "changefreq": "daily", "priority": "1.0"},
        {"loc": f"{BASE_URL}/about", "lastmod": "2026-01-01", "changefreq": "monthly", "priority": "0.5"},
        {"loc": f"{BASE_URL}/contact", "lastmod": "2026-01-01", "changefreq": "monthly", "priority": "0.5"},
        {"loc": f"{BASE_URL}/faq", "lastmod": "2026-01-01", "changefreq": "monthly", "priority": "0.4"},
    ]
    write_sitemap("sitemap-static.xml", static_urls)
    sitemap_entries.insert(0, {"loc": f"{BASE_URL}/sitemap-static.xml", "lastmod": now})

    # Generate index
    generate_sitemap_index(sitemap_entries)
    print(f"Generated {len(sitemap_entries)} sitemaps + index")


if __name__ == "__main__":
    main()
```

## Crawler Notification Workflow Summary

1. **Generate** → Create or update sitemap files
2. **Upload** → Deploy to production (e.g., `public/` directory or static file server)
3. **Register** → Add `Sitemap:` directive to `robots.txt`
4. **Submit** → Google Search Console + Bing Webmaster Tools (web UI)
5. **Ping** → Automated HTTP pings (via cron or CI/CD)
6. **Monitor** → Crawl stats, index coverage, sitemap processing errors

## Troubleshooting

### Common Sitemap Submission Issues

| Issue | Likely Cause | Solution |
|---|---|---|
| "Couldn't fetch" | Sitemap URL inaccessible or returns non-200 status | Check server response, ensure file is at the correct path |
| "Has errors" | XML parsing error, invalid URL, encoding issue | Validate XML against schema, check entity escaping |
| "URLs not indexed" | Content quality, noindex tags, redirect chains | Check page-level noindex, ensure content is unique and valuable |
| "Redirect error" | Sitemap URL redirects to another URL | Ensure sitemap URL returns 200, not 301/302 |
| "Blocked by robots.txt" | Sitemap or listed URLs blocked | Check robots.txt for conflicting rules |

### Sitemap Discovery Issues

- **Verification**: Ensure property is verified in Search Console
- **Crawl**: Use URL Inspection tool to test a sitemap URL directly
- **Timeout**: Large sitemaps take time to process — check back in 24–48 hours
- **Robots.txt**: Ensure sitemap path is not blocked by `Disallow` rules
