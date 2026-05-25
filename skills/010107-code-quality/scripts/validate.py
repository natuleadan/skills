#!/usr/bin/env python3
"""Validate code quality standards in a project."""
import sys
from pathlib import Path


def check_quality(dir_path: Path) -> list[dict]:
    findings = []

    # Check TypeScript config
    tsconfig = dir_path / "tsconfig.json"
    if tsconfig.exists():
        content = tsconfig.read_text()
        findings.append({"status": "ok", "check": "tsconfig.json", "detail": "Found"})
        if "strict" in content:
            findings.append({"status": "ok", "check": "  strict mode", "detail": "Enabled"})
        if "noUncheckedIndexedAccess" in content:
            findings.append({"status": "ok", "check": "  noUncheckedIndexedAccess", "detail": "Configured"})
    else:
        findings.append({"status": "warn", "check": "tsconfig.json", "detail": "Not found"})

    # Check for .ts files with `any` usage
    ts_files = list(dir_path.rglob("*.ts")) + list(dir_path.rglob("*.tsx"))
    any_count = 0
    enum_count = 0
    for f in ts_files:
        content = f.read_text()
        if ": any" in content or ":any" in content:
            any_count += 1
        if "enum " in content:
            enum_count += 1
    if any_count:
        findings.append({"status": "info", "check": "TypeScript: `any` usage", "detail": f"{any_count} file(s) — review recommended"})
    else:
        findings.append({"status": "ok", "check": "TypeScript: no `any` usage", "detail": "Clean"})
    if enum_count:
        findings.append({"status": "info", "check": "TypeScript: `enum` usage", "detail": f"{enum_count} file(s) — consider union types"})

    # Check for test files
    test_files = list(dir_path.rglob("*.test.ts")) + list(dir_path.rglob("*.test.tsx")) + list(dir_path.rglob("*.spec.ts"))
    if test_files:
        findings.append({"status": "ok", "check": "Test files", "detail": f"{len(test_files)} file(s)"})
    else:
        findings.append({"status": "info", "check": "Test files", "detail": "None found"})

    # Check for vitest config
    vitest_cfg = dir_path / "vitest.config.ts"
    if vitest_cfg.exists():
        findings.append({"status": "ok", "check": "Vitest config", "detail": "vitest.config.ts"})

    # Check for .env usage (not hardcoded secrets)
    ts_content = " ".join(f.read_text() for f in ts_files)
    suspicious = [k for k in ["sk-", "api_key=", "secret=", "password="] if k in ts_content.lower() and ".env" not in ts_content]
    if suspicious:
        findings.append({"status": "warn", "check": "Possible hardcoded secrets", "detail": f"Found patterns: {', '.join(suspicious)}"})
    else:
        findings.append({"status": "ok", "check": "No hardcoded secrets detected", "detail": "Good"})

    return findings


def main():
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/tmp/skill-cq")
    if not root.exists():
        print(f"Directory not found: {root}")
        sys.exit(1)

    print(f"Validating code quality in: {root}")
    findings = check_quality(root)
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
