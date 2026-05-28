---
name: 010122-multi-currency-architecture
description: Multi-currency architecture — price-per-currency with FK chain to countries and taxes, geo detection via edge headers, admin CRUD.
license: MIT
compatibility: PostgreSQL 16+ with Drizzle ORM or raw SQL
---

# Multi-Currency Architecture

## When to use

When building e-commerce or subscription systems that need to display and charge in multiple currencies based on the user's geographic location.

## References

| Topic | File |
|---|---|
| Currency + country + tax FK chain | `references/fk-chain.md` |
| Price table design per currency | `references/price-table.md` |
| Geo-based detection pipeline | `references/geo-detection.md` |
| CurrencyProvider and admin CRUD | `references/currency-provider.md` |

## Quick checklist

- [ ] `sys_currencies`: code, name, symbol, countryId FK, isDefault, isActive
- [ ] `sys_taxes`: countryId FK, currencyId FK, name, rate, isActive
- [ ] `prd_prices`: productId, variantId, currencyId FK, price, compareAtPrice, cost, isActive, validFrom, validUntil
- [ ] Unique constraint: `(productId, variantId, currencyId)` with `NULLS NOT DISTINCT`
- [ ] Geo detection: edge header (`cf-ipcountry`) → sys_countries → sys_currencies
- [ ] Fallback chain: user preference cookie → geo detection → default currency (USD)
- [ ] CurrencyProvider context: read-only (immutable without user preference)
- [ ] Admin CRUD: generic factory with FK protection on DELETE
