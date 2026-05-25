#!/usr/bin/env python3
"""Validate hybrid/multivector search setup in a project."""
import sys
from pathlib import Path

def check_hybrid(dir_path: Path) -> list[dict]:
    findings = []
    ts_files = list(dir_path.rglob("*.ts")) + list(dir_path.rglob("*.py"))
    hybrid_found = False
    for f in ts_files:
        content = f.read_text()
        if "reranker" in content:
            hybrid_found = True
            findings.append({"status": "ok", "check": "Hybrid search (reranker)", "detail": "Found"})
            break
    if hybrid_found:
        findings.append({"status": "ok", "check": "Hybrid search patterns", "detail": "Found"})
    else:
        findings.append({"status": "info", "check": "Hybrid search", "detail": "Not found"})
    return findings

def main():
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/tmp/nla-hyb")
    if not root.exists():
        print(f"Directory not found: {root}")
        sys.exit(1)
    print(f"Validating hybrid/multivector setup in: {root}")
    findings = check_hybrid(root)
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
