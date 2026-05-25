# Polar API Reference

## Base URLs

| Environment | Base URL | Purpose |
|-------------|----------|---------|
| Production | `https://api.polar.sh/v1` | Real customers & live payments |
| Sandbox | `https://sandbox-api.polar.sh/v1` | Safe testing & integration work |

The sandbox environment is fully isolated — data, users, tokens, and organizations created there do not affect production. Create separate tokens in each environment.

## Authentication

### Organization Access Tokens (OAT)

Use an OAT to act on behalf of your organization (manage products, prices, checkouts, orders, subscriptions, benefits, etc.)

```
Authorization: Bearer polar_oat_xxxxxxxxxxxxxxxxx
```

Create OATs in your organization settings. Never expose an OAT in client-side code, public repos, or logs.

### Customer Access Tokens

For customer-facing flows, generate a **Customer Session** server-side via `POST /v1/customer-sessions/`, then use the returned customer access token with the **Customer Portal API**.

### Core API vs Customer Portal API

| Aspect | Core API | Customer Portal API |
|--------|----------|---------------------|
| Audience | Your server / backend | One of your customers |
| Auth Type | Organization Access Token (OAT) | Customer Access Token |
| Scope | Full org resources | Only authenticated customer's data |
| Typical Use | Admin dashboards, provisioning | Custom customer portal, gated app |
| Token Creation | Via dashboard (manual) | Via `/v1/customer-sessions/` (server-side) |

## SDK Usage

### TypeScript

```typescript
import { Polar } from "@polar-sh/sdk";

const polar = new Polar({
  accessToken: process.env.POLAR_ACCESS_TOKEN!,
  server: "sandbox", // omit or use "production" for live
});
```

### Python

```python
from polar import Polar

client = Polar(
    access_token=os.environ["POLAR_ACCESS_TOKEN"],
    server="sandbox",
)
```

## Pagination

All list endpoints support `page` and `limit` query parameters:

| Parameter | Type | Default | Max | Description |
|-----------|------|---------|-----|-------------|
| `page` | integer | 1 | - | Page number, 1-based |
| `limit` | integer | 10 | 100 | Items per page |

Response includes a `pagination` object:

```json
{
  "items": [...],
  "pagination": {
    "total_count": 250,
    "max_page": 3
  }
}
```

## Rate Limits

| Environment | Limit |
|-------------|-------|
| Production | 500 requests/min per organization |
| Sandbox | 100 requests/min per organization |
| Public validation endpoints | 3 requests/sec |

Exceeding the limit returns `429 Too Many Requests` with a `Retry-After` header.

---

## Products

### Create Product

```
POST /v1/products/
Scope: products:write
```

Creates a new product. Pass `prices` array with at least one price entry.

```typescript
const product = await polar.products.create({
  name: "My Product",
  description: "Product description",
  prices: [{
    amount_type: "fixed",
    price_amount: 2500, // cents ($25.00)
    price_currency: "usd",
  }],
  metadata: { product_id: "abc" },
});
```

### Get Product

```
GET /v1/products/{id}
Scope: products:read, products:write
```

### List Products

```
GET /v1/products/
Scope: products:read, products:write
```

Supports pagination with `page` and `limit` parameters (max 100).

### Update Product

```
PATCH /v1/products/{id}
Scope: products:write
```

Updates product name, description, prices, etc.

### Update Product Benefits

```
POST /v1/products/{id}/benefits
Scope: products:write
```

Updates benefits granted by a product.

---

## Checkout Sessions

### Create Checkout Session

```
POST /v1/checkouts/
Scope: checkouts:write
```

Required: `products` (array of Polar product IDs).

```typescript
const checkout = await polar.checkouts.create({
  products: [productId1, productId2],
  success_url: "https://example.com/success",
  cancel_url: "https://example.com/cancel",
  customer_email: "user@example.com",
  metadata: { order_id: "ord_xxx" },
  locale: "en",
  allow_discount_codes: true,
});
```

Returns a session object with a `url` field for redirecting the customer.

### Get Checkout Session

```
GET /v1/checkouts/{id}
Scope: checkouts:read
```

### List Checkout Sessions

```
GET /v1/checkouts/
Scope: checkouts:read
```

### Update Checkout Session

```
PATCH /v1/checkouts/{id}
Scope: checkouts:write
```

### Client-Side Checkout Confirm

```
POST /v1/checkouts/client/{client_secret}/confirm
```

Used for **custom checkout UIs** (not Polar's hosted page). Confirms a checkout session created via the client-side flow.

```typescript
const confirmed = await polar.checkouts.client.confirm({
  clientSecret: checkout.client_secret,
});
```

> Note: If using Polar's hosted checkout (the standard flow), this endpoint is not needed. The hosted page handles confirmation automatically.

---

## Orders

### Get Order

```
GET /v1/orders/{id}
Scope: orders:read
```

### List Orders

```
GET /v1/orders/
Scope: orders:read
```

Supports filtering and pagination.

### Update Order

```
PATCH /v1/orders/{id}
Scope: orders:write
```

Update billing details before generating the invoice.

### Generate Invoice

```
POST /v1/orders/{id}/invoice
Scope: orders:read
```

Returns `202` — invoice generation is asynchronous. Listen for `order.updated` webhook and check `is_invoice_generated` field.

### Get Invoice

```
GET /v1/orders/{id}/invoice
Scope: orders:read
```

Returns `404` if invoice hasn't been generated yet.

---

## Order Lifecycle Webhook Events

| Event | Description |
|-------|-------------|
| `order.created` | Order created (status may be `pending` or `paid`) |
| `order.paid` | Order fully processed and paid — **use this for fulfillment** |
| `order.updated` | Order status/amount changed; invoice generated |
| `order.refunded` | Order was refunded (partially or fully) |

> Prefer `order.paid` over `order.created` for fulfillment logic. The `order.created` event may fire with `pending` status before payment is confirmed.
