# Testing with Evals

## Creating test cases

Save test prompts to `evals/evals.json`:

```json
{
  "skill_name": "my-skill",
  "evals": [
    {
      "id": 1,
      "prompt": "Realistic user task",
      "expected_output": "Description of expected result",
      "files": [],
      "expectations": [
        "Verifiable statement about the output"
      ]
    }
  ]
}
```

For a more realistic example with multiple test cases and categories:

```json
{
  "skill_name": "010101-package-security",
  "evals": [
    {
      "id": 1,
      "category": "global-config",
      "prompt": "Check my npm security settings globally",
      "expected_output": "Script runs npm audit.py and reports missing settings",
      "files": [],
      "expectations": [
        "Audit script is invoked",
        "Missing settings are clearly listed with remediation commands",
        "Recommendation includes min-release-age, ignore-scripts, save-exact, audit-level"
      ]
    },
    {
      "id": 2,
      "category": "project-config",
      "prompt": "I'm worried about supply chain attacks, help me harden my pnpm project",
      "expected_output": "Provides pnpm-specific security configuration",
      "files": [],
      "expectations": [
        "References pnpm.md for configuration details",
        "Recommends minimumReleaseAge, ignoreScripts, blockExoticSubdeps",
        "Recommends trustedDependencies for packages that need build scripts"
      ]
    },
    {
      "id": 3,
      "category": "no-trigger",
      "prompt": "How do I install Express?",
      "expected_output": "Skill does not trigger (use 010103-package-ops instead)",
      "files": [],
      "expectations": [
        "No security configuration is suggested",
        "Installation instructions are deferred to another skill"
      ]
    }
  ]
}
```

## Writing good assertions

Assertions are objectively verifiable statements checked against the output. Good assertions are:

- **Descriptive** — read clearly in a benchmark viewer
- **Discriminating** — pass when the skill genuinely succeeds and fail when it doesn't
- **Substantive** — test real content correctness, not just filename existence

## Running tests

For each test case, spawn two runs in parallel:

1. **With-skill** — the agent has access to the skill
2. **Baseline** — without the skill (or with the previous version)

Save timing data when runs complete (`timing.json` with `total_tokens` and `duration_ms`).

## Grading

Evaluate each assertion against the outputs.

- **Pass**: Clear evidence in the output
- **Fail**: No evidence, or evidence contradicts

Save as `grading.json` with fields: `text`, `passed`, `evidence`.

## Benchmarking

Aggregate run results into a summary with:
- Pass rate (mean ± stddev)
- Execution time
- Token usage
- Delta between configurations

## Iteration loop

1. Draft the skill
2. Create test prompts
3. Run with-skill and baseline tests
4. Review results (qualitative + quantitative)
5. Identify patterns: non-discriminating assertions, flaky evals, time/token tradeoffs
6. Improve the skill based on feedback
7. Rerun → review → repeat
8. Stop when feedback is all empty or progress plateaus
