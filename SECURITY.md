# Security Policy

## Supply-Chain & Hygiene Controls

This repository enforces automated defense-in-depth across local hooks and GitHub Actions:

1. **Three-Day Dependency Cooldown**: `cargo --config 'resolver.min-publish-age="3 days"'` and the cooldown gate in `crates/xtask/src/main.rs` prevent immediate adoption of newly published or compromised crate versions.
2. **Static Analysis (CodeQL)**: `.github/workflows/security.yml` runs GitHub CodeQL analysis for Rust on every push, pull request, and weekly schedule.
3. **Dependency Audit & SBOM**: `cargo metadata` inventories are exported as CI build artifacts on every security run.
4. **Anti-Leak Hygiene Gate**: `crates/xtask/src/hygiene.rs` blocks hardcoded user paths, restricted tokens, and oversized files before code can be pushed.

## Reporting a Vulnerability

Please report suspected security issues privately using GitHub Security Advisories for this repository rather than opening public issues.
