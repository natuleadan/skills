# Repo Architecture

## Multi-category structure

Skills follow a numeric hierarchical code: `domain/category/skill-code/`:

```text
skills/
├── 01-programming/
│   ├── 0101-node/
│   │   ├── 010101-package-security/
│   │   ├── 010102-install-and-setup/
│   │   └── 010103-package-ops/
│   └── 0102-agents/
│       └── 010201-skill-creator/
├── 02-biology/                ← coming soon
└── 03-cooking/                ← coming soon
```

Each skill directory contains `SKILL.md`, plus optional `scripts/`, `references/`, and `assets/`.

## marketplace.json

Each skill must be registered in `.claude-plugin/marketplace.json` with its full path:

```json
{
  "plugins": [{
    "source": "./",
      "skills": [
        "./skills/01-programming/0101-node/010101-package-security",
        "./skills/01-programming/0101-node/010102-install-and-setup",
        "./skills/01-programming/0101-node/010103-package-ops",
        "./skills/01-programming/0102-agents/010201-skill-creator"
      ]
  }]
}
```

The path is relative to the repo root (where `source: "./"` points). `npx skills add` reads these paths and resolves SKILL.md from each.

## validate-all.py

Run from repo root to validate all registered skills:

```bash
python3 tools/validate-all.py
```

Checks:
- Every path in marketplace.json exists
- Every SKILL.md has valid frontmatter (custom parser, no external YAML lib)
- Required fields: `name` and `description`
- Name rules: max 64 chars, lowercase + hyphens only, no leading/trailing hyphens, no consecutive hyphens, NFKC-normalized, matches directory name
- Description: max 1024 characters
- Compatibility: max 500 characters (optional)
- Allowed fields only: `name`, `description`, `license`, `compatibility`, `metadata`, `allowed-tools`
- Skill has at least one `.py` file in `scripts/`
- Warns on empty `.md` files in `references/`

## Adding a new skill

1. Create `skills/<domain>/<category>/<skill-code>/SKILL.md`
2. Add Python script(s) in `skill-name/scripts/`
3. Register in `.claude-plugin/marketplace.json`
4. Validate: `python3 tools/validate-all.py`
5. Commit and push

Users install with:
```bash
npx skills add natuleadan/skills --skill skill-name
```
