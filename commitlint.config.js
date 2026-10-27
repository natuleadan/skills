// Custom rules that encode the repository commit policy:
// - title between 3 and 7 words, counting `type(scope):`
// - a blank line, then at least 3 bullets
// - each bullet `- **Title**: body`, body between 3 and 7 words
const commitPolicy = {
  rules: {
    "header-word-count": ({ header }, _when, value = [3, 7]) => {
      const [min, max] = Array.isArray(value) ? value : [3, 7];
      const words = header.trim().split(/\s+/).filter(Boolean).length;
      return [
        words >= min && words <= max,
        `header has ${words} words (min ${min}, max ${max})`,
      ];
    },
    "body-bullets": ({ body }, _when, value = 3) => {
      const min = Array.isArray(value) ? value[0] : value;
      const bullets = (body || "")
        .split("\n")
        .filter((line) => line.startsWith("- ")).length;
      return [bullets >= min, `body has ${bullets} bullets (min ${min})`];
    },
    "body-bullet-format": ({ body }) => {
      const bullets = (body || "")
        .split("\n")
        .filter((line) => line.startsWith("- "));
      for (const line of bullets) {
        const match = line.slice(2).match(/^\*\*[^*]+\*\*:\s*(\S.*)$/);
        if (!match) {
          return [false, `bullet missing '**Title**:' prefix -> ${line.slice(0, 60)}`];
        }
        const words = match[1].trim().split(/\s+/).filter(Boolean).length;
        if (words < 3 || words > 7) {
          return [
            false,
            `bullet has ${words} words (min 3, max 7) -> ${match[1].slice(0, 60)}`,
          ];
        }
      }
      return [true, "bullets have the required format"];
    },
  },
};

const config = {
  extends: ["@commitlint/config-conventional"],
  plugins: [commitPolicy],
  rules: {
    "scope-empty": [2, "never"],
    "scope-case": [2, "always", "lower-case"],
    "type-enum": [
      2,
      "always",
      [
        "feat", // MINOR bump - New features
        "fix", // PATCH bump - Bug fixes
        "upgrade", // MAJOR bump - Breaking changes
        "docs", // NO BUMP - Documentation
        "style", // NO BUMP - Style (no logical change)
        "refactor", // NO BUMP - Refactoring
        "perf", // PATCH bump - Performance improvements
        "test", // NO BUMP - Tests
        "chore", // NO BUMP - Chores (deps, config)
        "ci", // NO BUMP - CI/CD
        "revert", // PATCH bump - Reverting commit
      ],
    ],
    "type-case": [2, "always", "lowercase"],
    "type-empty": [2, "never"],
    "subject-empty": [2, "never"],
    "subject-full-stop": [2, "never", "."],
    "subject-case": [2, "always", "lower-case"],
    "header-max-length": [2, "always", 100],
    "header-word-count": [2, "always", [3, 7]],
    "body-bullets": [2, "always", [3]],
    "body-bullet-format": [2, "always"],
  },
};

export default config;
