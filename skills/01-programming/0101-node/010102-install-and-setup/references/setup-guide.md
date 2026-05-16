# Detailed Setup Guide

Step-by-step installation instructions for npm → pnpm → bun.

## Step 1: Install Node.js (includes npm)

### Official installer (recommended for beginners)

1. Go to https://nodejs.org
2. Download the LTS version (macOS .pkg)
3. Run the installer — it adds `node` and `npm` to PATH automatically

### Homebrew

```bash
brew install node
```

### nvm (Node Version Manager, for managing multiple versions)

```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash
# restart terminal, then:
nvm install --lts
```

### Verify

```bash
node --version    # e.g., v24.15.0
npm --version     # e.g., 11.12.1
```

No further PATH configuration is needed — the installer handles it.

## Step 2: Install pnpm (via npm)

Once npm is available, install pnpm globally:

```bash
npm install -g pnpm
```

### Configure PATH for pnpm global binaries

pnpm stores global binaries in `~/Library/pnpm/bin` on macOS. If `pnpm` itself is not found after installation, add this to `~/.zshrc`:

```bash
export PATH="$HOME/Library/pnpm/bin:$PATH"
```

Then reload:

```bash
source ~/.zshrc
```

### Verify

```bash
pnpm --version    # e.g., 11.1.2
```

### pnpm setup (automates PATH configuration)

pnpm includes a setup command that configures PATH automatically:

```bash
pnpm setup
```

This adds the necessary lines to `~/.zshrc`. Run it once and then open a new terminal.

## Step 3: Install bun (via pnpm global)

Bun can be installed through pnpm's global package management:

```bash
pnpm add -g bun
```

This installs bun into pnpm's global store and creates a shim at `~/Library/pnpm/bin/bun`.

### Verify

```bash
bun --version     # e.g., 1.3.14
```

If `bun: command not found`, ensure `~/Library/pnpm/bin` is in your PATH.

### Alternative — Official installer (standalone)

```bash
curl -fsSL https://bun.sh/install | bash
```

This puts bun at `~/.bun/bin/bun` and adds it to `~/.zshrc` automatically.

### Removing bun installed via pnpm

```bash
pnpm remove -g bun
```

## Final verification

Run all checks in a fresh terminal:

```bash
node --version
npm --version
pnpm --version
bun --version
```

All four should print version numbers.

## Troubleshooting

### "command not found" after installation

| Tool | Most likely fix |
|---|---|
| npm | Reinstall Node.js — npm is bundled with it |
| pnpm | Add `~/Library/pnpm/bin` to PATH, or run `pnpm setup` |
| bun (via pnpm) | Same as pnpm — bun is in the same pnpm global bin dir |
| bun (standalone) | Add `~/.bun/bin` to PATH, or reinstall |

### PATH configuration snippet for `~/.zshrc`

```bash
export PATH="$HOME/Library/pnpm/bin:$PATH"
export PATH="$HOME/.bun/bin:$PATH"
```

### Permission errors (EACCES)

If you get permission errors with npm global installs, configure npm to use a local directory:

```bash
npm config set prefix ~/.npm-global
export PATH="$HOME/.npm-global/bin:$PATH"
```
