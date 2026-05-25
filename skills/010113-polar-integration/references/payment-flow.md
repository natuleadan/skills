# Payment Flow

## Product Sync — syncVariantToProcessor()

### Architecture

Polar requires real products with prices — ad-hoc/custom pricing without a product is NOT supported.

**Solution:** Sync each product/variant from your `products` + `product_variants` tables to Polar ONCE, then reuse the `processor_product_id` in all checkouts.

### Flow

```
initiatePayment(orderId)
  → load order items
  → for each item:
      syncVariantToProcessor(productId, variantId?)
        1. Check payment_processor_products cache (product_id + variant_id + currency + processor)
        2a. CACHE HIT + synced → return processor_product_id
        2b. CACHE HIT + outdated → PATCH Polar API → mark synced → return id
        2c. CACHE MISS → POST Polar API → INSERT row → return id
  → build lineItems array with real polar_product_ids
  → PaymentService.createCheckoutSession(lineItems)
```

### Key Rules

1. **Source of truth is your application DB** — `products`, `product_variants`, `product_prices`
2. **Polar is a mirror** — never push data back from Polar to your DB
3. **Sync is triggered in `initiatePayment`** — not in createOrder (too early)
4. **Each variant = separate Polar product** — Polar has no native variant concept
5. **Prices in cents** — Polar API expects `price_amount` as integer cents (multiply by 100)
6. **Currency lowercase** — Polar expects `usd`, not `USD`
7. **Cache key:** `(product_id, variant_id, currency_code, processor)` — unique constraint

### When to Sync

| Event | Action |
|-------|--------|
| User clicks "Place Order" | Sync all items in cart |
| Product price changes | Mark as `outdated` → sync on next checkout |
| Product deleted | Archive in Polar, mark as `archived` |
| Admin "Sync All" | Find all `outdated` products, re-sync |

### Sync Statuses

- `synced` — up to date, ready for checkout
- `outdated` — price/name changed in DB, needs re-sync
- `failed` — Polar API error, retry on next checkout
- `archived` — product soft-deleted in DB

### Polar Products API (Create)

```
POST /v1/products/
Scope: products:write
```

Used when product is not yet in Polar. Creates the product with prices.

```
PATCH /v1/products/{id}
Scope: products:write
```

Used when product exists but price changed — updates the existing Polar product.

### Pricing

Polar prices use `amount_type` values:
- `fixed` — one-time payment (no recurring)
- `monthly` / `yearly` — subscription pricing

Prices are in integer cents. Example: `price_amount: 2500` = $25.00.

---

## Checkout Sessions

### Create Checkout Session

```
POST /v1/checkouts/
Scope: checkouts:write
```

**Required fields:**
- `products` — array of Polar product IDs (at least 1 required, NO ad-hoc without products)
- `success_url` — redirect after successful payment

**Optional fields:**
- `customer_email` — pre-fill customer email
- `metadata` — key-value pairs (max 255 chars per value)
- `allow_discount_codes` — enable/disable discount codes
- `custom_field_data` — custom field values
- `locale` — override language (e.g., `es`, `fr`, `de`)

### Get Checkout Session

```
GET /v1/checkouts/{id}
Scope: checkouts:read
```

### Checkout Session Implementation

```typescript
static async createCheckoutSession(
  orderId, orderNumber, lineItems, currencyCode, totalAmount, lang, customerEmail
) {
  const productIds = lineItems.map(item => item.polarProductId);

  const session = await polarClient.createCheckout({
    products: productIds,
    success_url: `${PUBLIC_URL}/orders/${orderNumber}`,
    cancel_url: `${PUBLIC_URL}/orders/${orderNumber}`,
    customer_email: customerEmail,
    locale: lang,
    metadata: {
      order_id: orderId,
      order_number: orderNumber,
      line_items: JSON.stringify(lineItems.map(i => ({
        product_id: i.productId,
        variant_id: i.variantId,
        qty: i.quantity,
      }))),
    },
  });

  // Persist in payments table
  return { url: session.url, paymentId: payment.id };
}
```

### Key Rules

1. **Products array is REQUIRED** — Polar rejects requests with empty products
2. **Metadata is string-only** — JSON must be stringified
3. **URLs must be absolute** — use `NEXT_PUBLIC_URL` from `env.public.ts`
4. **No query params for status** — payment status from DB only (`payments.status`), not URL
5. **One session = one order** — don't reuse sessions
6. **Store checkout_id** — save in `payments.polar_checkout_id` for webhook reconciliation

---

## Checkout Localization

### Overview

- Polar checkout auto-detects customer language from browser settings
- Can override via API `locale` parameter or querystring `?locale=`
- Feature flag must be enabled for the organization (beta)

### Supported Languages

| Language | Locale | Status |
|----------|--------|--------|
| English | `en` | default |
| Spanish | `es` | available |
| French | `fr` | available |
| German | `de` | available |
| Italian | `it` | available |
| Dutch | `nl` | available |
| Swedish | `sv` | available |
| Hungarian | `hu` | available |
| Portuguese (Brazil) | `pt` | available |
| Portuguese (Portugal) | `pt-PT` | available |
| Korean | `kr` | coming soon |

### Language Mapping

Map your app's language codes to Polar locales, falling back to `en` for unsupported languages:

```typescript
const locale = lang === "es" ? "es" : lang === "fr" ? "fr" : "en";
```

### Override Methods (precedence order)

1. **Querystring** — `?locale=es` (highest priority)
2. **API parameter** — `locale: "es"` in checkout creation
3. **Browser detection** — automatic (default)

### Known Limitations (Beta)

- Error messages displayed in English
- Transactional emails (receipts, confirmations) in English
- Customer portal in English
- No language selector on checkout page — determined automatically

---

## Multi-Currency Support

### Current State

Polar multi-currency is **in development** (Epic #7842, ongoing). Current limitation: same price structure required across all currencies.

### Source of Truth

Your `product_prices` table is the single source of truth for all prices and currencies.

### Currency Resolution

```typescript
const defaultCurrency = await db.getDefaultCurrency(); // e.g., "USD"
const currencyCode = (defaultCurrency ?? "USD").toLowerCase();
```

### Cache Key

Unique constraint includes currency_code: `(product_id, variant_id, currency_code, processor)`. This allows the same product to have separate Polar entries per currency.

### Important Rules

1. **Currency stored UPPERCASE in DB** (`USD`) but sent **lowercase to Polar** (`usd`)
2. **Each currency = separate Polar product** — no shared products across currencies
3. **Default currency** comes from app settings
4. **Order currency** comes from `orders.currency_code`

### Future: When Polar Multi-Currency Matures

1. Create single Polar product with multi-currency prices
2. Use `prices` array with multiple currency entries
3. Remove currency from cache key (one product, multiple prices)

### Currency Conversion

No automatic conversion. Each product must have explicit prices per currency in `product_prices`.

---

## Error Handling

### Common API Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `POLAR_ACCESS_TOKEN is not configured` | Missing env var | Add to `.env` |
| `Polar API error 401` | Invalid/expired token | Regenerate in Polar Dashboard |
| `Polar API error 404` | Wrong product ID | Check processor_product_id in payment_processor_products |
| `Polar API error 422` | Invalid payload | Check currency format (lowercase), prices (in cents) |
| `No active price found` | Product has no product_prices | Ensure product has active price before checkout |

### Common Checkout Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `Order has no items` | Empty cart | Prevent checkout with empty cart |
| `Order is not pending payment` | Wrong status | Only allow checkout from `pending` status |
| `products: List should have at least 1 item` | Empty products array | Ensure syncVariantToProcessor returns valid IDs |

### Error Flow

```typescript
static async initiatePayment(orderId, lang) {
  try {
    // ... sync and checkout logic
    return { url: result.url };
  } catch (error) {
    return {
      error: error instanceof Error ? error.message : "Payment initiation failed",
    };
  }
}
```

### Frontend Handling

```typescript
const paymentResult = await initiatePaymentAction(orderId, lang);

if (paymentResult.error) {
  router.push(`/orders/${orderNo}`);
  return;
}

if (paymentResult.url) {
  window.location.href = paymentResult.url;
}
```

### Retry Logic

- **Sync failures:** Mark as `failed`, retry on next checkout
- **Webhook failures:** Polar retries automatically (exponential backoff, up to 10 times)
- **Checkout failures:** Return error to user, don't auto-retry

### Rate Limits

- **Production:** 500 requests per minute per organization
- **Sandbox:** 100 requests per minute per organization
- Public validation endpoints: 3 requests per second
- Response: `429 Too Many Requests` with `Retry-After` header

---

## Merchant of Record (MoR) Model

### Overview

Polar is a Merchant of Record, NOT a Payment Service Provider (PSP):
- Polar handles international sales taxes globally (VAT, GST, US Sales Tax)
- Built on top of Stripe (+ more PSPs in the future)
- Polar acts as reseller of digital goods — handles tax liability

### PSP vs MoR

| Aspect | PSP (Stripe) | MoR (Polar) |
|--------|-------------|-------------|
| Base fee | 2.9% + $0.30 | 4% + $0.40 |
| Tax compliance | Your responsibility | Included |
| International sales | You handle | Polar handles |
| Dashboard | Basic | Full product/customer/order management |
| Flexibility | High | Moderate |
| API Level | Low-level, full control | High-level, optimized for monetization |

### Tax Coverage

- US Delaware C Corp — registers for US State Sales Taxes upon reaching thresholds
- EU VAT (Irish OSS VAT)
- UK VAT
- Global payments — liable for tax compliance on all sales internationally
- Expands registrations as needed via accounting firms

### Important Notes

- You're still responsible for your own income/revenue tax in your country
- Polar VAT number uses OSS format (not country-specific)
- Some accounting software doesn't recognize EU prefix — manual entry may be needed
- In markets Polar isn't registered, they still take on liability
- Polar may block payments from countries where compliance is impossible
