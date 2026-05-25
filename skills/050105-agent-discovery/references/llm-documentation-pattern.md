# LLM Documentation Pattern

How to make documentation accessible to AI agents via standardized files, MCP servers, and agent skills.

## llms.txt Standard

The `llms.txt` convention (llmstxt.org) defines two files at the root of a documentation site:

### llms.txt (Index)

A concise index of all pages with titles and descriptions, enabling agents to discover what documentation exists before fetching full content:

```
https://docs.example.com/llms.txt
```

Format: one line per page with title and path. Agents fetch this first to find relevant pages.

### llms-full.txt (Complete)

The entire documentation content in a single file, enabling agents to load all documentation at once:

```
https://docs.example.com/llms-full.txt
```

This is the recommended approach for giving an agent full context about a project. Agents load this file once and have all the information they need.

### Usage

```bash
# Point your agent to the complete docs
# Paste this URL into your coding agent:
https://mpp.dev/llms-full.txt
```

## MCP Server for Documentation

Documentation sites can expose an MCP server for agent-driven exploration. The MCP server provides tools that let agents search and read documentation on demand:

| Tool | Description |
|---|---|
| `list_pages` | List all documentation pages with their paths |
| `read_page` | Read the content of a specific documentation page |
| `search_docs` | Search documentation for a query string |

### Installation

```bash
# Claude
claude mcp add --transport http docs https://docs.example.com/api/mcp

# Codex
codex mcp add --transport http docs https://docs.example.com/api/mcp

# Manual config (.mcp.json)
{
  "mcpServers": {
    "docs": {
      "url": "https://docs.example.com/api/mcp"
    }
  }
}
```

### Source Code Tools

Documentation MCP servers can also provide access to source code:

| Tool | Description |
|---|---|
| `list_sources` | List available source code repositories |
| `list_source_files` | List files in a directory |
| `read_source_file` | Read a source code file |
| `get_file_tree` | Get a recursive file tree |
| `search_source` | Search source code for a pattern |

## Agent Skills

Installable agent skills provide structured knowledge about a project:

```bash
npx skills add org/repo -g
```

After installation, the agent automatically knows how to use the project's APIs, SDKs, and integration patterns without loading documentation files.

## Relationship to Other Discovery Mechanisms

| Mechanism | Audience | Format | Use Case |
|---|---|---|---|
| `sitemap.xml` | Search engines | XML | URL discovery for indexing |
| `llms.txt` | AI agents | Plain text | Page index for agents |
| `llms-full.txt` | AI agents | Plain text | Complete context loading |
| MCP server for docs | AI agents | JSON-RPC | Interactive documentation exploration |
| Agent skills | AI agents | SKILL.md + references | Structured domain knowledge |
