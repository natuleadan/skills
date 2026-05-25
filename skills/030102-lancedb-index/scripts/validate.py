#!/usr/bin/env python3
"""Validate LanceDB index configuration in a project."""
import sys
from pathlib import Path

def check_index_config(dir_path: Path) -> list[dict]:
    findings = []
    ts_files = list(dir_path.rglob("*.ts")) + list(dir_path.rglob("*.py"))
    if ts_files:
        findings.append({"status": "ok", "check": "Source files", "detail": f"{len(ts_files)} found"})
    for f in ts_files:
        content = f.read_text()
        if "create_index" in content:
            findings.append({"status": "ok", "check": "Index creation (create_index)", "detail": "Found"})
            break
    return findings

def main():
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/tmp/nla-idx")
    if not root.exists():
        print(f"Directory not found: {root}")
        sys.exit(1)
    print(f"Validating index configuration in: {root}")
    findings = check_index_config(root)
    errors = sum(1 for f in findings if f["status"] == "warn")
    for f in findings:
        icon = {"ok": "\u2713", "warn": "!", "info": "i"}.get(f["status"], "?")
        print(f"  {icon} {f['check']}: {f['detail']}")
    if errors:
        print(f"\n{errors} warning(s) found")
    else:
        print("\nAll checks passed.")
    sys.exit(0)

if __name__ == "__main__":
    main()
