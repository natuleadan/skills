# Response Format

Standard envelope for all API responses:

```typescript
// Success
return { code: 1, msg: "ok", data: result }

// Error
return { code: 0, msg: "Not found", data: null }
```

Controllers return raw data; the top-level wrapper is applied centrally.
