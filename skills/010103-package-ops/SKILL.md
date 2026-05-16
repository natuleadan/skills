---
name: 010103-package-ops
license: MIT
description: "Day-to-day package management operations for npm, pnpm, and bun: install, update, audit, publish, outdated, doctor, and dependency troubleshooting. Use this skill whenever the user asks about managing dependencies, updating packages, running npm audit, pnpm audit, bun pm audit, publishing a package with npm publish/pnpm publish/bun publish, checking outdated packages with npm outdated/pnpm outdated/bun outdated, using npm doctor/pnpm doctor, running npm ci/pnpm install --frozen-lockfile/bun install --frozen-lockfile, using npm ls/pnpm ls/bun pm ls to inspect dependency trees, resolving version conflicts with overrides or packageExtensions, or using npm/pnpm/bun commands beyond initial setup. Do NOT trigger for initial toolchain installation (use 010102-install-and-setup) or supply chain security hardening (use 010101-package-security)."
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
