---
name: 010303-code-quality
description: TypeScript strict patterns, testing best practices (vitest, TDD, coverage), and security rules (secrets, validation, XSS, injection, CORS).
---

# Code Quality Standards

## Overview

Cross-cutting quality standards for TypeScript, testing, and security that apply to both frontend and backend code.

## Quick Reference

### TypeScript

- No `any` — use generics `<T extends { name: string }>` or `unknown` + type guard
- No `enum` — use union literals (`type Status = 'active' | 'inactive'`)
- No `!` non-null assertion — use proper null checks
- No `@ts-ignore` — use `@ts-expect-error` only for intentional tests
- Use `import type` / `export type` for type-only imports
- `const` by default, early returns to reduce complexity

### Testing

- Use Vitest with `describe`/`it`/`expect`
- Integration tests with `@testing-library/react` + `userEvent`
- Follow AAA pattern: Arrange, Act, Assert
- 80% line coverage, 100% critical paths
- No `.only`, no `.skip`, no testing implementation details

### Security

- No hardcoded secrets — always use env vars
- Validate all input at boundaries (Zod schemas)
- Use parameterized queries to prevent SQL injection
- Prevent open redirects with URL validation
- Sanitize logs to strip secrets
- Never trust client-provided roles

## References

- [TypeScript Rules](references/typescript-rules.md)
- [Testing](references/testing.md)
- [Security](references/security.md)
