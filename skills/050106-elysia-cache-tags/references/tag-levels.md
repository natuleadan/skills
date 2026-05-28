# 3-Level Tag System

## Structure

```
L1: cache:tags:{domain}:{entityId}  → Entidad específica
L2: cache:tags:{domain}             → Colección del dominio
L3: cache:tags:cross:{scope}        → Cross-domain
```

## Domain constants

```typescript
export const CACHE_DOMAINS = {
  PRODUCTS: "products",
  VARIANTS: "variants",
  PRICES: "prices",
  INVENTORY: "inventory",
  MEDIAS: "medias",
  RATINGS: "ratings",
  COUPONS: "coupons",
  CATEGORIES: "categories",
  STOREHOUSES: "storehouses",
} as const

export const CACHE_CROSS = {
  CATALOG: "catalog",
  ADMIN: "admin",
  CHECKOUT: "checkout",
} as const
```

## Tag functions

```typescript
function tagProduct(id: string) { return `cache:tags:products:${id}` }
const tagProducts = "cache:tags:products"
const tagCatalog = "cache:tags:cross:catalog"
```

## TTL strategy

| Entity | Value TTL | Tag set TTL |
|---|---|---|
| Product list | 30s | 60s |
| Product detail | 30s | 60s |
| Signed URL | 3500s | — |
| Category list | 30s | 60s |
