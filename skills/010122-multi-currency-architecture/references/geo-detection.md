# Geo-Based Currency Detection

## Pipeline

```
Edge header (cf-ipcountry: "FR") → sys_countries → sys_currencies → "EUR"
```

## Implementation (Next.js layout)

```typescript
const headersList = await headers()
const geoCountry = headersList.get("cf-ipcountry") || "US"

const countries = await db.query.countries.findMany({ where: eq(countries.isActive, true) })
const currencies = await db.query.currencies.findMany({ where: eq(currencies.isActive, true) })

const matchedCountry = countries.find(c => c.code === geoCountry)
const countryCurrency = matchedCountry
  ? currencies.find(c => c.countryId === matchedCountry.id)
  : null
const currentCurrency = countryCurrency?.code || "USD"
```

## Fallback chain

1. User preference cookie (`nxt_currency` or similar) — set by CurrencyProvider
2. Geo detection via edge header
3. Default currency (USD or isDefault in sys_currencies)

## Edge headers

| Header | Source | Value |
|---|---|---|
| `cf-ipcountry` | Cloudflare | ISO country code (US, FR, etc.) |
| `x-vercel-ip-country` | Vercel | ISO country code |
| `x-forwarded-for` | Any proxy | Client IP for fallback |
