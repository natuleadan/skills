# Next.js MPP Payment Middleware

Native Next.js route handler wrapper that gates routes behind MPP payment intents using HTTP 402.

## Install

```bash
npm install mppx
# or
bun add mppx
```

## Quick Start

Import `Mppx` and `tempo` from `mppx/nextjs` to create a Next.js-aware payment handler. Each intent returns a wrapper that accepts a route handler.

### One-Time Payments

```typescript
// app/api/premium/route.ts
import { Mppx, tempo } from "mppx/nextjs"

const mppx = Mppx.create({ methods: [tempo()] })

export const GET = mppx.charge({ amount: "1" })(
  () => Response.json({ data: "paid content" }),
)
```

### Session Payments

Use `mppx.session()` for pay-as-you-go billing with prepaid balance:

```typescript
// app/api/content/route.ts
import { Mppx, tempo } from "mppx/nextjs"

const mppx = Mppx.create({ methods: [tempo()] })

export const GET = mppx.session({ amount: "1", unitType: "token" })(
  () => Response.json({ data: "session content" }),
)
```

## Identifying the Payer

After payment verification, parse the `Authorization` header to read the payer's identity:

```typescript
// app/api/premium/route.ts
import { Credential } from "mppx"
import { Mppx, tempo } from "mppx/nextjs"

const mppx = Mppx.create({ methods: [tempo()] })

export const GET = mppx.charge({ amount: "1" })(
  (request) => {
    const credential = Credential.deserialize(request.headers.get("Authorization")!)
    const payer = credential.source // "did:pkh:eip155:1:0x..."
    return Response.json({ payer })
  },
)
```

## Intents

| Intent | Method | Description |
|---|---|---|
| One-time | `mppx.charge({ amount })` | Pay once per request before receiving the resource |
| Session | `mppx.session({ amount, unitType })` | Pay-as-you-go with prepaid balance and per-request billing |

## Payment Methods

Register the methods your server supports:

```typescript
import { Mppx, tempo, stripe } from "mppx/nextjs"

const mppx = Mppx.create({
  methods: [
    tempo(),
    stripe({ secretKey: process.env.STRIPE_SECRET_KEY }),
  ],
})
```

For the full protocol specification and method details, see `050105-agent-discovery/references/http-402-payments.md`.
