# Safe Commit Protocol

## The Problem

1. Ran `git reset --hard` without `git stash` first → lost all changes
2. Staged changes from multiple contexts (refactor + tests) in a single commit
3. Did not verify old-path imports BEFORE moving files
4. Deleted files remained as pending changes instead of being staged

### What Went Wrong

```bash
# ❌ BAD: Mixing contexts
git add .
git commit -m "refactor(payment): ..."

# AFTER:
# stripe webhook imported @/lib/modules/payment/gateway (old path)
# Build failed ❌

# AFTER:
git reset --hard <hash>  # WITHOUT git stash first
# Lost ALL changes
```

### The Correct Approach

**Step 1: Separate contexts BEFORE staging**
```bash
git status --short | grep -v "test/"
git reset
git add .

# Commit 1: Refactor
git commit -m "refactor(payment): move processors..."

# Commit 2: Tests
git add src/test/
git commit -m "test(payment): update paths..."
```

**Step 2: Verify old-path imports BEFORE staging**
```bash
# BEFORE any git add:
grep -r "@/lib/modules/payment/gateway" src/

# Found: src/app/api/webhooks/stripe/route.ts
# ✅ Fixed IN THE SAME COMMIT where files are moved
```

**Step 3: Ensure deleted files are included**
```bash
git status --short | grep "^ D"  # Check what is pending

# If you see:
#  D src/lib/modules/payment/gateway.ts
# Run:
git add -u  # Stages ALL deletions
git commit -m "..."
```

---

## Disaster Recovery: 3 Steps

### If you already lost commits (git reflog)

```bash
# 1. View history
git reflog | head -20
# Output:
#   abc1234 commit: test(payment): update tests
#   def5678 commit: refactor(payment): move processors
#   ghi9012 reset: moving to ghi9012  ← This is where everything was lost

# 2. Recover
git reset --hard def5678  # The last commit BEFORE the reset

# 3. Verify
git log --oneline -3
# All commits are back ✅
```

### If you ran `reset --hard` without stash

**The changes are lost forever.** But:

```bash
# Try this (sometimes works):
git fsck --lost-found
ls .git/lost-found/other/

# If nothing, learn for next time:
# ALWAYS run: git stash BEFORE reset --hard
```

### If you staged changes from multiple features

```bash
git reset                          # Unstage everything
git status --short | head -20      # See what is there
git diff src/lib/external/         # See changes for one feature
# Re-stage by feature/commit
```

---

## Checklist Going Forward

### BEFORE staging
- [ ] Do the changes belong to a single context?
- [ ] Did I `grep` for all old imports?
- [ ] Are old imports fixed in the same commit?

### BEFORE committing
- [ ] Does `git status --short | grep "^ D"` show pending deletions?
- [ ] Did I run `git add -u` to include deletions?
- [ ] Is the message semantic (`fix:`, `refactor:`, `test:`)?
- [ ] Did I notify the team?

### BEFORE reset/rebase/force-push
- [ ] `git stash` (save local changes)
- [ ] `git reflog` (document what is being done)
- [ ] Notify the team first

---

## 3 Commits = 3 Steps (Winning Formula)

For large refactors:

```bash
# 1. STRUCTURE: Name/config changes
git add documentation/ src/lib/env.ts
git commit -m "refactor(processor): standardize naming to payment-gateway"

# 2. REFACTOR: File movement (with deletions)
git add src/lib/external/ src/lib/internal/ src/app/api/webhooks/
git add -u  # ← IMPORTANT: deletions
git commit -m "refactor(payment): move processors"

# 3. TESTS: Update paths in tests
git add src/test/
git commit -m "test(payment): update paths"

# Verify
npm run build  # ✓
git status     # empty
git log --oneline -3  # see the 3 commits
```

---

## Summary: Never Lose Your Work Again

1. **`git add .` is dangerous** → stage by context
2. **grep BEFORE moving files** → find old imports
3. **`git add -u` for deletions** → do not leave pending changes
4. **`git stash` BEFORE reset** → always save local changes
5. **3 small commits > 1 giant commit** → easier to review and revert

**Golden Rule**: Small, frequent commits = easy recovery.
