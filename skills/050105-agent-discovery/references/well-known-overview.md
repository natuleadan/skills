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
| `/.well-known/api-catalog` | RFC 9727 | API catalog for automated API discovery |
| `/.well-known/oauth-protected-resource` | RFC 9728 | OAuth 2.0 protected resource metadata |
| `/.well-known/openid-configuration` | OpenID Connect Discovery 1.0 | OpenID Provider configuration |
| `/.well-known/webfinger` | RFC 7033 | WebFinger protocol for resource discovery |
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

## API Catalog (RFC 9727)

RFC 9727 defines the `/.well-known/api-catalog` endpoint and `rel=api-catalog` link relation for automated discovery of a Publisher's HTTP APIs.

### Endpoint

A Publisher supporting this URI SHALL resolve `GET /.well-known/api-catalog` and return an API catalog document. A HEAD request SHOULD return a `Link` header with `rel=api-catalog`.

### Link Relation

The `api-catalog` link relation can appear in HTTP headers and HTML:

```http
Link: </my_api_catalog.json>; rel=api-catalog
```

```html
<a href="my_api_catalog.json" rel="api-catalog">Example Publisher APIs</a>
```

### Linkset Format

The catalog MUST use the Linkset format (`application/linkset+json`, RFC 9264) with profile URI `https://www.rfc-editor.org/info/rfc9727`:

```json
{
  "linkset": [
    {
      "anchor": "https://example.com/.well-known/api-catalog",
      "item": [
        {
          "href": "https://api.example.com/v1/users",
          "type": "application/openapi+json"
        },
        {
          "href": "https://api.example.com/v1/products"
        }
      ]
    }
  ]
}
```

The `item` link relation (RFC 6573) identifies each API as a member of the catalog. Additional metadata (OpenAPI specs, version info, usage policies) can be included per entry.

### Nesting and Multi-Domain

An API catalog may contain links to other API catalogs using `api-catalog` as the relation type:

```json
{
  "linkset": [
    {
      "anchor": "https://example.com/.well-known/api-catalog",
      "item": [
        { "href": "https://developer.example.com/apis/foo" },
        { "href": "https://developer.example.com/apis/bar" }
      ],
      "api-catalog": "https://apis.example.net/.well-known/api-catalog"
    }
  ]
}
```

For APIs distributed across multiple domains, Publishers should publish `/.well-known/api-catalog` at each domain and redirect to a canonical instance.

### Operational Considerations

- **Scalability**: Group APIs by category (gaming, IoT, AI). Use nested catalogs to keep each manageable.
- **Monitoring**: Track requests to `/.well-known/api-catalog` and correlate with API usage. Remove stale entries.
- **Current data**: Include deprecation metadata for legacy versions. Audit descriptions for correctness.
- **Integration**: API management frameworks can generate the catalog as a pre-release step.

### Security Considerations

- **TLS**: Serve `/.well-known/api-catalog` exclusively over HTTPS to prevent tampering.
- **Access control**: Read-only for external requests. Write privileges limited to catalog maintainers.
- **Rate limiting**: Apply to mitigate abuse and DoS on the catalog endpoint.
- **Audit**: Ensure no internal/private APIs are mistakenly exposed in a public catalog.
- **Zombie APIs**: Regular audits help decommission legacy APIs that are no longer supported.

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
