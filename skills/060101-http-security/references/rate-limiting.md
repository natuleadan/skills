# Rate Limiting Patterns Reference

## Algorithm Comparison

| Aspect | Fixed Window | Sliding Window |
|--------|-------------|----------------|
| Redis commands per request | ~2 | ~4 |
| Precision | Fixed boundary reset | Rolling approximation |
| Cost at scale | Lower | Higher |
| Best for | Traffic protection, anti-abuse | Per-second billing, strict limits |

Fixed window is sufficient for abuse prevention. Sliding window adds precision at higher cost.

## Route Tiers Pattern

| Tier | Relative Limit | Rationale |
|------|---------------|-----------|
| Auth | Low | Safety net for login endpoints |
| API | Medium | General API endpoints |
| Public | Medium-High | Content pages, high traffic |
| Admin | Low | Administrative actions |

## Safety Features

| Feature | Purpose |
|---------|---------|
| Timeout (1s) | Fail open if rate limiter is down |
| Ephemeral cache | Blocked IPs cached in-memory — no DB call |
| Auto deny list | Block known malicious IPs from threat feeds |
| Analytics | Monitor rate limit hits |

## Rate Limit Info Headers

Every rate-limited response should include:

| Header | Example | Purpose |
|--------|---------|---------|
| `X-RateLimit-Limit` | `100` | Max requests per window |
| `X-RateLimit-Remaining` | `87` | Requests left in window |
| `Retry-After` | `10` | Seconds until reset |
