# Versioning Lesson

How commit types map to semantic version bumps (major.minor.patch).

## Semantic Versioning Rules

```
MAJOR.MINOR.PATCH
  │     │     └── Bug fixes, reverts, performance (non-breaking)
  │     └──────── New features (backward-compatible)
  └────────────── Breaking changes (incompatible with previous)
```

## Commit Type → Version Bump

| Type | Bump | When to use |
|------|------|-------------|
| `upgrade` | **MAJOR** | API changes that break existing integrations, env var requirements, DB schema changes requiring migration |
| `feat` | **MINOR** | New functionality that doesn't break existing behavior |
| `fix` | **PATCH** | Corrects a bug without changing the API |
| `perf` | **PATCH** | Performance improvements without API changes |
| `revert` | **PATCH** | Reverting a previous commit |
| `docs` | **NONE** | Documentation only |
| `style` | **NONE** | Formatting, whitespace, semicolons |
| `refactor` | **NONE** | Code restructure without behavior change |
| `test` | **NONE** | Adding or modifying tests |
| `chore` | **NONE** | Dependencies, build config, tooling |
| `ci` | **NONE** | CI/CD workflows |

## Choosing the Right Type

### Is it a MAJOR (`upgrade`)?
- [ ] Does it require changes in consuming code or environment?
- [ ] Does it remove or rename a public API, endpoint, or function?
- [ ] Does it require a new required environment variable?
- [ ] Does it require a database migration that can break existing deployments?

### Is it a MINOR (`feat`)?
- [ ] Does it add new functionality?
- [ ] Can existing code continue working without changes?
- [ ] Is this new and additive, not a fix?

### Is it a PATCH (`fix`, `perf`, `revert`)?
- [ ] Does it correct incorrect behavior?
- [ ] Does it improve performance without changing behavior?
- [ ] Does it revert a previous commit?

### Is it NONE?
- [ ] Does it only affect developers (tests, docs, CI)?
- [ ] Would users not notice this change in production?

## Breaking Change Checklist (`upgrade` type)

When making a breaking change:

- [ ] Use `upgrade` type (not `feat` or `fix`)
- [ ] Describe the breaking change clearly in the subject
- [ ] Include migration instructions in the commit body
- [ ] Warn about deployment requirements (e.g., new env vars, migrations)

## Multi-Commit PR Behavior

When a PR includes multiple commits, semantic-release uses the **highest impact** commit:

- One `feat` + ten `fix` commits → **MINOR** bump
- One `upgrade` + any others → **MAJOR** bump
- Only `chore`/`docs`/`test` commits → **NO release**

## No Release Scenarios

A push to `main` with only these types will **not** trigger a release:
`docs`, `style`, `refactor`, `test`, `chore`, `ci`

This is intentional — internal-only changes don't need a public release.
