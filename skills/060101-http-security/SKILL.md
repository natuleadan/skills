---
name: 060101-http-security
description: Multi-layer web security patterns — rate limiting, Content Security Policy, security headers, CORS, IP deny lists, and graceful degradation.
license: MIT
---

# Security Patterns

## Architecture Overview

Security is applied at three layers:

```
1. Edge/Proxy Layer    ← Rate limiting, CSP, security headers, IP deny
2. Application Layer   ← Auth rate limit, session validation, input sanitization
3. Infrastructure Layer ← Auto-protection, firewall, DDoS mitigation
```

## Layer 1: Edge/Proxy

### Rate Limiting

Applied before requests reach application code.

- **Algorithm**: Fixed window (cheaper) or sliding window (stricter)
- **Identifier**: Client IP (`x-forwarded-for` → `x-real-ip`)
- **Tiers**: Different limits per route group (auth, api, public)

```
Request → match route tier → ratelimit.limit(ip) → pass or 429
                              ↓ (timeout → allow on failure)
                        Application handler
```

### Content Security Policy (CSP)

Dynamic CSP built from environment variables:

| Directive | Purpose | Configurable via |
|-----------|---------|-----------------|
| `script-src` | Allowed JS sources | CSP_SCRIPT_SRC_DOMAINS |
| `style-src` | Allowed CSS sources | CSP_STYLE_SRC_DOMAINS |
| `img-src` | Allowed image sources | CSP_IMG_SRC_DOMAINS |
| `font-src` | Allowed font sources | CSP_FONT_SRC_DOMAINS |
| `connect-src` | Allowed API/WS connections | CSP_CONNECT_SRC_DOMAINS |
| `frame-src` | Allowed iframe sources | CSP_FRAME_SRC_DOMAINS |

### Security Headers

| Header | Value |
|--------|-------|
| `X-Content-Type-Options` | `nosniff` |
| `X-Frame-Options` | `SAMEORIGIN` |
| `X-XSS-Protection` | `1; mode=block` |
| `Referrer-Policy` | `strict-origin-when-cross-origin` |
| `Permissions-Policy` | `camera=(self), microphone=(self), geolocation=(self)` |
| `Strict-Transport-Security` | `max-age=31536000; includeSubDomains; preload` |

## Layer 2: Application

- Auth rate limits (e.g., 10 req/60s on login endpoints)
- Session validation on every protected action
- Input sanitization (XSS prevention)
- CSRF tokens on mutations

## Layer 3: Infrastructure

- Auto IP deny list from open-source threat feeds
- DDoS protection at cloud provider level
- Database connection limits and query timeouts

## Graceful Degradation

If the rate limiting service is unreachable:

1. Timeout (e.g., 1s) triggers catch clause
2. Request is allowed through (fail open)
3. Security headers still applied
4. Next request retries — resumes when service is back

## Quick Reference

```bash
# Test security headers
curl -I https://example.com | grep -i "x-\|strict-\|referrer-\|permissions-"

# Test rate limiting
for i in $(seq 1 20); do curl -s -o /dev/null -w "%{http_code}\n" https://example.com/api/endpoint; done
```

## References

- [Security Patterns](references/security-patterns.md)
- [Rate Limiting](references/rate-limiting.md)
- [Request Headers](references/request-headers.md)
- [Environment Variables](references/environment-variables.md) — Secret generation, rotation, .env hierarchy
