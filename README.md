<p align="center">
  <a href="https://github.com/natuleadan"><img src="https://avatars.githubusercontent.com/u/210283438?v=4&s=120" width="120" height="120" alt="natuleadan" /></a>
</p>

<h1 align="center">Natuleadan Skills</h1>
<p align="center"><strong>Agent skills for AI coding agents across multiple domains</strong></p>

<p align="center">
  <img src="https://img.shields.io/badge/Count-24-8B5CF6?style=for-the-badge" alt="24 skills" />
  <img src="https://img.shields.io/badge/Domains-2-blue?style=for-the-badge" alt="2 domains" />
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge" alt="MIT License" /></a>
  <br />
  <a href="https://skills.sh/natuleadan/skills"><img src="https://skills.sh/b/natuleadan/skills" alt="Skills" /></a>
</p>

## 1. What is Natuleadan Skills?

A collection of agent skills for AI coding agents spanning multiple domains. Skills are packaged instructions and scripts that extend agent capabilities. Currently focused on programming (Node.js, architecture, vector search) and business CRM, with biology and cooking domains planned.

Skills follow the [Agent Skills](https://agentskills.io/) format and are installable via `npx skills add`.

## 2. Available Skills

Skills use numeric codes to encode a three-level hierarchy: domain, category, and skill. Each skill lives at `skills/<skill-code>-<name>/` with a `SKILL.md` file.

| Domain | Category | Skill | Description |
|---|---|---|---|
| `01-programming` | `0101-node` | `010101-package-security` | Hardens npm, pnpm, and bun against supply chain attacks |
| | | `010102-install-and-setup` | Installs and configures the JS/TS toolchain from scratch |
| | | `010103-package-ops` | Day-to-day package management: install, update, audit, publish |
| | `0102-agents` | `010201-skill-creator` | Guides creation of new Agent Skills |
| | `0103-standards` | `010301-frontend-coding` | React, accessibility, and frontend performance best practices |
| | | `010302-backend-arch` | Error handling, module structure, env management, API patterns |
| | | `010303-code-quality` | TypeScript strict patterns, testing (vitest), and security rules |
| | `0104-git` | `010401-git-commits` | Conventional commits, safe staging, disaster recovery via git reflog |
| | | `010402-release-automation` | Semantic-release, version bump mapping, post-release sync |
| | `0105-architecture` | `010501-web-caching` | Three-tier caching strategy: browser/CDN, runtime cache, distributed cache |
| | | `010502-web-clean-arch` | Clean Architecture layer ordering and strict inward dependency flow |
| | | `010503-web-security` | Multi-layer security: rate limiting, CSP, security headers, CORS |
| | | `010504-web-server-actions` | Server Actions: form handling, auth, typed returns, error patterns |
| | | `010505-web-zero-trust` | Zero Trust auth: single validation, role propagation, no client trust |
| | `0106-deploy` | `010601-docker-deploy` | Docker multi-stage builds, env mgmt, CI/CD integration |
| | `0107-elysia` | `010701-elysia-patterns` | Elysia API framework: plugins, controllers, auto-routing, auth macros |
| | `0108-nextjs` | `010801-nextjs-compiler` | SWC compiler optimization: removeConsole, tree-shaking, bundle size |
| | `0109-auth` | `010901-better-auth` | Better Auth integration: setup, API endpoints, client SDK, session provider |
| | `0110-database` | `011001-prisma-database` | Prisma 7 setup with PostgreSQL adapter and Better Auth schema models |
| | `0111-vector` | `011101-lancedb-search-core` | Vector search fundamentals: distance metrics, ANN, embeddings |
| | | `011102-lancedb-index-optimization` | Vector index types (IVF, HNSW, PQ), quantization, reindexing |
| | | `011103-lancedb-fts-search` | Full-text search with BM25: FTS indexing, fuzzy, boolean queries |
| | | `011104-lancedb-hybrid-multivector` | Hybrid search (vector+FTS), multivector (ColBERT), filtering |
| `04-business` | `0401-crm` | `040101-contact-crm` | Three-entity CSV contact management with UUID linking, phone validation, and auto-export |

## 3. Technology Stack

- **[skills.sh](https://skills.sh)** — Agent skills registry and distribution
- **Python 3** — Skill validation and automation scripts (`tools/validate-all.py`)
- **Node.js / npx** — Skill installation via `npx skills add`
- **Husky 9** — Git hooks (pre-commit + commit-msg)
- **Commitlint 20** — Conventional commit enforcement
- **Bun** — Package manager and runtime (local development only)

## 4. Project Status

**Active domains:** `01-programming` (23 skills) and `04-business` (1 skill).

| Domain | Skills |
|---|---|
| `01-programming` | 010101-package-security, 010102-install-and-setup, 010103-package-ops, 010201-skill-creator, 010301-frontend-coding, 010302-backend-arch, 010303-code-quality, 010401-git-commits, 010402-release-automation, 010501-web-caching, 010502-web-clean-arch, 010503-web-security, 010504-web-server-actions, 010505-web-zero-trust, 010601-docker-deploy, 010701-elysia-patterns, 010801-nextjs-compiler, 010901-better-auth, 011001-prisma-database, 011101-lancedb-search-core, 011102-lancedb-index-optimization, 011103-lancedb-fts-search, 011104-lancedb-hybrid-multivector |
| `04-business` | 040101-contact-crm — CSV-based CRM with Org→Contact→Product linking |
| `05-architecture` | 050101-caching, 050102-clean-arch, 050103-docker-deploy, 050104-elysia-patterns, 050105-nextjs-compiler, 050106-security, 050107-server-actions, 050108-zero-trust, 050201-better-auth, 050301-prisma-database, 050401-search-core, 050402-index-optimization, 050403-fts-search, 050404-hybrid-multivector |

**Placeholder domains:** `02-biology` and `03-cooking` — ready for future skills.

**CI/CD:** Every push and pull request is automatically validated via GitHub Actions (`tools/validate-all.py`) to ensure all skills remain compliant.

## 5. Getting Started

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

## 6. Architecture

Skills are structured as a flat registry with a plugin manifest and domain-organized directories. The system has three layers:

1. **Registry** — `.claude-plugin/marketplace.json` declares all available skills and their paths. This is the single source of truth for what the repo contains.
2. **Skills** — Each skill is a directory under `skills/<domain>/` containing `SKILL.md` (instructions), `scripts/` (Python automation), and optionally `references/` (supporting documentation).
3. **Validation** — `tools/validate-all.py` reads the marketplace manifest, resolves each skill path, and validates every SKILL.md against the Agent Skills format specification.

## 7. Coding Standards

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

## 8. Testing & Validation

```bash
python3 tools/validate-all.py
```

The validation script performs the following checks:

- **Registry integrity** — Every path in `marketplace.json` resolves to an existing skill directory
- **Frontmatter validation** — Custom YAML parser checks required fields and naming rules
- **Directory matching** — Skill name must match the containing directory name
- **metadata.json** — Every skill must have a valid `metadata.json` with `version`, `abstract`, and `references`
- **Empty files** — Warns on empty `.md` files in `references/`

## 9. Development Workflow

1. **Plan** — Define the skill domain, category, and functionality
2. **Create** — Scaffold `skills/<domain>/<category>/<skill-code>/` with `SKILL.md`, `scripts/`, and `references/`
3. **Register** — Add the skill path to `.claude-plugin/marketplace.json`
4. **Validate** — Run `python3 tools/validate-all.py` to check format compliance
5. **Commit** — Stage changes and commit with a conventional message (`feat(skills): add new-skill-name`). Husky automatically runs validation and commitlint
6. **Push** — Push to GitHub; users update via `npx skills update natuleadan/skills`

## 10. Contributing

Our Contribution Guidelines document provides detailed conventions for skill creation, covering directory structure, SKILL.md frontmatter rules, naming, validation with `python3 tools/validate-all.py`, and commit format. All contributions must pass validation before merging. [Contribution Guidelines](CONTRIBUTING.md)

## 11. Licensing

MIT — Leonardo Jara

## 12. Ownership & Copyright

Maintained by Leonardo Jara ([@leojara95](https://github.com/leojara95)) under the natuleadan organization ([@natuleadan](https://github.com/natuleadan)).

---

## Contributors

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
