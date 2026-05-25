# Agent Skills Discovery (v0.2.0)

Defines a mechanism for discovering Agent Skills using the `/.well-known/agent-skills/` path prefix. Skills currently scattered across GitHub repos and docs sites get a predictable discovery endpoint.

## URI Structure

```
https://example.com/.well-known/agent-skills/index.json
```

## Discovery Index

Publishers MUST provide an index at `/.well-known/agent-skills/index.json`:

```json
{
  "$schema": "https://schemas.agentskills.io/discovery/0.2.0/schema.json",
  "skills": [
    {
      "name": "code-review",
      "type": "skill-md",
      "description": "Review code for bugs, security issues, and best practices.",
      "url": "/.well-known/agent-skills/code-review/SKILL.md",
      "digest": "sha256:c4d5e6f7a8b9..."
    },
    {
      "name": "wrangler",
      "type": "archive",
      "description": "Deploy and manage Cloudflare Workers projects.",
      "url": "/.well-known/agent-skills/wrangler.tar.gz",
      "digest": "sha256:a1b2c3d4e5f6..."
    }
  ]
}
```

### Top-Level Fields

| Field | Required | Description |
|---|---|---|
| `$schema` | Yes | Schema version URI. Clients use this to determine how to parse the index. |
| `skills` | Yes | Array of skill entries. |

### Skill Entry Fields

| Field | Required | Description |
|---|---|---|
| `name` | Yes | Skill identifier. 1-64 chars, lowercase alphanumeric and hyphens only. |
| `type` | Yes | Distribution type: `"skill-md"` (single SKILL.md file) or `"archive"` (bundled archive). |
| `description` | Yes | Brief description. Max 1024 chars. SHOULD match SKILL.md frontmatter. |
| `url` | Yes | URL to the skill artifact. Resolved per RFC 3986 using the index URL as base. |
| `digest` | Yes | SHA-256 content digest: `sha256:{64-hex-chars}`. |

### URL Resolution

- Path-absolute: `/.well-known/agent-skills/code-review/SKILL.md`
- Absolute: `https://cdn.example.com/v2/skills/code-review/SKILL.md`
- Relative: `code-review/SKILL.md`

### Versioning

The `$schema` field identifies the index version. Clients encountering an unrecognized `$schema` SHOULD warn and NOT process the index. If `$schema` is absent, clients treat the index as v0.1.0 for backward compatibility.

## Distribution Types

### type: "skill-md"

A single SKILL.md file. Suitable for skills without supporting resources.

```
skill-name/
└── SKILL.md
```

### type: "archive"

A `.tar.gz` or `.zip` containing the full skill directory:

```
archive.tar.gz
├── SKILL.md
├── scripts/
│   └── extract.py
├── references/
│   └── REFERENCE.md
└── assets/
    └── schema.json
```

Archives MUST contain SKILL.md at the root. MUST NOT contain path traversal (`..`) or absolute paths.

## Integrity Verification

- **Digest format**: `sha256:{SHA-256(raw_bytes)}`
- **Change detection**: Compare digest against cached value — skip re-download on match.
- **Download verification**: Compute SHA-256 after download, reject on mismatch.

Clients MUST verify downloaded content. A mismatch indicates corruption or tampering.

## Progressive Disclosure

| Level | What | When Loaded | Token Cost |
|---|---|---|---|
| 1 | `name` + `description` from index | At startup or probing | ~100 tokens/skill |
| 2 | Full SKILL.md body | When skill is activated | < 5k tokens recommended |
| 3 | Referenced files (scripts, references, assets) | On demand, as needed | Unlimited |

## Archive Safety

Clients unpacking archives MUST:

- Reject path traversal (`..`) or absolute paths.
- Reject symlinks/hard links resolving outside the skill directory.
- Enforce a reasonable limit on total unpacked size (decompression bomb protection).

## Security Considerations

- **Trust**: Skills contain instructions and executable code. Use only from trusted origins.
- **Prompt injection**: A malicious SKILL.md can inject instructions. Validate artifacts come from allowlisted domains.
- **Origin allowlisting**: Maintain a configurable allowlist. Reject unlisted origins unless user explicitly approves.
- **Script execution**: Clients SHALL NOT execute `scripts/` files by default. Implement a permissions model.

## HTTP Considerations

| File | Content-Type |
|---|---|
| `index.json` | `application/json` |
| `SKILL.md` | `text/markdown` or `text/plain` |
| `.tar.gz` | `application/gzip` |
| `.zip` | `application/zip` |

Servers SHOULD set Cache-Control and CORS headers. Clients MUST handle redirects and respect cache headers.

## Client Implementation

1. Fetch `/.well-known/agent-skills/index.json`
2. Check `$schema` against known versions
3. Compare digests against cache — skip unchanged skills
4. Download and verify changed/new skill artifacts
5. Apply progressive disclosure: load metadata → full instructions → resources on demand
6. Gate script execution behind permissions model
