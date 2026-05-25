# Error Codes Format

Structured error responses with error codes and tracing.

## Error Code Format

`PREFIX_CATEGORY_INDEX`

- **PREFIX** — domain (VAL = validation, AUTH = authentication, DB = database, etc.)
- **CATEGORY** — specific category (000 = general, 001 = format, 002 = permissions, etc.)
- **INDEX** — sequential counter within category (001, 002, 003, etc.)

Example: `VAL_000_001` (validation general error #1)

## Response Structure

### Success Response

```json
{
  "status": 200,
  "data": { "user": {...} },
  "traceId": "uuid-string"
}
```

### Error Response

```json
{
  "status": 400,
  "error": {
    "code": "VAL_000_001",
    "message": "Invalid email format",
    "details": {...}
  },
  "traceId": "uuid-string"
}
```

## Usage Rules

- [ ] **Always include traceId** — UUID generated per request (for debugging/logs)
- [ ] **Use error codes** — enable client-side error handling by code
- [ ] **Include details** — validation errors should list field-specific problems
- [ ] **Consistent format** — all API responses follow ApiSuccessResponse or ApiErrorResponse
- [ ] **Never leak internals** — don't expose database errors directly
