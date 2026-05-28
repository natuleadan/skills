"""Validate that all reference files referenced in SKILL.md exist."""

import re
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
SKILL_MD = SKILL_DIR / "SKILL.md"

if not SKILL_MD.exists():
    print("SKILL.md not found")
    sys.exit(1)

content = SKILL_MD.read_text()
refs = re.findall(r"\(references/([^)]+)\)", content)
missing = []

for ref in refs:
    path = SKILL_DIR / "references" / ref
    if not path.exists():
        missing.append(ref)

if missing:
    print("Missing reference files:")
    for m in missing:
        print(f"  - references/{m}")
    sys.exit(1)

print(f"All {len(refs)} reference files exist")
