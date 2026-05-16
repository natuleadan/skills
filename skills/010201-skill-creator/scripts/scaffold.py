#!/usr/bin/env python3
"""scaffold.py — Create a new skill skeleton with SKILL.md, references/, evals/, scripts/."""

import argparse
import os
import sys


def to_title(name: str) -> str:
    return " ".join(word.capitalize() for word in name.split("-"))


def main():
    parser = argparse.ArgumentParser(description="Create a new skill skeleton")
    parser.add_argument("name", help="Skill name (e.g., my-skill)")
    parser.add_argument("--category", default=".", help="Category directory (e.g., node/security)")
    args = parser.parse_args()

    name = args.name
    category = args.category.strip("/")
    skill_dir = os.path.join(category, name)

    if os.path.exists(skill_dir):
        print(f"Error: {skill_dir} already exists")
        sys.exit(1)

    os.makedirs(os.path.join(skill_dir, "references"))
    os.makedirs(os.path.join(skill_dir, "scripts"))
    os.makedirs(os.path.join(skill_dir, "evals"))

    with open(os.path.join(skill_dir, "SKILL.md"), "w") as f:
        f.write(f"""---
name: {name}
description: TODO: Describe what this skill does and when to trigger it.
---

# {to_title(name)}

TODO: Write instructions here.

## How to use this skill

1. Step one
2. Step two

## References

- `references/guide.md` — Detailed guide

## Validation

Run `python scripts/validate.py` to verify.
""")

    with open(os.path.join(skill_dir, "evals", "evals.json"), "w") as f:
        f.write(f"""\
{{
  "skill_name": "{name}",
  "evals": [
    {{
      "id": 1,
      "prompt": "Realistic user task prompt here",
      "expected_output": "Description of expected result",
      "files": [],
      "expectations": [
        "Verifiable assertion about the output"
      ]
    }}
  ]
}}
""")

    with open(os.path.join(skill_dir, "scripts", "validate.py"), "w") as f:
        f.write(f"""\
#!/usr/bin/env python3
\"\"\"validate.py — Validation for {name}.\"\"\"

import sys


def main():
    print("Validation for {name} — TODO")
    print("Add your validation logic here")


if __name__ == "__main__":
    main()
""")

    print(f"\u2705 Created skill: {skill_dir}")
    print()
    print("  SKILL.md         — Edit this file")
    print("  references/      — Add detailed docs here")
    print("  scripts/         — Add executable code here")
    print("  evals/evals.json — Add test cases here")
    print()
    print("Next steps:")
    print(f"  1. Edit {skill_dir}/SKILL.md")
    print(f"  2. Edit {skill_dir}/evals/evals.json")
    print("  3. Register in .claude-plugin/marketplace.json")


if __name__ == "__main__":
    main()
