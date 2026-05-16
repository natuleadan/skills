# Contributing to Natuleadan Skills

> Before editing any skill, read all conventions below. Skills are consumed by AI agents — structure and formatting must be exact.

---

## Quick Start

```bash
git clone https://github.com/natuleadan/skills.git
cd skills
bun install              # husky + commitlint
python3 tools/validate-all.py  # verify baseline
```

---

## Skill Structure

Each skill lives in a **4-level numeric hierarchy**:

```
skills/
  <domain>/
    <category>/
      <skill-code>-<skill-name>/
        SKILL.md
        metadata.json
        scripts/       (optional — Python .py files)
        references/    (optional — supporting .md files)
```

### Levels

| Level | Format | Example |
|---|---|---|
| Domain | `NN-name` | `01-programming` |
| Category | `NNNN-name` | `0101-node` |
| Skill | `NNNNNN-name` | `010101-package-security` |

- Codes auto-sort alphabetically in CLI output (npx skills add)
- Domains and categories that don't exist yet should contain only a `.gitkeep`

### Domain directory

| Directory | Status |
|---|---|
| `01-programming/` | Active — 4 skills |
| `02-biology/` | Placeholder (`.gitkeep`) |
| `03-cooking/` | Placeholder (`.gitkeep`) |

---

## SKILL.md Format

### Frontmatter

```yaml
---
name: <skill-code>-<skill-name>
description: "<Explicit description with trigger phrases. If the description contains ': ', it MUST be double-quoted.>"
---
```

**Rules:**
- `name` — lowercase, hyphens only, max 64 chars, must match directory name exactly
- `description` — max 1024 chars. If it contains `: ` (colon-space), wrap in **double quotes** (`"..."`). Single quotes are accepted but double quotes are preferred
- Allowed fields: `name`, `description`, `license`, `compatibility`, `metadata`, `allowed-tools`
- No other frontmatter fields are permitted

### Description Trigger Phrases

Descriptions should list **when** to activate, using explicit trigger phrases:

```yaml
description: "Use this skill whenever the user asks about X, Y, or Z. Also trigger when the user mentions A, B, or C. Do NOT trigger for unrelated topics."
```

This helps agents decide whether to load the skill — be precise about scope.

### Body

- Markdown below the frontmatter
- Max **300 lines** per file — split into references/ if larger
- Progressive disclosure: `SKILL.md` references supporting files via relative links

---

## metadata.json

Every skill **must** have a `metadata.json`:

```json
{
  "version": "1.0.0",
  "abstract": "One-sentence summary of what this skill does.",
  "references": []
}
```

Fields:
- `version` — semver string
- `abstract` — short summary (max 200 chars)
- `references` — array of URLs (can be empty)

---

## Naming Rules

- **Skill name**: max 64 chars, lowercase, hyphens only, no leading/trailing/consecutive hyphens
- **Directory name**: must match `name` field in SKILL.md exactly (NFKC-normalized)
- **Domain name**: numeric prefix (`01-`, `02-`)
- All content in **English** for cross-agent compatibility

---

## Validation

Always run before committing:

```bash
python3 tools/validate-all.py
```

Checks performed:
- Every path in `marketplace.json` resolves to an existing directory
- `SKILL.md` has valid frontmatter with required fields
- `name` matches directory name
- `description` does not contain unquoted `: `
- No unknown frontmatter fields
- `metadata.json` exists in each skill

Husky runs this automatically on `git commit`.

---

## Commit Conventions

Format: `type(scope): description`

| Type | Usage |
|---|---|
| `feat` | New skill or feature |
| `fix` | Bug fix |
| `upgrade` | Breaking change |
| `docs` | Documentation |
| `chore` | Config, tooling, CI |

Rule: scope required, max 100 chars, lowercase.

---

## Adding a New Skill

1. Pick the next numeric code in the hierarchy
2. Create `skills/<domain>/<category>/<NNNNNN-name>/` with `SKILL.md` and `metadata.json`
3. Add optional `scripts/` (`.py` files) or `references/`
4. Register the path in `.claude-plugin/marketplace.json` under the appropriate plugin
5. Run `python3 tools/validate-all.py`
6. Commit — husky runs validation again automatically

---

## Adding a New Domain

1. Add numeric prefix (e.g., `04-robotics/`)
2. Create `skills/04-robotics/.gitkeep`
3. Add a new plugin entry in `.claude-plugin/marketplace.json` with the domain name
4. Repeat the skill creation process for each skill in the domain
