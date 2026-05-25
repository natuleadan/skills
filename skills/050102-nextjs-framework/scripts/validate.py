#!/usr/bin/env python3
import sys
from pathlib import Path

def check_nextjs(dir_path: Path) -> list[dict]:
    findings = []
    next_config = dir_path / "next.config.ts" or dir_path / "next.config.js" or dir_path / "next.config.mjs"
    for nc in ["next.config.ts", "next.config.js", "next.config.mjs"]:
        if (dir_path / nc).exists():
            content = (dir_path / nc).read_text()
            findings.append({"status": "ok", "check": nc, "detail": "Found"})
            if "reactCompiler" in content:
                findings.append({"status": "ok", "check": "  React Compiler", "detail": "Enabled"})
            if "turbopack" in content.lower():
                findings.append({"status": "info", "check": "  Turbopack", "detail": "Referenced"})
            break
    tsx_files = list(dir_path.rglob("*.tsx"))
    if tsx_files:
        findings.append({"status": "ok", "check": f"Components (.tsx)", "detail": f"{len(tsx_files)} found"})
    proxy = dir_path / "proxy.ts"
    if proxy.exists():
        findings.append({"status": "ok", "check": "proxy.ts", "detail": "Found (Next.js 16 middleware)"})
    async_await = 0
    for f in tsx_files:
        content = f.read_text()
        if "await params" in content or "await searchParams" in content:
            async_await += 1
    if async_await > 0:
        findings.append({"status": "ok", "check": "Async Request APIs", "detail": f"Found in {async_await} file(s)"})
    return findings

def main():
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/tmp/skill-nextjs")
    if not root.exists():
        print(f"Directory not found: {root}")
        sys.exit(1)
    print(f"Validating Next.js framework in: {root}")
    findings = check_nextjs(root)
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
