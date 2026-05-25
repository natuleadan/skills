#!/usr/bin/env python3
"""Validate release automation configuration in a project."""
import sys
import json
from pathlib import Path


def check_release_config(dir_path: Path) -> list[dict]:
    findings = []

    # Check .releaserc.json
    rc = dir_path / ".releaserc.json"
    if rc.exists():
        findings.append({"status": "ok", "check": ".releaserc.json", "detail": "Found"})
        try:
            data = json.loads(rc.read_text())
            plugins = data.get("plugins", [])
            plugin_names = [p[0] if isinstance(p, list) else p for p in plugins]
            for name in ["@semantic-release/commit-analyzer", "@semantic-release/release-notes-generator",
                         "@semantic-release/changelog", "@semantic-release/github"]:
                if any(name in p for p in plugin_names):
                    findings.append({"status": "ok", "check": f"  Plugin: {name}", "detail": "Configured"})
        except json.JSONDecodeError:
            findings.append({"status": "warn", "check": "  JSON syntax", "detail": "Invalid"})
    else:
        findings.append({"status": "info", "check": ".releaserc.json", "detail": "Not found"})

    # Check GitHub Actions workflow
    workflows_dir = dir_path / ".github" / "workflows"
    if workflows_dir.is_dir():
        wf_files = list(workflows_dir.glob("*.yml")) + list(workflows_dir.glob("*.yaml"))
        if wf_files:
            findings.append({"status": "ok", "check": "CI workflow files", "detail": f"{len(wf_files)} found"})
            for wf in wf_files:
                content = wf.read_text()
                if "semantic-release" in content:
                    findings.append({"status": "ok", "check": f"  {wf.name}: semantic-release", "detail": "Found"})
    else:
        findings.append({"status": "info", "check": "CI workflows", "detail": "No .github/workflows/ directory"})

    # Check commitlint config
    for cfg in ["commitlint.config.js", "commitlint.config.cjs"]:
        if (dir_path / cfg).exists():
            findings.append({"status": "ok", "check": f"{cfg}", "detail": "Found"})
            break

    return findings


def main():
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/tmp/nla-release")
    if not root.exists():
        print(f"Directory not found: {root}")
        sys.exit(1)

    print(f"Validating release automation in: {root}")
    findings = check_release_config(root)
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
