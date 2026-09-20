const config = {
  extends: ["@commitlint/config-conventional"],
  rules: {
    "scope-empty": [2, "never"],
    "scope-case": [2, "always", "lower-case"],
    "type-enum": [
      2,
      "always",
      [
        "feat", // ✨ MINOR bump (0.1.0 → 0.2.0) - New features
        "fix", // 🐛 PATCH bump (0.1.0 → 0.1.1) - Bug fixes
        "upgrade", // 🔥 MAJOR bump (1.0.0 → 2.0.0) - Major changes (breaking changes)
        "docs", // 📖 NO BUMP - Documentation
        "style", // 💅 NO BUMP - Style (no logical change)
        "refactor", // ♻️  NO BUMP - Refactoring
        "perf", // ⚡ PATCH bump - Performance improvements
        "test", // ✅ NO BUMP - Tests
        "chore", // 🔧 NO BUMP - Chores (deps, config)
        "ci", // 🤖 NO BUMP - CI/CD
        "revert", // ↩️  PATCH bump - Reverting commit
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
