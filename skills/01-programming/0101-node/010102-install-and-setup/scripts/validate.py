#!/usr/bin/env python3
"""validate.py — Check that npm, pnpm, and bun are installed and PATH is correct."""

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path


def get_version(exe: str) -> str:
    try:
        result = subprocess.run(
            [exe, "--version"], capture_output=True, text=True, timeout=10
        )
        return result.stdout.strip() or result.stderr.strip() or "unknown"
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return "unknown"


def check(name: str, exe: str) -> tuple[int, int]:
    path = shutil.which(exe)
    if path:
        version = get_version(exe)
        print(f"  \u2705 {name}: {version} (at {path})")
        return 1, 0
    else:
        print(f"  \u274c {name}: NOT FOUND")
        return 0, 1


def parse_args():
    parser = argparse.ArgumentParser(
        description="Check that npm, pnpm, and bun are installed and PATH is correct."
    )
    parser.add_argument(
        "--dir",
        default=".",
        help="Directory with Node.js installation to check (default: current dir)",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    passed = 0
    failed = 0

    print("=== Package Manager Validation ===")
    print()

    print("--- Tool Installation ---")
    p, f = check("node", "node")
    passed += p; failed += f
    p, f = check("npm", "npm")
    passed += p; failed += f

    pnpm = shutil.which("pnpm")
    if pnpm:
        p, f = check("pnpm", "pnpm")
        passed += p; failed += f
    else:
        print("  \u274c pnpm: NOT FOUND")
        print("     Try: npm install -g pnpm")
        print("     Then: pnpm setup")
        failed += 1

    bun = shutil.which("bun")
    if bun:
        p, f = check("bun", "bun")
        passed += p; failed += f
    else:
        print("  \u26a0\ufe0f  bun: NOT FOUND (optional, only needed if you use bun)")
        print("     Try: pnpm add -g bun")

    print()
    print("--- PATH Check ---")
    path_env = os.environ.get("PATH", "")
    global_bin_dirs = []

    if sys.platform == "win32":
        appdata = os.environ.get("APPDATA", "")
        global_bin_dirs = [
            Path(appdata) / "pnpm",
        ]
        path_advice = "Add to PATH: set PATH=%s;%%PATH%%"
    else:
        home = Path.home()
        global_bin_dirs = [
            home / "Library/pnpm/bin",
            home / ".bun/bin",
        ]
        path_advice = "Add to shell config: export PATH=\"%s:$PATH\""

    for d in global_bin_dirs:
        dirpath = str(d)
        if dirpath.lower() in [p.lower() for p in path_env.split(os.pathsep)]:
            print(f"  \u2705 {dirpath} is in PATH")
        else:
            print(f"  \u26a0\ufe0f  {dirpath} is NOT in PATH")
            print(f"     {path_advice % dirpath}")

    print()
    print(f"=== Results: {passed} found, {failed} missing ===")

    if failed > 0:
        print("Some tools are missing. Run 'python scripts/validate.py' after installing.")
        sys.exit(1)
    else:
        print("All required tools are installed and PATH is configured correctly.")
        sys.exit(0)


if __name__ == "__main__":
    main()
