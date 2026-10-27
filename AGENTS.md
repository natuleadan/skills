# Natuleadan Skills - Agent Guide

Installable agent skills for AI coding agents.

## Links

- [README.md](README.md) - installation and development
- [SKILLS.md](SKILLS.md) - complete catalog
- [CONTRIBUTING.md](CONTRIBUTING.md) - format, validation and commits

## Skills

17 skills: one platform skill and sixteen industry skills.

- `natuleadan-skills` - groups the platform open-source programs as references.
  The references are stubs until each program is defined.
- `agriculture-ai-tools`, `biology-ai-tools`, `commerce-ai-tools`,
  `construction-ai-tools`, `education-ai-tools`, `energy-ai-tools`,
  `entertainment-ai-tools`, `environment-ai-tools`,
  `food-and-beverage-ai-tools`, `government-ai-tools`, `healthcare-ai-tools`,
  `logistics-ai-tools`, `manufacturing-ai-tools`, `security-ai-tools`,
  `space-ai-tools`, `technology-ai-tools`.

Industry skills are provider-agnostic: no platform concepts, vendor names or
pricing.

## Format

Every skill lives in `skills/<name>/` with:

- `SKILL.md` - frontmatter (`name`, `description`) and instructions.
- `metadata.json` - `version`, `abstract`, `references`.
- `references/*.md` - notes, each with a mermaid `sequenceDiagram`.
- `scripts/main.ts` - optional explicit entry point.

Rules:

- No code blocks in markdown except mermaid.
- No `code/` directory, no executables, no Python.
- `SKILL.md` has no mermaid; references have at least one.
- Files stay under 300 lines.

## Commands

- `pnpm validate` - validate skills and audit industry neutrality.
- `pnpm industry` - audit only the industry skills.
- `pnpm notices` - regenerate `ThirdPartyNotices.txt`.
- `pnpm skill <name>` - run a skill script with Node.
- `pnpm changeset` - record a change for the next release.

Husky runs validation on commit and on push. The repository is Apache-2.0.
