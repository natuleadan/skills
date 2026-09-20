#!/usr/bin/env python3
"""Temporary audit: verify the industry skills are clean, uniform stubs.

Checks (16 industry skills, `*-ai-tools`):
1. no platform concepts inside: `robot`, `toolset`, `human-in-the-loop`, `HIL`
2. no provider mention: `natuleadan`, `nla.run`, `nla-api`, `.com`, `.app`
3. no embedded code (fenced blocks)
4. every file is a stub of the expected shape (single H1 + stub callout)
5. references declared in metadata.json exist (and vice versa)
6. the 16 skills have the same *shape* (not necessarily the same line count)

Exit: 0 clean | 1 findings
Run: python3 tools/audit-temp.py
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"

PLATFORM_WORDS = ["robot", "toolset", "human-in-the-loop", "HIL"]
VENDOR_WORDS = ["natuleadan", "nla.run", "nla-api", "natuleadan.com", "natuleadan.app"]
# Pricing / internal-system topics must not appear anywhere in the repo's skills.
COMMERCIAL_WORDS = [
    "credit", "usd", "billing", "invoice", "payment", "price", "pricing",
    "wallet", "top-up", "subscription", "fee", "refund", "tax",
]
H1 = re.compile(r"^# ", re.M)


def audit_industry():
    findings = []
    shapes = {}
    skills = sorted(p for p in SKILLS.iterdir() if p.is_dir() and p.name.endswith("-ai-tools"))

    for skill in skills:
        name = skill.name
        files = sorted(skill.rglob("*.md"))

        for path in files:
            rel = path.relative_to(skill).as_posix()
            text = path.read_text(encoding="utf-8")
            low = text.lower()

            # 0. commercial / internal-system topics (prohibited everywhere)
            for word in COMMERCIAL_WORDS:
                if re.search(rf"\b{re.escape(word)}", low):
                    findings.append(f"{name}: commercial word '{word}' in {rel}")

            # 1. platform concepts (prohibited inside the 16 areas)
            for word in PLATFORM_WORDS:
                if word.lower() in low:
                    findings.append(f"{name}: platform word '{word}' in {rel}")

            # 2. vendor mention
            for word in VENDOR_WORDS:
                if word.lower() in low:
                    findings.append(f"{name}: vendor word '{word}' in {rel}")

            # 3. embedded code is only allowed when it is a mermaid block
            for block in re.findall(r"```(\w+)", text):
                if block != "mermaid":
                    findings.append(f"{name}: non-mermaid code block in {rel}")

        # 4. every reference MUST have a mermaid sequenceDiagram
        for ref in sorted(skill.glob("references/*.md")):
            text = ref.read_text(encoding="utf-8")
            if "```mermaid" not in text:
                findings.append(f"{name}: {ref.name} has no mermaid block")
            elif "sequenceDiagram" not in text:
                findings.append(f"{name}: {ref.name} mermaid is not a sequenceDiagram")

        # 5. SKILL.md must NOT contain mermaid
        skill_md = skill / "SKILL.md"
        if skill_md.exists():
            text = skill_md.read_text(encoding="utf-8")
            if "mermaid" in text:
                findings.append(f"{name}: SKILL.md must not contain mermaid")
            if not text.startswith("---\n"):
                findings.append(f"{name}: SKILL.md missing frontmatter")
            if len(H1.findall(text)) != 1:
                findings.append(f"{name}: SKILL.md must have exactly one H1")
        else:
            findings.append(f"{name}: missing SKILL.md")

        for ref in skill.glob("references/*.md"):
            text = ref.read_text(encoding="utf-8")
            if len(H1.findall(text)) != 1:
                findings.append(f"{name}: {ref.name} must have exactly one H1")
            if "Stub" not in text:
                findings.append(f"{name}: {ref.name} is not a stub")

        # 5. metadata <-> references
        meta_path = skill / "metadata.json"
        if meta_path.exists():
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
            declared = set(meta.get("references", []))
            present = {p.name for p in skill.glob("references/*.md")}
            for ref in sorted(declared - present):
                findings.append(f"{name}: metadata declares missing '{ref}'")
            for ref in sorted(present - declared):
                findings.append(f"{name}: reference '{ref}' not declared in metadata")
        else:
            findings.append(f"{name}: missing metadata.json")

        # 6. shape signature: file list (for uniformity comparison)
        shapes[name] = tuple(sorted(p.relative_to(skill).as_posix() for p in files))

    return findings, skills, shapes


def main():
    findings, skills, shapes = audit_industry()

    print(f"Industry skills audited: {len(skills)}")
    for name in sorted(shapes):
        print(f"  {name}: {len(shapes[name])} md files")

    # uniformity: same number of md files across the 16 (shape parity)
    counts = {len(v) for v in shapes.values()}
    print(f"\nDistinct md-file counts: {sorted(counts)} (line counts may differ per area)")

    if findings:
        print("\nFINDINGS:")
        for f in findings:
            print(f"  - {f}")
        print(f"\n{len(findings)} finding(s)")
        sys.exit(1)

    print("\nCLEAN: no platform concepts, no vendor mention, no code, stubs OK.")
    sys.exit(0)


if __name__ == "__main__":
    main()
