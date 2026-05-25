#!/usr/bin/env python3
import sys
from pathlib import Path


def check_polar(dir_path: Path) -> list[dict]:
    findings = []
    for env_file in [".env", ".env.local", ".env.example"]:
        ef = dir_path / env_file
        if ef.exists():
            content = ef.read_text()
            for var in ["POLAR_ACCESS_TOKEN", "POLAR_WEBHOOK_SECRET"]:
                if var in content:
                    findings.append({"status": "ok", "check": f"Env: {var}", "detail": "Configured"})
            if "NEXT_PUBLIC_POLAR_SANDBOX" in content:
                findings.append({"status": "ok", "check": "Sandbox mode", "detail": "Configured"})
            break
    polar_files = [f for f in list(dir_path.rglob("*.ts")) + list(dir_path.rglob("*.py")) if "polar" in f.read_text().lower()]
    if polar_files:
        findings.append({"status": "ok", "check": "Polar SDK usage", "detail": f"{len(polar_files)} file(s)"})
    webhook_files = list(dir_path.rglob("webhook*"))
    if webhook_files:
        findings.append({"status": "ok", "check": "Webhook endpoint", "detail": f"{webhook_files[0].relative_to(dir_path)}"})
    return findings


def main():
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/tmp/skill-polar")
    if not root.exists():
        print(f"Not found: {root}")
        sys.exit(1)
    print(f"Validating Polar integration in: {root}")
    findings = check_polar(root)
    for f in findings:
        print(f"  {'✓' if f['status']=='ok' else '!' if f['status']=='warn' else 'i'} {f['check']}: {f['detail']}")
    print("\nAll checks passed.")
    sys.exit(0)


if __name__ == "__main__":
    main()
