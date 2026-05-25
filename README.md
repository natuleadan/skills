<p align="center">
  <a href="https://github.com/natuleadan"><img src="https://avatars.githubusercontent.com/u/210283438?v=4&s=120" width="120" height="120" alt="natuleadan" /></a>
</p>

<h1 align="center">Natuleadan Skills</h1>
<p align="center"><strong>Agent skills for AI coding agents across 20 domains of human knowledge</strong></p>

<p align="center">
  <img src="https://img.shields.io/badge/Count-27-8B5CF6?style=for-the-badge" alt="27 skills" />
  <img src="https://img.shields.io/badge/Domains-20-blue?style=for-the-badge" alt="20 domains" />
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge" alt="MIT License" /></a>
  <br />
  <a href="https://skills.sh/natuleadan/skills"><img src="https://skills.sh/b/natuleadan/skills" alt="Skills" /></a>
</p>

## 1. What is Natuleadan Skills?

A collection of agent skills for AI coding agents spanning 20 domains, from programming and business to artificial intelligence, security, and data engineering. Each skill is a self-contained package of instructions, reference documentation, and Python validation scripts. Skills follow the [Agent Skills](https://agentskills.io/) format and are installable via `npx skills add`.

Our [Skills Index](SKILLS.md) lists the complete catalog with domain, category, and description for every skill.

## 2. Available Skills

27 skills across 7 active domains: programming, business, artificial intelligence, devops, web, security, and data. 13 additional domains are reserved for future expansion.

See the full catalog: [Skills Index](SKILLS.md)

## 3. Technology Stack

[skills.sh](https://skills.sh) handles registry and distribution. Python 3 runs validation via `tools/validate-all.py`. Node.js powers installation via `npx skills add`. Husky 9 and Commitlint 20 enforce conventional commits on every change. Bun is used for local development.

## 4. Project Status

Seven domains are active: `01-programming` (15 skills), `02-business` (1), `03-artificial` (4), `04-devops` (1), `05-web` (2), `06-security` (3), and `07-data` (1). Domains `08` through `20` are reserved for future expansion.

Every push and pull request is automatically validated via GitHub Actions to ensure all skills remain compliant.

## 5. Getting Started

Prerequisites: Node.js 18+, Python 3.8+, and optionally Bun.

```bash
# Install all skills
npx skills add natuleadan/skills

# Install a specific skill
npx skills add natuleadan/skills --skill 010101-package-security
```

For local development: `git clone`, `bun install`, then `python3 tools/validate-all.py`.

## 6. Architecture

Skills use a flat directory structure with six-digit codes that encode a three-level hierarchy: domain (first 2 digits), category (next 2), and skill (last 2). The naming format is `DDCCSS-word-word` — exactly two hyphenated words after the code, each at least four characters. Every skill lives directly under `skills/` with a `SKILL.md`, `scripts/`, and optional `references/` directory.

The manifest at `.claude-plugin/marketplace.json` is the single source of truth for what the repo contains. Our [Contribution Guidelines](CONTRIBUTING.md) document provides full conventions for skill creation.

## 7. Coding Standards

Commit messages use conventional format: `type(scope): description`. Supported types include `feat`, `fix`, `upgrade` (breaking), `docs`, `refactor`, `test`, `chore`, `ci`, and others. Scope is mandatory, subject is lowercase, maximum 100 characters.

Skill names: lowercase, hyphens only, maximum 64 characters, must match the directory name. All content is written in English. Frontmatter requires `name` and `description`; optional fields include `license`, `compatibility`, `metadata`, and `allowed-tools`.

## 8. Testing & Validation

Every skill is validated through `python3 tools/validate-all.py` which checks registry integrity, frontmatter compliance, directory-to-name matching, `metadata.json` completeness, and empty files. CI runs this on every push. Our validation process is documented in [CONTRIBUTING.md](CONTRIBUTING.md).

## 9. Development Workflow

Plan the skill domain and functionality, create the directory with `SKILL.md` + `scripts/` + `references/`, register the path in `marketplace.json`, run `validate-all.py`, commit with a conventional message, and push. Husky runs validation automatically on every commit.

## 10. Contributing

Our [Contribution Guidelines](CONTRIBUTING.md) document provides detailed conventions for skill creation, covering directory structure, SKILL.md frontmatter rules, naming, validation, and commit format. All contributions must pass `python3 tools/validate-all.py` before merging.

## 11. License & Legal

MIT — Leonardo Jara. See [LICENSE](LICENSE) for full terms.

## 12. Ownership & Copyright

Maintained by Leonardo Jara ([@leojara95](https://github.com/leojara95)) under the natuleadan organization ([@natuleadan](https://github.com/natuleadan)).

---

## Community

<p align="left">
  <a href="https://github.com/natuleadan"><img src="https://avatars.githubusercontent.com/u/210283438?v=4&s=48" width="48" height="48" alt="natuleadan" title="natuleadan"/></a>
  <a href="https://github.com/leojara95"><img src="https://avatars.githubusercontent.com/u/268038834?v=4&s=48" width="48" height="48" alt="leojara95" title="leojara95"/></a>
</p>

---

## Star History

<a href="https://www.star-history.com/#natuleadan/skills&Date">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/image?repos=natuleadan/skills&type=date&theme=dark" />
    <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/image?repos=natuleadan/skills&type=date&theme=light" />
    <img alt="Star History Chart" src="https://api.star-history.com/image?repos=natuleadan/skills&type=date" />
  </picture>
</a>
