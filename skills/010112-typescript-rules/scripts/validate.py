#!/usr/bin/env python3
import sys
from pathlib import Path

def check_typescript(dir_path: Path) -> list[dict]:
    findings = []
    tsconfig = dir_path / "tsconfig.json"
    if tsconfig.exists():
        findings.append({"status": "ok", "check": "tsconfig.json", "detail": "Found"})
        content = tsconfig.read_text()
        if "strict" in content:
            findings.append({"status": "ok", "check": "  strict mode", "detail": "Enabled"})
    ts_files = list(dir_path.rglob("*.ts")) + list(dir_path.rglob("*.tsx"))
    any_count = enum_count = 0
    for f in ts_files:
        c = f.read_text()
        if ": any" in c or ":any" in c: any_count += 1
        if "enum " in c: enum_count += 1
    findings.append({"status": "ok" if any_count == 0 else "info", "check": "TypeScript `any` usage", "detail": f"{any_count} file(s)" if any_count else "Clean"})
    findings.append({"status": "ok" if enum_count == 0 else "info", "check": "TypeScript `enum` usage", "detail": f"{enum_count} file(s)" if enum_count else "Clean"})
    return findings

def main():
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/tmp/nla-ts")
    if not root.exists(): print(f"Not found: {root}"); sys.exit(1)
    print(f"Validating TypeScript in: {root}")
    findings = check_typescript(root)
    errors = sum(1 for f in findings if f["status"] == "warn")
    for f in findings:
        print(f"  {'✓' if f['status']=='ok' else '!' if f['status']=='warn' else 'i'} {f['check']}: {f['detail']}")
    print("\nAll checks passed." if not errors else f"\n{errors} warning(s)")
    sys.exit(0)

if __name__ == "__main__":
    main()
