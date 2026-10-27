#!/usr/bin/env python3
"""Validate a commit message against the repository rules.

Rules:
- Title: `type(scope): description`, lowercase scope, 3 to 7 words.
- Blank line after the title.
- At least 3 bullets, each `- **Title**: body`, body of 3 to 7 words.

Usage: python3 tools/check-commit.py <message-file>
Exit: 0 valid, 1 invalid, 2 bad usage.
"""
import re
import sys

TYPES = (
    "feat", "fix", "test", "docs", "chore", "refactor",
    "perf", "style", "ci", "build", "revert", "upgrade",
)


def validate(path):
    lines = [l.rstrip() for l in open(path, encoding="utf-8").read().split("\n")]
    lines = [l for l in lines if not l.startswith("#")]
    while lines and lines[0] == "":
        lines.pop(0)

    errors = []
    if not lines:
        errors.append("the message is empty")
    else:
        title = lines[0]
        if not re.match(r"^(?:%s)\([a-z0-9-]+\): \S" % "|".join(TYPES), title):
            errors.append("title must be 'type(scope): description'")

        words = len(title.split())
        if words < 3 or words > 7:
            errors.append(f"title has {words} words (min 3, max 7)")

        if len(lines) < 2 or lines[1] != "":
            errors.append("missing blank line after the title")

        bullets = []
        started = False
        for line in lines[1:]:
            if line.startswith("- "):
                started = True
                bullets.append(line)
            elif started:
                break

        if len(bullets) < 3:
            errors.append(f"{len(bullets)} bullets (min 3)")

        for index, bullet in enumerate(bullets, 1):
            match = re.match(r"^\*\*[^*]+\*\*:\s*(\S.*)$", bullet[2:])
            if not match:
                errors.append(f"bullet {index}: missing '**Title**:' prefix")
                continue
            body_words = len(match.group(1).split())
            if body_words < 3 or body_words > 7:
                errors.append(
                    f"bullet {index}: {body_words} words (min 3, max 7)"
                )

    for error in errors:
        print(f"  FAIL  {error}", file=sys.stderr)
    if not errors:
        print("  OK    commit message valid")
    return 1 if errors else 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: check-commit.py <message-file>", file=sys.stderr)
        sys.exit(2)
    sys.exit(validate(sys.argv[1]))
