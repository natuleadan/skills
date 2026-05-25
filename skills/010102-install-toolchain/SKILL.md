---
name: 010102-install-toolchain
license: MIT
compatibility: Requires Node.js 18+ and npm (ships with Node.js)
description: "Installs and configures JavaScript toolchain — npm, pnpm, bun, Node.js version managers, and PATH setup for new development environments."
---

# Package Manager Install & Setup

This skill guides you through installing and configuring a JavaScript/TypeScript package manager toolchain in this exact order:

```
npm  (comes with Node.js)  →  pnpm (via npm)  →  bun (via pnpm global)
```

Each tool is installed using the previous one.

## How to use this skill

1. If the user needs **step-by-step installation instructions** → read `references/setup-guide.md`
2. If the user needs **validation of existing setup** → run `python scripts/validate.py` and interpret the results
3. If the user reports **"command not found"** → read the Troubleshooting section in `references/setup-guide.md`

## Quick reference

```bash
# Install
npm install -g pnpm          # install pnpm via npm
pnpm add -g bun              # install bun via pnpm
pnpm setup                   # configure PATH for global bins

# Validate
python scripts/validate.py

# Verification
node --version && npm --version && pnpm --version && bun --version
```

## References

- `references/setup-guide.md` — Full step-by-step install guide with troubleshooting
- `scripts/validate.py` — Validation script for checking your setup
