---
name: 010113-polar-integration
description: Polar.sh payment integration — product sync, checkout sessions, webhooks, schema design, multi-currency, MoR model, sandbox testing, and API reference.
---

# Polar.sh Payment Integration

## Overview

Polar.sh is a Merchant of Record (MoR) platform that handles payment processing, tax collection, and billing. This skill covers the full integration flow: product synchronization, checkout sessions, webhook handling, database schema, and sandbox testing.

## Architecture

```
Products DB → Sync Service → Polar API (Products/Variants/Prices)
                                       ↓
Client → Checkout Session → Polar Hosted Flow → Order Created
                                       ↓
Polar → Webhook → Application → Update Payment Status → Fulfillment
```

## Quick Reference

### Environment Variables
- `POLAR_ACCESS_TOKEN` — Server-side API token (format: `polar_oat_*`)
- `POLAR_WEBHOOK_SECRET` — Webhook signature verification
- `NEXT_PUBLIC_POLAR_SANDBOX` — Toggle sandbox/production (`true` or omitted)

### Core Flows
1. **Sync products** to Polar before checkout — each product+variant+currency becomes a Polar product
2. **Create checkout session** with line items and metadata — Polar handles the hosted payment UI
3. **Handle webhooks** for order lifecycle events (`order.paid`, `checkout.expired`, etc.)
4. **Verify signatures** using Standard Webhooks spec — `@polar-sh/nextjs` handles this automatically

### Supported Countries
Polar supports 50+ countries including US, EU, UK, Canada, Australia, Brazil, Mexico, Colombia, Peru, Chile, and others. See [Payment Flow](references/payment-flow.md) for MoR model details.

## References

- [Payment Flow](references/payment-flow.md) — Product sync, checkout, multi-currency, error handling, MoR model
- [Webhooks & Schema](references/webhooks-schema.md) — Webhook events, DB schema, signature verification
- [API Reference](references/api-reference.md) — Polar REST API essentials (auth, products, checkout, orders)
- [Sandbox & Setup](references/sandbox-setup.md) — Sandbox environment, API keys, webhook configuration
