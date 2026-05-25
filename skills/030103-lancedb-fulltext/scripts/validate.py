#!/usr/bin/env python3
"""Validate FTS configuration in a project."""
import sys
from pathlib import Path

def check_fts(dir_path: Path) -> list[dict]:
    findings = []
    ts_files = list(dir_path.rglob("*.ts")) + list(dir_path.rglob("*.py"))
    for f in ts_files:
        content = f.read_text()
        if "create_fts_index" in content or "create_index" in content:
            findings.append({"status": "ok", "check": "FTS index creation", "detail": "Found"})
            break
    if not findings:
        findings.append({"status": "info", "check": "FTS index creation", "detail": "Not found"})
    return findings

def main():
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/tmp/nla-fts")
    if not root.exists():
        print(f"Directory not found: {root}")
        sys.exit(1)
    print(f"Validating FTS setup in: {root}")
    findings = check_fts(root)
    errors = sum(1 for f in findings if f["status"] == "warn")
    for f in findings:
        icon = {"ok": "✓", "warn": "!", "info": "i"}.get(f["status"], "?")
        print(f"  {icon} {f['check']}: {f['detail']}")
    if errors:
        print(f"\n{errors} warning(s) found")
    else:
        print("\nAll checks passed.")
    sys.exit(0)

if __name__ == "__main__":
    main()
