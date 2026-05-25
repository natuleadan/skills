# Universal Commerce Protocol (UCP)

Open standard enabling interoperability between commerce entities (businesses, platforms, Payment Service Providers, AI agents) through standardized discovery, capability negotiation, and multi-transport support.

## Overview

UCP addresses fragmented commerce by providing a common language and functional primitives. It enables platforms (including AI agents) to autonomously discover merchant capabilities, negotiate supported features, and complete purchases — with or without human intervention.

### Key Features

- **Composable Architecture**: Capabilities (e.g., Checkout, Order) and Extensions (e.g., Discounts, Fulfillment) allow flexible implementation.
- **Dynamic Discovery**: Businesses declare supported capabilities in a standardized profile at `/.well-known/ucp`. Platforms discover and configure autonomously.
- **Transport Agnostic**: REST, MCP (Model Context Protocol), A2A (Agent-to-Agent), or Embedded protocols.
- **Built on Standards**: OAuth 2.0, JWK, OpenAPI, OpenRPC, JSON Schema.

## Well-Known Discovery

Businesses publish their UCP profile at `/.well-known/ucp`:

```json
{
  "ucp": {
    "version": "2026-04-08",
    "services": { ... },
    "capabilities": { ... },
    "payment_handlers": { ... }
  },
  "signing_keys": [
    {
      "kid": "business_2025",
      "kty": "EC",
      "crv": "P-256",
      "use": "sig",
      "alg": "ES256"
    }
  ]
}
```

Platforms fetch this profile to discover available capabilities, transports, and supported versions.

## Namespace Governance

UCP uses reverse-domain naming to encode governance authority into capability identifiers, eliminating the need for a central registry.

### Naming Convention

```
{reverse-domain}.{service}.{capability}
```

| Name | Authority | Service | Capability |
|---|---|---|---|
| `dev.ucp.shopping.checkout` | ucp.dev | shopping | checkout |
| `dev.ucp.shopping.fulfillment` | ucp.dev | shopping | fulfillment |
| `dev.ucp.common.identity_linking` | ucp.dev | common | identity_linking |
| `com.example.payments.installments` | example.com | payments | installments |

### Spec URL Binding

The origin of `spec` and `schema` URLs MUST match the namespace authority. Platforms MUST validate this binding.

## Capabilities & Extensions

### Capability Definition

```json
{
  "dev.ucp.shopping.checkout": [{
    "version": "2026-04-08",
    "spec": "https://ucp.dev/2026-04-08/specification/checkout",
    "schema": "https://ucp.dev/2026-04-08/schemas/shopping/checkout.json"
  }]
}
```

### Extension Pattern

Extensions augment existing capabilities using the `extends` field:

```json
{
  "dev.ucp.shopping.fulfillment": [{
    "version": "2026-04-08",
    "extends": "dev.ucp.shopping.checkout"
  }],
  "dev.ucp.shopping.discount": [{
    "version": "2026-04-08",
    "extends": ["dev.ucp.shopping.checkout", "dev.ucp.shopping.cart"]
  }]
}
```

Multi-parent extensions extend more than one capability (e.g., discounts apply during both checkout and cart).

### Schema Composition

Extensions modify base schemas via JSON Schema `allOf` chains. Extension schemas declare composed types with `$defs` keys matching parent capability names:

```json
{
  "$defs": {
    "dev.ucp.shopping.checkout": {
      "allOf": [
        { "$ref": "checkout.json" },
        {
          "properties": {
            "discounts": { "$ref": "#/$defs/discounts_object" }
          }
        }
      ]
    }
  }
}
```

## Negotiation Protocol

### Platform Advertisement

Platforms communicate their profile URI with every request:

**HTTP Transport:**
```http
POST /checkout HTTP/1.1
UCP-Agent: profile="https://agent.example/profiles/shopping-agent.json"
```

**MCP Transport:**
```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "create_checkout",
    "arguments": {
      "meta": {
        "ucp-agent": {
          "profile": "https://agent.example/profiles/shopping-agent.json"
        }
      }
    }
  }
}
```

### Intersection Algorithm

1. **Compute intersection**: Include business capability if platform declares the same name.
2. **Select version**: For each intersected capability, pick the highest mutual version (latest date). Exclude if no mutual version.
3. **Prune orphaned extensions**: Remove extensions whose parent capabilities are not in the intersection. For multi-parent, at least one parent must be present.
4. **Repeat** until no more removals (handles transitive extension chains).

### Response Capability Declaration

Businesses MUST include active capabilities in every response:

```json
{
  "ucp": {
    "version": "2026-04-08",
    "capabilities": ["dev.ucp.shopping.checkout", "dev.ucp.shopping.fulfillment"]
  },
  "checkout": { ... }
}
```

## Transports

| Transport | Spec Format | Use Case |
|---|---|---|
| REST | OpenAPI 3.x (JSON) | General-purpose HTTP APIs |
| MCP | OpenRPC (JSON) | AI agent tool calls |
| A2A | Agent Card Specification | Agent-to-agent communication |
| Embedded | OpenRPC (JSON) | In-page/iframe checkout |

Service definitions declare available transports with endpoint URLs:

```json
{
  "dev.ucp.shopping": [{
    "version": "2026-04-08",
    "transport": "rest",
    "endpoint": "https://business.example.com/ucp/v1",
    "schema": "https://ucp.dev/2026-04-08/services/shopping/rest.openapi.json"
  }, {
    "transport": "mcp",
    "endpoint": "https://business.example.com/ucp/mcp"
  }]
}
```

## Payment Architecture

### Trust Triangle

UCP defines a trust triangle between three parties:

- **Platform** (e.g., AI agent, shopping app) — initiates checkout, handles user interaction
- **Business** (merchant) — provides goods/services, owns the checkout session
- **Payment Credential Provider** (PSP, wallet) — handles payment credential issuance and verification

### Payment Handlers

Payment handlers declare supported instruments and tokenization methods:

```json
{
  "com.example.processor_tokenizer": [{
    "id": "processor_tokenizer",
    "available_instruments": [{
      "type": "card",
      "constraints": { "brands": ["visa", "mastercard", "amex"] }
    }],
    "config": {
      "type": "CARD",
      "tokenization_specification": {
        "type": "PUSH",
        "parameters": {
          "token_retrieval_url": "https://api.psp.example.com/v1/tokens"
        }
      }
    }
  }]
}
```

### AP2 Mandates (Autonomous Agents)

For agentic commerce without human intervention, UCP supports AP2 (Agent-to-PSP) mandates. Agents hold pre-authorized payment mandates from credential providers, enabling autonomous checkout without redirecting the user.

### PCI Scope

UCP's payment architecture keeps PCI-sensitive data within the Payment Credential Provider's scope. Platforms and businesses handle tokenized credentials only.

## Identity & Authentication

UCP uses OAuth 2.0 for Identity Linking, enabling platforms to act on behalf of users:

```json
{
  "dev.ucp.common.identity_linking": [{
    "config": {
      "scopes": {
        "dev.ucp.shopping.order:read": {},
        "dev.ucp.shopping.order:manage": {}
      }
    }
  }]
}
```

Signing keys in JWK format are published in profiles for webhook verification and message signatures.

## Standard Capabilities

| Capability | Description | Transports |
|---|---|---|
| Checkout | Cart management, tax calculation, payment processing | REST, MCP, A2A, Embedded |
| Cart | Cart read/manage | REST, MCP, Embedded |
| Catalog | Product search and lookup | REST, MCP |
| Order | Order lifecycle webhooks (shipped, delivered, returned) | REST, MCP |
| Identity Linking | OAuth 2.0 authorization flow | REST, MCP |

## Relationship to Existing Skills

| Aspect | Related Skill |
|---|---|
| MCP Transport | `050105-agent-discovery/references/mcp-server-cards.md` |
| Well-Known Discovery | `050105-agent-discovery/references/well-known-overview.md` |
| Payment Architecture | `050105-agent-discovery/references/http-402-payments.md` |
| Agent Capabilities | `050105-agent-discovery/references/agent-skills-discovery.md` |
| Browser-Based Commerce | `050105-agent-discovery/references/webmcp-api.md` |
