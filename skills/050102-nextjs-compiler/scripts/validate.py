#!/usr/bin/env python3
"""Validate Next.js compiler configuration in a project."""
import sys
from pathlib import Path


def check_nextjs_config(dir_path: Path) -> list[dict]:
    findings = []
    for name in ["next.config.js", "next.config.mjs"]:
        cfg = dir_path / name
        if cfg.exists():
            findings.append({"status": "ok", "check": f"{name} exists", "detail": "Found"})
            content = cfg.read_text()
            if "compiler:" in content or "compiler:" in content:
                findings.append({"status": "ok", "check": "Compiler section", "detail": "Found"})
            else:
                findings.append({"status": "info", "check": "Compiler section", "detail": "Not found (optional)"})
            if "removeConsole" in content:
                findings.append({"status": "ok", "check": "removeConsole", "detail": "Configured"})
            if "optimizePackageImports" in content:
                findings.append({"status": "ok", "check": "optimizePackageImports", "detail": "Configured"})
            if "output" in content and "standalone" in content:
                findings.append({"status": "ok", "check": "output: standalone", "detail": "Configured"})
            return findings

    findings.append({"status": "warn", "check": "next.config.js/mjs", "detail": "Not found"})
    return findings


def main():
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/tmp/nla-dummy")
    if not root.exists():
        print(f"Directory not found: {root}")
        sys.exit(1)

    print(f"Validating Next.js compiler config in: {root}")
    findings = check_nextjs_config(root)
    errors = 0
    for f in findings:
        icon = {"ok": "\u2713", "warn": "!", "info": "i"}.get(f["status"], "?")
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
