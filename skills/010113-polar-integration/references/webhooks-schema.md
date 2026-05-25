# Webhooks & Schema

## Webhooks

### Overview

- Follows Standard Webhooks specification
- Built-in signature validation via `@polar-sh/nextjs` Webhooks utility
- Fully typed webhook payloads
- Supports Slack & Discord formatting
- Asynchronous event notifications (no polling needed)

### Setup Steps

1. Add endpoint in organization settings → "Add Endpoint"
2. Specify absolute URL: `https://your-domain.com/api/webhooks/polar`
3. Format: Raw (JSON) for custom integrations
4. Set secret key — cryptographically signs requests
5. Subscribe to desired events

### Signature Verification

- Headers: `webhook-id`, `webhook-timestamp`, `webhook-signature`
- `@polar-sh/nextjs` handles base64 encoding automatically
- Reject unsigned/invalid requests with 403
- Custom validation: secret must be base64-encoded before generating signature

### Implementation (Next.js)

**Route:** `src/app/api/webhooks/polar/route.ts`

- Uses `Webhooks()` from `@polar-sh/nextjs`
- Granular handlers: `onOrderPaid`, `onOrderCreated`, `onCheckoutExpired`, `onCheckoutCanceled`
- Automatic signature verification
- Returns 200 for unknown events
- Logs all events for debugging

### Local Development — Polar CLI

```bash
# Install
curl -fsSL https://polar.sh/install.sh | bash

# Login
polar login

# Listen for webhooks
polar listen http://localhost:3000/

# Copy the generated secret to .env
POLAR_WEBHOOK_SECRET=whsec_xxxxx
```

> The secret from `polar listen` MUST match `POLAR_WEBHOOK_SECRET` in `.env` or you'll get 403 errors.

### Key Events

| Event | Action |
|-------|--------|
| `order.paid` | Confirm payment, payments → `paid`, orders → `confirmed` |
| `order.created` | Optional — create pending payment record |
| `order.refunded` | Update payments → `refunded` |
| `order.updated` | Order status/amount changed; invoice generated |
| `checkout.created` | Checkout session created |
| `checkout.updated` | Checkout session changed |
| `checkout.expired` | Cancel payment, payments → `expired` |
| `subscription.created` | Track new subscription |
| `subscription.active` | Activate subscription benefits |
| `subscription.canceled` | Revoke subscription benefits |
| `subscription.updated` | Subscription changed |
| `product.created` | Sync to local catalog |
| `product.updated` | Mark local product as outdated |
| `customer.created` | Create/update customer record |
| `customer.updated` | Update customer data |
| `customer.deleted` | Soft-delete customer |
| `benefit.created` | New benefit available |
| `benefit.updated` | Benefit changed |
| `benefit_grant.created` | Grant access to benefit |
| `benefit_grant.revoked` | Revoke benefit access |

### Delivery Monitoring

- Historic deliveries visible in Polar Dashboard → Webhooks → Endpoint
- Review payload sent for each delivery
- Trigger redelivery in case of failure

### Failure Handling

- **Retries:** Up to 10 retries with exponential backoff
- **Timeouts:** Polar timeout 10 seconds; recommended response time under 2 seconds
- **Auto-disable:** Endpoint auto-disabled after 10 consecutive failed deliveries (admin gets email)
- **Re-enable:** Manually re-enable in dashboard after fixing issues

### IP Allowlist

For firewalls/reverse proxies, allow these IPs:
```
3.134.238.10
3.129.111.220
52.15.118.168
74.220.50.0/24
74.220.58.0/24
```

### Troubleshooting

| HTTP Status | Likely Cause | Fix |
|-------------|-------------|-----|
| 404 | Route doesn't exist | Verify route: `curl -X POST <endpoint-url>`; try trailing `/` on Polar URL |
| 3xx | Redirect not followed | Polar doesn't follow redirects; ensure URL matches final destination |
| 403 | Auth middleware blocks it | Exclude webhook route from auth middleware; disable Cloudflare Bot Fight Mode if used |
| 403 (Invalid Signature) | Secret mismatch | Base64-encode secret before generating signature (`@polar-sh/nextjs` handles this) |

---

## Database Schema

### payments

Payment records linked to orders.

| Column | Type | Notes |
|--------|------|-------|
| id | uuid PK | gen_random_uuid() |
| order_id | uuid FK → orders | NOT NULL |
| provider | text | DEFAULT 'polar' |
| payment_method | text | nullable |
| polar_checkout_id | text | Polar checkout session ID |
| polar_session_id | text | nullable |
| polar_order_id | text | Polar order ID (from webhook) |
| amount | numeric | NOT NULL, CHECK >= 0 |
| currency_code | varchar(3) | DEFAULT 'USD' |
| status | payment_status | DEFAULT 'pending' |
| payment_url | text | Polar checkout URL |
| redirect_url | text | success redirect |
| failure_reason | text | nullable |
| meta_data | jsonb | DEFAULT '{}' |
| soft_delete | boolean | DEFAULT false |
| created_at | timestamptz | DEFAULT now() |
| updated_at | timestamptz | DEFAULT now() |

**Indexes:** order_id, polar_checkout_id, polar_session_id, status, soft_delete

**Status enum** (`payment_status`):
`pending`, `initiated`, `processing`, `paid`, `failed`, `cancelled`, `refunded`, `expired`

### payment_processor_products

Maps products/variants to Polar products for checkout reuse.

| Column | Type | Notes |
|--------|------|-------|
| id | uuid PK | gen_random_uuid() |
| product_id | uuid FK → products | NOT NULL |
| variant_id | uuid FK → product_variants | NULLABLE |
| price_id | uuid FK → product_prices | NOT NULL |
| currency_code | varchar | NOT NULL |
| price | numeric | NOT NULL, CHECK > 0 |
| processor | text | DEFAULT 'polar' |
| processor_product_id | text | NOT NULL — Polar product ID |
| processor_price_id | text | nullable — Polar price ID |
| sync_status | processor_sync_status | DEFAULT 'synced' |
| last_synced_at | timestamptz | DEFAULT now() |
| soft_delete | boolean | DEFAULT false |
| created_at | timestamptz | DEFAULT now() |
| updated_at | timestamptz | DEFAULT now() |

**Unique constraint:** `(product_id, variant_id, currency_code, processor)`
**Indexes:** product_id, variant_id, processor_product_id, sync_status, processor, soft_delete

**Sync status enum** (`processor_sync_status`):
`synced`, `outdated`, `failed`, `archived`

### Access Control Policies

- **Users:** SELECT own payments (via order ownership)
- **Editors:** Full CRUD on both tables
- **Service role:** Bypasses policies (used by sync + webhook)

---

## Architecture & Data Flow

### Module Structure

```
src/lib/modules/payment/
├── actions.ts              → Server actions (initiate, cancel, status)
├── service.ts              → PaymentService orchestrator
├── types.ts                → PaymentRecord, PaymentStatus, etc.
├── repository.ts           → PaymentRepository (payments + payment_processor_products queries)
│
└── polar/
    ├── client.ts           → Raw HTTP calls to Polar API
    ├── types.ts            → Polar API response types
    ├── product-sync.ts     → syncVariantToProcessor(), buildLineItems()
    └── service.ts          → PolarService (checkout sessions, confirm, cancel)
```

### Data Flow

```
Cart → Checkout → Place Order
  │
  ├─ placeOrderAction (cart → pending)
  │
  ├─ initiatePaymentAction
  │   ├─ PaymentService.initiatePayment()
  │   │   ├─ Load order + items
  │   │   ├─ buildLineItems()
  │   │   │   └─ syncVariantToProcessor() for each item
  │   │   │       ├─ Check payment_processor_products cache
  │   │   │       ├─ MISS → POST /v1/products/ → INSERT cache
  │   │   │       └─ HIT → return processor_product_id
  │   │   ├─ PolarService.createCheckoutSession()
  │   │   │   └─ POST /v1/checkouts/ with product IDs
  │   │   └─ INSERT payments record
  │   └─ Return checkout URL
  │
  └─ Redirect to Polar checkout
      │
      ├─ Success → /orders/{orderNumber}
      │
      └─ Cancel → /orders/{orderNumber}

Webhook (async)
  │
  ├─ order.paid → PaymentService.confirmPayment()
  │   ├─ UPDATE payments SET status='paid'
  │   └─ UPDATE orders SET status='confirmed'
  │
  └─ checkout.expired → PaymentService.cancelPayment()
      └─ UPDATE payments SET status='expired'
```

### Key Files

| File | Purpose |
|------|---------|
| `polar/client.ts` | HTTP layer — polarCreateProduct, polarCreateCheckout, polarUpdateProduct |
| `polar/product-sync.ts` | Sync logic — cache lookup, create/update in Polar, DB persistence |
| `polar/service.ts` | Checkout orchestration — createCheckoutSession, confirmPayment |
| `payment/service.ts` | Facade — initiatePayment, confirmPayment, cancelPayment |
| `payment/actions.ts` | Server actions — expose to frontend |
| `payment/repository.ts` | Data access — queries for payments + payment_processor_products |
| `api/webhooks/polar/route.ts` | Webhook handler — process Polar events |

### Environment Variables

```
POLAR_ACCESS_TOKEN=pol_oat_xxxxx
POLAR_WEBHOOK_SECRET=whsec_xxxxx
POLAR_ORGANIZATION_ID=org_xxxxx
NEXT_PUBLIC_POLAR_SANDBOX=true
```

### API Endpoints Used

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/v1/products/` | POST | Create product in Polar |
| `/v1/products/{id}` | GET | Get product details |
| `/v1/products/{id}` | PATCH | Update product (price, name) |
| `/v1/checkouts/` | POST | Create checkout session |
| `/v1/checkouts/{id}` | GET | Get checkout status |
