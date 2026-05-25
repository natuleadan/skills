#!/usr/bin/env python3
"""Validate backend architecture patterns in a project."""
import sys
from pathlib import Path


def check_backend(dir_path: Path) -> list[dict]:
    findings = []

    src = dir_path / "src"

    # Check for env.ts
    env_file = src / "lib" / "env.ts"
    if not env_file.exists():
        env_file = src / "env.ts"
    if env_file.exists():
        findings.append({"status": "ok", "check": "env.ts configuration", "detail": str(env_file.relative_to(dir_path))})
        content = env_file.read_text()
        if "requireEnv" in content:
            findings.append({"status": "ok", "check": "  requireEnv() pattern", "detail": "Found"})
    else:
        findings.append({"status": "info", "check": "env.ts", "detail": "Not found"})

    # Check for service layer
    service_files = list(dir_path.rglob("service*.ts"))
    if service_files:
        findings.append({"status": "ok", "check": "Service layer files", "detail": f"{len(service_files)} file(s)"})
    else:
        findings.append({"status": "info", "check": "Service layer", "detail": "No service*.ts files found"})

    # Check for repository layer
    repo_files = list(dir_path.rglob("repository*.ts"))
    if repo_files:
        findings.append({"status": "ok", "check": "Repository layer files", "detail": f"{len(repo_files)} file(s)"})
    else:
        findings.append({"status": "info", "check": "Repository layer", "detail": "No repository*.ts files found"})

    # Check for error handling patterns
    error_files = list(dir_path.rglob("error*.ts"))
    if error_files:
        findings.append({"status": "ok", "check": "Error handling files", "detail": f"{len(error_files)} file(s)"})
    else:
        pass  # not required, may use inline error handling

    # Check for actions
    actions_dir = dir_path / "actions"
    if actions_dir.is_dir():
        findings.append({"status": "ok", "check": "Server Actions directory", "detail": "Found"})

    return findings


def main():
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/tmp/skill-be")
    if not root.exists():
        print(f"Directory not found: {root}")
        sys.exit(1)

    print(f"Validating backend architecture in: {root}")
    findings = check_backend(root)
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
