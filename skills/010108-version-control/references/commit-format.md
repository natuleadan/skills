# Commit Format Lesson

Rules for writing conventional commit messages.

## Format Structure

```
type(scope): description

[optional body]
```

## Type Rules

- [ ] Type must be lowercase
- [ ] Type must be one of the approved list: `feat`, `fix`, `upgrade`, `docs`, `style`, `refactor`, `perf`, `test`, `chore`, `ci`, `revert`
- [ ] No custom types (e.g., `feature`, `bugfix`, `hotfix` are invalid)
- [ ] Type must match the actual change — do not use `chore` for new features

## Scope Rules

- [ ] Scope is **mandatory** — never omit it
- [ ] Scope must be lowercase
- [ ] Scope must be hyphenated for multi-word (`auth-service`, not `authService`)
- [ ] Scope must reflect the affected area: `auth`, `api`, `database`, `ui`, `cache`, `storage`, etc.
- [ ] Use consistent scope names across the team

## Description Rules

- [ ] Description must be in imperative mood: "add" not "added", "fix" not "fixed"
- [ ] Description must start with lowercase
- [ ] No period at the end of the subject line
- [ ] Max 100 characters for the entire subject line (`type(scope): description`)
- [ ] Description must be meaningful — avoid vague messages like "fix bug" or "update code"

## Body Rules (optional)

- [ ] Leave a blank line between subject and body
- [ ] Body explains the **why**, not the **what**
- [ ] Reference issues in the body: `Fixes #123`
- [ ] Use plain text — no markdown in commit body

## What NOT to Do

- [ ] Never use passive voice: ❌ `fixed`, `updated`, `added` → ✅ `fix`, `update`, `add`
- [ ] Never use uppercase type: ❌ `Feat(auth)` → ✅ `feat(auth)`
- [ ] Never use uppercase scope: ❌ `feat(Auth)` → ✅ `feat(auth)`
- [ ] Never use generic types: ❌ `merge`, `wip`, `temp`
- [ ] Never omit scope: ❌ `feat: add login` → ✅ `feat(auth): add login`
- [ ] Never use `BREAKING CHANGE:` footer (not configured in this project — use `upgrade` type instead)

## Validation

Commits are validated by `commitlint` on every PR. A failing commit blocks merge.

Run locally before pushing:
```bash
commitlint --from HEAD~1 --to HEAD
```

See [examples/commits.md](../examples/commits.md) for valid commit examples.
