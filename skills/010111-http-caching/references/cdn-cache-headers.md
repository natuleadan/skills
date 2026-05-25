# CDN Cache Headers

## Overview

CDN caching stores content (pages, API responses, static assets) on edge nodes globally. Configure via `Cache-Control` headers.

## Cache-Control Header Priority

Three levels with decreasing priority:

| Header | Affects | Stripped before browser |
|--------|---------|------------------------|
| Platform-specific CDN header | CDN only | Yes |
| `CDN-Cache-Control` | CDN + downstream CDNs | No |
| `Cache-Control` | Browser + all | No |

### Priority Rules

| Headers set | Cache behavior |
|-------------|---------------|
| `Cache-Control: s-maxage=60` | 60s on CDN |
| `CDN-Cache-Control: s-maxage=120` + `Cache-Control: s-maxage=60` | 120s (CDN-Cache-Control wins) |
| Platform CDN header + `CDN-Cache-Control: s-maxage=120` + `Cache-Control: s-maxage=60` | Platform value wins |

### Recommended Settings Per Content Type

| Content type | Recommended header |
|-------------|-------------------|
| Server-rendered, same for all | `max-age=0, s-maxage=86400` |
| Semi-static (products, blog) | `max-age=120, s-maxage=86400` |
| Personalized | `private, max-age=0` |
| Hashed assets (JS, CSS, fonts) | `max-age=31536000, immutable` |

## Directives

### s-maxage

TTL in seconds for the CDN. Minimum 1s, maximum 1 year.

```typescript
response.headers.set("Cache-Control", "public, s-maxage=60");
```

### stale-while-revalidate

Serve stale content while refreshing in background.

```typescript
response.headers.set("Cache-Control", "s-maxage=1, stale-while-revalidate=59");
```

### stale-if-error

Serve stale content if origin returns error.

```typescript
response.headers.set("Cache-Control", "max-age=604800, stale-if-error=86400");
```

### private

Prevents CDN caching (browser only).

```typescript
response.headers.set("Cache-Control", "private, max-age=0");
```

## Vary Header

Creates separate cache entries per header value (e.g., country-based caching):

```typescript
response.headers.set("Cache-Control", "s-maxage=3600");
response.headers.set("Vary", "X-Country");
```

## Cacheable Response Criteria

A response is cacheable when:
- Method is `GET` or `HEAD`
- Status is `200`, `404`, `410`, `301`, `302`, `307`, or `308`
- Max size: 10MB (non-streaming) / 20MB (streaming)
- Max TTL: 1 year
- No `set-cookie`, `private`, `no-cache`, or `no-store` headers
- No `Authorization` header in request

## CDN Cache Status Values

| Status | Meaning |
|--------|---------|
| `HIT` | Served from cache |
| `MISS` | Not in cache, fetched from origin |
| `STALE` | Served stale content from cache |
| `REVALIDATED` | Stale content revalidated in background |
| `BYPASS` | Cache bypassed (excluded by rules) |
| `DYNAMIC` | Uncached dynamic content |

## Image Optimization

For optimized image delivery via CDN:
- Use framework image components (`next/image`, etc.) for user-facing images (product photos, hero, avatars)
- Use regular `<img>` for icons, SVGs, and images under 10KB
- Configure allowed remote image domains
- OG/social images use dedicated OG image generation (not image optimization)
