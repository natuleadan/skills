# Agent Content Negotiation

How web servers can serve optimized content to AI agents and automated crawlers via content negotiation, markdown conversion, and signal-based permission frameworks.

## Content Negotiation for AI Agents

Content negotiation (RFC 9110) allows clients and servers to agree on the best representation of a resource. AI agents can request markdown instead of HTML by sending the `Accept: text/markdown` header:

```bash
curl https://example.com/page \
  -H "Accept: text/markdown"
```

When the server supports this, it returns `content-type: text/markdown` with the page converted to markdown. This reduces token waste for AI processing by stripping navigation, headers, footers, scripts, and styles.

```typescript
const r = await fetch("https://example.com/page", {
  headers: { Accept: "text/markdown" },
})
const tokenCount = r.headers.get("x-markdown-tokens")
const markdown = await r.text()
```

### x-markdown-tokens Header

Responses converted to markdown may include an `x-markdown-tokens` header estimating the token count of the markdown document. Use this to:

- Calculate context window size before processing
- Decide on chunking strategy
- Estimate cost for LLM API calls

## Content Signals Framework

Content Signals is a framework for expressing preferences about how content may be used after access. Servers can include a `Content-Signal` header:

```
Content-Signal: ai-train=yes, search=yes, ai-input=yes
```

| Signal | Description |
|---|---|
| `ai-train` | Whether content may be used for AI/ML training |
| `search` | Whether content may be used for search indexing |
| `ai-input` | Whether content may be used as AI input (including agentic use) |

Each signal is a key-value pair with values `yes` or `no`. Clients consuming content should check this header before using the content for any listed purpose.

### Relationship to robots.txt

Content Signals operates at the HTTP response level (per-page), while robots.txt operates at the crawl level (directory-wide). Both should be used together:

- `robots.txt`: Controls which paths crawlers may access
- `Content-Signal`: Controls how accessed content may be used
- `meta robots` tags: Controls indexing per page

## LLMs.txt Pattern

The `llms.txt` pattern provides a documentation index file for AI agents, similar to how `sitemap.xml` helps search engines discover content. A website can expose an `llms.txt` file at its root containing links to all available documentation pages:

```
https://example.com/llms.txt
```

This file acts as a table of contents for AI agents, listing available pages organized by category. Agents fetch this file first to discover what content is available before exploring further.

### Relationship to sitemaps

| Aspect | sitemap.xml | llms.txt |
|---|---|---|
| Audience | Search engines | AI agents |
| Format | XML | Plain text / Markdown |
| Detail | URLs + metadata | URLs + descriptions + hierarchy |
| Priority | Required for indexing | Optional for discovery |

Both can coexist. Use sitemaps for search engine crawling and llms.txt for AI agent content discovery.

## Cloudflare Markdown for Agents

Cloudflare's network supports real-time HTML-to-markdown conversion at the edge for enabled zones. When an AI system requests a page with `Accept: text/markdown`, Cloudflare intercepts the request, fetches the original HTML from the origin, converts it to markdown, and serves the markdown response.

### Output Format

The markdown response follows a consistent structure:

1. **YAML frontmatter** (optional) — extracted from `<meta>` tags:

```yaml
---
title: Page Title
description: A short summary of the page.
image: https://example.com/cover.png
---
```

| Frontmatter field | Source `<meta>` tag | Fallback |
|---|---|---|
| `title` | `<meta name="title">` | `<meta property="og:title">` |
| `description` | `<meta name="description">` | `<meta property="og:description">` |
| `image` | — | `<meta property="og:image">` |

Only fields with values are emitted. If no supported meta tags exist, frontmatter is omitted.

2. **Body markdown** — converted from the document body. Non-content elements (headers, footers, navigation, scripts, styles) are stripped during pre-processing.

3. **JSON-LD** (optional) — preserved as a fenced `json` code block at the end:

```markdown
... main content ...

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Article Title"
}
```
```

### How to Enable

#### Dashboard

1. Log in to Cloudflare dashboard → your zone → **AI Crawl Control**
2. Enable **Markdown for Agents**

Requires Pro or Business plan. Available at no additional cost for Pro, Business, Enterprise, and SSL for SaaS customers.

#### API

```bash
curl -X PATCH 'https://api.cloudflare.com/client/v4/zones/{zone_tag}/settings/content_converter' \
  -H 'Content-Type: application/json' \
  -H "Authorization: Bearer {api_token}" \
  --data-raw '{"value": "on"}'
```

#### Configuration Rules (subdomain/path-specific)

```bash
curl --request PUT \
  --url "https://api.cloudflare.com/client/v4/zones/{zone_id}/rulesets/phases/http_config_settings/entrypoint" \
  --header "Authorization: Bearer {api_token}" \
  --header "Content-Type: application/json" \
  --data '{
    "rules": [{
      "expression": "http.host eq \"docs.example.com\"",
      "action": "set_config",
      "action_parameters": {
        "content_converter": true
      },
      "description": "Enable for docs subdomain"
    }]
  }'
```

Expression can use `http.host` for subdomains or `starts_with(http.request.uri.path, "/blog/")` for paths.

#### Custom Hostnames (SaaS)

Enable for specific custom hostnames via custom metadata:

```bash
curl --request PATCH \
  --url "https://api.cloudflare.com/client/v4/zones/{zone_id}/custom_hostnames/{custom_hostname_id}" \
  --header "Authorization: Bearer {api_token}" \
  --header "Content-Type: application/json" \
  --data '{
    "custom_metadata": {
      "content_converter": "enabled"
    }
  }'
```

Then create a configuration rule matching the metadata:

```bash
curl --request PUT \
  --url "https://api.cloudflare.com/client/v4/zones/{zone_id}/rulesets/phases/http_config_settings/entrypoint" \
  --header "Authorization: Bearer {api_token}" \
  --header "Content-Type: application/json" \
  --data '{
    "rules": [{
      "expression": "lookup_json_string(cf.hostname.metadata, \"content_converter\") eq \"enabled\"",
      "action": "set_config",
      "action_parameters": {
        "content_converter": true
      },
      "description": "Enable for opted-in custom hostnames"
    }]
  }'
```

### Limitations

- Only converts from HTML. Other document types not supported.
- Origin response cannot exceed 2 MB (2,097,152 bytes).
- If enabled but responses remain `text/html`, zone compatibility may need verification.

## Other Markdown Conversion APIs

When content negotiation is not available from the source, alternative APIs:

| API | Use case |
|---|---|
| Workers AI `toMarkdown()` | Arbitrary document conversion + summarization |
| Browser Run `/markdown` | Dynamic pages requiring JS rendering before conversion |

### Workers AI toMarkdown()

```typescript
const result = await ai.toMarkdown(html)
// Returns structured markdown from arbitrary HTML input
```

Supports multiple document types and can include summarization. Part of the Workers AI runtime.

### Browser Run Markdown Endpoint

```typescript
const md = await browser.markdown("https://example.com/page")
// Renders page in headless browser, returns markdown
```

Useful for SPAs and pages that require JavaScript execution before content is available.

## Implementation Checklist

- [ ] Add `Accept: text/markdown` support check for your site
- [ ] Configure `Content-Signal` headers for AI usage preferences
- [ ] Create `llms.txt` for AI agent content discovery
- [ ] Enable edge markdown conversion if using Cloudflare
- [ ] Ensure `<meta name="title">` and `<meta name="description">` are present for YAML frontmatter
- [ ] Verify JSON-LD structured data is preserved in markdown output
- [ ] Test with `curl -H "Accept: text/markdown"` to verify conversion
- [ ] Check `x-markdown-tokens` header for token estimates
