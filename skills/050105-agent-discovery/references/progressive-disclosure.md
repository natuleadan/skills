# Progressive Disclosure Pattern

Progressive disclosure manages context efficiency by loading information in layers — only what is needed, when it is needed. This is the core loading strategy for Agent Skills Discovery and applies broadly to any agent-facing content distribution.

## The Three Levels

| Level | What | When Loaded | Token Cost |
|---|---|---|---|
| 1 | Index metadata (name + description) | At startup or probing | ~100 tokens per item |
| 2 | Full instructions (SKILL.md body) | When skill is activated | < 5k tokens recommended |
| 3 | Supporting resources (scripts, references, assets) | On demand, as needed | Unlimited |

### Level 1: Index Metadata

The discovery index provides `name` and `description` for every available skill. Clients load only these fields at startup or when probing a service. This allows the agent to decide which skills are relevant without paying the cost of loading full instructions.

**Source**: `index.json` skills array entries.

### Level 2: Full Instructions

When a task matches a skill's description, the client fetches the artifact. For `skill-md` type, this is the SKILL.md directly. For `archive` type, the agent downloads the archive and extracts SKILL.md.

**Source**: The artifact at the URL specified in the index entry.

### Level 3: Supporting Resources

The SKILL.md references additional files via relative links (scripts, references, assets). Clients load these only when the task requires them:

```markdown
## Quick Start
Extract text from PDF:
```python
import pdfplumber
with pdfplumber.open("document.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```

## Form Filling
For PDF form filling, see [references/FORMS.md](references/FORMS.md).

## Advanced Extraction
For complex tables, run `scripts/extract_tables.py` or see [references/TABLES.md](references/TABLES.md).
```

An agent extracting text loads SKILL.md and stops. An agent filling a form follows the link to `references/FORMS.md`. Table extraction resources remain unfetched.

## Benefits

- **No upfront token waste**: Loading metadata for 50 skills costs ~5k tokens, not 250k.
- **Just-in-time loading**: Resources enter context only when needed for the specific task.
- **Bundling without penalty**: A skill can bundle extensive reference material without paying context cost until referenced.

## Implementation Pattern

```typescript
interface DiscoveryIndex {
  skills: Array<{
    name: string
    description: string     // Level 1: loaded at discovery
    url: string
    digest: string
  }>
}

interface SkillArtifact {
  body: string              // Level 2: loaded on activation
  references: Map<string, string>  // Level 3: loaded on demand
}
```

## Guidelines for Skill Authors

- Keep SKILL.md under 5k tokens for fast activation.
- Use relative links for additional resources.
- Structure the SKILL.md so common tasks can be completed without loading references.
- Put edge cases, advanced usage, and reference tables in separate files.

## Guidelines for Client Implementers

- Cache Level 1 metadata aggressively (rarely changes).
- Fetch Level 2 only when a skill matches the current task.
- Intercept relative links in SKILL.md and fetch from the unpacked archive or URL.
- Consider prefetching Level 3 resources only when the agent decides to use them.
