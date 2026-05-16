# npm Security Configuration

npm v11.10.0+ (February 2026) introduced `min-release-age` for supply chain attack mitigation. Use the latest stable release.

## Global configuration

File: `~/.npmrc`

```ini
# Block packages published less than 1 day ago
min-release-age=1

# Block all postinstall/preinstall scripts
ignore-scripts=true

# Always pin exact versions when installing
save-exact=true

# Only fail CI on high/critical vulnerabilities
audit-level=high
```

To set via CLI:
```bash
npm config set min-release-age 1
npm config set ignore-scripts true
npm config set save-exact true
npm config set audit-level high
```

### How min-release-age works

- **Unit**: days
- `min-release-age=1` = reject packages published less than 1 day ago
- Internally stored as `before` timestamp in npm config
- Override per install: `npm install --min-release-age=0 <package>`
- Override in `.npmrc` per project: `min-release-age=0`

### How ignore-scripts works

- Blocks all lifecycle scripts: `preinstall`, `install`, `postinstall`, `prepublish`, etc.
- Needed by some packages: `esbuild`, `sharp`, `bcrypt`, `node-sass`
- npm does NOT have an allowlist equivalent to pnpm's `onlyBuiltDependencies`
- To allow specific packages, set `ignore-scripts=false` and audit manually
- Recommended approach: keep `ignore-scripts=true` globally, set `ignore-scripts=false` only in project-level `.npmrc` where you trust the deps

### save-exact

- Makes `npm install <pkg>` save an exact version (`"axios": "1.14.0"`) instead of a range (`"axios": "^1.14.0"`)
- Prevents unexpected version drift on `npm install`
- Also checked by pnpm and yarn when they read `.npmrc`, though each tool may handle it differently

### audit-level

- Controls the minimum vulnerability level that causes `npm audit` to exit with code 1
- Values: `info`, `low`, `moderate`, `high`, `critical` (default: `low`)
- Set to `high` in production to ignore non-critical advisories

## Per-project configuration

File: `./.npmrc` (project root)

```ini
# Project-level overrides
ignore-scripts=false
min-release-age=0
engine-strict=true
save-exact=true
```

## Safe commands

| Context | Command | Why |
|---|---|---|
| CI/CD, production | `npm ci` | Installs exactly from lockfile; fails if out of sync |
| Local dev, adding packages | `npm install <pkg>` | Updates lockfile |
| Verify provenance | `npm audit signatures` | Checks packages were built from claimed source |
| CI vulnerability check | `npm audit --audit-level=high` | Fails build on high/critical vulns |
| Generate SBOM | `npm sbom` | Creates SPDX/CycloneDX bill of materials |

**Critical rule**: In CI/CD, always use `npm ci`, NOT `npm install`. `npm ci` enforces lockfile integrity.

## Troubleshooting

### "Package too new" error

```
npm ERR! code ENOTACCEPTABLE
npm ERR! package axios@1.14.1 was published less than 1 day ago
```

**Solution** — override per install:
```bash
npm install axios --min-release-age=0
```

Or for a project, add to `.npmrc`:
```ini
min-release-age=0
```

### Postinstall script blocked

```
npm WARN ignoring scripts in <package>
```

**Solution**: Either disable ignore-scripts globally (not recommended), or set per-project:
```bash
echo "ignore-scripts=false" >> ./.npmrc
```
Then audit the dependencies that need scripts before installing.

### Lockfile out of sync

```
npm ERR! Found: package.json and package-lock.json are out of sync.
```

**Solution**: Run `npm install` to regenerate the lockfile, then commit both:
```bash
npm install
git add package.json package-lock.json
```

