#!/usr/bin/env python3
"""Validate LanceDB vector search setup in a project."""
import sys
from pathlib import Path

def check_vector_setup(dir_path: Path) -> list[dict]:
    findings = []
    ts_files = list(dir_path.rglob("*.ts")) + list(dir_path.rglob("*.py"))
    if ts_files:
        findings.append({"status": "ok", "check": "Source files", "detail": f"{len(ts_files)} found"})
    for f in ts_files:
        content = f.read_text()
        if "lancedb" in content:
            findings.append({"status": "ok", "check": "LanceDB dependency", "detail": "Found"})
            break
    if "lancedb" not in str([f.read_text() for f in ts_files if "lancedb" in f.read_text()]):
        findings.append({"status": "info", "check": "LanceDB dependency", "detail": "Not found in code"})
    return findings

def main():
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/tmp/nla-vec")
    if not root.exists():
        print(f"Directory not found: {root}")
        sys.exit(1)
    print(f"Validating vector search setup in: {root}")
    findings = check_vector_setup(root)
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
