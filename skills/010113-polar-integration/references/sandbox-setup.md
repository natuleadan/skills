# Sandbox & Setup

## Sandbox Environment

### Overview

- Isolated from production — `sandbox.polar.sh`
- Separate user account and organization required
- No real money processing — safe for testing
- Unlimited accounts for testing different scenarios
- Test payments using Stripe test cards: `4242 4242 4242 4242`

### API Configuration

- **Sandbox Base URL:** `https://sandbox-api.polar.sh`
- **Production Base URL:** `https://api.polar.sh`
- Access token must be created IN sandbox — production tokens don't work
- SDK parameter: `server: 'sandbox'`

### Environment Variables

```
POLAR_ACCESS_TOKEN=pol_oat_xxxxx       # Must be sandbox token
POLAR_WEBHOOK_SECRET=whsec_xxxxx       # Must be sandbox webhook secret
POLAR_ORGANIZATION_ID=org_xxxxx        # Sandbox organization ID
NEXT_PUBLIC_POLAR_SANDBOX=true         # Enables sandbox mode
```

### SDK Sandbox Configuration

```typescript
function getBaseUrl(): string {
  return process.env.NEXT_PUBLIC_POLAR_SANDBOX === "true"
    ? "https://sandbox-api.polar.sh"
    : "https://api.polar.sh";
}
```

### Webhook Configuration

1. Configure in Sandbox Dashboard → Settings → Webhooks
2. URL: `https://your-domain.com/api/webhooks/polar`
3. Subscribe to: `order.paid`, `order.created`, `checkout.expired`, `checkout.canceled`

### Testing Payments

1. Add a product to your app's cart
2. Proceed to checkout — you'll be redirected to Polar's hosted payment page
3. Use Stripe test card: `4242 4242 4242 4242`
4. Future expiration date + any CVC
5. Complete customer funnel including checkout redirect
6. Verify webhook receives `order.paid` event

### Limitations

- Subscriptions auto-canceled 90 days after creation
- No real payouts or transfers
- Separate data from production — no cross-environment queries

---

## MCP Integration

Polar offers MCP (Model Context Protocol) servers for AI-assisted workflows:

- **Sandbox MCP:** `https://mcp.polar.sh/mcp/polar-sandbox`
- **Production MCP:** `https://mcp.polar.sh/mcp/polar-mcp`

---

## Polar CLI for Local Development

### Install

```bash
curl -fsSL https://polar.sh/install.sh | bash
```

### Login

```bash
polar login
```

### Listen for Webhooks

```bash
polar listen http://localhost:3000/
```

The CLI generates a webhook secret — copy it to your `.env`:
```
POLAR_WEBHOOK_SECRET=whsec_xxxxx
```

The secret from `polar listen` MUST match `POLAR_WEBHOOK_SECRET` in `.env` or signature verification will fail (403).

---

## Production Setup Checklist

- [ ] Create production organization at `polar.sh`
- [ ] Generate production `POLAR_ACCESS_TOKEN` (format: `polar_oat_*`)
- [ ] Set `NEXT_PUBLIC_POLAR_SANDBOX=false` (or omit the variable)
- [ ] Configure production webhook endpoint URL
- [ ] Set `POLAR_WEBHOOK_SECRET` from production dashboard
- [ ] Test end-to-end flow with a real $1 product before going live
- [ ] Never expose `POLAR_ACCESS_TOKEN` in client-side code
- [ ] Verify webhook route is excluded from auth middleware
