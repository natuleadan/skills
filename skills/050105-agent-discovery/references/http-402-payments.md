# HTTP 402 Payments (x402 & MPP)

Machine-to-machine payment protocols using the HTTP 402 `Payment Required` status code. Two standards exist: **x402** (Coinbase, USDC on Base) and **MPP** (Tempo/Stripe, multi-method). Both follow the same core challenge–credential–receipt flow.

## HTTP 402 Payment Required

The 402 status code was reserved in the original HTTP specification for "Payment Required" but never standardized. Recent machine-to-machine payment protocols have revived it as the signal for pay-per-use API access, eliminating API keys, subscriptions, and billing portals.

## Core Payment Flow

Both x402 and MPP share the same four-step flow:

```
1. Client Request      →  Agent/App requests a resource
2. 402 + Challenge     ←  Server responds with cost and payment options
3. Retry + Credential  →  Client attaches signed payment proof
4. Resource + Receipt  ←  Server verifies and returns the resource
```

## x402 Protocol (Coinbase)

x402 is an open payments protocol by Coinbase that uses the 402 status code for autonomous AI agent payments, primarily with USDC on Base (Ethereum L2).

### Server Middleware

```javascript
import { x402PaymentRequired } from "@x402/express-middleware"

app.get("/premium-data",
  x402PaymentRequired({
    amount: "0.10",
    address: "0x1234...",
    assetAddress: "0xA0b86991...",
    network: "base-mainnet",
  }),
  (req, res) => {
    res.json({ data: "Premium content" })
  }
)
```

### 402 Response Format

```json
{
  "maxAmountRequired": "0.10",
  "resource": "/api/market-data",
  "description": "Access to real-time market data requires payment.",
  "payTo": "0xABCDEF1234567890...",
  "asset": "0xA0b86991C6218b36c1d19D4a2e9Eb0cE3606EB48",
  "network": "base-mainnet",
  "expiresAt": "2025-05-25T12:00:00Z",
  "nonce": "a1b2c3d4",
  "paymentId": "pay_abc123"
}
```

| Field | Description |
|---|---|
| `maxAmountRequired` | Payment amount (e.g., `"0.10"`) |
| `resource` | The requested API endpoint |
| `description` | Human-readable payment description |
| `payTo` | Developer's wallet address |
| `asset` | Token contract address (USDC) |
| `network` | Blockchain identifier (e.g., `base-mainnet`) |
| `expiresAt` | Timestamp after which the request is invalid |
| `nonce` | Unique identifier to prevent replay attacks |

### Client-Side Flow

```javascript
import { x402Client } from "@x402/client"

const client = new x402Client()
client.setWallet(await connectWallet())

const data = await client.fetch("https://api.example.com/premium-data")
```

The client intercepts 402 responses, presents payment confirmation to the user, signs an EIP-712 message, attaches it to the retried request, and returns the response on success.

### Wallet Integration

When payment is required, the wallet displays: request domain, payment amount, token, and specific resource. Users confirm in one click — no API keys or accounts.

## MPP — Machine Payments Protocol

MPP is an open standard proposed to the IETF, developed by Tempo Labs and Stripe. It generalizes HTTP 402 to support any payment method via an extensible challenge–credential–receipt flow.

### Payment Flow

```http
# Step 1: Client requests resource
GET /premium-data HTTP/1.1

# Step 2: Server challenges with 402
HTTP/1.1 402 Payment Required
WWW-Authenticate: MPP challenge="eyJhbGciOiJIUzI1NiIs..."

# Step 3: Client responds with payment credential
GET /premium-data HTTP/1.1
Authorization: MPP credential="eyJwYXltZW50SWQiOiJ..."

# Step 4: Server verifies and returns resource
HTTP/1.1 200 OK
Payment-Receipt: MPP receipt="eyJzdGF0dXMiOiJ..."
```

### Headers

| Header | Direction | Description |
|---|---|---|
| `WWW-Authenticate: MPP challenge=...` | Server → Client | Payment requirements, supported methods, prices |
| `Authorization: MPP credential=...` | Client → Server | Signed payment proof |
| `Payment-Receipt: MPP receipt=...` | Server → Client | Proof of delivery / payment acceptance |

### Challenge Structure

```json
{
  "version": "1",
  "challengeId": "ch_abc123",
  "methods": [
    {
      "name": "tempo",
      "currencies": ["USDC.e"],
      "chains": ["base-mainnet"],
      "charge": { "amount": "0.10", "currency": "USDC.e" }
    },
    {
      "name": "stripe",
      "currencies": ["USD"],
      "charge": { "amount": "0.10", "currency": "USD" }
    }
  ],
  "reason": "Payment required for premium data",
  "expiresAt": "2025-05-25T12:00:00Z"
}
```

### Payment Methods

| Method | Type | Settlement | Use Case |
|---|---|---|---|
| Tempo (stablecoins) | On-chain | ~200ms | Agentic payments, micropayments |
| Stripe (cards) | Card network | Instant auth | Human users, cards/wallets |
| Lightning (Bitcoin) | L2 | Instant | Bitcoin micropayments |
| Solana | L2 | ~400ms | SOL/SPL token payments |
| Stellar | L1 | ~5s | SEP-41 token payments |
| RedotPay | Hybrid | Instant | Balance/stablecoin rails |
| Custom | Any | Varies | Extensible via method API |

### Sessions (Pay-as-You-Go)

MPP supports sessions for high-frequency payments. Client deposits funds into a payment channel; each request deducts from the balance without on-chain transactions:

```javascript
const session = await client.session.create({
  method: "tempo",
  deposit: "5.00",
  maxPerRequest: "0.05",
})

const data = await session.fetch("https://api.example.com/stream-data")
```

### Subscriptions (Recurring)

MPP supports recurring billing with scoped access keys:

```javascript
const sub = await client.subscription.create({
  method: "tempo",
  amount: "9.99",
  interval: "monthly",
})
```

## Discovery Integration

### MCP Server Cards

x402 payment metadata can be linked from MCP Server Cards for pre-connection discovery:

```json
{
  "payment": {
    "href": "https://example.com/.well-known/mcp/pay.json",
    "rel": "payment-policy",
    "rails": ["x402"]
  }
}
```

### OpenAPI Discovery

MPP defines an OpenAPI extension for advertising payment terms:

```yaml
paths:
  /premium-data:
    get:
      x-mpp-payment:
        amount: "0.10"
        currency: "USDC.e"
        methods: ["tempo", "stripe"]
```

Agents can discover costs before making requests, enabling autonomous budgeting decisions.

## SDK Reference

| Platform | Server Middleware | Client Library |
|---|---|---|
| TypeScript | Express, Next.js, Elysia, Hono | `Mppx.create()`, `Fetch.polyfill()` |
| Python | FastAPI | `mppx.Client` |
| Rust | Axum | `mppx.Client` |
| Go | net/http | `mppx.Client` |
| Ruby | Rack | `mppx.Client` |

```javascript
// TypeScript server (Elysia)
import { mppx } from "mppx/elysia"

app.use(mppx({
  methods: [tempo({ secret: process.env.MPP_SECRET_KEY })],
}))

// TypeScript client
import { mppx } from "mppx/client"

const fetch = mppx.create({ wallet })
const data = await fetch("https://api.example.com/premium-data")
```

## Security Considerations

- **HMAC Challenges**: Server signs challenges with a secret key. Clients verify before paying.
- **Replay prevention**: Each challenge includes a unique `nonce` and `expiresAt`. Credentials are single-use.
- **Body digest**: Request bodies can be hashed in the credential to bind payment to a specific request.
- **Server verification**: Credentials are verified server-side before processing the request.
- **Secret management**: `MPP_SECRET_KEY` must be kept server-side, never logged, and rotated safely.

## Comparison: x402 vs MPP

| Aspect | x402 | MPP |
|---|---|---|
| Developed by | Coinbase | Tempo Labs + Stripe |
| Standardization | Whitepaper | IETF proposal |
| Payment methods | USDC on Base (primary) | Stablecoins, cards, Lightning, Solana, Stellar, custom |
| Sessions | No | Yes (payment channels) |
| Subscriptions | No | Yes |
| SDK languages | JS/TS | TypeScript, Python, Rust, Go, Ruby |
| Framework support | Express | Express, Next.js, Elysia, Hono, FastAPI, Axum, Rack |
| Discovery | Inline in 402 | OpenAPI + inline |
| MCP integration | Payment field in Server Card | Full MCP transport + middleware |

## Relationship to MCP

Both x402 and MPP can monetize MCP servers on a per-tool-call basis:

```
MCP Server → registerTool() + payment middleware
Client     → 402 → pay → retry with credential → tool result
```

MPP provides an official MCP transport for payment-gated JSON-RPC tool calls. The MCP transport maps Challenges, Credentials, and Receipts to MCP protocol messages, enabling payment without leaving the MCP protocol.
