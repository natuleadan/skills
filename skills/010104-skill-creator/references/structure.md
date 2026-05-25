# Skill Structure

## Required structure

```text
my-skill/
├── SKILL.md                     ← Required: instructions + frontmatter
├── references/                  ← Optional: supplementary docs loaded as needed
├── scripts/                     ← Optional: executable code for deterministic tasks
├── assets/                      ← Optional: files used in output
├── evals/                       ← Optional: test definitions
└── README.md                    ← Optional: documentation for the skill
```

Only `SKILL.md` is required. Everything else is optional.

## Progressive disclosure (three-level loading)

1. **Metadata** (name + description in frontmatter) — always in context (~100 words)
2. **SKILL.md body** — loaded whenever skill triggers (<100 lines recommended, max 230)
3. **Bundled resources** (references/, scripts/, assets/) — loaded on demand

### Rules for SKILL.md size

- **< 100 lines**: OK
- **100–200 lines**: Warning — consider using references/
- **200–230 lines**: Serious warning — must split
- **> 230 lines**: Error — references/ required

### How to organize

SKILL.md acts as a **router**: detect intent, load the right reference file, answer. For example:

```
If the user asks about installing tools → read references/setup-guide.md
If the user asks about validation → run scripts/validate.py
If the user asks about troubleshooting → read references/setup-guide.md (Troubleshooting section)
```

- Put detailed per-topic guides in `references/`
- Put reusable code in `scripts/`
- Reference files from SKILL.md with clear guidance on when to read them

## Domain organization pattern

When a skill supports multiple domains:

```text
my-skill/
├── SKILL.md           ← Router: detects which variant is needed
└── references/
    ├── domain-a.md
    ├── domain-b.md
    └── domain-c.md
```
