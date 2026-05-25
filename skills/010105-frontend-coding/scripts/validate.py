#!/usr/bin/env python3
"""Validate frontend coding standards in a project."""
import sys
from pathlib import Path


def check_frontend(dir_path: Path) -> list[dict]:
    findings = []

    src = dir_path / "src"

    # Check for "use client" usage patterns
    tsx_files = list(dir_path.rglob("*.tsx"))
    if tsx_files:
        findings.append({"status": "ok", "check": "React components (.tsx)", "detail": f"{len(tsx_files)} file(s)"})

    # Check for accessibility attributes
    a11y_count = 0
    for f in tsx_files:
        content = f.read_text()
        if "aria-" in content:
            a11y_count += 1
        if "role=" in content:
            a11y_count += 1
    if a11y_count > 0:
        findings.append({"status": "ok", "check": "Accessibility attributes (aria-*, role)", "detail": f"Found in files"})
    else:
        findings.append({"status": "info", "check": "Accessibility attributes", "detail": "None detected"})

    # Check for semantic HTML
    semantic_count = 0
    for f in tsx_files:
        content = f.read_text()
        for tag in ["<button", "<nav", "<main", "<header", "<footer", "<section", "<article"]:
            if tag in content:
                semantic_count += 1
                break
    if semantic_count > 0:
        findings.append({"status": "ok", "check": "Semantic HTML elements", "detail": "Found"})

    # Check for lazy loading
    lazy_count = 0
    for f in tsx_files:
        content = f.read_text()
        if "loading=" in content or "next/dynamic" in content or "lazy" in content:
            lazy_count += 1
    if lazy_count > 0:
        findings.append({"status": "ok", "check": "Lazy loading patterns", "detail": "Found"})

    # Check for keys in lists
    key_warn = 0
    for f in tsx_files:
        content = f.read_text()
        if ".map(" in content and "key=" not in content:
            key_warn += 1
    if key_warn > 0:
        findings.append({"status": "warn", "check": ".map() without key prop", "detail": f"Potential issue in {key_warn} file(s)"})
    else:
        findings.append({"status": "ok", "check": "List keys in .map()", "detail": "No violations detected"})

    return findings


def main():
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/tmp/skill-fd")
    if not root.exists():
        print(f"Directory not found: {root}")
        sys.exit(1)

    print(f"Validating frontend coding standards in: {root}")
    findings = check_frontend(root)
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
