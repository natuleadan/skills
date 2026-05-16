#!/usr/bin/env python3
"""audit-project.py — Check project-level supply chain security settings in package.json."""

import json
import sys
from pathlib import Path
from typing import Optional


def load_package_json(path: Path) -> Optional[dict]:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError:
        return None


def check_engines(pkg: dict) -> list[dict]:
    issues = []
    engines = pkg.get("engines", {})
    if not engines:
        issues.append({"setting": "engines", "status": "missing", "detail": "Add engines.node to package.json (e.g., \"node\": \">=18.0.0\")"})
    elif "node" not in engines:
        issues.append({"setting": "engines.node", "status": "missing", "detail": "Add engines.node to package.json"})
    else:
        issues.append({"setting": "engines.node", "status": "ok", "detail": f"Node >= {engines['node']}"})
    return issues


def check_engine_strict(pkg: dict, npmrc_content: Optional[str]) -> list[dict]:
    issues = []
    rtp = pkg.get("engineStrict")
    npmrc_ok = npmrc_content and "engine-strict=true" in npmrc_content
    if npmrc_ok:
        issues.append({"setting": "engine-strict (.npmrc)", "status": "ok", "detail": "engine-strict=true set in project .npmrc"})
    else:
        issues.append({"setting": "engine-strict", "status": "missing", "detail": "Add engine-strict=true to project .npmrc to enforce engines field"})
    return issues


def check_package_manager(pkg: dict) -> list[dict]:
    issues = []
    pm = pkg.get("packageManager")
    if pm:
        issues.append({"setting": "packageManager", "status": "ok", "detail": f"{pm}"})
    else:
        issues.append({"setting": "packageManager", "status": "missing", "detail": "Add packageManager field (e.g., \"pnpm@11.1.2\") for Corepack enforcement"})
    return issues


def check_overrides(pkg: dict) -> list[dict]:
    issues = []
    npm_overrides = pkg.get("overrides", {})
    pnpm_overrides = pkg.get("pnpm", {}).get("overrides", {})
    if npm_overrides or pnpm_overrides:
        count = len(npm_overrides) + len(pnpm_overrides)
        issues.append({"setting": "overrides", "status": "ok", "detail": f"{count} override(s) configured ({len(npm_overrides)} npm, {len(pnpm_overrides)} pnpm)"})
    else:
        issues.append({"setting": "overrides", "status": "missing", "detail": "No overrides configured. Add overrides to pin transitive deps with CVEs."})
    return issues


def check_pnpm_advanced(pkg: dict) -> list[dict]:
    issues = []
    pnpm = pkg.get("pnpm", {})
    allowed = pnpm.get("allowedVersions", {})
    never_built = pnpm.get("neverBuiltDependencies", [])

    if allowed:
        issues.append({"setting": "pnpm.allowedVersions", "status": "ok", "detail": f"{len(allowed)} package(s) restricted"})
    else:
        issues.append({"setting": "pnpm.allowedVersions", "status": "skipped", "detail": "Not configured (optional — restricts specific packages to version ranges)"})

    if never_built:
        issues.append({"setting": "pnpm.neverBuiltDependencies", "status": "ok", "detail": f"{len(never_built)} package(s) blocked from build scripts"})
    else:
        issues.append({"setting": "pnpm.neverBuiltDependencies", "status": "skipped", "detail": "Not configured (optional — blocks specific packages from ever running scripts)"})

    return issues


def check_trusted_deps(pkg: dict) -> list[dict]:
    issues = []
    trusted = pkg.get("trustedDependencies", [])
    if trusted:
        issues.append({"setting": "trustedDependencies (bun)", "status": "ok", "detail": f"{len(trusted)} trusted package(s) configured"})
    else:
        issues.append({"setting": "trustedDependencies (bun)", "status": "skipped", "detail": "Not configured (optional — bun's script allowlist equivalent to onlyBuiltDependencies)"})
    return issues


def check_npm_audit():
    issues = []
    print()
    print("  Running npm audit...")
    import subprocess
    result = subprocess.run([sys.executable, "-m", "pip", "--version"], capture_output=True, text=True)
    result2 = subprocess.run(["npm", "audit", "--audit-level=high"], capture_output=True, text=True)
    rc = result2.returncode
    if rc == 0:
        issues.append({"setting": "npm audit (high+)", "status": "ok", "detail": "No high/critical vulnerabilities found"})
    else:
        out = result2.stdout.strip() or result2.stderr.strip()
        issues.append({"setting": "npm audit (high+)", "status": "warning", "detail": f"Vulnerabilities found (exit {rc}). Run: npm audit"})
    return issues


def main():
    parser = argparse.ArgumentParser(description="Audit project-level supply chain security settings")
    parser.add_argument("--dir", default=".", help="Project directory (default: CWD)")
    parser.add_argument("--no-audit", action="store_true", help="Skip npm audit run")
    args = parser.parse_args()

    base = Path(args.dir).resolve()
    if not base.is_dir():
        print(f"Error: {base} is not a directory")
        sys.exit(1)

    pkg_path = base / "package.json"
    pkg = load_package_json(pkg_path)

    print("=== Project Supply Chain Security Audit ===")
    print()

    if not pkg:
        print("  ❌ package.json not found")
        sys.exit(1)

    npmrc_content = None
    npmrc_path = base / ".npmrc"
    if npmrc_path.exists():
        npmrc_content = npmrc_path.read_text()

    passed = 0
    failed = 0
    warnings = 0

    checks = [
        ("engines", lambda: check_engines(pkg)),
        ("engine-strict", lambda: check_engine_strict(pkg, npmrc_content)),
        ("packageManager", lambda: check_package_manager(pkg)),
        ("overrides", lambda: check_overrides(pkg)),
        ("pnpm advanced", lambda: check_pnpm_advanced(pkg)),
        ("trustedDependencies", lambda: check_trusted_deps(pkg)),
    ]

    for label, fn in checks:
        print(f"--- {label} ---")
        results = fn()
        for r in results:
            icon = {"ok": "  ✅", "missing": "  ❌", "skipped": "  ⚠️", "warning": "  ⚠️"}.get(r["status"], "  ❓")
            print(f"{icon} {r['setting']}: {r['detail']}")
            if r["status"] == "missing":
                failed += 1
            elif r["status"] == "ok":
                passed += 1
            elif r["status"] == "skipped":
                passed += 1
            elif r["status"] == "warning":
                warnings += 1
        print()

    if not args.no_audit:
        print("--- npm audit ---")
        audit_results = check_npm_audit()
        for r in audit_results:
            icon = {"ok": "  ✅", "warning": "  ⚠️"}.get(r["status"], "  ❓")
            print(f"{icon} {r['setting']}: {r['detail']}")
            if r["status"] == "warning":
                warnings += 1
        print()

    print(f"=== Results: {passed} OK, {failed} issues, {warnings} warnings ===")
    print()

    if failed > 0:
        print("Fix the missing settings above and re-run.")
        sys.exit(1)

    if warnings > 0:
        print("All required settings are configured. Review warnings for optional improvements.")
        sys.exit(0)

    print("All project security settings are properly configured.")
    sys.exit(0)


if __name__ == "__main__":
    import argparse
    main()
