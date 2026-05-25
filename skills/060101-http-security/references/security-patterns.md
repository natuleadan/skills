# Security Patterns Reference

## Multi-Layer Security

| Layer | What it protects | Examples |
|-------|-----------------|----------|
| Edge/Proxy | Network-level | Rate limiting, IP deny, CSP, headers |
| Application | Business-level | Auth, session validation, XSS prevention |
| Infrastructure | System-level | Firewall, DDoS protection, connection limits |

## CSP Configuration

```javascript
// Example CSP generation from env vars
const cspDirectives = {
  "script-src": ["'self'", ...parseDomains(process.env.CSP_SCRIPT_SRC_DOMAINS)],
  "style-src": ["'self'", "'unsafe-inline'", ...parseDomains(process.env.CSP_STYLE_SRC_DOMAINS)],
  "img-src": ["'self'", "data:", ...parseDomains(process.env.CSP_IMG_SRC_DOMAINS)],
  "font-src": ["'self'", ...parseDomains(process.env.CSP_FONT_SRC_DOMAINS)],
  "connect-src": ["'self'", ...parseDomains(process.env.CSP_CONNECT_SRC_DOMAINS)],
  "media-src": ["'self'", ...parseDomains(process.env.CSP_MEDIA_SRC_DOMAINS)],
  "frame-src": [...parseDomains(process.env.CSP_FRAME_SRC_DOMAINS)],
  "base-uri": ["'self'"],
}
```

## Security Headers Checklist

- [ ] `X-Content-Type-Options: nosniff`
- [ ] `X-Frame-Options: SAMEORIGIN`
- [ ] `X-XSS-Protection: 1; mode=block`
- [ ] `Referrer-Policy: strict-origin-when-cross-origin`
- [ ] `Permissions-Policy` restricts camera, mic, geo
- [ ] `Strict-Transport-Security` with `preload`
- [ ] CSP restricts script/style sources
- [ ] CORS limits origins and methods

## CORS Configuration

```javascript
{
  origin: process.env.APP_URL || "http://localhost:3000",
  methods: ["GET", "POST", "PUT", "PATCH", "DELETE"],
  allowedHeaders: ["Content-Type", "Authorization"],
  credentials: true,
  maxAge: 86400,
}
```

## Request Header IP Resolution

Standard fallback chain:
```
x-forwarded-for → x-real-ip → req.socket.remoteAddress → 127.0.0.1
```
