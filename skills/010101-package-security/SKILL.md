---
name: 010101-package-security
license: MIT
description: Secures npm, pnpm, and bun against supply chain attacks — lockfile enforcement, provenance, version pinning, dependency audit, and script blocking.
---

# Package Manager Security

This skill helps you harden npm, pnpm, and bun against supply chain attacks. It provides configuration guides, best practices, and troubleshooting for all three package managers.

## How to use this skill

1. Identify which package manager(s) the user's query is about (npm, pnpm, bun, or multiple)
2. If they ask about **npm** → read `references/npm.md`
3. If they ask about **pnpm** → read `references/pnpm.md`
4. If they ask about **bun** → read `references/bun.md`
5. If they ask about multiple or general concepts (lockfiles, CI/CD, version pinning) → read all relevant files
6. Answer concisely and directly. Provide configuration snippets and commands the user can copy/paste.

## Common concepts (apply to all three)

These security practices apply regardless of package manager. Mention them when relevant.

### Lockfile enforcement
- Always commit the lockfile: `package-lock.json` (npm), `pnpm-lock.yaml` (pnpm), `bun.lock` (bun)
- In CI/CD, use the frozen-lockfile equivalent:
  - npm: `npm ci`
  - pnpm: `pnpm install --frozen-lockfile`
  - bun: `bun install --frozen-lockfile`
- Review lockfile changes in PRs — unexpected additions can indicate compromised deps

### Version pinning
- Prefer exact versions (`"axios": "1.12.0"`) over ranges (`"axios": "^1.12.0"`)
- Tilde ranges (`"axios": "~1.12.0"`) are safer than caret ranges for production
- Never use `"*"` or `"latest"` in production

### Supply chain monitoring
- `npm audit signatures` — verify package provenance
- Integrate SCA (Software Composition Analysis) tools for vulnerability scanning
- Block known C2 domains at the firewall/DNS level

## Audit existing setup

Run `python scripts/audit.py` to check global security settings (npmrc, pnpm config, bunfig).

Run `python scripts/audit-project.py` from your project root to check project-level settings (package.json: overrides, engines, packageManager, pnpm config).

Run `python scripts/scan-exotic.py` to scan lockfiles for dependencies from exotic sources (git repos, tarballs, local paths). Use `--ci` to fail in CI if any exotic deps found.

## Output format

When providing configuration:
1. Show the exact file content (with file path comment)
2. Explain what each setting does
3. Provide the command to apply it
4. If troubleshooting, explain the root cause

## References

- `references/npm.md` — npm-specific security configuration
- `references/pnpm.md` — pnpm-specific security configuration
- `references/bun.md` — bun-specific security configuration
- `references/cross-cutting.md` — Registries, overrides, engines, SBOM, lockfile review, git deps
- `scripts/audit.py` — Audit script that checks all global security settings
- `scripts/audit-project.py` — Project-level audit (package.json checks)
- `scripts/scan-exotic.py` — Lockfile scanner for exotic dependency sources
