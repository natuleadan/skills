#!/usr/bin/env python3
"""scan-exotic.py — Scan lockfiles for dependencies from exotic sources (git repos, tarballs, local paths)."""

import argparse
import json
import re
import sys
from pathlib import Path


REGISTRY_PATTERNS = [
    r"https?://registry\.npmjs\.org/",
    r"https?://registry\.yarnpkg\.com/",
    r"https?://npm\.pkg\.github\.com/",
    r"https?://pkgs\.dev\.azure\.com/",  # Azure DevOps
    r"https?://registry\.npmmirror\.com/",
]


EXOTIC_INDICATORS = [
    "tarball:",
    "type: git",
    "type:",
    "repo:",
    "commit:",
    "link:",
    "directory:",
]


def is_registry_url(url: str) -> bool:
    return any(re.search(p, url) for p in REGISTRY_PATTERNS)


def scan_pnpm_lock(path: Path) -> list[dict]:
    findings = []
    content = path.read_text()
    lines = content.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        resolution_match = re.match(r"^\s+resolution:\s*\{", line)
        if not resolution_match:
            i += 1
            continue
        block = line
        while "}" not in block and i + 1 < len(lines):
            i += 1
            block += " " + lines[i].strip()
        pkg_name = None
        if i >= 1:
            pkg_line = lines[i - 1] if i >= 1 else ""
            pkg_match = re.match(r"^\s+/(.+?)/\d", pkg_line)
            if pkg_match:
                pkg_name = pkg_match.group(1)
        if "integrity:" in block and not any(ind in block for ind in EXOTIC_INDICATORS):
            i += 1
            continue
        tarball_match = re.search(r"tarball:\s*(https?://\S+)", block)
        url = tarball_match.group(1).rstrip(",}") if tarball_match else "(non-registry source)"
        if url != "(non-registry source)" and is_registry_url(url):
            i += 1
            continue
        version_match = re.search(r"/(\d[\d.]+)", lines[i - 1] if i >= 1 else "")
        version = version_match.group(1) if version_match else "?"
        findings.append({
            "package": pkg_name or "?",
            "version": version,
            "source": url,
            "lockfile": path.name,
        })
        i += 1
    return findings


def scan_package_lock(path: Path) -> list[dict]:
    findings = []
    data = json.loads(path.read_text())
    for key, info in data.get("packages", {}).get("", {}).items():
        if key == "":
            continue
        resolved = info.get("resolved", "")
        if resolved and not is_registry_url(resolved):
            pkg_name = info.get("name", key.split("/node_modules/")[-1] if "/node_modules/" in key else key)
            findings.append({
                "package": pkg_name,
                "version": info.get("version", "?"),
                "source": resolved,
                "lockfile": path.name,
            })
    return findings


def main():
    parser = argparse.ArgumentParser(description="Scan lockfiles for exotic dependencies")
    parser.add_argument("--dir", default=".", help="Project directory (default: CWD)")
    parser.add_argument("--ci", action="store_true", help="Exit with code 1 if exotic deps found")
    args = parser.parse_args()

    base = Path(args.dir).resolve()
    if not base.is_dir():
        print(f"Error: {base} is not a directory")
        sys.exit(1)

    print("=== Exotic Dependency Scanner ===")
    print()

    all_findings = []

    for lockfile in ["pnpm-lock.yaml", "package-lock.json"]:
        path = base / lockfile
        if not path.exists():
            print(f"--- {lockfile} ---")
            print("  ⚠️  Not found")
            print()
            continue
        print(f"--- {lockfile} ---")
        scanner = scan_pnpm_lock if lockfile == "pnpm-lock.yaml" else scan_package_lock
        findings = scanner(path)
        if not findings:
            print("  ✅ No exotic sources detected")
        else:
            for f in findings:
                print(f"  🔴 {f['package']}@{f['version']}  → {f['source']}")
            all_findings.extend(findings)
        print()

    if all_findings:
        print(f"=== Result: {len(all_findings)} exotic source(s) found ===")
        print("Review each dependency above. If legitimate, add blockExoticSubdeps and use onlyBuiltDependencies.")
        if args.ci:
            sys.exit(1)
    else:
        print("=== Result: Clean — all dependencies from standard registries ===")
        sys.exit(0)


if __name__ == "__main__":
    main()
