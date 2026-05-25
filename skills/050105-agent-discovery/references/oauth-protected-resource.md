# OAuth 2.0 Protected Resource Metadata (RFC 9728)

Defines a metadata format enabling OAuth 2.0 clients and authorization servers to obtain information needed to interact with an OAuth 2.0 protected resource. Metadata is published at a well-known location derived from the resource's URL.

## Well-Known Endpoint

Protected resources supporting metadata MUST make a JSON document available at a URL formed by inserting `/.well-known/oauth-protected-resource` into the resource identifier between the host and path/query components.

### No Path Component

```
Resource identifier: https://resource.example.com
Metadata URL:       https://resource.example.com/.well-known/oauth-protected-resource
```

### With Path Component (Multi-Tenant)

```
Resource identifier: https://resource.example.com/resource1
Metadata URL:       https://resource.example.com/.well-known/oauth-protected-resource/resource1
```

The terminating slash after the host MUST be removed before inserting the well-known string.

## Metadata Parameters

| Parameter | Required | Description |
|---|---|---|
| `resource` | REQUIRED | The protected resource's resource identifier URL. |
| `authorization_servers` | OPTIONAL | Array of OAuth authorization server issuer identifiers (RFC 8414). |
| `scopes_supported` | RECOMMENDED | Array of scope values used in authorization requests for this resource. |
| `bearer_methods_supported` | OPTIONAL | Array of bearer token methods: `header`, `body`, `query` (RFC 6750). |
| `jwks_uri` | OPTIONAL | URL of the resource's JWK Set document (RFC 7517). Must use HTTPS. |
| `resource_signing_alg_values_supported` | OPTIONAL | Array of JWS signing algorithms for resource responses. `none` MUST NOT be used. |
| `dpop_signing_alg_values_supported` | OPTIONAL | Array of JWS algorithms for validating DPoP proof JWTs (RFC 9449). |
| `dpop_bound_access_tokens_required` | OPTIONAL | Boolean. Default `false`. |
| `tls_client_certificate_bound_access_tokens` | OPTIONAL | Boolean. Default `false`. |
| `authorization_details_types_supported` | OPTIONAL | Array of authorization details type values (RFC 9396). |
| `resource_name` | RECOMMENDED | Human-readable name for display to end users. |
| `resource_documentation` | OPTIONAL | URL of developer documentation. |
| `resource_policy_uri` | OPTIONAL | URL of usage policy. |
| `resource_tos_uri` | OPTIONAL | URL of terms of service. |

## Human-Readable Internationalization

Language tags are appended with `#` delimiter:

```json
{
  "resource_name#en": "My Resource",
  "resource_name#fr": "La mia bella risorsa",
  "resource_name#ja": "マイリソース"
}
```

If sent without a language tag, the string MUST be used as-is. It is RECOMMENDED to include an untagged instance alongside language-specific ones.

## Signed Metadata

Metadata MAY be provided as a signed JWT via the `signed_metadata` parameter. Signed metadata MUST be digitally signed using JWS and MUST contain an `iss` (issuer) claim. Signed values take precedence over unsigned JSON elements.

```json
{
  "resource": "https://resource.example.com",
  "signed_metadata": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

Consumers MAY ignore signed metadata if unsupported. If supported, the signature MUST be validated against a key belonging to the issuer.

## WWW-Authenticate Discovery

A protected resource can signal its metadata URL in a 401 response:

```http
HTTP/1.1 401 Unauthorized
WWW-Authenticate: Bearer resource_metadata="https://resource.example.com/.well-known/oauth-protected-resource"
```

### End-to-End Flow

1. Client requests resource without access token.
2. Server responds 401 with `WWW-Authenticate: Bearer resource_metadata=...`.
3. Client fetches protected resource metadata from the URL.
4. Client validates metadata (resource value MUST match the request URL).
5. Client builds authorization server metadata URL from `authorization_servers`.
6. Client performs OAuth authorization flow.
7. Client retries resource request with access token.

### Metadata Change Notification

The server may send a new `WWW-Authenticate` challenge with `resource_metadata` at any time to indicate metadata has changed. Clients SHOULD fetch and apply updated metadata.

## Authorization Server Metadata

Authorization servers can list protected resources via the `protected_resources` parameter (RFC 8414 extension):

```json
{
  "protected_resources": [
    "https://resource.example.com",
    "https://resource.example.net"
  ]
}
```

When both sides publish lists, they SHOULD be cross-checked for consistency.

## Example Response

```json
{
  "resource": "https://resource.example.com",
  "authorization_servers": [
    "https://as1.example.com",
    "https://as2.example.net"
  ],
  "bearer_methods_supported": ["header", "body"],
  "scopes_supported": ["profile", "email", "phone"],
  "resource_documentation": "https://resource.example.com/docs"
}
```

## Security Considerations

- **TLS**: MUST support TLS. Metadata URLs protect against disclosure and tampering.
- **Impersonation**: The `resource` value in metadata MUST exactly match the URL used to fetch it. Client MUST verify. This prevents attackers from publishing metadata for a resource they don't control.
- **Audience-restricted tokens**: RECOMMENDED (RFC 8707). Prevents malicious RS from reusing tokens at other resources.
- **SSRF**: Clients fetching AS metadata based on RS metadata should block requests to internal IP ranges.
- **Phishing**: Follow OAuth best practices: display AS domain, use origin-bound authenticators, apply domain reputation checks.
- **Metadata caching**: HTTP caching applies. Use `Cache-Control` with appropriate `max-age`.
- **Signed vs unsigned**: Unsigned metadata relies on TLS/PKIX. Signed metadata adds JWS-based integrity independent of PKIX.
