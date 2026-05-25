# After Pushing to Main: The Complete Cycle

## What Happens When We Push to Main

```
git push origin main
  ↓
GitHub Actions starts
  ↓
@semantic-release/commit-analyzer
  ↓
Analyzes commits since last tag
  ↓
Determines version: MAJOR/MINOR/PATCH
  ↓
Generates: package.json, CHANGELOG.md, git tag
  ↓
Pushes changes to origin/main
  ↓
DONE ✅
```

## What I Need to Do After

### Step 1: Fetch New Tags

```bash
git fetch origin --tags
```

**Why**: semantic-release creates a vX.Y.Z tag that lives on the remote. I need to pull it locally.

### Step 2: Sync Dev with Main

```bash
git checkout dev
git rebase main
```

**Why**: GitHub Actions updated main (package.json + CHANGELOG). Dev needs those changes.

### Alternative: merge (less recommended)

```bash
git checkout dev
git pull origin main  # = git fetch + git merge
```

**Problem**: Creates a merge commit that has no conventional type (fix:, feat:, etc.). Better to use rebase.

## The Complete Cycle

| Step | Command | Branch | What happens |
|------|---------|--------|-------------|
| 1 | `git commit -m "fix(...):"` | dev | I make changes |
| 2 | `git push origin dev` | dev | Push to remote |
| 3 | `git checkout main` | main | Switch to main |
| 4 | `git pull origin main` | main | Pull remote main changes |
| 5 | `git merge dev` | main | Merge dev commits |
| 6 | `git push origin main` | main | ⏳ **GitHub Actions runs here** |
| 7 | `git fetch origin --tags` | main | Fetch new tags |
| 8 | `git checkout dev` | dev | Switch back to dev |
| 9 | `git rebase main` | dev | ✅ Sync dev with main |
| 10 | `git push origin dev` | dev | ✅ (Optional) Update remote backup |

## Verify Everything Worked

```bash
# Did GitHub Actions generate a new tag?
git tag | tail -3

# Changes on remote main?
git log origin/main --oneline -3

# Is dev in sync?
git log --oneline -3  # View my commits
git log origin/main --oneline -1  # View latest on main
# Should be equivalent (same commits, possibly different order)
```

## Common Errors

### ❌ Not syncing dev after GA

```bash
git push origin main
# ❌ FORGETS:
# git fetch origin --tags
# git checkout dev && git rebase main
```

**Problem**: Dev falls behind main, subsequent commits may have conflicts.

### ❌ Using merge instead of rebase

```bash
git checkout dev
git merge main  # ❌ Creates merge commit
```

**Problem**: The merge commit has no conventional type. If we push to main again later, semantic-release can't analyze it correctly.

### ❌ Forgetting to fetch tags

```bash
git push origin main
git checkout dev  # ❌ FORGETS git fetch --tags
git rebase main
```

**Problem**: Tags are not available locally. `git log` won't show vX.Y.Z correctly.

## The Formula: Always After Push to Main

```bash
# Step 1: Fetch everything from remote
git fetch origin --tags

# Step 2: Sync local dev with local main
git checkout dev
git rebase main

# Step 3 (Optional but recommended): Update remote backup
git push origin dev
```

Or in one command:

```bash
git fetch origin --tags && git checkout dev && git rebase main && git push origin dev
```

**Note on Step 3**: After rebase, local dev will be ahead of origin/dev because it incorporated semantic-release changes. It's recommended to push to keep the backup in sync, but NOT mandatory (remote dev is not a release branch).

## Golden Rule

> **After any push to main, ALWAYS sync dev with main via rebase.**

This ensures:
- ✅ Dev has semantic-release changes (package.json, CHANGELOG)
- ✅ Clean history (rebase, no merge commits)
- ✅ New tags available locally
- ✅ Ready for subsequent commits
