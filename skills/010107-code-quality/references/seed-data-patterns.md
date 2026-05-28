# Seed Data Patterns

## Anonymized seed data

Never use real user data, real emails, or real product names in seed data.

```typescript
// GOOD
const productDefs = [
  { name: "Example Product A", price: 49.99 },
  { name: "Example Product B", price: 29.99 },
]

// BAD (reveals real products)
const productDefs = [
  { name: "Acme Corp Premium Widget 2024", price: 49.99 },
]
```

## Multi-language seed pattern

When seeding translations, create entries for each language:

```typescript
const translations = [
  // English (source)
  { lang: "en", name: "Example Product", slug: "example-product", description: "An example product" },
  // Spanish (translated)
  { lang: "es", name: "Producto de Ejemplo", slug: "producto-ejemplo", description: "Un producto de ejemplo" },
  // Arabic (translated)
  { lang: "ar", name: "منتج مثال", slug: "منتج-مثال", description: "منتج مثال" },
]
```

## Multi-currency seed pattern

```typescript
const prices = [
  { productName: "Example Product A", currency: "USD", price: 49.99 },
  { productName: "Example Product A", currency: "EUR", price: 45.99 },
  { productName: "Example Product A", currency: "GBP", price: 39.99 },
]
```

## Image/Media seed

Use placeholder image services for seed data:

```typescript
const IMG = (seed: string, w = 600, h = 400) =>
  `https://picsum.photos/seed/${seed}/${w}/${h}`
```

Never use real product images or screenshots.

## Rating/review seed

```typescript
const ratings = [
  { rating: 5, title: "Excellent", review: "Great product, highly recommended." },
  { rating: 4, title: "Very good", review: "Works as expected, good value." },
]
```

Keep reviews generic. Never copy real customer reviews.

## User seed

```typescript
const users = [
  { email: "admin@example.com", role: "admin", name: "Admin User" },
  { email: "editor@example.com", role: "editor", name: "Editor User" },
]
```

Use `example.com` emails. Never use real email addresses.
