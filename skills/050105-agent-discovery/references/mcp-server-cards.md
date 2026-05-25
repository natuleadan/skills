# MCP Server Cards (SEP-2127)

SEP-2127 proposes a standardized discovery mechanism for HTTP-based MCP (Model Context Protocol) servers using a `.well-known/mcp/server-card.json` endpoint. This enables MCP clients to discover server capabilities, available transports, authentication requirements, and protocol versions before establishing a connection.

## Discovery Endpoint

```
https://example.com/.well-known/mcp/server-card.json
```

## Server Card Structure

```json
{
  "name": "io.modelcontextprotocol.anonymous/brave-search",
  "description": "MCP server for Brave Search API integration",
  "title": "Brave Search",
  "websiteUrl": "https://anonymous.modelcontextprotocol.io/examples",
  "version": "1.0.2",
  "supportedProtocolVersions": ["2025-03-12", "2025-06-15"],
  "remotes": [
    {
      "url": "https://mcp.example.com/brave-search",
      "supportedProtocolVersions": ["2025-06-15"],
      "authentication": {
        "scheme": "bearer",
        "resource": "https://mcp.example.com/brave-search"
      }
    }
  ],
  "capabilities": {
    "tools": {},
    "resources": {},
    "prompts": {}
  },
  "packages": [
    {
      "name": "@example/brave-search",
      "registry": "npm"
    }
  ]
}
```

### Key Fields

| Field | Description |
|---|---|
| `name` | Reverse-DNS namespaced identifier. |
| `title` | Human-readable display name. |
| `description` | Brief description of server purpose. |
| `websiteUrl` | Link to server documentation or homepage. |
| `version` | Semantic version of the server card. |
| `supportedProtocolVersions` | Array of MCP protocol versions this server supports. |
| `remotes` | Connection endpoints, each with URL, protocol versions, and auth. |
| `capabilities` | Declared capabilities: tools, resources, prompts. |
| `packages` | Registry packages (npm, PyPI, etc.) for local installation. |

### Remote Entry

Each remote in the `remotes` array represents a connection endpoint:

| Field | Description |
|---|---|
| `url` | Base URL of the MCP server endpoint. |
| `supportedProtocolVersions` | Protocol versions available at this endpoint. |
| `authentication` | Auth scheme and resource identifier. |

## Relationship to Registry server.json

MCP Server Cards are designed as a strict subset of the MCP Registry `server.json` format. Key differences:

| Aspect | server.json (Registry) | Server Card (.well-known) |
|---|---|---|
| Purpose | Full server metadata for registry listings | Pre-connection discovery |
| Audience | Registry consumers browsing/installing | MCP clients connecting directly |
| Scope | Complete with all primitives | Discovery-focused, minimal |
| Location | Registry API | `.well-known/mcp/server-card.json` |
| Breaking changes | Versioned | Avoided (subset contract) |

Server Cards should introduce no breaking changes to `server.json`. They can be additive (e.g., adding `tools` to Server Cards without changing server.json).

## Relationship to Agent Cards

The Agent Card standard provides a protocol-agnostic `.well-known/ai-catalog.json` for discovering AI services. MCP Server Cards fit into this ecosystem:

- `ai-catalog.json` lists all AI capabilities at an origin, referencing MCP, A2A, or other protocols.
- `server-card.json` provides the MCP-specific details needed to connect.

Example flow:

```
Restaurant A website
  → .well-known/ai-catalog.json  lists:
      - "Book a table" → references MCP Server Card at reservation-saas.com
      - "View jobs"    → references MCP Server Card at jobs-saas.com

Reservation SaaS
  → .well-known/mcp/server-card.json  lists all restaurant endpoints
```

## Authentication

Authentication is declared per-remote, not at the top level, because different endpoints may require different auth:

```json
{
  "remotes": [
    {
      "url": "https://mcp.example.com/public",
      "authentication": null
    },
    {
      "url": "https://mcp.example.com/private",
      "authentication": {
        "scheme": "bearer",
        "resource": "https://auth.example.com/token"
      }
    }
  ]
}
```

## Dynamic Primitives

Some servers may not be able to enumerate all tools, resources, or prompts statically. The SEP discusses a `"dynamic"` value option for tools/resources/prompts, but this remains an open discussion thread with community opposition.

## Payment / Paid MCP Servers

For paid MCP servers, a lightweight payment link can be added without turning the Server Card into a billing spec:

```json
{
  "payment": {
    "href": "https://example.com/.well-known/mcp/pay.json",
    "rel": "payment-policy",
    "rails": ["x402"]
  }
}
```

Pricing can then evolve independently via the linked payment policy document with normal HTTP caching.

## Open Threads (as of SEP draft)

| Topic | Status |
|---|---|
| Dynamic as a value for tools/primitives | Under discussion, community opposition |
| Server instructions as a field | Deferred — not in server.json either |
| Primitives per-remote vs top-level | Under discussion |
| Headers in remotes (too permissive?) | Under discussion |
| Drop `.json` suffix from Resource distribution | Under discussion |
| `.well-known` placement with multiplicity suffixes | Under discussion |
| Localization (i18n for title/description) | Feature request, not yet addressed |

## Server Implementation

```nginx
location /.well-known/mcp/server-card.json {
    alias /var/www/mcp/server-card.json;
    default_type application/json;
}
```

```typescript
// Next.js route handler
import { NextResponse } from "next/server"

export async function GET() {
  return NextResponse.json({
    name: "io.example/my-server",
    description: "My MCP server",
    version: "1.0.0",
    remotes: [
      {
        url: process.env.MCP_SERVER_URL,
        authentication: {
          scheme: "bearer",
          resource: process.env.AUTH_URL,
        },
      },
    ],
    capabilities: {
      tools: {},
    },
  })
}
```
