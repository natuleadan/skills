# Changesets

This repository uses changesets for versioning.

## Creating a changeset

```bash
npm run changeset
```

Follow the prompts to select the type of change (patch/minor/major) and describe it.

## Versioning

```bash
npm run version
```

This will:
1. Bump versions in package.json
2. Generate CHANGELOG.md entries
3. Sync version to .claude-plugin/plugin.json

## Publishing

```bash
git add .
git commit -m "chore: version skills"
git tag v<new-version>
git push && git push --tags
```
