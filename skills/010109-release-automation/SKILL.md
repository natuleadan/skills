---
name: 010109-release-automation
description: Semantic version mapping, semantic-release automation, post-release workflow, and release configuration for conventional commits.
license: MIT
---

# Release Automation

## Overview

Automated versioning and releases using semantic-release. Covers version bump rules, semantic-release setup, post-push synchronization, and configuration files.

## Quick Reference

### Version Bump Mapping

| Commit Type | Bump | Example |
|-------------|------|---------|
| `upgrade` | MAJOR | Breaking API change |
| `feat` | MINOR | New feature |
| `fix` | PATCH | Bug fix |
| `perf` | PATCH | Performance improvement |
| `docs` | NONE | Documentation |
| `refactor` | NONE | Code restructure |

### Release Flow

```
Push to main → GitHub Actions
  → semantic-release analyzes commits
  → Determines version (MAJOR/MINOR/PATCH)
  → Updates package.json + CHANGELOG.md
  → Creates git tag + GitHub Release
```

### Post-Release Sync

```bash
git fetch origin --tags
git checkout dev
git rebase main
```

## References

- [Versioning](references/versioning.md) — Commit-to-version mapping
- [Semantic Release](references/semantic-release.md) — Automation setup
- [Post-Release Workflow](references/post-release.md) — Post-push sync guide
- [Configuration](references/config.md) — commitlint + .releaserc.json + CI
