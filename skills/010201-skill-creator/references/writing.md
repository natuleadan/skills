# Writing Patterns

## Imperative tone

Use direct commands: "Read the file", "Parse the output", "Save to path".

## Explain the why

AI models have strong reasoning capabilities. When you explain WHY something matters, they generalize better and handle edge cases correctly on their own. Avoid heavy-handed "ALWAYS" or "NEVER" — reframe and explain the reasoning instead.

For example, instead of:

> ALWAYS use exact version pinning.

Write:

> Prefer exact version pinning because supply chain attacks exploit version ranges. When a malicious version gets published under a minor bump (e.g., 1.12.0 → 1.12.1), a caret range will silently pull it in. Exact versions give you control over when to update.

## Include examples

Show concrete input → output pairs:

```markdown
**Example 1:**
Input: User asks "How do I block postinstall scripts for npm?"
Output: Set `ignore-scripts=true` in `~/.npmrc`:
  ```
  npm config set ignore-scripts true
  ```
```

## Keeping it lean

Remove instructions that aren't pulling their weight. If the skill makes the agent waste steps doing unproductive work, trim those parts. Every instruction should serve a clear purpose.

## Adding reusable scripts

When creating a skill, look for repeated work across usage patterns. If users independently need similar helper code, bundle that script in `scripts/` and reference it in SKILL.md. This saves every future invocation from reinventing the wheel.

```markdown
## Validation
Run `python scripts/validate.py` to check your setup.
```
