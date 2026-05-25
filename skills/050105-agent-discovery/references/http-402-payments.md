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

MPP is an open standard submitted to the IETF as [`draft-ryan-httpauth-payment`](https://datatracker.ietf.org/doc/draft-ryan-httpauth-payment/), developed by Tempo Labs and Stripe. The full specification suite is published at [paymentauth.org](https://paymentauth.org/). MPP generalizes HTTP 402 to support any payment method via an extensible challenge–credential–receipt flow.

### Architecture

MPP follows a modular architecture separating stable protocol mechanics from evolving payment ecosystems:

```
Core        → HTTP 402 semantics, "Payment" auth scheme, headers, IANA registries
Intents     → Abstract payment patterns (charge, authorize, subscription)
Methods     → Concrete implementations for specific networks (Tempo, Stripe, Lightning, etc.)
Extensions  → Optional additions (discovery, identity, MCP transport)
```

### Design Principles

1. **Extensible core**: Minimal protocol designed for safe extension.
2. **Network agnostic and multi-rail**: Supports bank rails, credit cards, and stablecoins.
3. **Currency agnostic**: No implicit advantages for any currency or asset.
4. **Durable by design**: Follows web standards; security and replay protection are first-class concerns.

### IETF Draft

The core specification is [`draft-ryan-httpauth-payment`](https://datatracker.ietf.org/doc/draft-ryan-httpauth-payment/) — "The 'Payment' HTTP Authentication Scheme". It registers the `Payment` auth scheme with IANA and defines the 402 flow semantics.

### Payment Flow

```http
# Step 1: Client requests resource
GET /premium-data HTTP/1.1

# Step 2: Server challenges with 402
HTTP/1.1 402 Payment Required
WWW-Authenticate: Payment challenge="eyJhbGciOiJIUzI1NiIs..."

# Step 3: Client responds with payment credential
GET /premium-data HTTP/1.1
Authorization: Payment credential="eyJwYXltZW50SWQiOiJ..."

# Step 4: Server verifies and returns resource
HTTP/1.1 200 OK
Payment-Receipt: Payment receipt="eyJzdGF0dXMiOiJ..."
```

### Headers

| Header | Direction | Description |
|---|---|---|
| `WWW-Authenticate: Payment challenge=...` | Server → Client | Payment requirements, supported methods, prices |
| `Authorization: Payment credential=...` | Client → Server | Signed payment proof |
| `Payment-Receipt: Payment receipt=...` | Server → Client | Proof of delivery / payment acceptance |

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

| Method | Type | Settlement | Draft |
|---|---|---|---|---|
| Tempo (stablecoins) | On-chain | ~200ms | [`draft-tempo-charge`](https://paymentauth.org/) |
| Stripe (cards) | Card network | Instant auth | [`draft-stripe-charge`](https://paymentauth.org/) |
| EVM (ERC-20) | L2 | ~200ms | [`draft-evm-charge`](https://paymentauth.org/) |
| Lightning (Bitcoin) | L2 | Instant | [`draft-lightning-charge`](https://paymentauth.org/) |
| Solana | L2 | ~400ms | [`draft-solana-charge`](https://paymentauth.org/) |
| Stellar | L1 | ~5s | [`draft-stellar-charge`](https://paymentauth.org/) |
| Hedera | L1 | ~5s | [`draft-hedera-charge`](https://paymentauth.org/) |
| RedotPay | Hybrid | Instant | RedotPay |
| Custom | Any | Varies | Extensible via method API |

Each method spec defines the request schema, Credential format, and server verification logic for its specific network.

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

### Payment Discovery Draft

The IETF [`draft-payment-discovery`](https://paymentauth.org/) defines a standard way for services to advertise their payment terms. Clients can discover costs and supported methods before making requests, enabling autonomous budgeting decisions.

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

For framework-specific integration guides:

- **Elysia**: See `050101-elysia-framework/references/elysia-payment-middleware.md`
- **Next.js**: See `050102-nextjs-framework/references/mpp-payment-middleware.md`

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
| Standardization | Whitepaper | IETF draft (`draft-ryan-httpauth-payment`) |
| Auth scheme | Custom JSON body | `WWW-Authenticate: Payment` (IANA registered) |
| Payment methods | USDC on Base (primary) | 8 methods: Tempo, Stripe, EVM, Lightning, Solana, Stellar, Hedera, RedotPay |
| Sessions | No | Yes (Lightning, Tempo) |
| Subscriptions | No | Yes (Tempo) |
| SDK languages | JS/TS | TypeScript, Python, Rust, Go, Ruby |
| Framework support | Express | Express, Next.js, Elysia, Hono, FastAPI, Axum, Rack |
| Discovery | Inline in 402 | `draft-payment-discovery` + OpenAPI |
| MCP integration | Payment field in Server Card | `draft-payment-transport-mcp` (JSON-RPC + MCP) |

## Relationship to MCP

Both x402 and MPP can monetize MCP servers on a per-tool-call basis:

```
MCP Server → registerTool() + payment middleware
Client     → 402 → pay → retry with credential → tool result
```

### MCP Transport (IETF Draft)

The IETF [`draft-payment-transport-mcp`](https://paymentauth.org/) defines a JSON-RPC and MCP transport for MPP. It maps Challenges, Credentials, and Receipts to MCP protocol messages, enabling payment without leaving the MCP protocol:

```
MCP Request (tool call)
  ↓
MCP Response (402: Payment required)
  → JSON-RPC error with Challenge embedded
  ↓
MCP Request (retry with Credential)
  ↓
MCP Response (tool result + Receipt)
```

This transport works with both MCP over HTTP and MCP over JSON-RPC. The MCP transport spec is maintained alongside the core MPP specs at [paymentauth.org](https://paymentauth.org/).

## IANA Registration

The core MPP spec registers the `Payment` HTTP Authentication Scheme with IANA. This means compliant HTTP clients and servers can use the standard `WWW-Authenticate` and `Authorization` header parsing logic rather than custom headers.
