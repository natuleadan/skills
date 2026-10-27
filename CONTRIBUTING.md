# Contributing to Natuleadan Skills

> Read these conventions before editing a skill. Skills are consumed by AI
> agents, so structure and formatting must be exact.

## Quick start

1. Clone `https://github.com/natuleadan/skills.git`.
2. Run `pnpm install` to install tooling and Husky hooks.
3. Run `pnpm validate` to confirm the baseline is clean.

## Skill structure

Every skill lives in a flat directory under `skills/`:

| Path | Required | Purpose |
|---|---|---|
| `SKILL.md` | yes | frontmatter plus instructions |
| `metadata.json` | yes | version, abstract and reference list |
| `references/*.md` | optional | supporting notes with mermaid diagrams |
| `scripts/main.ts` | optional | explicit entry point, never automatic |

There is one platform skill, `natuleadan-skills`, and sixteen industry skills
ending in `-ai-tools`.

### Naming

- Lowercase letters, digits and hyphens only.
- Maximum 64 characters, no leading, trailing or consecutive hyphens.
- The `name` field in `SKILL.md` must match the directory name exactly.
- A new platform program becomes a reference of `natuleadan-skills`, not a new
  top-level skill.

### Content rules

- All content is in English.
- No fenced code blocks in any markdown file; the only exception is `mermaid`.
- No `code/` directory and no executable files.
- No Python anywhere in `skills/` or `tools/`.
- Every file under `references/` contains at least one mermaid
  `sequenceDiagram`.
- `SKILL.md` never contains mermaid.
- Every markdown file stays under 300 lines.
- Industry skills stay provider-agnostic: no platform concepts, vendor names or
  pricing.

## SKILL.md

Frontmatter carries two required fields:

- `name` - lowercase, hyphens only, matches the directory.
- `description` - up to 1024 characters, with explicit trigger phrases. Quote it
  with double quotes when it contains a colon followed by a space.

The body holds short instructions and links to the references. Keep it under 300
lines and push detail into `references/`.

Write descriptions that say when to activate the skill, for example "use this
skill when applying AI tools to healthcare". Do not describe unrelated topics.

## metadata.json

Four fields, no extras:

- `version` - semver string for the skill.
- `abstract` - one sentence, at most 200 characters.
- `references` - array of file names inside `references/`, not URLs.

Declared references must exist, and every existing reference must be declared.

## Scripts

A skill may ship `scripts/main.ts`. Rules:

- The entry point is always `main.ts`.
- Only `.ts` or `.mjs` files are allowed inside `scripts/`.
- Scripts are executed explicitly with `pnpm skill <name>`, never by an agent
  on its own.
- The working directory is the skill directory.
- Keep scripts deterministic and side-effect free unless their purpose is to
  change something.

Helpers can live next to `main.ts`; import them with a relative path.

## Validation

Run `pnpm validate` before every commit. It checks:

- Frontmatter and directory names match.
- References exist and contain a mermaid sequence diagram.
- No non-mermaid code blocks in any markdown file.
- No `code/`, no executables and no Python.
- `scripts/` starts at `main.ts` and holds only TypeScript or ESM.
- Every skill is registered in `.claude-plugin/marketplace.json` and
  `.claude-plugin/plugin.json`.
- License and version match across manifests.
- Industry skills stay neutral and uniform.

The `pre-commit` hook runs the same command; the `pre-push` hook runs it again.

## Commit conventions

Format: `type(scope): description`. The scope is mandatory, in English and lower
case.

| Type | Use |
|---|---|
| `feat` | new skill or feature |
| `fix` | bug fix |
| `upgrade` | breaking change |
| `docs` | documentation |
| `style` | formatting only |
| `refactor` | internal restructuring |
| `perf` | performance |
| `test` | tests |
| `chore` | configuration and tooling |
| `ci` | CI or hooks |
| `revert` | revert a previous commit |

Title and body rules:

- Title has 3 to 7 words, counting `type(scope):`.
- Maximum 100 characters, no trailing period.
- Blank line after the title.
- At least 3 bullets shaped `- **Label**: body`.
- Each bullet body has 3 to 7 words.

Example:

> docs(skills): explain releases and versions
>
> - **Versions**: come from changesets
> - **Releases**: tag and zip
> - **Baseline**: zero point zero is unreleased

Rules live in `commitlint.config.js` and run in the `commit-msg` hook and in the
Conventional Commits CI job.

## Adding a skill

1. Choose a lowercase hyphenated name.
2. Create `skills/<name>/` with `SKILL.md` and `metadata.json`.
3. Add `references/` with one mermaid diagram per file, or `scripts/main.ts`.
4. Register the path in `.claude-plugin/marketplace.json` and
   `.claude-plugin/plugin.json`.
5. Run `pnpm validate`.
6. Commit and open a pull request.

## Releases

Versions come from changesets. Add a change with `pnpm changeset`, merge the
pull request, and the release pull request applies `changeset version`. Never
edit the version by hand.

The release job tags `main` with `v<version>` and publishes
`skills_v<version>.zip`. Version `0.0.0` means unreleased and is skipped.
