# Multi-Tier API Key Configuration

## Architecture

Multiple API key configurations for different access tiers. Each tier has its own prefix, rate limits, and permissions.

```typescript
apiKey([
  {
    configId: "basic",
    defaultPrefix: "basic_",
    rateLimit: { maxRequests: 100, timeWindow: 60 * 60 * 1000 },
  },
  {
    configId: "pro",
    defaultPrefix: "pro_",
    rateLimit: { maxRequests: 10000, timeWindow: 60 * 60 * 1000 },
    enableMetadata: true,
  },
  {
    configId: "enterprise",
    defaultPrefix: "ent_",
    rateLimit: { maxRequests: 100000, timeWindow: 60 * 60 * 1000 },
    enableMetadata: true,
  },
])
```

## Creating Keys Per Tier

```typescript
export async function assignKey(userId: string, tier: string) {
  const { data, error } = await auth.api.createApiKey({
    body: {
      userId,
      name: `Plan ${tier}`,
      configId: tier,
      permissions: {
        reports: tier === "enterprise" ? ["read", "export"] : ["read"],
        api: ["read"],
      },
    },
  })
  return { key: data?.key, error }
}
```

## Enforcing Tier in Endpoints

```typescript
.get("/reports", async ({ request }) => {
  const apiKey = request.headers.get("x-api-key")
  const result = await auth.api.verifyApiKey({
    body: { key: apiKey, permissions: { reports: ["read"] } },
  })
  if (!result.valid) return { status: 403 }
  if (result.key?.configId === "basic") {
    return { status: 403, error: "Upgrade required for reports" }
  }
  return { data: await getReports() }
}, { auth: true })
```

## Tier Pricing Pattern

| Tier | Prefix | Rate Limit | Access |
|------|--------|------------|--------|
| Basic | `basic_` | 100 req/h | Public endpoints |
| Pro | `pro_` | 10k req/h | + Reports (read) |
| Enterprise | `ent_` | 100k req/h | + Reports (export) |

Each endpoint checks `configId` and `permissions`. Invalid tier → 403.
