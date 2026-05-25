#!/usr/bin/env python3
"""Validate Docker deployment configuration in a project."""
import sys
from pathlib import Path


def check_docker_config(dir_path: Path) -> list[dict]:
    findings = []

    dockerfile = dir_path / "Dockerfile"
    if dockerfile.exists():
        content = dockerfile.read_text()
        if "FROM" in content:
            findings.append({"status": "ok", "check": "Dockerfile exists", "detail": "Found"})
        if "AS " in content:
            findings.append({"status": "ok", "check": "Multi-stage build", "detail": "Found"})
        else:
            findings.append({"status": "warn", "check": "Multi-stage build", "detail": "Not using multi-stage"})
        if "USER " in content and "root" not in content.split("USER")[-1].split("\n")[0]:
            findings.append({"status": "ok", "check": "Non-root user", "detail": "Found"})
        else:
            findings.append({"status": "info", "check": "Non-root user", "detail": "Not specified (consider adding)"})
    else:
        findings.append({"status": "warn", "check": "Dockerfile", "detail": "Not found"})

    compose = dir_path / "docker-compose.yml"
    if compose.exists():
        findings.append({"status": "ok", "check": "docker-compose.yml", "detail": "Found"})
        content = compose.read_text()
        if "cap_drop" in content:
            findings.append({"status": "ok", "check": "Capability hardening", "detail": "Found"})
        if "read_only" in content:
            findings.append({"status": "ok", "check": "Read-only root filesystem", "detail": "Found"})
    else:
        findings.append({"status": "info", "check": "docker-compose.yml", "detail": "Not found"})

    dc_ignore = dir_path / ".dockerignore"
    if dc_ignore.exists():
        content = dc_ignore.read_text()
        for pattern in [".env", "node_modules", ".git"]:
            if pattern in content:
                findings.append({"status": "ok", "check": f".dockerignore excludes {pattern}", "detail": "Found"})
    else:
        findings.append({"status": "info", "check": ".dockerignore", "detail": "Not found"})

    return findings


def main():
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/tmp/skill-dummy")
    if not root.exists():
        print(f"Directory not found: {root}")
        sys.exit(1)

    print(f"Validating Docker deployment in: {root}")
    findings = check_docker_config(root)
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
