#!/usr/bin/env python3
"""Validate caching configuration in a project."""
import os
import sys
from pathlib import Path


def find_config(dir_path: Path) -> list[dict]:
    findings = []
    next_config = dir_path / "next.config.mjs"
    if next_config.exists():
        content = next_config.read_text()
        if "cacheLife" in content or "cacheTag" in content:
            findings.append({"status": "ok", "check": "Runtime cache usage (cacheLife/cacheTag)", "detail": "Found"})
        else:
            findings.append({"status": "warn", "check": "Runtime cache usage (cacheLife/cacheTag)", "detail": "Not found - consider adding"})
        if "stale-while-revalidate" in content or "s-maxage" in content:
            findings.append({"status": "ok", "check": "CDN cache headers", "detail": "Found"})
        else:
            findings.append({"status": "warn", "check": "CDN cache headers", "detail": "Not found in config"})
    else:
        findings.append({"status": "info", "check": "next.config.mjs", "detail": "Not found - no Next.js config to validate"})

    cache_py = next(dir_path.rglob("cache.ts"), None)
    if cache_py and cache_py.exists():
        content = cache_py.read_text()
        if "multi(" in content:
            findings.append({"status": "ok", "check": "Atomic transactions (multi/exec)", "detail": "Found"})
        if "execBatch" in content or "Promise.all" in content:
            findings.append({"status": "ok", "check": "Pipeline batching", "detail": "Found"})
    else:
        findings.append({"status": "info", "check": "Distributed cache client", "detail": "cache.ts not found"})

    return findings


def main():
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/tmp/skill-dummy")
    if not root.exists():
        print(f"Directory not found: {root}")
        sys.exit(1)

    print(f"Validating caching patterns in: {root}")
    findings = find_config(root)
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
