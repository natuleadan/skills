#!/usr/bin/env python3
"""Validate Elysia controller structure in a project."""
import sys
from pathlib import Path


def check_elysia_patterns(dir_path: Path) -> list[dict]:
    findings = []
    controllers_dir = dir_path / "controllers"
    if controllers_dir.is_dir():
        ctrl_files = list(controllers_dir.glob("*.ctrl.ts"))
        if ctrl_files:
            findings.append({"status": "ok", "check": "Controller files found", "detail": f"{len(ctrl_files)} file(s)"})
            for cf in ctrl_files:
                content = cf.read_text()
                if "new Elysia" in content:
                    findings.append({"status": "ok", "check": f"  {cf.name}: Elysia instance", "detail": "Found"})
                if "prefix:" in content:
                    findings.append({"status": "ok", "check": f"  {cf.name}: Route prefix", "detail": "Found"})
                if "detail:" in content:
                    findings.append({"status": "ok", "check": f"  {cf.name}: OpenAPI detail", "detail": "Found"})
        else:
            findings.append({"status": "info", "check": "Controller files (*.ctrl.ts)", "detail": "None found"})
    else:
        findings.append({"status": "info", "check": "controllers/ directory", "detail": "Not found"})

    # Check for typical imports
    ts_files = list(dir_path.rglob("*.ts"))
    elysia_imports = sum(1 for f in ts_files if "elysia" in f.read_text())
    if elysia_imports:
        findings.append({"status": "ok", "check": "Elysia package usage", "detail": f"Found in {elysia_imports} file(s)"})

    return findings


def main():
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/tmp/skill-dummy")
    if not root.exists():
        print(f"Directory not found: {root}")
        sys.exit(1)

    print(f"Validating Elysia patterns in: {root}")
    findings = check_elysia_patterns(root)
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
