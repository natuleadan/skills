# OpenID Connect Discovery 1.0

Defines how an OpenID Connect Relying Party (RP) discovers the End-User's OpenID Provider (OP) and obtains configuration information needed to interact with it, including OAuth 2.0 endpoint locations.

## Well-Known Endpoint

OpenID Providers supporting Discovery MUST make a JSON document available at the path formed by concatenating `/.well-known/openid-configuration` to the Issuer.

### No Path Component

```
Issuer:  https://server.example.com
Config:  https://server.example.com/.well-known/openid-configuration
```

### With Path Component (Multi-Tenant)

```
Issuer:  https://server.example.com/issuer1
Config:  https://server.example.com/issuer1/.well-known/openid-configuration
```

Any terminating `/` on the Issuer MUST be removed before appending the well-known path.

## WebFinger Issuer Discovery

Issuer discovery is OPTIONAL. If the RP knows the OP's location out-of-band, it can skip to the configuration request.

Discovery uses WebFinger (`/.well-known/webfinger`) with:

| Parameter | Value |
|---|---|
| `resource` | Normalized identifier for the End-User |
| `rel` | `http://openid.net/specs/connect/1.0/issuer` |
| `host` | Authority component from the normalized identifier |

### Identifier Normalization

The user input Identifier determines which normalization applies:

| Input Pattern | Example | Scheme | Resource | Host |
|---|---|---|---|---|
| `user@host` | `joe@example.com` | `acct:` | `acct:joe@example.com` | `example.com` |
| `https://host/path` | `https://example.com/joe` | `https:` | `https://example.com/joe` | `example.com` |
| `host:port` | `example.com:8080` | `https:` | `https://example.com:8080/` | `example.com:8080` |
| `acct:user@host` | `acct:joe@example.com` | `acct:` | `acct:joe@example.com` | `example.com` |

Steps:
1. If no scheme component, check for `user@host` — assume `acct:` scheme.
2. Otherwise, assume `https:` scheme.
3. If explicit scheme (`https:`, `acct:`), no normalization.
4. Strip any fragment component.
5. Resulting URI is the WebFinger `resource`; authority is the `host`.

### WebFinger Examples

#### Email Address Input

```
GET /.well-known/webfinger?resource=acct%3Ajoe%40example.com&rel=http%3A%2F%2Fopenid.net%2Fspecs%2Fconnect%2F1.0%2Fissuer HTTP/1.1
Host: example.com

HTTP/1.1 200 OK
Content-Type: application/jrd+json

{
  "subject": "acct:joe@example.com",
  "links": [
    {
      "rel": "http://openid.net/specs/connect/1.0/issuer",
      "href": "https://server.example.com"
    }
  ]
}
```

#### URL Input

```
GET /.well-known/webfinger?resource=https%3A%2F%2Fexample.com%2Fjoe&rel=http%3A%2F%2Fopenid.net%2Fspecs%2Fconnect%2F1.0%2Fissuer HTTP/1.1
Host: example.com
```

#### Hostname and Port Input

```
GET /.well-known/webfinger?resource=https%3A%2F%2Fexample.com%3A8080%2F&rel=http%3A%2F%2Fopenid.net%2Fspecs%2Fconnect%2F1.0%2Fissuer HTTP/1.1
Host: example.com:8080
```

#### acct URI Input

```
GET /.well-known/webfinger?resource=acct%3Ajuliet%2540capulet.example%40shopping.example.com&rel=http%3A%2F%2Fopenid.net%2Fspecs%2Fconnect%2F1.0%2Fissuer HTTP/1.1
Host: shopping.example.com
```

## OpenID Provider Metadata Parameters

| Parameter | Required | Description |
|---|---|---|
| `issuer` | REQUIRED | OP's Issuer Identifier URL (https, no query/fragment). |
| `authorization_endpoint` | REQUIRED | URL of the OAuth 2.0 Authorization Endpoint. |
| `token_endpoint` | REQUIRED* | URL of the OAuth 2.0 Token Endpoint. Required unless only Implicit Flow used. |
| `userinfo_endpoint` | RECOMMENDED | URL of the UserInfo Endpoint. |
| `jwks_uri` | REQUIRED | URL of the OP's JWK Set document (https). |
| `registration_endpoint` | RECOMMENDED | URL of the Dynamic Client Registration Endpoint. |
| `scopes_supported` | RECOMMENDED | Array of supported OAuth 2.0 scope values. MUST include `openid`. |
| `response_types_supported` | REQUIRED | Array of supported response_type values. MUST include `code`, `id_token`, `id_token token`. |
| `response_modes_supported` | OPTIONAL | Array of supported response_mode values. Default: `["query", "fragment"]`. |
| `grant_types_supported` | OPTIONAL | Array of supported Grant Type values. Default: `["authorization_code", "implicit"]`. |
| `acr_values_supported` | OPTIONAL | Array of supported Authentication Context Class References. |
| `subject_types_supported` | REQUIRED | Array of Subject Identifier types (`pairwise`, `public`). |
| `id_token_signing_alg_values_supported` | REQUIRED | Array of JWS signing algorithms for ID Tokens. MUST include `RS256`. |
| `id_token_encryption_alg_values_supported` | OPTIONAL | Array of JWE encryption algorithms for ID Tokens. |
| `id_token_encryption_enc_values_supported` | OPTIONAL | Array of JWE encryption methods for ID Tokens. |
| `userinfo_signing_alg_values_supported` | OPTIONAL | Array of JWS signing algorithms for UserInfo responses. |
| `userinfo_encryption_alg_values_supported` | OPTIONAL | Array of JWE encryption algorithms for UserInfo. |
| `userinfo_encryption_enc_values_supported` | OPTIONAL | Array of JWE encryption methods for UserInfo. |
| `request_object_signing_alg_values_supported` | OPTIONAL | Array of JWS algorithms for Request Objects. SHOULD support `none` and `RS256`. |
| `request_object_encryption_alg_values_supported` | OPTIONAL | Array of JWE encryption algorithms for Request Objects. |
| `request_object_encryption_enc_values_supported` | OPTIONAL | Array of JWE encryption methods for Request Objects. |
| `token_endpoint_auth_methods_supported` | OPTIONAL | Array of Client Authentication methods. Default: `client_secret_basic`. |
| `token_endpoint_auth_signing_alg_values_supported` | OPTIONAL | Array of JWS algorithms for client auth JWTs. SHOULD support `RS256`. |
| `display_values_supported` | OPTIONAL | Array of display parameter values (`page`, `popup`, etc.). |
| `claim_types_supported` | OPTIONAL | Array of Claim Types (`normal`, `aggregated`, `distributed`). Default: `normal`. |
| `claims_supported` | RECOMMENDED | Array of Claim Names the OP may supply values for. |
| `service_documentation` | OPTIONAL | URL of developer documentation. |
| `claims_locales_supported` | OPTIONAL | Array of BCP47 language tags for Claims. |
| `ui_locales_supported` | OPTIONAL | Array of BCP47 language tags for the UI. |
| `claims_parameter_supported` | OPTIONAL | Boolean. Default `false`. |
| `request_parameter_supported` | OPTIONAL | Boolean. Default `false`. |
| `request_uri_parameter_supported` | OPTIONAL | Boolean. Default `true`. |
| `require_request_uri_registration` | OPTIONAL | Boolean. Default `false`. |
| `op_policy_uri` | OPTIONAL | URL of the OP's requirements for RPs. |
| `op_tos_uri` | OPTIONAL | URL of the OP's terms of service. |

## Example Configuration Response

```json
{
  "issuer": "https://server.example.com",
  "authorization_endpoint": "https://server.example.com/connect/authorize",
  "token_endpoint": "https://server.example.com/connect/token",
  "token_endpoint_auth_methods_supported": ["client_secret_basic", "private_key_jwt"],
  "token_endpoint_auth_signing_alg_values_supported": ["RS256", "ES256"],
  "userinfo_endpoint": "https://server.example.com/connect/userinfo",
  "jwks_uri": "https://server.example.com/jwks.json",
  "registration_endpoint": "https://server.example.com/connect/register",
  "scopes_supported": ["openid", "profile", "email", "address", "phone", "offline_access"],
  "response_types_supported": ["code", "code id_token", "id_token", "id_token token"],
  "subject_types_supported": ["public", "pairwise"],
  "id_token_signing_alg_values_supported": ["RS256", "ES256", "HS256"],
  "userinfo_signing_alg_values_supported": ["RS256", "ES256", "HS256"],
  "request_object_signing_alg_values_supported": ["none", "RS256", "ES256"],
  "display_values_supported": ["page", "popup"],
  "claim_types_supported": ["normal", "distributed"],
  "claims_supported": ["sub", "iss", "auth_time", "name", "given_name", "family_name", "email"],
  "claims_parameter_supported": true,
  "service_documentation": "https://server.example.com/connect/service_documentation.html",
  "ui_locales_supported": ["en-US", "fr-FR"]
}
```

## Validation

The `issuer` value returned in the configuration response MUST be identical to the Issuer URL used as the prefix to `/.well-known/openid-configuration`. This MUST also be identical to the `iss` Claim value in ID Tokens issued from this Issuer. If validation fails, the configuration MUST NOT be used.

## Relationship to OAuth Protected Resource Metadata

| Aspect | OpenID Discovery (this spec) | RFC 9728 |
|---|---|---|
| Target | OpenID Provider / Authorization Server | Protected Resource / Resource Server |
| Well-known | `/.well-known/openid-configuration` | `/.well-known/oauth-protected-resource` |
| Discovery | WebFinger-based issuer discovery | WWW-Authenticate header |
| Auth metadata | Authorization endpoints, token endpoint, JWKS | Bearer methods, scopes, DPoP, TLS binding |

## Security Considerations

- **TLS**: MUST support TLS per BCP 195. Certificate check per RFC 6125.
- **Impersonation**: The `issuer` value MUST match the URL used to fetch metadata. Prevents attackers from publishing fake Discovery documents with their own endpoints and keys.
- **iss Claim validation**: The `issuer` in metadata MUST match `iss` in ID Tokens. Prevents token substitution attacks.
- **CORS**: All endpoints accessed by clients (Token, UserInfo, JWKS, Registration) SHOULD support CORS for browser-based clients. Authorization Endpoint should NOT use CORS (it's redirected, not directly accessed).
