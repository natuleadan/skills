# Package Operations Guide

## Installing packages

| Action | npm | pnpm | bun |
|---|---|---|---|
| Install from lockfile | `npm ci` | `pnpm install --frozen-lockfile` | `bun install --frozen-lockfile` |
| Install with upgrades | `npm install` | `pnpm install` | `bun install` |
| Add dependency | `npm install <pkg>` | `pnpm add <pkg>` | `bun add <pkg>` |
| Add dev dependency | `npm install -D <pkg>` | `pnpm add -D <pkg>` | `bun add -d <pkg>` |
| Add global package | `npm install -g <pkg>` | `pnpm add -g <pkg>` | `bun add -g <pkg>` |
| Remove dependency | `npm uninstall <pkg>` | `pnpm remove <pkg>` | `bun remove <pkg>` |

## Updating dependencies

| Action | npm | pnpm | bun |
|---|---|---|---|
| Update all | `npm update` | `pnpm update` | `bun update` |
| Update single pkg | `npm update <pkg>` | `pnpm update <pkg>` | `bun update <pkg>` |
| Check outdated | `npm outdated` | `pnpm outdated` | `bun outdated` |
| Interactive update | `npm outdated -g` | — | — |

## Auditing

| Action | npm | pnpm | bun |
|---|---|---|---|
| Run audit | `npm audit` | `pnpm audit` | `bun pm audit` |
| Audit with severity | `npm audit --audit-level=high` | — | — |
| Fix vulnerabilities | `npm audit fix` | `pnpm audit --fix` | — |
| Audit signatures | `npm audit signatures` | — | — |

## Publishing

| Action | npm | pnpm | bun |
|---|---|---|---|
| Publish package | `npm publish` | `pnpm publish` | `bun publish` |
| Dry run | `npm publish --dry-run` | `pnpm publish --dry-run` | — |
| Version bump | `npm version <patch\|minor\|major>` | `pnpm version <patch\|minor\|major>` | — |
| Tag release | `npm publish --tag beta` | `pnpm publish --tag beta` | — |

## Troubleshooting

### npm doctor

Run `npm doctor` to check your npm environment:

```
npm doctor
```

Checks: npm version, Node.js version, registry connectivity, permission issues, git availability.

### pnpm doctor

```
pnpm doctor
```

Checks: pnpm version, store integrity, configuration issues.

### Dependency conflicts

When package managers report version conflicts:

1. Check for peer dependency mismatches in the error output
2. Use `npm ls <pkg>` / `pnpm ls <pkg>` / `bun pm ls` to see the dependency tree
3. Consider `overrides` (npm/pnpm) or `pnpm.packageExtensions` for pnpm
4. For bun, check `bun.lock` with `bun pm hash-mismatch`

### Lockfile regeneration

To regenerate a lockfile from scratch:

```bash
# npm
rm package-lock.json && npm install

# pnpm
rm pnpm-lock.yaml && pnpm install

# bun
rm bun.lock && bun install
```

## Best practices

- Always commit lockfiles to version control
- Use `--frozen-lockfile` in CI to catch unexpected changes
- Review lockfile diffs in pull requests
- Run `npm audit` / `pnpm audit` regularly in CI
- Pin production dependencies with `save-exact=true`
- Use `overrides` to enforce specific versions of transitive dependencies
