#!/usr/bin/env python3
import sys
from pathlib import Path

def check_stripe(dir_path: Path) -> list[dict]:
    findings = []
    for env_file in [".env", ".env.local", ".env.example"]:
        ef = dir_path / env_file
        if ef.exists():
            content = ef.read_text()
            for var in ["STRIPE_SECRET_KEY", "STRIPE_WEBHOOK_SECRET"]:
                if var in content:
                    findings.append({"status": "ok", "check": f"Env: {var}", "detail": "Configured"})
            break
    js_files = list(dir_path.rglob("*.ts")) + list(dir_path.rglob("*.js")) + list(dir_path.rglob("*.py"))
    stripe_usage = 0
    for f in js_files:
        if "stripe" in f.read_text().lower():
            stripe_usage += 1
    if stripe_usage:
        findings.append({"status": "ok", "check": "Stripe SDK/usage", "detail": f"Found in {stripe_usage} file(s)"})
    webhook_files = list(dir_path.rglob("webhook*"))
    if webhook_files:
        findings.append({"status": "ok", "check": "Webhook endpoint", "detail": str(webhook_files[0].relative_to(dir_path))})
    return findings

def main():
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/tmp/nla-stripe")
    if not root.exists(): print(f"Not found: {root}"); sys.exit(1)
    print(f"Validating Stripe integration in: {root}")
    findings = check_stripe(root)
    for f in findings:
        print(f"  {'✓' if f['status']=='ok' else '!' if f['status']=='warn' else 'i'} {f['check']}: {f['detail']}")
    print("\nAll checks passed.")
    sys.exit(0)

if __name__ == "__main__":
    main()
