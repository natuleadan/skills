# Cross-Cutting Supply Chain Security

## Overrides: Patching transitive dependencies

When a CVE is found in a transitive dependency, you can force a specific version without waiting for the intermediate package to update.

### npm

```json
{
  "overrides": {
    "axios": "1.14.0",
    "minimatch": "3.1.2"
  }
}
```

Overrides apply to the entire tree. If `library-a` depends on `axios@^0.27`, the override forces `axios@1.14.0` everywhere.

Scoped override (only override when used as a dep of a specific package):
```json
{
  "overrides": {
    "library-a": {
      "axios": "1.14.0"
    }
  }
}
```

### pnpm

```json
{
  "pnpm": {
    "overrides": {
      "axios": "1.14.0"
    }
  }
}
```

pnpm also supports `pnpm.packageExtensions` to fix broken package metadata:

```json
{
  "pnpm": {
    "packageExtensions": {
      "express": {
        "dependencies": {
          "ejs": "^3.1.10"
        }
      }
    }
  }
}
```

### bun

bun supports the same `overrides` field as npm in `package.json`.

## Registry configuration & dependency confusion

Dependency confusion: a public package with the same name as an internal private package is published to the public registry. When your CI installs, it may pull the public malicious version instead of your private one.

### scoped registries

Always use scoped packages for private code, and configure per-scope registries:

```ini
; ~/.npmrc or ./.npmrc
@mycompany:registry=https://npm.pkg.github.com/
@internal:registry=https://registry.internal.example.com/
```

### registry order

npm/pnpm try scoped registries first, then fall back to the default `registry`. Setting the default registry explicitly prevents ambiguity:

```ini
registry=https://registry.npmjs.org/
```

### dependency confusion detection

Run `python scripts/scan-exotic.py` to detect non-registry sources in lockfiles.

### verification checklist

- Every `@scope` used in `package.json` has a corresponding `@scope:registry` in `.npmrc`
- No internal package names are publicly available on npm
- CI uses `--frozen-lockfile` so no unexpected registry resolution occurs

## save-exact: Pin versions automatically

By default `npm install axios` saves `"axios": "^1.14.0"` (caret range). With `save-exact=true`, it saves `"axios": "1.14.0"` (exact).

### enable globally

```ini
; ~/.npmrc
save-exact=true
```

### enable per project

```ini
; ./.npmrc
save-exact=true
```

This also affects pnpm and yarn when they read `.npmrc`.

### trade-off

- Pro: prevents unexpected major/minor upgrades on `npm install`
- Con: requires explicit manual updates (`npm install axios@1.15.0`) to get new versions
- Recommended for: production applications, libraries published to registry

## engines & engine-strict

Prevent your package from running on vulnerable or incompatible Node.js versions.

### package.json

```json
{
  "engines": {
    "node": ">=18.0.0",
    "npm": ">=9.0.0"
  }
}
```

### enforce with engine-strict

```ini
; ./.npmrc
engine-strict=true
```

Without `engine-strict`, `engines` is just a warning. With it, `npm install` fails if the current Node version doesn't satisfy `engines.node`.

### pnpm

pnpm respects `engines` from `package.json` and can also enforce via:

```yaml
# pnpm-workspace.yaml
engineStrict: true
```

### bun

bun respects `engines` in `package.json` and warns on mismatch but does not block by default.

## packageManager: Lock the package manager version

```json
{
  "packageManager": "pnpm@11.1.2"
}
```

- Corepack (ships with Node.js 18+) enforces this
- `corepack enable` must be run once
- Prevents "works on my machine" issues
- Blocks use of the wrong package manager entirely (e.g., `npm install` in a pnpm project)

### common settings

```json
"packageManager": "npm@11.12.1"
"packageManager": "pnpm@11.1.2"
"packageManager": "bun@1.3.14"
"packageManager": "yarn@4.5.0"
```

## SBOM generation

Software Bill of Materials for supply chain transparency and compliance.

### npm SBOM

```bash
# Generate SPDX SBOM
npm sbom

# Generate CycloneDX SBOM
npm sbom --format=cyclonedx

# Output to file
npm sbom --output-file=sbom.spdx.json
```

Supports SPDX 2.3 and CycloneDX 1.5 formats.

### pnpm SBOM

pnpm doesn't have a built-in sbom command. Use third-party tools:

```bash
# With @cyclonedx/cyclonedx-npm
npx @cyclonedx/cyclonedx-npm --output-file sbom.xml

# With cdxgen
npx cdxgen -o sbom.json
```

### bun SBOM

bun doesn't have a native sbom command. Use npm's sbom against `bun.lock`:

```bash
# Generate from lockfile
npm sbom --lockfile=bun.lock
```

## Lockfile diff review in PRs

Lockfile changes in PRs should be reviewed carefully — unexpected additions can indicate compromised dependencies.

### what to check

| Signal | What it means |
|---|---|
| New package added | Was it intentional? Does the PR description mention it? |
| `resolved` URL changed | Did a package source change unexpectedly? |
| `integrity` hash changed | Did the package content change (possible tampering)? |
| Old package removed | Was it intentionally removed, or is something hiding removal? |
| Version downgrade | Trust policy violation or dependency confusion? |

### automation

```bash
# Check lockfile diff for additions/deletions
git diff HEAD --stat package-lock.json

# Show all added packages
git diff HEAD -- package-lock.json | grep '^+"' | head -20
```

Run `python scripts/scan-exotic.py --ci` in CI to fail if any exotic source is detected in the lockfile.

## Git-based dependencies

Dependencies from git repos bypass registry security entirely (no integrity checks, no provenance).

```json
{
  "dependencies": {
    "my-lib": "github:user/repo#commit",
    "other-lib": "git+https://github.com/user/repo.git",
    "another": "user/repo"
  }
}
```

### risks

- No `integrity` or provenance guarantees
- The resolved version can change without notice (branch references)
- If the repo is compromised, all dependents are compromised

### best practices

- Pin to a specific commit hash, not a branch name
- Audit the package source before adding
- Prefer published registry versions over git deps
- If you must use git deps, mirror them to a private registry

### detection

`python scripts/scan-exotic.py` detects git-resolved packages in lockfiles.
