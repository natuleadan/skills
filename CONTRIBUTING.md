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
| `scripts/main.ts` | yes | generated stub and explicit entry point |

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
- No spaced hyphen ` - ` in Markdown prose; the only exception is the
  copyright line `2023 - Present.`.
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

- `name`: lowercase, hyphens only, matches the directory.
- `description`: up to 1024 characters, with explicit trigger phrases. Quote it
  with double quotes when it contains a colon followed by a space.

The body holds short instructions and links to the references. Keep it under 300
lines and push detail into `references/`.

Write descriptions that say when to activate the skill, for example "use this
skill when applying AI tools to healthcare". Do not describe unrelated topics.

## metadata.json

Four fields, no extras:

- `version`: semver string for the skill.
- `abstract`: one sentence, at most 200 characters.
- `references`: array of file names inside `references/`, not URLs.

Declared references must exist, and every existing reference must be declared.

## Scripts

Every skill ships `scripts/main.ts`, generated from
`tools/skill-script-template.txt` by `tools/generate-skill-scripts.ts`. Never
edit a script by hand: change the template and run `pnpm scripts:generate`.

The stub contract:

- `pnpm skill <name> --help` lists the skill and its planned commands, derived
  from `metadata.json.references`.
- `pnpm skill <name> --version` prints the skill version.
- `pnpm skill <name> <command>` returns a JSON stub with `status: stub`.
- An unknown command exits 2.

`pnpm scripts:check` verifies that every generated file matches the template and
runs the smoke tests. `pnpm validate` includes it.

When a capability is implemented, add `scripts/<command>.ts` next to `main.ts`
and route the command to it. The entry point stays `main.ts`. Only `.ts` and
`.mjs` are allowed.

## Validation

Run `pnpm validate` before every commit. It checks:

- Frontmatter and directory names match.
- References exist and contain a mermaid sequence diagram.
- No non-mermaid code blocks in any markdown file.
- No spaced hyphen ` - ` in Markdown prose; exception: `2023 - Present.`.
- No `code/`, no executables and no Python.
- `scripts/` starts at `main.ts` and holds only TypeScript or ESM.
- Every skill is registered in `.claude-plugin/marketplace.json` and
  `.claude-plugin/plugin.json`.
- License and version match across manifests.
- `ThirdPartyNotices.txt` matches the installed dependencies.
- Every skill has a generated `scripts/main.ts` and passes the smoke test.
- Industry skills stay neutral and uniform.

The `pre-commit` hook runs the same command; the `pre-push` hook runs it again.

## Third-party notices

`ThirdPartyNotices.txt` is generated, never edited by hand. The generator reads
the direct development dependencies and writes the table with their licenses and
repositories. Run `pnpm notices` after changing dependencies; `pnpm validate`
fails when the file is out of date.

## Commit conventions

Format: `type(scope): description`. The scope is mandatory, in English and lower
case.

Scopes: `skills`, `tools`, `docs`, `ci`, `workflow`, `hooks`, `release`,
`license`, `deps`. CI rejects any other scope.

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
3. Add `references/` with one mermaid diagram per file.
4. Register the path in `.claude-plugin/marketplace.json` and
   `.claude-plugin/plugin.json`.
5. Run `pnpm scripts:generate`.
6. Run `pnpm validate`.
7. Commit and open a pull request.

## Releases

Versions come from changesets. Add a change with `pnpm changeset` and merge the
pull request. The Version Packages workflow then opens or updates a release pull
request and runs `changeset version` plus `sync-plugin-version`. That generates
the version in `package.json`, the plugin manifests and the `CHANGELOG.md` entry.
Never edit those by hand.

Merge the release PR to cut the version. The release job tags `main` with
`v<version>` and publishes `skills_v<version>.zip`. Version `0.0.0` means
unreleased and is skipped.
