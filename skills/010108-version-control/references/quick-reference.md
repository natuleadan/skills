# Semantic Commits Reference

## Format

```
type(scope): description
```

## Types & Version Impact

| Type | Bump | Purpose |
|------|------|---------|
| `upgrade` | MAJOR | Breaking changes |
| `feat` | MINOR | New features |
| `fix` | PATCH | Bug fixes |
| `perf` | PATCH | Performance improvements |
| `revert` | PATCH | Reverts a commit |
| `docs` | NONE | Documentation |
| `style` | NONE | Formatting |
| `refactor` | NONE | Refactoring |
| `test` | NONE | Tests |
| `chore` | NONE | Dependencies, config |
| `ci` | NONE | CI/CD pipelines |

## Rules Summary

- Lowercase type and scope
- Imperative mood ("add" not "added")
- No period at end of subject
- Max 100 characters total
- Scope is mandatory

## Release Flow

1. Commit with conventional format → `main`
2. GitHub Actions runs `semantic-release`
3. Auto-bumps version in `package.json`
4. Generates `CHANGELOG.md`
5. Creates GitHub Release with tag

See lessons for detailed rules and examples for code.
