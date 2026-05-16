#!/usr/bin/env python3
"""validate.py — Check package manager environment and operations."""

import argparse
import subprocess
import sys


def check_tool(name: str, version_flag: str = "--version") -> tuple[bool, str]:
    try:
        result = subprocess.run([name, version_flag], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            return True, result.stdout.strip().split("\n")[0]
        return False, result.stderr.strip()
    except FileNotFoundError:
        return False, "not found"
    except Exception as e:
        return False, str(e)


def cmd_install():
    tools = [("npm", "npm"), ("pnpm", "pnpm"), ("bun", "bun")]
    print("=== Package Manager Status ===")
    print()
    all_ok = True
    for name, cmd in tools:
        ok, ver = check_tool(cmd)
        status = f"  ✅ {name}: {ver}" if ok else f"  ❌ {name}: {ver}"
        print(status)
        if not ok:
            all_ok = False
    print()
    if all_ok:
        print("All package managers available.")
    else:
        print("Some tools are missing — install via install-and-setup skill.")
    return all_ok


def cmd_outdated():
    for pm in ["npm", "pnpm", "bun"]:
        ok, _ = check_tool(pm)
        if not ok:
            continue
        print(f"--- {pm} outdated ---")
        try:
            result = subprocess.run([pm, "outdated"], capture_output=True, text=True, timeout=30)
            out = result.stdout.strip() or result.stderr.strip() or "All packages up to date"
            print(f"  {out}")
        except Exception as e:
            print(f"  Error: {e}")
        print()
    return True


def cmd_audit():
    for pm, audit_cmd in [("npm", ["npm", "audit", "--audit-level=high"]), ("pnpm", ["pnpm", "audit"])]:
        ok, _ = check_tool(pm)
        if not ok:
            continue
        print(f"--- {pm} audit ---")
        try:
            result = subprocess.run(audit_cmd, capture_output=True, text=True, timeout=60)
            out = result.stdout.strip() or result.stderr.strip()
            if result.returncode == 0:
                print("  ✅ No vulnerabilities found")
            else:
                print(f"  ⚠️ Vulnerabilities found (exit {result.returncode})")
                print(f"  {out.split(chr(10))[0]}")
        except Exception as e:
            print(f"  Error: {e}")
        print()
    return True


def cmd_publish():
    print("=== Publish Checklist ===")
    print()
    checks = [
        ("package.json has version", lambda: _check_package_json("version")),
        ("package.json has name", lambda: _check_package_json("name")),
        ("Lockfile committed", _check_lockfile),
    ]
    all_ok = True
    for label, fn in checks:
        ok, detail = fn()
        icon = "✅" if ok else "❌"
        print(f"  {icon} {label}: {detail}")
        if not ok:
            all_ok = False
    print()
    if all_ok:
        print("Ready to publish.")
    else:
        print("Fix issues above before publishing.")
    return all_ok


def _check_package_json(field: str) -> tuple[bool, str]:
    import json
    from pathlib import Path
    pkg = Path.cwd() / "package.json"
    if not pkg.exists():
        return False, "package.json not found"
    try:
        data = json.loads(pkg.read_text())
        val = data.get(field)
        if val:
            return True, val
        return False, f"No '{field}' field"
    except json.JSONDecodeError:
        return False, "Invalid JSON"


def _check_lockfile() -> tuple[bool, str]:
    from pathlib import Path
    for lf in ["package-lock.json", "pnpm-lock.yaml", "bun.lock", "bun.lockb"]:
        if (Path.cwd() / lf).exists():
            return True, f"{lf} found"
    return False, "No lockfile found"


def cmd_doctor():
    for pm in ["npm", "pnpm"]:
        ok, _ = check_tool(pm)
        if not ok:
            continue
        print(f"--- {pm} doctor ---")
        try:
            result = subprocess.run([pm, "doctor"], capture_output=True, text=True, timeout=30)
            out = result.stdout.strip() or result.stderr.strip()
            for line in out.split("\n")[:10]:
                print(f"  {line}")
        except Exception as e:
            print(f"  Error: {e}")
        print()
    return True


def main():
    parser = argparse.ArgumentParser(description="Check package manager environment")
    parser.add_argument("command", nargs="?", default="install", choices=["install", "outdated", "audit", "publish", "doctor"],
                        help="Operation to check (default: install)")
    args = parser.parse_args()

    commands = {
        "install": cmd_install,
        "outdated": cmd_outdated,
        "audit": cmd_audit,
        "publish": cmd_publish,
        "doctor": cmd_doctor,
    }

    ok = commands[args.command]()
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
