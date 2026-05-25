# Auto-Router

Scan `controllers/` for `*.ctrl.ts` files and auto-generate route registration:

```bash
# Regenerate after adding/changing controllers
node scripts/generate-routes.ts
```

## Controller Conventions

- **File name**: `kebab-case.ctrl.ts`
- **Export name**: `{name}Controller` (camelCase)
- **Prefix**: Matches resource name
- **Tags**: OpenAPI grouping via `detail.tags`
- **Response**: Return raw data (wrapper at top level)
