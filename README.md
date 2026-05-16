<p align="center">
  <a href="https://github.com/natuleadan"><img src="https://avatars.githubusercontent.com/u/210283438?v=4&s=120" width="120" height="120" alt="natuleadan" /></a>
</p>

<h1 align="center">Natuleadan Skills</h1>
<p align="center"><strong>Agent skills for AI coding agents across multiple domains</strong></p>

<p align="center">
  <img src="https://img.shields.io/badge/Skills-4-8B5CF6?style=for-the-badge" alt="4 skills" />
  <img src="https://img.shields.io/badge/Domains-3-blue?style=for-the-badge" alt="3 domains" />
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge" alt="MIT License" /></a>
</p>

## Project Description

A collection of agent skills for AI coding agents spanning multiple domains. Skills are packaged instructions and scripts that extend agent capabilities. Currently focused on programming (Node.js), with biology and cooking domains planned.

Skills follow the [Agent Skills](https://agentskills.io/) format and are installable via `npx skills add`.

## Technology Stack

- **[skills.sh](https://skills.sh)** — Agent skills registry and distribution
- **Python 3** — Skill validation and automation scripts (`tools/validate-all.py`)
- **Node.js / npx** — Skill installation via `npx skills add`
- **Husky 9** — Git hooks (pre-commit + commit-msg)
- **Commitlint 20** — Conventional commit enforcement
- **Bun** — Package manager and runtime (local development only)

## Project Architecture

Skills are structured as a flat registry with a plugin manifest and domain-organized directories. The system has three layers:

1. **Registry** — `.claude-plugin/marketplace.json` declares all available skills and their paths. This is the single source of truth for what the repo contains.
2. **Skills** — Each skill is a directory under `skills/<domain>/` containing `SKILL.md` (instructions), `scripts/` (Python automation), and optionally `references/` (supporting documentation).
3. **Validation** — `tools/validate-all.py` reads the marketplace manifest, resolves each skill path, and validates every SKILL.md against the Agent Skills format specification.

## Getting Started

### Prerequisites

- **Node.js 18+** — Required for `npx skills add` (end users)
- **Python 3.8+** — Required for local validation (contributors)
- **Bun** — Recommended for local development (optional)

### Installation

```bash
# Install all skills
npx skills add natuleadan/skills

# Install a specific skill
npx skills add natuleadan/skills --skill 010101-package-security

# Update a skill after changes
npx skills update natuleadan/skills --skill 010101-package-security
```

### Local Setup

```bash
git clone https://github.com/natuleadan/skills.git
cd skills
bun install         # Install husky + commitlint
python3 tools/validate-all.py  # Verify everything works
```

## Project Structure

```text
skills/
├── .claude-plugin/
│   └── marketplace.json          ← skill registry
├── .husky/
│   ├── pre-commit                ← runs validate-all.py
│   └── commit-msg                ← runs commitlint
├── skills/                       ← domain folders
├── 01-programming/           ← active domain
│   ├── 0101-node/
│   │   ├── 010101-package-security/
│   │   ├── 010102-install-and-setup/
│   │   └── 010103-package-ops/
│   └── 0102-agents/
│       └── 010201-skill-creator/
├── 02-biology/               ← coming soon
└── 03-cooking/               ← coming soon
├── tools/
│   └── validate-all.py           ← validation script
├── .gitignore
├── LICENSE
├── README.md
├── package.json
├── commitlint.config.js
└── bun.lock
```

Every skill lives at `skills/<domain>/<category>/<skill-code>/` and contains a `SKILL.md` file.

## Key Features

- **4 production-ready skills** for Node.js development: security auditing, toolchain setup, package operations, and agent skill creation
- **Multi-domain architecture** — extendable to any domain (biology, cooking, etc.) by adding a new directory under `skills/`
- **Automatic validation** — Python-based validator checks every SKILL.md for correct frontmatter, naming conventions, and required fields
- **Conventional commits** — Husky + Commitlint enforce standardized commit messages following the conventional commits specification
- **Marketplace integration** — Skills are registered via `.claude-plugin/marketplace.json` and installable through the `npx skills` CLI

## Development Workflow

1. **Plan** — Define the skill domain, category, and functionality
2. **Create** — Scaffold `skills/<domain>/<category>/<skill-code>/` with `SKILL.md`, `scripts/`, and `references/`
3. **Register** — Add the skill path to `.claude-plugin/marketplace.json`
4. **Validate** — Run `python3 tools/validate-all.py` to check format compliance
5. **Commit** — Stage changes and commit with a conventional message (`feat(skills): add new-skill-name`). Husky automatically runs validation and commitlint
6. **Push** — Push to GitHub; users update via `npx skills update natuleadan/skills`

## Coding Standards

### Commit Messages

Format: `type(scope): description`

| Type | Usage |
|---|---|
| `feat` | New feature or skill |
| `fix` | Bug fix |
| `upgrade` | Breaking change |
| `docs` | Documentation |
| `chore` | Configuration, tooling |

Rules: scope is required, max 100 characters, lowercase subject.

### Skill Naming

- Max 64 characters
- Lowercase with hyphens only
- No leading, trailing, or consecutive hyphens
- Must match directory name (NFKC-normalized)
- All skills written in **English** for cross-agent compatibility

### Skill Frontmatter (SKILL.md)

Required fields: `name`, `description`. Allowed fields: `name`, `description`, `license`, `compatibility`, `metadata`, `allowed-tools`.

## Testing / Validation

```bash
python3 tools/validate-all.py
```

The validation script performs the following checks:

- **Registry integrity** — Every path in `marketplace.json` resolves to an existing skill directory
- **Frontmatter validation** — Custom YAML parser checks required fields and naming rules
- **Directory matching** — Skill name must match the containing directory name
- **Script presence** — Each skill must have at least one Python script in its `scripts/` directory
- **Empty files** — Warns on empty `.md` files in `references/`

## Contributing

Contributions are welcome. To add a new skill:

1. Create `skills/<domain>/<category>/<skill-code>/SKILL.md`
2. Add Python scripts in `skill-name/scripts/`
3. Register the path in `.claude-plugin/marketplace.json`
4. Run `python3 tools/validate-all.py` to verify
5. Commit using conventional commit format

All code must pass validation before merging. Husky hooks run automatically on commit.

## License

MIT — Leonardo Jara

## Contributors

<p align="left">
  <a href="https://github.com/natuleadan"><img src="https://avatars.githubusercontent.com/u/210283438?v=4&s=48" width="48" height="48" alt="natuleadan" title="natuleadan"/></a>
  <a href="https://github.com/leojara95"><img src="https://avatars.githubusercontent.com/u/268038834?v=4&s=48" width="48" height="48" alt="leojara95" title="leojara95"/></a>
</p>

## Star History

<a href="https://www.star-history.com/#natuleadan/skills&Date">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/image?repos=natuleadan/skills&type=date&theme=dark" />
    <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/image?repos=natuleadan/skills&type=date&theme=light" />
    <img alt="Star History Chart" src="https://api.star-history.com/image?repos=natuleadan/skills&type=date" />
  </picture>
</a>
