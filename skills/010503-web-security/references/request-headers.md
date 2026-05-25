# Request Headers Reference

## IP & Location Headers

Vercel (and most CDN/proxy platforms) inject these headers automatically.

| Header | Format | Example |
|--------|--------|---------|
| `x-forwarded-for` | IP address | `203.0.113.1` |
| `x-real-ip` | IP address | `203.0.113.1` |
| `x-forwarded-host` | Hostname | `example.com` |
| `x-forwarded-proto` | Protocol | `https` or `http` |

### Vercel-Specific Geo Headers

| Header | Format | Example |
|--------|--------|---------|
| `x-vercel-ip-continent` | ISO 3166-1 | `NA`, `EU`, `AS` |
| `x-vercel-ip-country` | ISO 3166-1 | `US`, `GB`, `MX` |
| `x-vercel-ip-country-region` | ISO 3166-2 | `California`, `England` |
| `x-vercel-ip-city` | City name | `San Francisco` |
| `x-vercel-ip-latitude` | Decimal degrees | `37.7749` |
| `x-vercel-ip-longitude` | Decimal degrees | `-122.4194` |
| `x-vercel-ip-timezone` | IANA timezone | `America/Chicago` |
| `x-vercel-ip-postal-code` | Postal code | `94102` |
| `x-vercel-deployment-url` | URL | `project.vercel.app` |
| `x-vercel-id` | Trace ID | Region + instance |
| `x-vercel-signature` | HMAC-SHA1 | Webhook verification |
