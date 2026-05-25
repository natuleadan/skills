# Elysia MPP Payment Middleware

Native Elysia middleware that gates routes behind MPP payment intents using HTTP 402.

## Install

```bash
bun add mppx elysia
# or
npm install mppx elysia
```

## Quick Start

Import `Mppx` and `tempo` from `mppx/elysia` to create an Elysia-aware payment handler.

### Route Guard

Use `.guard()` with `beforeHandle` to scope payment to specific routes:

```typescript
import { Elysia } from "elysia"
import { Mppx, tempo } from "mppx/elysia"

const mppx = Mppx.create({ methods: [tempo()] })

const app = new Elysia()
  .guard(
    { beforeHandle: mppx.charge({ amount: "1" }) },
    (app) => app.get("/premium", () => ({ data: "paid content" })),
  )
```

### Global Application

Use `.onBeforeHandle()` to apply payment to all routes:

```typescript
import { Elysia } from "elysia"
import { Mppx, tempo } from "mppx/elysia"

const mppx = Mppx.create({ methods: [tempo()] })

const app = new Elysia()
  .onBeforeHandle(mppx.charge({ amount: "1" }))
  .get("/premium", () => ({ data: "paid content" }))
  .get("/another", () => ({ data: "also paid" }))
```

### Session Payments

Use `mppx.session()` to gate routes behind session-based payment intents for pay-as-you-go billing:

```typescript
import { Elysia } from "elysia"
import { Mppx, tempo } from "mppx/elysia"

const mppx = Mppx.create({ methods: [tempo()] })

const app = new Elysia()
  .guard(
    { beforeHandle: mppx.session({ amount: "1", unitType: "token" }) },
    (app) => app.get("/content", () => ({ data: "session content" })),
  )
```

## Identifying the Payer

After payment verification, the `Authorization` header still contains the credential. Parse it to read the payer's identity:

```typescript
import { Credential } from "mppx"
import { Mppx, tempo } from "mppx/elysia"

const mppx = Mppx.create({ methods: [tempo()] })

const app = new Elysia()
  .guard(
    { beforeHandle: mppx.charge({ amount: "1" }) },
    (app) =>
      app.get("/premium", ({ request }) => {
        const credential = Credential.deserialize(request.headers.get("Authorization")!)
        const payer = credential.source // "did:pkh:eip155:1:0x..."
        return { payer }
      }),
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
import { Mppx, tempo, stripe } from "mppx/elysia"

const mppx = Mppx.create({
  methods: [
    tempo(),
    stripe({ secretKey: process.env.STRIPE_SECRET_KEY }),
  ],
})
```

For the full protocol specification and method details, see `050105-agent-discovery/references/http-402-payments.md`.
