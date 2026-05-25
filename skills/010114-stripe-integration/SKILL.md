---
name: 010114-stripe-integration
description: Stripe payment integration — Checkout Sessions, PaymentIntents, Connect, billing, Treasury, and migration from deprecated APIs.
license: MIT
compatibility: Requires Node.js 20+ or Bun 1.2+ and internet access
---

# Stripe Integration

Latest Stripe API version: **2026-03-25.dahlia**. Always use the latest API version and SDK.

## Integration Routing

| Building... | Recommended API | Details |
|---|---|---|
| One-time payments | Checkout Sessions | [Payments](references/payments.md) |
| Custom payment form with embedded UI | Checkout Sessions + Payment Element | [Payments](references/payments.md) |
| Saving a payment method for later | Setup Intents | [Payments](references/payments.md) |
| Connect platform or marketplace | Accounts v2 (`/v2/core/accounts`) | [Connect](references/connect.md) |
| Subscriptions or recurring billing | Billing APIs + Checkout Sessions | [Billing](references/billing.md) |
| Embedded financial accounts / banking | v2 Financial Accounts | [Treasury](references/treasury.md) |

## Quick Reference

### API Hierarchy (most to least recommended)
1. **Checkout Sessions** — Hosted payment page, minimal PCI burden
2. **PaymentIntents** — Custom payment UI with Payment Element
3. **SetupIntents** — Save payment methods for future use

### Environment Variables
- `STRIPE_SECRET_KEY` — Server-side API key (sk_live_... or sk_test_...)
- `STRIPE_WEBHOOK_SECRET` — Webhook signature verification (whsec_...)
- `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY` — Client-side (pk_live_... or pk_test_...)

## References

- [Payments](references/payments.md) — Checkout Sessions, PaymentIntents, SetupIntents, migration
- [Billing](references/billing.md) — Subscriptions, Customer Portal
- [Connect](references/connect.md) — Platforms, marketplaces, Accounts v2
- [Treasury](references/treasury.md) — Financial Accounts v2
- [Installation](references/install.md) — Stripe CLI setup
- [Projects CLI](references/projects-cli.md) — Stripe Projects commands
