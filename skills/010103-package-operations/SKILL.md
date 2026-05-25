---
name: 010103-package-operations
license: MIT
description: "Day-to-day package management for npm, pnpm, and bun — install, update, audit, publish, dependency inspection, and version conflict resolution."
---

# Package Operations

This skill covers day-to-day package management operations across npm, pnpm, and bun.

## How to use this skill

1. If the user asks about **installing or removing packages** → run `python scripts/validate.py install`
2. If the user asks about **updating dependencies** → run `python scripts/validate.py outdated`
3. If the user asks about **auditing for vulnerabilities** → run `python scripts/validate.py audit`
4. If the user asks about **publishing packages** → run `python scripts/validate.py publish`
5. If the user asks about **dependency troubleshooting** → run `python scripts/validate.py doctor`

## Quick reference

| Task | npm | pnpm | bun |
|---|---|---|---|
| Install | `npm install` | `pnpm install` | `bun install` |
| Add dep | `npm install <pkg>` | `pnpm add <pkg>` | `bun add <pkg>` |
| Remove | `npm uninstall <pkg>` | `pnpm remove <pkg>` | `bun remove <pkg>` |
| Update all | `npm update` | `pnpm update` | `bun update` |
| Audit | `npm audit` | `pnpm audit` | `bun pm audit` |
| Outdated | `npm outdated` | `pnpm outdated` | `bun outdated` |
| Publish | `npm publish` | `pnpm publish` | `bun publish` |
| Doctor | `npm doctor` | `pnpm doctor` | `bun --help` |

## Best practices

- Always review lockfile changes before committing
- Use `--frozen-lockfile` in CI (`npm ci`, `pnpm install --frozen-lockfile`, `bun install --frozen-lockfile`)
- Pin exact versions in production: set `save-exact=true` in `.npmrc`
- Audit regularly: `npm audit --audit-level=high`
- Keep a change log when updating dependencies

## References

- `references/ops-guide.md` — PM-specific commands for install, update, audit, publish, and troubleshooting
- `scripts/validate.py` — Validation tool for package operations
