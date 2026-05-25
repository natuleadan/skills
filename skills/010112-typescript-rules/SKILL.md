---
name: 010112-typescript-rules
description: TypeScript strict mode, generics, mapped types, conditional types, Zod validation, migration strategy, and anti-patterns.
license: MIT
---

# TypeScript Rules

## Overview

TypeScript 5.7+ language patterns covering strict mode configuration, type safety, advanced typesystem constructs, best practices, Zod validation, and incremental migration from JavaScript.

## Quick Reference

### Strict Mode
```json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true
  }
}
```

### Core Rules
- No `any` — use `unknown`, generics, or `Record<string, unknown>`
- No `enum` — union literals (`type Status = "active" | "inactive"`) or `as const`
- No `!` non-null assertions — use guards or `Result<T, E>`
- No `@ts-ignore` — `@ts-expect-error` only for intentional error tests
- `import type` / `export type` for type-only imports
- Strict equality `===`, `const` by default

### Type System
- Discriminated unions for exhaustive checking
- Generics with constraints (`<T extends { id: string }>`)
- Mapped types (`Partial<T>`, `Immutable<T>`, `Getters<T>`)
- Conditional types (`IsString<T>`, `ArrayElement<T>`, `Awaited<T>`)
- `satisfies` operator for compile-time validation
- Zod schemas for runtime validation at boundaries

## References

- [Type Safety](references/type-safety.md) — Strict mode, no any, discriminated unions, type guards
- [Advanced Types](references/advanced-types.md) — Generics, mapped types, conditional types, satisfies
- [Rules & Anti-Patterns](references/rules-anti-patterns.md) — No enum, import type, Zod, Result pattern, all lint rules (merged)
- [Migration Strategy](references/migration-strategy.md) — JS→TS incremental migration, JSDoc, tsconfig
- [Code Examples](references/code-examples.md) — Repository pattern, DTOs, conditional types, Zod
- [Quick Reference](references/quick-reference.md) — Type system cheat sheet, utility types, keywords
