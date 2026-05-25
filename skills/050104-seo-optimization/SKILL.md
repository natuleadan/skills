---
name: 050104-seo-optimization
description: "Technical SEO optimization: XML Sitemaps protocol, robots.txt, metadata, Open Graph, canonical URLs, structured data (JSON-LD), search engine submission."
---

# SEO Optimization

Technical SEO covers how search engines discover, crawl, and index content. This skill provides the protocol-level knowledge and implementation patterns needed to make any web application search-engine friendly.

## References

| Topic | File |
|---|---|
| Complete XML Sitemaps protocol, validation, cross-submission | [references/sitemaps-protocol.md](references/sitemaps-protocol.md) |
| robots.txt syntax, patterns, security | [references/robots-txt.md](references/robots-txt.md) |
| HTML meta, Open Graph, Twitter Cards, canonical, hreflang | [references/metadata-og.md](references/metadata-og.md) |
| JSON-LD structured data (Organization, WebSite, Article, Product, BreadcrumbList, FAQPage, etc.) | [references/structured-data.md](references/structured-data.md) |
| Search engine submission, ping, monitoring, incremental strategy | [references/search-submission.md](references/search-submission.md) |

## Quick Start

```bash
# Generate a sitemap.xml from known routes
# Place at root: http://example.com/sitemap.xml

# Notify Google
curl "https://www.google.com/ping?sitemap=http://example.com/sitemap.xml"

# Verify in robots.txt (at root: /robots.txt)
echo "Sitemap: http://example.com/sitemap.xml" >> robots.txt
```

## When to Use

- Setting up sitemap.xml for a new site
- Implementing robots.txt to guide crawlers
- Adding structured data for rich results
- Configuring Open Graph for social sharing
- Auditing SEO for existing sites
- Diagnosing crawling/indexing issues
