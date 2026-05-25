# Well-Known URIs Overview

RFC 8615 defines a standardized location for well-known URIs using the `/.well-known/` path prefix. This provides a predictable endpoint for automated clients to discover metadata and capabilities without prior configuration.

## URI Pattern

```
https://example.com/.well-known/{name}
```

The path after `/.well-known/` is registered with IANA or defined by a specification. Clients can probe this path on any origin to discover if the service supports a given feature.

## Common Well-Known Registrations

| Endpoint | Spec | Purpose |
|---|---|---|
| `/.well-known/robots.txt` | — | Historical (robots.txt at root, not well-known) |
| `/.well-known/security.txt` | RFC 9116 | Security contact information |
| `/.well-known/change-password` | RFC 8615 | Change password URL |
| `/.well-known/acme-challenge/` | RFC 8555 | Automatic certificate management |
| `/.well-known/ai-catalog.json` | Agent Card (draft) | AI agent capability catalog, protocol-agnostic |
| `/.well-known/agent-skills/index.json` | Agent Skills Discovery v0.2.0 | Skill directory for AI agents |
| `/.well-known/mcp/server-card.json` | MCP Server Cards SEP-2127 (draft) | MCP server capability discovery |
| `/.well-known/nodeinfo` | NodeInfo | Federated service metadata |

## Design Principles

- **Predictability**: A client that knows a spec can probe any origin without documentation.
- **No prior config**: No API keys, no service-specific URLs needed for discovery.
- **Low cost**: A single HEAD/GET request tells the client if the feature exists.
- **Composability**: Multiple specs can coexist under different `.well-known/` paths.
- **Per-origin scope**: Each origin controls its own well-known paths.

## Server Implementation

```nginx
# Nginx — serve static files
location /.well-known/ {
    root /var/www/well-known;
    default_type application/json;
}
```

```typescript
// Next.js App Router route handler
import { NextResponse } from "next/server"

export async function GET() {
  return NextResponse.json({
    skills: [
      {
        name: "example-skill",
        type: "skill-md",
        description: "An example skill.",
        url: "/.well-known/agent-skills/example-skill/SKILL.md",
        digest: "sha256:abc123...",
      },
    ],
  })
}
```

Clients MUST handle redirects (3xx), respect cache headers, and support CORS when accessing from browser-based environments.
