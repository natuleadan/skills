# WebMCP API

W3C Community Group draft (May 2026) that defines a JavaScript API (`navigator.modelContext`) enabling web applications to expose client-side tools to AI agents. WebMCP is the browser-side equivalent of the Model Context Protocol (MCP): tools run in client-side script instead of on a backend HTTP server.

## Overview

```
MCP Server Cards → HTTP servers exposing tools remotely
WebMCP           → Web pages exposing tools via JavaScript in the browser
```

Both are MCP — one server-side, one browser-side. WebMCP enables collaborative workflows where users and agents work together within the same web interface, sharing context and maintaining user control.

## API Reference

### Navigator Extension

```javascript
// Access the ModelContext for the current document
const context = navigator.modelContext
```

Each `Navigator` has an associated `ModelContext` scoped to the current `Document`. It changes on navigation away from `about:blank`.

### registerTool()

```javascript
navigator.modelContext.registerTool(tool, options?)
```

Registers a JavaScript function as a tool callable by agents. Throws on:
- Duplicate tool name
- Empty name or description
- Name >128 chars or containing invalid characters (non-ASCII alphanumeric, `_`, `-`, `.`)
- Invalid `inputSchema` (circular references, `undefined` from `toJSON()`)
- Document not fully active
- Permissions policy denies `"tools"` feature

### ModelContextTool Dictionary

```javascript
{
  name: "search_products",        // required, 1-128 chars [a-z0-9_.-]
  title: "Search Products",       // optional, USVString for native UI display
  description: "Search product catalog by query string", // required
  inputSchema: {                  // optional JSON Schema object
    type: "object",
    properties: {
      query: { type: "string" }
    }
  },
  execute: async (input, client) => {  // required callback
    const results = await searchProducts(input.query)
    return results
  },
  annotations: {                  // optional
    readOnlyHint: false,
    untrustedContentHint: false
  }
}
```

| Field | Type | Description |
|---|---|---|
| `name` | `DOMString` | Unique identifier. 1-128 chars, `[a-zA-Z0-9_.-]` |
| `title` | `USVString` | Human-readable label for UI. Recommend localization. |
| `description` | `DOMString` | Natural language description for agent understanding. |
| `inputSchema` | `object` | JSON Schema describing expected input parameters. |
| `execute` | `ToolExecuteCallback` | Async callback invoked when agent calls the tool. |
| `annotations` | `ToolAnnotations` | Optional metadata about tool behavior. |

### ToolAnnotations

| Field | Type | Default | Description |
|---|---|---|---|
| `readOnlyHint` | `boolean` | `false` | Tool does not modify state (read-only). Helps agents decide safety. |
| `untrustedContentHint` | `boolean` | `false` | Tool output contains untrusted data from the registering page's perspective. |

### ModelContextRegisterToolOptions

```javascript
{
  signal: abortController.signal,  // AbortSignal to auto-unregister
  exposedTo: ["https://trusted.site"]  // origins that can see this tool
}
```

| Field | Type | Description |
|---|---|---|
| `signal` | `AbortSignal` | Unregisters the tool when aborted. |
| `exposedTo` | `sequence<USVString>` | Controls cross-origin visibility. Must be potentially trustworthy origins. |

### ModelContextClient

Passed to the `execute` callback, enables user interaction during tool execution:

```javascript
execute: async (input, client) => {
  const confirmed = await client.requestUserInteraction(async () => {
    // Show confirmation dialog, get user approval
    return await showConfirmDialog("Search products?")
  })
  if (!confirmed) return { cancelled: true }
  return await searchProducts(input.query)
}
```

| Method | Description |
|---|---|
| `requestUserInteraction(callback)` | Requests user input during tool execution. Returns callback result. |

### Events

```javascript
navigator.modelContext.ontoolchange = (event) => {
  console.log("Tools changed")
}
```

Fired when tools are registered or unregistered in the document tree, including cross-origin iframes if the tool's `exposedTo` allows it.

## Declarative WebMCP

(TODO in spec) Future support for registering tools declaratively via HTML forms. The user agent would synthesize a JSON Schema from form elements and handle execution automatically.

## Permissions Policy

Access is gated behind the `"tools"` policy-controlled feature:

```http
Permissions-Policy: tools=(self "https://trusted.app")
```

Default allowlist is `'self'` — only same-origin scripts can register tools.

## Interaction with Agents

### Event Loop Integration

- Tools live in a `Document`'s event loop.
- The browser's agent runs in parallel on an AI agent queue.
- Steps queued from the browser agent onto the page's main thread use the `webmcp task source`.
- Timing between `toolchange` events and other task sources (e.g., timer) is not guaranteed.

### Page Observations

The browser agent obtains a snapshot of the page's tools and context via observations — implementation-defined data structures containing tool maps and page state (often including screenshots, not just DOM serialization).

## Security Considerations

- **SecureContext**: API only available on HTTPS pages (`[SecureContext]`).
- **Origin isolation**: `exposedTo` restricts cross-origin visibility. Same-origin documents always see tools.
- **User interaction gating**: `requestUserInteraction()` enables requiring user confirmation before tool execution.
- **Permissions Policy**: Default `'self'` prevents cross-origin iframes from registering tools without explicit opt-in.
- **Untrusted content hint**: Pages can mark tools whose output may contain untrusted data.

## Comparison: WebMCP vs MCP Server Cards

| Aspect | MCP Server Cards (SEP-2127) | WebMCP |
|---|---|---|
| Transport | HTTP | Browser JavaScript API |
| Discovery | `.well-known/mcp/server-card.json` | `navigator.modelContext` |
| Tool registration | Declared in JSON | `registerTool()` call |
| Execution | Remote HTTP call | Local JavaScript callback |
| Authentication | OAuth/Bearer per remote | Origin-based (Permissions Policy) |
| User interaction | N/A (server-side) | `requestUserInteraction()` |
| Client | Any MCP client | Browser's agent / in-page JS agent |
| Standard | IETF SEP (draft) | W3C CG (draft) |
