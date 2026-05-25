#!/usr/bin/env python3
"""Validate directory structure follows Clean Architecture layering."""
import sys
from pathlib import Path


REQUIRED_DIRS = [
    "domain", "application", "infrastructure", "actions",
]
OPTIONAL_DIRS = [
    "components", "hooks", "app", "pages",
]


def check_dir_structure(dir_path: Path) -> list[dict]:
    findings = []
    for d in REQUIRED_DIRS:
        p = dir_path / "src" / d
        if not p.is_dir():
            p = dir_path / d
        if p.is_dir():
            findings.append({"status": "ok", "check": f"{p.relative_to(dir_path)}/ exists", "detail": "Found"})
            has_files = any(p.iterdir())
            if not has_files:
                findings.append({"status": "warn", "check": f"{p.relative_to(dir_path)}/ has content", "detail": "Empty directory"})
        else:
            findings.append({"status": "warn", "check": f"src/{d}/ or {d}/ exists", "detail": "Missing"})

    for d in OPTIONAL_DIRS:
        if (dir_path / "src" / d).is_dir():
            findings.append({"status": "ok", "check": f"src/{d}/ exists", "detail": "Found"})

    src_path = dir_path / "src"
    if src_path.is_dir():
        for py_file in src_path.rglob("*.ts"):
            relative = py_file.relative_to(src_path)
            content = py_file.read_text()
            if str(relative).startswith("domain"):
                if "infrastructure" in content or "infra" in content:
                    findings.append({"status": "warn", "check": f"Domain layer purity ({relative})", "detail": "Imports from infrastructure"})

    return findings


def main():
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/tmp/nla-dummy")
    if not root.exists():
        print(f"Directory not found: {root}")
        sys.exit(1)

    print(f"Validating Clean Architecture in: {root}")
    findings = check_dir_structure(root)
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
