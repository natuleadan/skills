#!/usr/bin/env python3
"""validate.py — Validate skill structure and content."""

import json
import re
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parent.parent
SKILL_FILE = SKILL_DIR / "SKILL.md"
META_FILE = SKILL_DIR / "metadata.json"
REQUIRED_REFERENCES = [
    "references/accessibility.md",
    "references/touch-interaction.md",
    "references/form-ux.md",
    "references/navigation-patterns.md",
    "references/ux-writing.md",
    "references/cognitive-load.md",
]


def load_metadata() -> dict:
    if not META_FILE.exists():
        print("  X metadata.json not found")
        return {}
    with open(META_FILE) as f:
        return json.load(f)


def parse_frontmatter(text: str) -> dict:
    result = {}
    lines = text.split("\n")
    for line in lines:
        m = re.match(r"^(\S[\w-]*):\s*(.*)", line.rstrip())
        if m:
            result[m.group(1)] = m.group(2).strip()
    return result


def validate():
    errors = 0

    if not SKILL_FILE.exists():
        print("  X SKILL.md not found")
        errors += 1
    else:
        content = SKILL_FILE.read_text()
        meta = parse_frontmatter(content)
        if "name" not in meta:
            print("  X SKILL.md missing frontmatter 'name'")
            errors += 1
        if "description" not in meta:
            print("  X SKILL.md missing frontmatter 'description'")
            errors += 1

    meta_data = load_metadata()
    for field in ("name", "version", "description", "abstract"):
        if field not in meta_data:
            print(f"  X metadata.json missing required field '{field}'")
            errors += 1

    for ref in REQUIRED_REFERENCES:
        if not (SKILL_DIR / ref).exists():
            print(f"  X Reference file missing: {ref}")
            errors += 1

    if errors:
        print(f"  {errors} error(s) found")
    else:
        print("  Valid")

    return errors


if __name__ == "__main__":
    exit(validate())
