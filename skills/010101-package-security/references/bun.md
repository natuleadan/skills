# bun Security Configuration

Bun v1.3+ introduced `minimumReleaseAge`. Use the latest stable release.

## Global configuration

File: `~/.bunfig.toml`

```toml
# Block packages published less than 86400 seconds (24 hours) ago
minimumReleaseAge = 86400
```

### How minimumReleaseAge works

- **Unit**: seconds
- `86400` seconds = 24 hours
- Override per install: `bun install --minimum-release-age 0`
- Bun does NOT have a persistent ignore-scripts or allowlist feature (as of v1.3.x)

### trustedDependencies (bun's script allowlist)

bun supports an allowlist for lifecycle scripts via `package.json`:

```json
{
  "trustedDependencies": ["esbuild", "sharp", "bcrypt"]
}
```

Only packages listed here can run `postinstall` scripts. This is bun's equivalent to pnpm's `onlyBuiltDependencies`.

### What bun does NOT have (vs npm/pnpm)

| Feature | npm | pnpm | bun |
|---|---|---|---|
| ignore-scripts | ✅ `~/.npmrc` | ✅ `config.yaml` | ❌ Not available |
| allowlist for scripts | ❌ | ✅ `onlyBuiltDependencies` | ✅ `trustedDependencies` |
| blockExoticSubdeps | ❌ | ✅ | ❌ |
| trustPolicy | ❌ | ✅ | ❌ |
| Provenance verification | ✅ `npm audit signatures` | ❌ built-in | ❌ |

## Safe commands

| Context | Command | Why |
|---|---|---|
| CI/CD, production | `bun install --frozen-lockfile` | Fails if lockfile out of sync |
| Local dev | `bun install` | Updates lockfile normally |
| Add new dep | `bun add <pkg>` | With `--frozen-lockfile` for strict mode |

## Troubleshooting

### "Package too new" error

```text
error: Package "axios@1.14.1" was published less than 86400 seconds ago
```

**Solution** — override per install:
```bash
bun install axios --minimum-release-age 0
```

Temporarily in `bunfig.toml`:
```toml
minimumReleaseAge = 0
```

### Postinstall scripts execute (no built-in block)

Bun does not have an `ignore-scripts` flag. To mitigate:

1. **Audit the package** before installing — check its `package.json` for `"scripts"` hooks
2. **Use a sandboxed environment** (container runtime) for `bun install` if untrusted
3. **Consider using pnpm or npm** in the same project for stricter control, since bun lacks these features

### Lockfile out of sync

```
error: lockfile is out of date with package.json
```

**Solution**:
```bash
bun install
# Then re-run with frozen to verify
bun install --frozen-lockfile
```

## Workaround: using npm/pnpm alongside bun

If you need bun's runtime but want npm/pnpm's security features:

```bash
# Use pnpm for install (with full security)
pnpm install --frozen-lockfile

# Use bun for runtime execution
bun run src/index.ts
```

This way you get pnpm's `onlyBuiltDependencies`, `trustPolicy`, and `blockExoticSubdeps` while still using bun as the runtime.
