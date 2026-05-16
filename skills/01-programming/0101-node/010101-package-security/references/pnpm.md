# pnpm Security Configuration

pnpm v10.16+ introduced `minimumReleaseAge`. Use the latest stable release.

## Global configuration

File: `~/Library/Preferences/pnpm/config.yaml`

```yaml
ignoreScripts: true
minimumReleaseAge: 1440
```

To set via CLI:
```bash
pnpm config set ignore-scripts true --global
pnpm config set minimumReleaseAge 1440 --global
```

### How minimumReleaseAge works

- **Unit**: minutes
- `1440` minutes = 24 hours
- Block packages published less than N minutes ago
- Override per install: `pnpm install --minimum-release-age 0 <package>`
- Override per project in `.npmrc`: `minimumReleaseAge=0`

### How ignoreScripts works

- Blocks all lifecycle scripts
- pnpm v10+ disables postinstall scripts in dependencies by default
- Unlike npm, pnpm DOES support exemptions via `onlyBuiltDependencies`

## Per-project configuration (pnpm-workspace.yaml)

File: `./pnpm-workspace.yaml`

```yaml
packages:
  - "packages/*"

# Only allow these specific packages to run build scripts
onlyBuiltDependencies:
  - esbuild
  - sharp
  - bcrypt

# Block dependencies from exotic sources (git repos, tarballs)
blockExoticSubdeps: true

# Trust policy: reject if trust level decreased from previous release
trustPolicy: no-downgrade

# Minimum release age override (minutes)
minimumReleaseAge: 1440
```

### onlyBuiltDependencies

- **Why use it**: Most supply chain attacks use postinstall scripts. By default-blocking all scripts and explicitly allowing only trusted packages, you prevent compromised dependencies from executing code.
- **How it works**: Only packages listed here can run `postinstall`, `preinstall`, etc.
- **When to add**: If a dependency fails to install with `ERR_PNPM_UNBUILT_DEPENDENCIES`, add it here after verifying it genuinely needs build scripts

### blockExoticSubdeps

- **Why use it**: Prevents transitive dependencies from fetching code from git repositories or direct tarball URLs — unusual sources that attackers use
- **Effect**: All transitive deps must come from configured registries

### trustPolicy: no-downgrade

- **Why use it**: Rejects package versions whose trust evidence decreased (e.g., previously had provenance attestation, now doesn't)
- **Combined with**: `trustPolicyExclude` (allow specific packages to bypass) and `trustPolicyIgnoreAfter` (ignore trust checks for old packages)

### allowedVersions

Restrict specific packages to specific semver ranges:

```yaml
# pnpm-workspace.yaml
allowedVersions:
  axios: 1.14.0
  esbuild: '>=0.25.0'
```

Useful for enforcing security policies (e.g., "no one can install lodash < 4.17.21").

### neverBuiltDependencies

Never allow specific packages to run build scripts, even if they are in `onlyBuiltDependencies`:

```yaml
# pnpm-workspace.yaml
neverBuiltDependencies:
  - node-gyp
```

These packages will never execute lifecycle scripts regardless of other settings.

### packageExtensions

Fix broken or missing dependency metadata from upstream packages:

```yaml
# pnpm-workspace.yaml
packageExtensions:
  express:
    dependencies:
      ejs: ^3.1.10
```

Can also add/remove `peerDependencies` and `optionalDependencies`.

## packageManager field

pnpm recommends setting the package manager in `package.json`:

```json
{
  "packageManager": "pnpm@11.1.2"
}
```

Requires `corepack enable` (ships with Node.js 18+). Enforces pnpm version across the team.

## Safe commands

| Context | Command | Why |
|---|---|---|
| CI/CD, production | `pnpm install --frozen-lockfile` | Fails if lockfile out of sync |
| Local dev | `pnpm install` | Updates lockfile normally |
| Add new dep | `pnpm add <pkg>` | With `--frozen-lockfile` to prevent unexpected resolution |

## Troubleshooting

### "Package too new" error

```
ERR_PNPM_UNSATISFIED_MINIMUM_RELEASE_AGE
```

**Solution** — override per install:
```bash
pnpm install axios --minimum-release-age 0
```

Or in project `.npmrc`:
```ini
minimumReleaseAge=0
```

### Build script blocked for a legitimate package

```
ERR_PNPM_UNBUILT_DEPENDENCIES
```

**Solution**: Add the package to `onlyBuiltDependencies` in `pnpm-workspace.yaml`:

```yaml
onlyBuiltDependencies:
  - esbuild  # already there
  - sharp    # already there
  - new-pkg  # add the new one
```

Then run `pnpm install` again.

### Trust policy violation

```text
ERR_PNPM_TRUST_POLICY_VIOLATION
```

**Solution**: Either update the package to a version with proper attestation, or exclude it:

```yaml
trustPolicyExclude:
  - legacy-pkg@1.2.3
```

### Lockfile out of sync

```
ERR_PNPM_LOCKFILE_OUTDATED
```

**Solution**:
```bash
pnpm install --no-frozen-lockfile
git add pnpm-lock.yaml
```

## Configuration precedence (lowest to highest)

1. Global `config.yaml` (system-wide)
2. `~/.npmrc` (user home)
3. `./.npmrc` (project root)
4. `./pnpm-workspace.yaml` (project root)
5. CLI flags (e.g., `--minimum-release-age 0`)
