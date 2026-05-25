#!/usr/bin/env python3
"""Validate Server Action patterns in a project."""
import sys
from pathlib import Path


def check_server_actions(dir_path: Path) -> list[dict]:
    findings = []

    actions_dir = dir_path / "actions"
    if actions_dir.is_dir():
        findings.append({"status": "ok", "check": "actions/ directory", "detail": "Found"})
        ts_files = list(actions_dir.rglob("*.ts"))
        if ts_files:
            findings.append({"status": "ok", "check": f"Action files found", "detail": f"{len(ts_files)} file(s)"})
            for af in ts_files:
                content = af.read_text()
                relative = af.relative_to(dir_path)
                if '"use server"' in content or "'use server'" in content:
                    findings.append({"status": "ok", "check": f"  {relative}: use server directive", "detail": "Found"})
                else:
                    findings.append({"status": "warn", "check": f"  {relative}: use server directive", "detail": "Missing"})
                if "export async function" in content:
                    findings.append({"status": "ok", "check": f"  {relative}: async export", "detail": "Found"})
                if "redirect(" in content:
                    findings.append({"status": "info", "check": f"  {relative}: uses redirect", "detail": "Found"})
        else:
            findings.append({"status": "info", "check": "Action files", "detail": "No .ts files found in actions/"})
    else:
        findings.append({"status": "warn", "check": "actions/ directory", "detail": "Not found"})

    return findings


def main():
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/tmp/nla-dummy")
    if not root.exists():
        print(f"Directory not found: {root}")
        sys.exit(1)

    print(f"Validating Server Actions in: {root}")
    findings = check_server_actions(root)
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
