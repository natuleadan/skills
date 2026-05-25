#!/usr/bin/env python3
"""Validate Zero Trust auth pattern in a project."""
import sys
from pathlib import Path


def check_zero_trust(dir_path: Path) -> list[dict]:
    findings = []

    # Check for common anti-patterns
    ts_files = list(dir_path.rglob("*.ts"))
    violations = []
    for f in ts_files:
        content = f.read_text()
        relative = f.relative_to(dir_path)
        # Check for client-provided role (common anti-pattern)
        lines = content.split("\n")
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if ("role" in stripped.lower() and
                any(x in stripped for x in ["body.", "query.", "params.", "formData.get" ]) and
                "role" in stripped.lower()):
                # This is a potential violation - accept role from client
                violations.append(f"  {relative}:{i} - {stripped.strip()[:80]}")

    if violations:
        findings.append({"status": "warn", "check": "Potential Zero Trust violations", "detail": f"{len(violations)} found"})
        for v in violations[:5]:
            findings.append({"status": "info", "check": v, "detail": ""})
    else:
        findings.append({"status": "ok", "check": "No Zero Trust violations detected", "detail": "Good"})

    # Check for session usage in actions
    actions_dir = dir_path / "actions"
    if actions_dir.is_dir():
        session_usage = sum(1 for f in actions_dir.rglob("*.ts") if "getSession" in f.read_text())
        if session_usage:
            findings.append({"status": "ok", "check": "Session validation in actions", "detail": f"Found in {session_usage} file(s)"})
        else:
            findings.append({"status": "info", "check": "Session validation in actions", "detail": "Not detected"})

    return findings


def main():
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/tmp/skill-dummy")
    if not root.exists():
        print(f"Directory not found: {root}")
        sys.exit(1)

    print(f"Validating Zero Trust auth in: {root}")
    findings = check_zero_trust(root)
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
