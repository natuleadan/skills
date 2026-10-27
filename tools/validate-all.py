#!/usr/bin/env python3
"""Validate every skill in skills/.

Rules:
- each skill has SKILL.md with frontmatter `name` and `description`
- each skill has metadata.json with `version`, `abstract`, `references`
- every declared reference exists in references/
- every reference contains a mermaid sequence diagram
- SKILL.md and references stay under 300 lines
- no fenced code blocks inside .md (only mermaid is allowed)
- no code/ directory and no executable files under skills/
- every path listed in .claude-plugin/marketplace.json exists
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"
FRONTMATTER = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.S)


def read_frontmatter(text):
    m = FRONTMATTER.match(text)
    if not m:
        return None
    data = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            data[k.strip()] = v.strip().strip('"')
    return data


def main():
    errors = []
    skills = sorted(p for p in SKILLS.iterdir() if p.is_dir())
    if not skills:
        print("ERROR: no skills found", file=sys.stderr)
        sys.exit(1)

    for skill in skills:
        name = skill.name

        skill_md = skill / "SKILL.md"
        if not skill_md.exists():
            errors.append(f"{name}: missing SKILL.md")
        else:
            fm = read_frontmatter(skill_md.read_text(encoding="utf-8"))
            if not fm:
                errors.append(f"{name}: SKILL.md has no frontmatter")
            else:
                for key in ("name", "description"):
                    if not fm.get(key):
                        errors.append(f"{name}: SKILL.md missing '{key}'")
                if fm.get("name") != name:
                    errors.append(f"{name}: frontmatter name '{fm.get('name')}' != folder")

        meta_path = skill / "metadata.json"
        if not meta_path.exists():
            errors.append(f"{name}: missing metadata.json")
        else:
            try:
                meta = json.loads(meta_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError as exc:
                errors.append(f"{name}: metadata.json invalid ({exc})")
                meta = {}
            for key in ("version", "abstract"):
                if not meta.get(key):
                    errors.append(f"{name}: metadata.json missing '{key}'")
            refs = meta.get("references")
            if refs is None:
                errors.append(f"{name}: metadata.json missing 'references'")
            else:
                for ref in refs:
                    ref_path = skill / "references" / ref
                    if not ref_path.exists():
                        errors.append(f"{name}: missing reference '{ref}'")
                        continue
                    ref_text = ref_path.read_text(encoding="utf-8")
                    if "```mermaid" not in ref_text or "sequenceDiagram" not in ref_text:
                        errors.append(
                            f"{name}: reference '{ref}' needs a mermaid sequenceDiagram"
                        )

        # line limits: SKILL.md and every reference stay under 300 lines
        for md in skill.rglob("*.md"):
            lines = len(md.read_text(encoding="utf-8").splitlines())
            if lines > 300:
                errors.append(
                    f"{name}: {md.relative_to(skill)} has {lines} lines (max 300)"
                )

        # skills are instructions, not code: no code/ directory, no executables
        if (skill / "code").exists():
            errors.append(f"{name}: code/ directory is not allowed in skills")
        for path in skill.rglob("*"):
            if path.is_file() and path.stat().st_mode & 0o111:
                errors.append(
                    f"{name}: executable file not allowed ({path.relative_to(skill)})"
                )

        # no code inside markdown; mermaid diagrams are allowed
        for md in skill.rglob("*.md"):
            text = md.read_text(encoding="utf-8")
            for block in re.findall(r"```(\w+)", text):
                if block != "mermaid":
                    errors.append(
                        f"{name}: non-mermaid code block in {md.relative_to(skill)} (only mermaid is allowed)"
                    )

    # the marketplace catalog must resolve to real directories
    marketplace = ROOT / ".claude-plugin" / "marketplace.json"
    if marketplace.exists():
        try:
            catalog = json.loads(marketplace.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"marketplace.json invalid ({exc})")
            catalog = {}
        for plugin in catalog.get("plugins", []):
            for entry in plugin.get("skills", []):
                if not (ROOT / entry).exists():
                    errors.append(f"marketplace.json: missing path '{entry}'")

    if errors:
        for e in errors:
            print(f"ERROR: {e}", file=sys.stderr)
        print(f"\n{len(errors)} error(s)", file=sys.stderr)
        sys.exit(1)

    print(f"All {len(skills)} skills valid.")
    sys.exit(0)


if __name__ == "__main__":
    main()
