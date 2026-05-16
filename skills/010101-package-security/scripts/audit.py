#!/usr/bin/env python3
"""audit.py — Check that npm, pnpm, and bun security settings are active."""

import argparse
import os
import sys
from pathlib import Path


def check_npmrc() -> list[dict]:
    issues = []
    path = Path.home() / ".npmrc"

    if not path.exists():
        issues.append({"setting": "~/.npmrc", "status": "missing", "detail": "File does not exist"})
        return issues

    content = path.read_text()
    checks = {
        "min-release-age": ("min-release-age", "Cooldown period not set. Add: min-release-age=1"),
        "ignore-scripts": ("ignore-scripts=true", "Scripts not blocked. Add: ignore-scripts=true"),
        "save-exact": ("save-exact=true", "Exact version pinning not set. Add: save-exact=true"),
        "audit-level": ("audit-level=", "Audit severity threshold not set. Add: audit-level=high"),
    }

    for key, (expected, advice) in checks.items():
        if expected not in content:
            issues.append({"setting": f"npmrc: {key}", "status": "missing", "detail": advice})

    scope_registries = [l for l in content.splitlines() if "@" in l and ":registry=" in l]
    if not scope_registries:
        issues.append({"setting": "npmrc: scoped registries", "status": "skipped", "detail": "No scoped registries configured (@scope:registry=...) — recommended for private packages to prevent dependency confusion"})

    return issues


def check_pnpm_config() -> list[dict]:
    issues = []
    home = Path.home()
    candidates = [
        home / "Library/Preferences/pnpm/config.yaml",       # macOS
        home / ".config/pnpm/rc",                             # Linux
        Path(os.environ.get("APPDATA", "")) / "pnpm/config.yaml",  # Windows
    ]

    path = None
    for c in candidates:
        if c.exists():
            path = c
            break

    if not path:
        issues.append({"setting": "pnpm config", "status": "missing", "detail": "Config file not found — expected at ~/Library/Preferences/pnpm/config.yaml (macOS), ~/.config/pnpm/rc (Linux), or %APPDATA%/pnpm/config.yaml (Windows)"})
        return issues

    content = path.read_text()

    if "minimumReleaseAge: 1440" not in content and "minimumReleaseAge:" not in content:
        issues.append({"setting": "pnpm: minimumReleaseAge", "status": "missing", "detail": "Add: minimumReleaseAge: 1440 (24h cooldown, in minutes)"})

    if "ignoreScripts: true" not in content:
        issues.append({"setting": "pnpm: ignoreScripts", "status": "missing", "detail": "Add: ignoreScripts: true"})

    return issues


def check_pnpm_workspace() -> list[dict]:
    issues = []
    path = Path.cwd() / "pnpm-workspace.yaml"

    if not path.exists():
        issues.append({"setting": "pnpm: blockExoticSubdeps", "status": "skipped", "detail": "pnpm-workspace.yaml not found (run this script from your project root)"})
        return issues

    content = path.read_text()
    if "blockExoticSubdeps: true" not in content:
        issues.append({"setting": "pnpm: blockExoticSubdeps", "status": "missing", "detail": "Add in pnpm-workspace.yaml: blockExoticSubdeps: true"})

    return issues


def check_project_npmrc() -> list[dict]:
    issues = []
    path = Path.cwd() / ".npmrc"

    if not path.exists():
        return issues

    content = path.read_text()
    if "engine-strict=true" not in content:
        issues.append({"setting": "project .npmrc: engine-strict", "status": "missing", "detail": "Add in project .npmrc: engine-strict=true (fails install if Node version doesn't match engines)"})

    return issues


def check_bunfig() -> list[dict]:
    issues = []
    home = Path.home()
    candidates = [
        home / ".bunfig.toml",                                              # Unix
        Path(os.environ.get("APPDATA", "")) / "bun/.bunfig.toml",           # Windows
    ]
    path = None
    for c in candidates:
        if c.exists():
            path = c
            break

    if not path:
        issues.append({"setting": "bunfig", "status": "missing", "detail": "File does not exist — expected at ~/.bunfig.toml (Unix) or %APPDATA%/bun/.bunfig.toml (Windows)"})
        return issues

    content = path.read_text()

    if "minimumReleaseAge" not in content:
        issues.append({"setting": "bun: minimumReleaseAge", "status": "missing", "detail": "Add: minimumReleaseAge = 86400 (24h cooldown, in seconds)"})

    return issues


def parse_args():
    parser = argparse.ArgumentParser(
        description="Check that npm, pnpm, and bun security settings are active."
    )
    parser.add_argument(
        "--dir",
        default=".",
        help="Project directory to check for pnpm-workspace.yaml and project .npmrc (default: current dir)",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    passed = 0
    failed = 0

    print("=== Package Manager Security Audit ===")
    print()

    for label, fn in [("npm (.npmrc)", check_npmrc), ("pnpm (global config)", check_pnpm_config), ("pnpm (workspace)", check_pnpm_workspace), ("project .npmrc", check_project_npmrc), ("bun (bunfig)", check_bunfig)]:
        print(f"--- {label} ---")
        issues = fn()
        if not issues:
            print("  ✅ All settings found")
            passed += 1
        else:
            for issue in issues:
                icon = "  ⚠️" if issue["status"] == "skipped" else "  ❌"
                print(f"{icon} {issue['setting']}: {issue['detail']}")
                if issue["status"] != "skipped":
                    failed += 1
                else:
                    passed += 1
        print()

    print(f"=== Results: {passed} OK, {failed} issues ===")
    print()
    print("Summary of recommended security settings:")
    print("  npm:   min-release-age=1, ignore-scripts=true, save-exact=true, audit-level=high")
    print("  pnpm:  minimumReleaseAge: 1440, ignoreScripts: true, blockExoticSubdeps: true")
    print("  bun:   minimumReleaseAge = 86400")
    print()
    print("For deeper analysis, run: python scripts/scan-exotic.py")
    print("  Project checks: python scripts/audit-project.py")
    print()

    if failed > 0:
        print("Some security settings are missing. Fix them and run this script again.")
        sys.exit(1)
    else:
        print("All security settings are properly configured.")
        sys.exit(0)


if __name__ == "__main__":
    main()
