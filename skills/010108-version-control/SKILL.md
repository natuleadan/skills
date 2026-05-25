---
name: 010108-version-control
description: Conventional commit format, git staging safety, disaster recovery with git reflog, and commit message best practices.
license: MIT
---

# Git Commits

## Overview

Conventional commit messages and safe git workflows. Covers commit format rules, staging discipline, disaster recovery, and commit examples.

## Quick Reference

### Format

```
type(scope): description

Body (optional, blank line required)
```

### Types

| Type | Version Bump | Usage |
|------|-------------|-------|
| `upgrade` | MAJOR | Breaking changes |
| `feat` | MINOR | New features |
| `fix` | PATCH | Bug fixes |
| `perf` | PATCH | Performance improvements |
| `revert` | PATCH | Reverting changes |
| `docs` | NONE | Documentation |
| `style` | NONE | Formatting, white-space |
| `refactor` | NONE | Code restructuring |
| `test` | NONE | Adding/fixing tests |
| `chore` | NONE | Tooling, config |
| `ci` | NONE | CI/CD changes |

### Safe Staging Rules

1. Stage by context — never `git add .` blindly
2. Check old imports with `grep` before moving files
3. Use `git add -u` to include deleted files
4. `git stash` before any `git reset --hard`
5. Small frequent commits over one giant commit

## References

- [Commit Format](references/commit-format.md) — Format rules, types, scope
- [Safe Git Workflow](references/commit-rules.md) — Staging safety, disaster recovery, reflog
- [Commit Examples](references/commit-examples.md) — Real commit examples by type
- [Quick Reference](references/quick-reference.md) — Cheat sheet
