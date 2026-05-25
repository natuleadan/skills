# Error Handling Lesson

Structured error handling: typed errors, consistent responses, trace IDs.

## Error Class Hierarchy

Create typed error classes instead of generic `Error`:

```typescript
// Base HTTP error
class HttpError extends Error {
  constructor(
    public status: number,
    public code: string,
    public userMessage: string,
    public details?: unknown
  ) {
    super(userMessage);
    this.name = 'HttpError';
  }
}

// Specialized subclasses
class ValidationError extends HttpError {
  constructor(details: unknown) {
    super(400, 'VAL_000_001', 'Invalid input', details);
    this.name = 'ValidationError';
  }
}

class UnauthorizedError extends HttpError {
  constructor() {
    super(401, 'AUTH_001_001', 'Authentication required');
    this.name = 'UnauthorizedError';
  }
}

class ForbiddenError extends HttpError {
  constructor() {
    super(403, 'AUTH_002_001', 'Insufficient permissions');
    this.name = 'ForbiddenError';
  }
}

class NotFoundError extends HttpError {
  constructor(resource: string) {
    super(404, 'BUS_000_001', `${resource} not found`);
    this.name = 'NotFoundError';
  }
}
```

## Error Code Pattern

Use structured codes `PREFIX_CATEGORY_INDEX`:

```typescript
// VAL = Validation, AUTH = Auth, BUS = Business, SYS = System
const ERROR_CODES = {
  VAL_000_001: 'Invalid input format',
  AUTH_001_001: 'Missing authentication',
  AUTH_001_002: 'Invalid token',
  AUTH_002_001: 'Insufficient permissions',
  BUS_000_001: 'Resource not found',
  BUS_000_002: 'Resource already exists',
  SYS_000_001: 'Internal server error',
} as const;
```

## Standardized API Response

Always return consistent shape:

```typescript
type ApiSuccessResponse<T> = {
  success: true;
  data: T;
  meta?: { count?: number; timestamp: string };
  traceId: string;
};

type ApiErrorResponse = {
  success: false;
  error: string;
  userMessage: string;
  code: string;
  details?: unknown;
  timestamp: string;
  traceId: string;
};

// Helper to create responses
function createSuccess<T>(data: T, traceId: string): ApiSuccessResponse<T> {
  return { success: true, data, meta: { timestamp: new Date().toISOString() }, traceId };
}

function createError(error: HttpError, traceId: string): ApiErrorResponse {
  return {
    success: false,
    error: error.message,
    userMessage: error.userMessage,
    code: error.code,
    details: error.details,
    timestamp: new Date().toISOString(),
    traceId,
  };
}
```

## Error Handler in Route Handlers

```typescript
export async function POST(req: Request) {
  const traceId = crypto.randomUUID();

  try {
    const body = await req.json();
    const validated = schema.parse(body); // Throws ValidationError if invalid
    const result = await service.create(validated);
    return Response.json(createSuccess(result, traceId));
  } catch (error) {
    if (error instanceof HttpError) {
      return Response.json(createError(error, traceId), { status: error.status });
    }
    // Database-level errors
    if (isDatabaseError(error)) {
      const mapped = mapDatabaseError(error, traceId);
      return Response.json(mapped, { status: 500 });
    }
    // Unknown
    console.error('[UNHANDLED]', traceId, error);
    return Response.json(
      createError(new HttpError(500, 'SYS_000_001', 'Something went wrong'), traceId),
      { status: 500 }
    );
  }
}
```

## Map Database Errors

```typescript
function mapDatabaseError(error: unknown, traceId: string): ApiErrorResponse {
  const pgCode = (error as { code?: string }).code;

  const map: Record<string, [number, string, string]> = {
    PGRST116: [404, 'BUS_000_001', 'Resource not found'],
    '22P02':  [400, 'VAL_000_001', 'Invalid UUID format'],
    '23505':  [409, 'BUS_000_002', 'Resource already exists'],
    '23503':  [400, 'BUS_000_003', 'Related resource not found'],
  };

  const [status, code, userMessage] = map[pgCode ?? ''] ?? [500, 'SYS_000_001', 'Internal error'];
  return { success: false, error: String(error), userMessage, code, timestamp: new Date().toISOString(), traceId };
}
```

## Server Actions Error Pattern

```typescript
'use server';

type ActionResult<T> =
  | { success: true; data: T }
  | { success: false; error: string; code: string };

export async function createUser(input: unknown): Promise<ActionResult<User>> {
  try {
    const validated = UserSchema.parse(input);
    const user = await db.users.create(validated);
    return { success: true, data: user };
  } catch (error) {
    if (error instanceof ValidationError) {
      return { success: false, error: error.userMessage, code: error.code };
    }
    return { success: false, error: 'Something went wrong', code: 'SYS_000_001' };
  }
}
```

## Anti-Patterns

| ❌ WRONG | ✅ RIGHT |
|---------|---------|
| `throw 'message'` | `throw new Error('message')` |
| Empty catch: `catch {}` | Log + return error response |
| Generic: `Error('failed')` | Typed: `new NotFoundError('user')` |
| No trace ID | Include `traceId` for debugging |
| Expose stack traces to client | Return safe `userMessage` only |
| `console.log` in prod | Use structured logger |
