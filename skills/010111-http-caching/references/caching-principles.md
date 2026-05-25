# Caching Principles

Six core principles for cache architecture:

1. **Runtime Cache first** for regional data (faster, no network call)
2. **Distributed cache** for global/stateful data
3. **CDN Cache** for HTTP responses same for all users
4. **Never cache user-specific data** without `Vary` header
5. **Tag-based invalidation** over TTL for predictable updates
6. **TTL fallback** ensures stale data is eventually refreshed

## Quick Reference

| Layer | Scope | TTL | Invalidation |
|-------|-------|-----|-------------|
| Browser/CDN | Global | hours-days | `Cache-Control`, redeploy |
| Runtime | Regional | seconds-hours | `revalidateTag`, `revalidatePath` |
| Distributed | Global | minutes-hours | TTL, manual delete |
