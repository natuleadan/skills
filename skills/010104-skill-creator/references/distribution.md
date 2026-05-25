# Distribution

## Repository structure

Skills are distributed via Git repositories. A single repo can contain one or many skills using a numeric code hierarchy:

```text
my-skills-repo/
├── .claude-plugin/
│   └── marketplace.json
├── 01-programming/
│   └── 0101-node/
│       └── 010101-package-security/
│           └── SKILL.md
├── tools/
│   └── validate-all.py
├── .gitignore
└── README.md
```

Skills follow the `domain/category/skill-code/SKILL.md` convention with numeric prefixes for grouping.

## Plugin manifest

The `.claude-plugin/marketplace.json` defines plugins — groupings of skills:

```json
{
  "name": "my-collection",
  "owner": {
    "name": "owner-name"
  },
  "metadata": {
    "description": "What this collection does",
    "version": "1.0.0"
  },
  "plugins": [
    {
      "name": "my-plugin",
      "description": "What these skills do",
      "source": "./",
      "strict": false,
      "skills": [
        "./01-programming/0101-node/010101-package-security",
        "./01-programming/0102-agents/010201-skill-creator"
      ]
    }
  ]
}
```

Paths are relative to the repo root (the `source` field anchors it there). Each path must resolve to a directory containing `SKILL.md`.

## Packaging

A `.skill` file is a distributable archive (ZIP file) containing the skill folder:

```text
my-skill.skill
├── SKILL.md
├── references/...
├── scripts/...
└── assets/...
```

The entry point must be `SKILL.md` at the archive root. Exclude `evals/`, `__pycache__/`, `.DS_Store`.

## Installation

```bash
# Install a specific skill
npx skills add natuleadan/skills --skill 010101-package-security

# Install all skills from a repo
npx skills add natuleadan/skills
```
