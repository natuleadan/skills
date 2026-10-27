<h1 align="center">Natuleadan Skills</h1>
<p align="center"><strong>One platform skill and sixteen industry AI tool skills for AI coding agents</strong></p>

<p align="center">
  <img src="https://img.shields.io/badge/Count-17-8B5CF6?style=for-the-badge" alt="17 skills" />
  <img src="https://img.shields.io/badge/Domains-17-blue?style=for-the-badge" alt="17 domains" />
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-Apache_2.0-blue.svg?style=for-the-badge" alt="Apache 2.0 License" /></a>
  <br />
  <a href="https://skills.sh/natuleadan/skills"><img src="https://skills.sh/b/natuleadan/skills" alt="Skills" /></a>
</p>

## 1. What is Natuleadan Skills?

A collection of agent skills for AI coding agents. Each skill is a
self-contained package of instructions and reference documentation, installable
with the Agent Skills format.

There is one platform skill, `natuleadan-skills`, holding the platform surface
as references instead of one skill per product. The other sixteen skills are
industry AI tool sets for a specific domain. The full list is in the
[Skills Index](SKILLS.md).

## 2. Catalog

17 skills:

- **Platform**: `natuleadan-skills` - APIs, declarative services, operations and data.
- **Industry**: `healthcare-ai-tools`, `biology-ai-tools`, `agriculture-ai-tools`,
  `food-and-beverage-ai-tools`, `energy-ai-tools`, `manufacturing-ai-tools`,
  `logistics-ai-tools`, `environment-ai-tools`, `education-ai-tools`,
  `commerce-ai-tools`, `entertainment-ai-tools`, `technology-ai-tools`,
  `construction-ai-tools`, `security-ai-tools`, `space-ai-tools`,
  `government-ai-tools`.

Every industry skill is provider-agnostic: it describes AI tooling for an area
and works with any compatible backend.

## 3. Install

Install the whole collection with `npx skills add natuleadan/skills`.

Install one skill with `npx skills add natuleadan/skills --skill natuleadan-skills`.

## 4. Requirements

- Node.js 24 or newer, which runs TypeScript entry points directly.
- pnpm 12 for development.
- No Python is required: validation, hooks and CI run on Node.

## 5. Development

Clone the repository, run `pnpm install`, then `pnpm validate`. The `prepare`
script installs the Husky hooks.

Useful commands:

- `pnpm validate` - validate skills and audit industry neutrality.
- `pnpm industry` - audit only the sixteen industry skills.
- `pnpm skill <name>` - run `skills/<name>/scripts/main.ts` with Node.
- `pnpm changeset` - record a change for the next release.
- `pnpm run version` - apply changesets and sync plugin versions.

## 6. Structure

Each skill lives under `skills/<name>/` and contains:

- `SKILL.md` - frontmatter with `name` and `description`, then the instructions.
- `metadata.json` - `version`, `abstract` and the list of references.
- `references/*.md` - prose notes, each with one or more mermaid diagrams.
- `scripts/main.ts` - optional entry point, run explicitly and never automatic.

The `.claude-plugin/marketplace.json` file is the catalog: every skill must be
registered there and in `.claude-plugin/plugin.json`.

## 7. Validation

`pnpm validate` enforces:

- Frontmatter and directory names match.
- Every reference declared in `metadata.json` exists and has a sequence diagram.
- No fenced code blocks in any markdown file, except mermaid.
- Files stay under 300 lines.
- No `code/` directory, no executables and no Python.
- `scripts/` only holds TypeScript or ESM and starts at `main.ts`.
- License and version match across manifests.
- Industry skills stay neutral: no platform concepts, vendor names or pricing.

Husky runs validation on every commit and before every push.

## 8. Commit Conventions

Format: `type(scope): description`, with the scope in English and lower case.

- The title has 3 to 7 words, counting `type(scope):`.
- A blank line follows, then at least 3 bullets shaped `- **Label**: body`.
- Each bullet body has 3 to 7 words.
- Maximum 100 characters per title.
- Types: feat, fix, upgrade, docs, style, refactor, perf, test, chore, ci, revert.

The rules live in `commitlint.config.js`, enforced by the `commit-msg` hook and
by the Conventional Commits job in CI.

## 9. Releases

Versions come from changesets. Add a change with `pnpm changeset`, merge it, and
the release pull request applies `changeset version`, which updates
`package.json`, the changelog and the plugin manifests.

A version of `0.0.0` means unreleased: the tag job skips it. Every other version
on `main` produces a tag `v<version>` and a release with `skills_v<version>.zip`.

## 10. Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md) before editing a skill. It covers the
directory layout, naming, frontmatter, references, scripts, validation and
commit format. All contributions must pass `pnpm validate`.

## 11. License

Apache License 2.0, copyright NATULEADAN SAS BIC 2023 - Present. See
[LICENSE](LICENSE), [NOTICE](NOTICE) and
[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

## 12. Ownership

Maintained by Leonardo Jara ([@leojara95](https://github.com/leojara95)) under
the natuleadan organization ([@natuleadan](https://github.com/natuleadan)).

---

## Star History

<a href="https://www.star-history.com/#natuleadan/skills&Date">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/image?repos=natuleadan/skills&type=date&theme=dark" />
    <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/image?repos=natuleadan/skills&type=date&theme=light" />
    <img alt="Star History Chart" src="https://api.star-history.com/image?repos=natuleadan/skills&type=date" />
  </picture>
</a>
