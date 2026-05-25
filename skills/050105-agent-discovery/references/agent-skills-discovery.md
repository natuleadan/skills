# Agent Skills Discovery (v0.2.0)

Defines a mechanism for discovering Agent Skills using the `/.well-known/agent-skills/` path prefix. Skills currently scattered across GitHub repos and docs sites get a predictable discovery endpoint.

## Problem

Agent Skills give AI agents domain-specific capabilities through structured instructions, scripts, and resources. Today, discovering skills requires searching GitHub repositories, reading vendor documentation, following social media links, or manual configuration. There is no standard way to answer: "What skills does example.com publish?"

## URI Structure

```
https://example.com/.well-known/agent-skills/index.json
```

Each skill in the index includes a `url` field pointing to its artifact. While publishers conventionally host skill files under `/.well-known/agent-skills/`, the `url` field allows skills at any location (CDN, versioned path, etc.).

Skill names MUST conform to: 1-64 characters, lowercase alphanumeric and hyphens only (`a-z`, `0-9`, `-`), MUST NOT start or end with a hyphen, MUST NOT contain consecutive hyphens.

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

> **Note**: In a future version, `url` may become optional for `type: "skill-md"` entries, defaulting to `/.well-known/agent-skills/{name}/SKILL.md`.

### URL Resolution

- Path-absolute: `/.well-known/agent-skills/code-review/SKILL.md`
- Absolute: `https://cdn.example.com/v2/skills/code-review/SKILL.md`
- Relative: `code-review/SKILL.md`

For `type: "archive"`, `url` points to the archive file. Clients SHOULD determine the archive format from the server's `Content-Type` header, falling back to the URL file extension if the header is absent or generic (e.g., `application/octet-stream`).

Clients encountering an unrecognized `type` value SHOULD skip that skill entry and MAY warn the user.

### Versioning

The `$schema` field identifies the index version. Clients encountering an unrecognized `$schema` SHOULD warn and NOT process the index. If `$schema` is absent, clients treat the index as v0.1.0 for backward compatibility. Clients MUST ignore unrecognized fields.

### Backward Compatibility (v0.1.0 → v0.2.0)

The v0.2.0 format is not backward-compatible with v0.1.0. Key differences:

| Aspect | v0.1.0 | v0.2.0 |
|---|---|---|
| Version field | `"version": "1.0"` | `$schema` URI |
| Files list | `files: ["SKILL.md", ...]` with no digests | Removed entirely |
| Artifact model | Multiple paths per skill | Single artifact (`url` + `digest`) |
| Entry fields | `files`, `package` | `type`, `url`, `digest` |

Clients MUST check `$schema` to determine how to process the index.

## Distribution Types

### type: "skill-md"

A single SKILL.md file. Suitable for skills without supporting resources.

```
skill-name/
└── SKILL.md
```

### type: "archive"

A `.tar.gz` or `.zip` containing the full skill directory. Archives SHOULD be in `.tar.gz` or `.zip` format. Clients MUST support at least both. Tradeoffs:

| Format | Pros | Cons |
|---|---|---|
| `.tar.gz` | UNIX file permissions, symlinks | No partial download |
| `.zip` | HTTP range requests for partial SKILL.md read | Limited perm/symlink support |

Archive contents represent the skill directory — files are placed at the archive root, NOT nested inside a wrapper directory:

```
wrangler.tar.gz
├── SKILL.md
├── scripts/
│   └── extract.py
├── references/
│   └── REFERENCE.md
└── assets/
    └── schema.json
```

Archives MUST contain `SKILL.md` at the root. MUST NOT contain path traversal (`..`) or absolute paths.

### Distribution Guidance

Simple skills (SKILL.md only) SHOULD use `type: "skill-md"`. Archives are intended for skills with supporting files where a single download preserves directory structure, file permissions, and symlinks.

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
- **Prompt injection**: A malicious SKILL.md can inject instructions. Validate artifacts come from allowlisted domains before loading into context.
- **Origin allowlisting**: Maintain a configurable allowlist. Reject unlisted origins unless user explicitly approves.
- **Access control**: Control write access to `/.well-known/agent-skills/` carefully, especially in shared hosting environments.
- **Script execution**: Clients SHALL NOT execute `scripts/` files by default. Implement a permissions model that only executes bundled scripts when explicitly allowed. Consider sandboxing execution environments, restricting filesystem and network access. Never execute scripts from untrusted origins without user approval.
- **Digest verification**: Clients MUST verify artifact digests after download. A mismatch indicates tampering or corruption; MUST NOT use unverified content.
- **Archive safety**: Validate digests before unpacking. Reject path traversal, symlinks resolving outside the skill directory, and decompression bombs.
- **External references**: Skills fetching external resources introduce additional trust boundaries.

## HTTP Considerations

| File | Content-Type |
|---|---|
| `index.json` | `application/json` |
| `SKILL.md` | `text/markdown` or `text/plain` |
| `.tar.gz` | `application/gzip` |
| `.zip` | `application/zip` |

Servers SHOULD set Cache-Control and CORS headers. Clients MUST handle redirects and respect cache headers.

## Relationship to Existing Specifications

This specification builds on:

- **RFC 2119 / RFC 8174** — Key words for requirement levels (MUST, SHOULD, MAY, etc.)
- **RFC 3986** — URI resolution (Section 5 for relative URL resolution)
- **RFC 8615** — Well-Known URIs (`.well-known/` path prefix)
- **Agent Skills Specification** — Skill format, SKILL.md structure, frontmatter conventions

## Client Implementation

1. **Fetch index.json** — Retrieve `/.well-known/agent-skills/index.json` to enumerate available skills.
2. **Check schema version** — Match `$schema` against known URIs. If absent, treat as v0.1.0. SHOULD NOT process an unrecognized `$schema`. MUST ignore unrecognized fields.
3. **Use digests for caching** — Compare each skill's digest against cached values. If it matches, skip re-downloading.
4. **Fetch and verify artifacts** — For `type: "skill-md"`, download SKILL.md, compute SHA-256, verify against digest. For `type: "archive"`, download archive, verify digest, unpack and validate structure. For unrecognized `type`, skip and warn.
5. **Apply progressive disclosure** — Load name + description at discovery. Load SKILL.md on activation. Load resources on demand.
6. **Cache aggressively** — Respect Cache-Control. Use digests to invalidate cached content. Cache for session duration.
7. **Gate script execution** — SHALL NOT execute scripts by default. Implement permissions model with sandboxing.

## Examples

### Simple Skill (SKILL.md Only)

```markdown
---
name: git-workflow
description: Follow team Git conventions for branching and commits.
---

# Git Workflow

Create feature branches from `main`:

```bash
git checkout -b feature/my-feature main
```

Commit messages use conventional commits:

```
feat: add user authentication
fix: resolve null pointer in login
```
```

### Complex Skill (Archive with Resources)

```
wrangler.tar.gz
├── SKILL.md
├── scripts/
│   └── deploy.sh
├── references/
│   ├── COMMANDS.md
│   └── CONFIGURATION.md
└── assets/
    └── wrangler.toml.template
```

The SKILL.md uses relative links for progressive disclosure:

```markdown
---
name: wrangler
description: Deploy and manage Cloudflare Workers projects.
---

# Wrangler

Run `scripts/deploy.sh` to deploy. For commands, see [references/COMMANDS.md](references/COMMANDS.md).
```

### Complete Discovery Index

```json
{
  "$schema": "https://schemas.agentskills.io/discovery/0.2.0/schema.json",
  "skills": [
    {
      "name": "code-review",
      "type": "skill-md",
      "description": "Review code for bugs and best practices.",
      "url": "/.well-known/agent-skills/code-review/SKILL.md",
      "digest": "sha256:c4d5e6f7..."
    },
    {
      "name": "git-workflow",
      "type": "skill-md",
      "description": "Follow team Git conventions.",
      "url": "/.well-known/agent-skills/git-workflow/SKILL.md",
      "digest": "sha256:a7b8c9d0..."
    },
    {
      "name": "wrangler",
      "type": "archive",
      "description": "Deploy and manage Cloudflare Workers.",
      "url": "/.well-known/agent-skills/wrangler.tar.gz",
      "digest": "sha256:f1e2d3c4..."
    }
  ]
}
```
