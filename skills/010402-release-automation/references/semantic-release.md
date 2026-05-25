# Semantic Release Lesson

How semantic-release automates versioning, changelog, and GitHub releases.

## What semantic-release Does Automatically

- [ ] Analyzes commits since last release
- [ ] Determines version bump (major/minor/patch/none) based on commit types
- [ ] Updates `package.json` version
- [ ] Generates/updates `CHANGELOG.md`
- [ ] Creates a Git tag (`v1.2.3`)
- [ ] Creates a GitHub Release with release notes
- [ ] Commits the changes back to the repo

## Required Files

- [ ] `.releaserc.json` — semantic-release configuration
- [ ] `commitlint.config.js` — commit message validation
- [ ] `.github/workflows/ci.yml` — GitHub Actions workflow

## Release Trigger Rules

- [ ] Releases only happen on push to `main` branch
- [ ] PRs and feature branches do **not** trigger releases
- [ ] `GITHUB_TOKEN` must be available in CI for creating GitHub releases
- [ ] `NPM_TOKEN` is not required if `npmPublish: false` is set

## Commit Analyzer Configuration Rules

- [ ] Custom types must be added to both `releaseRules` and `presetConfig.types`
- [ ] `upgrade` type maps to `major` release (not the default `BREAKING CHANGE` footer)
- [ ] Types not listed in `releaseRules` default to no release
- [ ] The `preset: 'conventionalcommits'` must be specified

## Changelog Rules

- [ ] Changelog is auto-generated from commit messages — write meaningful descriptions
- [ ] Sections map to commit types: `feat` → ✨ Features, `fix` → 🐛 Bug Fixes, etc.
- [ ] `style` type is hidden from changelog (`hidden: true`)
- [ ] `docs`, `test`, `chore`, `ci` appear in changelog with respective emoji sections

## Git Assets After Release

The release commits back to the repo with:
- `package.json` (updated version)
- `pnpm-lock.yaml` (updated lockfile)
- `CHANGELOG.md` (updated changelog)

Commit message format: `chore(release): bump version to X.Y.Z`

## CI/CD Pipeline Rules

- [ ] Semantic-release job must run **after** lint and test jobs pass
- [ ] `persist-credentials: false` must be set on `actions/checkout`
- [ ] `fetch-depth: 0` required to access full git history for tag detection
- [ ] Node.js version must match project requirements (22+)

## What Can Go Wrong

- [ ] Missing `fetch-depth: 0` → semantic-release can't find previous tags → always creates v1.0.0
- [ ] Missing `GITHUB_TOKEN` → can't create GitHub Release
- [ ] Wrong branch trigger → release runs on PRs unexpectedly
- [ ] Commits not following conventional format → no release triggers
- [ ] `@ts-ignore` or ESLint errors blocking CI → release never runs
