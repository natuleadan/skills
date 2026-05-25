#!/usr/bin/env python3
"""Validate commit conventions in a project."""
import sys
import json
from pathlib import Path


def check_commit_config(dir_path: Path) -> list[dict]:
    findings = []

    # Check commitlint config
    for cfg in ["commitlint.config.js", "commitlint.config.cjs", ".commitlintrc.json"]:
        cf = dir_path / cfg
        if cf.exists():
            findings.append({"status": "ok", "check": f"{cfg}", "detail": "Found"})
            content = cf.read_text()
            if "extends" in content:
                findings.append({"status": "ok", "check": "  commitlint extends", "detail": "Configured"})
            break

    # Check recent commit messages
    git_dir = dir_path / ".git"
    if git_dir.is_dir():
        try:
            result = __import__("subprocess").run(
                ["git", "log", "--oneline", "-10"],
                capture_output=True, text=True, cwd=dir_path
            )
            if result.stdout:
                conventional = 0
                total = 0
                for line in result.stdout.strip().split("\n"):
                    total += 1
                    if ":" in line.split(" ", 1)[-1]:
                        conventional += 1
                if total > 0:
                    pct = conventional / total * 100
                    findings.append({"status": "ok", "check": f"Conventional commits ({conventional}/{total})", "detail": f"{pct:.0f}%"})
        except Exception:
            findings.append({"status": "info", "check": "Git log", "detail": "Could not read"})

    return findings


def main():
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/tmp/skill-git")
    if not root.exists():
        print(f"Directory not found: {root}")
        sys.exit(1)

    print(f"Validating git commit conventions in: {root}")
    findings = check_commit_config(root)
    errors = 0
    for f in findings:
        icon = {"ok": "✓", "warn": "!", "info": "i"}.get(f["status"], "?")
        print(f"  {icon} {f['check']}: {f['detail']}")
        if f["status"] == "warn":
            errors += 1

    if errors:
        print(f"\n{errors} warning(s) found")
    else:
        print("\nAll checks passed.")
    sys.exit(0)


if __name__ == "__main__":
    main()
