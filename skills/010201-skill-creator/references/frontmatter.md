# Frontmatter

Every `SKILL.md` starts with YAML frontmatter between `---` delimiters.

```yaml
---
name: my-skill-name            # Required: lowercase kebab-case, unique identifier
description: ...               # Required: what it does AND when to trigger
---
```

## Name rules

- Lowercase only
- Hyphens for spaces (`my-skill`, not `my_skill` or `My Skill`)
- Must match the parent directory name
- Unique across the collection

## Description rules

The description is the primary trigger mechanism. It must include:

1. **What the skill does** — the task it helps with
2. **When to trigger** — specific contexts, keywords, and scenarios
3. **When NOT to trigger** — edge cases to avoid false positives

Write descriptions that are slightly **pushy** to avoid undertriggering. Instead of "Helps create dashboards", write:

> "Use this skill whenever the user mentions dashboards, data visualization, internal metrics, or wants to display any kind of company data, even if they don't explicitly ask for a 'dashboard'. Do NOT trigger for general data questions that don't involve visualization."

### Description optimization process

1. Create 20 trigger eval queries — mix of should-trigger and should-not-trigger
2. Focus should-not-trigger on **near-misses** (share keywords but need a different skill)
3. Review with the user for sign-off
4. Run the optimization loop: split into train/test, evaluate, propose improvements, select best by test score
5. Update the SKILL.md frontmatter

## Complete example

A real `SKILL.md` frontmatter block showing all elements:

```yaml
---
name: dependency-auditor
description: Audits project dependencies for known vulnerabilities, outdated packages, and license compliance. Use this skill whenever the user asks to check for vulnerable dependencies, run npm audit or pnpm audit, review package licenses, identify outdated packages with npm outdated or pnpm outdated, or generate a dependency report. Do NOT trigger for general package installation (use 010103-package-ops) or setting up security policies (use 010101-package-security).
---
```
