---
name: 050105-agent-discovery
description: "Agent and service discovery via well-known URIs: Agent Skills Discovery, MCP Server Cards, progressive disclosure, integrity verification."
---

# Agent & Service Discovery

How websites and services expose their capabilities to automated clients through standardized `.well-known/` endpoints defined by RFC 8615.

## References

| Topic | File |
|---|---|
| Well-known URI pattern overview, RFC 8615 registry, existing standards | [references/well-known-overview.md](references/well-known-overview.md) |
| Agent Skills Discovery v0.2.0: index.json format, digest verification, progressive loading, archives | [references/agent-skills-discovery.md](references/agent-skills-discovery.md) |
| MCP Server Cards SEP-2127: server-card.json, capabilities, remotes, auth | [references/mcp-server-cards.md](references/mcp-server-cards.md) |
| Progressive disclosure pattern: Level 1 metadata, Level 2 instructions, Level 3 resources | [references/progressive-disclosure.md](references/progressive-disclosure.md) |

## When to Use

- Adding agent skills discovery to a service
- Publishing MCP server capabilities
- Implementing progressive loading for agent content
- Setting up `.well-known/` endpoints for automated clients
- Distributing skills with integrity verification
