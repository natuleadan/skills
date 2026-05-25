---
name: 010106-backend-architecture
description: Backend architecture standards — typed error hierarchies, structured API responses, domain module layout, service/repository layering, env sanitization.
---

# Backend Architecture Standards

## Overview

Coding standards for backend module structure, error handling, and API response patterns.

## Quick Reference

### Module Structure

Standard module files:
- `types.ts` — Interfaces and types
- `schemas.ts` — Validation schemas (e.g., Zod)
- `constants.ts` — Domain constants
- `repository.ts` — Data access (queries + mutations)
- `service.ts` — Business logic
- `actions.ts` — Server Action entry points
- `utils.ts` — Pure helper functions

### Error Handling

- Use typed error classes: `HttpError` → `ValidationError`, `UnauthorizedError`, `ForbiddenError`, `NotFoundError`
- Structured API response: `{ data, error: { code, message, traceId } }`
- Error codes follow `PREFIX_CATEGORY_INDEX` (e.g., `VAL_000_001`)
- Database errors mapped to user-friendly messages

### Environment Variables

- Centralized `env.ts` with `requireEnv()` for validation
- All env vars accessed through this file only
- Logs sanitized before output (strip secrets, emails, tokens)

## References

- [Error Handling](references/error-handling.md)
- [Module Structure](references/module-structure.md)
