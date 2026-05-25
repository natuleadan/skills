# Configuration Examples

## commitlint.config.js

```js
const config = {
  extends: ["@commitlint/config-conventional"],
  rules: {
    "scope-empty": [2, "never"],
    "scope-case": [2, "always", "lower-case"],
    "type-enum": [
      2,
      "always",
      [
        "feat",     // ✨ MINOR
        "fix",      // 🐛 PATCH
        "upgrade",  // 🔥 MAJOR
        "docs",     // 📖 NONE
        "style",    // 💅 NONE
        "refactor", // ♻️  NONE
        "perf",     // ⚡ PATCH
        "test",     // ✅ NONE
        "chore",    // 🔧 NONE
        "ci",       // 🤖 NONE
        "revert",   // ↩️  PATCH
      ],
    ],
    "type-case": [2, "always", "lowercase"],
    "type-empty": [2, "never"],
    "subject-empty": [2, "never"],
    "subject-full-stop": [2, "never", "."],
    "subject-case": [2, "always", "lower-case"],
    "header-max-length": [2, "always", 100],
  },
};

export default config;
```

## .releaserc.json

```json
{
  "branches": [{ "name": "main", "prerelease": false }],
  "plugins": [
    [
      "@semantic-release/commit-analyzer",
      {
        "preset": "conventionalcommits",
        "releaseRules": [
          { "type": "upgrade", "release": "major" },
          { "type": "feat",    "release": "minor" },
          { "type": "fix",     "release": "patch" },
          { "type": "perf",    "release": "patch" },
          { "type": "revert",  "release": "patch" },
          { "type": "docs",    "release": false },
          { "type": "style",   "release": false },
          { "type": "refactor","release": false },
          { "type": "test",    "release": false },
          { "type": "chore",   "release": false },
          { "type": "ci",      "release": false }
        ]
      }
    ],
    [
      "@semantic-release/release-notes-generator",
      {
        "preset": "conventionalcommits",
        "presetConfig": {
          "types": [
            { "type": "upgrade",  "section": "🔥 Upgrade",       "hidden": false },
            { "type": "feat",     "section": "✨ Features",       "hidden": false },
            { "type": "fix",      "section": "🐛 Bug Fixes",      "hidden": false },
            { "type": "perf",     "section": "⚡ Performance",    "hidden": false },
            { "type": "docs",     "section": "📖 Documentation",  "hidden": false },
            { "type": "style",    "section": "💅 Style",          "hidden": true  },
            { "type": "refactor", "section": "♻️ Refactoring",    "hidden": false },
            { "type": "test",     "section": "✅ Tests",          "hidden": false },
            { "type": "chore",    "section": "🔧 Chore",          "hidden": false },
            { "type": "ci",       "section": "🤖 CI/CD",          "hidden": false },
            { "type": "revert",   "section": "↩️ Reverts",        "hidden": false }
          ]
        }
      }
    ],
    ["@semantic-release/changelog", {
      "changelogFile": "CHANGELOG.md"
    }],
    "@semantic-release/github",
    ["@semantic-release/npm", { "npmPublish": false }],
    ["@semantic-release/git", {
      "assets": ["package.json", "pnpm-lock.yaml", "CHANGELOG.md"],
      "message": "chore(release): bump version to ${nextRelease.version}"
    }]
  ]
}
```

## GitHub Actions — CI workflow (semantic-release job)

```yaml
semantic-release:
  needs: [lint, test]
  runs-on: ubuntu-latest
  permissions:
    contents: write
    issues: write
    pull-requests: write
  steps:
    - uses: actions/checkout@v4
      with:
        fetch-depth: 0
        persist-credentials: false
    - uses: actions/setup-node@v4
      with:
        node-version: 22
    - run: npm ci
    - run: npx semantic-release
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```
