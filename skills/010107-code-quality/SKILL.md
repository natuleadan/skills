---
name: 010107-code-quality
description: Testing practices (vitest, TDD, coverage), security rules (secrets, XSS, injection, CORS), and seed data patterns (anonymization, multi-language).
license: MIT
---

# Code Quality Standards

## Overview

Cross-cutting quality standards for testing and security. For TypeScript language rules, see [TypeScript Rules](../010112-typescript-rules/).

## Quick Reference

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

- [Testing](references/testing.md)
- [Security](references/security.md)
- [Seed Data Patterns](references/seed-data-patterns.md) — Anonymization, multi-language, multi-currency seed data conventions
