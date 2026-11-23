# AGENTS.md

Technical operating rules for this Rust repository.

## 1. Repository Scope

- Installable agent skill definitions (`SKILL.md`) and native Rust CLI utilities (`skills-core`).
- Pure-Cargo workspace (`crates/core` library + `crates/xtask` automation runner); no Node.js or Python runtime tooling (`package.json`, `pnpm-lock.yaml`, `husky`, `.prettierrc` are forbidden).

## 2. Toolchain & Validation

- Minimum Supported Rust Version (MSRV): **`rust-version = "1.85"`** (Rust 2024 edition).
- Enable hooks locally with `git config core.hooksPath .githooks` and run `cargo xtask validate` (`TOTAL PASS=8 FAIL=0`) before opening or updating any pull request.
- Clippy policy (`[workspace.lints]` in `Cargo.toml` and `clippy.toml` with `max-fn-params-bools = 0`) is enforced via `cargo clippy --workspace --all-targets --all-features -- -D warnings`; rustdoc policy (`[workspace.lints.rustdoc]`) via `RUSTDOCFLAGS="-D warnings" cargo doc --workspace --no-deps --all-features`, and every public item carries a runnable doc example (`cargo test --workspace --doc`). `unsafe_code = "forbid"` must never be weakened to `warn` or `allow`; immutable policy and public-API trait contracts (`Send + Sync`, `Debug`, `Error`, `#[non_exhaustive]`) live in `crates/core/tests/architecture.rs`.
- Do not run `cargo fmt` or automated code formatters in hooks, CI, or pre-commit steps.

## 3. Code Layout & Architecture

- Organize domain logic under `crates/core/src/modules/<domain>/` as a six-file layered modular layout (`entity.rs`, `dto.rs`, `repository.rs`, `service.rs`, `controller.rs`, `mod.rs`).
- Enforce unidirectional imports: `controller` calls `service` and `dto` (never `repository`); `entity` and `dto` must not import `service`, `repository`, or `controller`.
- Keep sibling constellations completely decoupled: never add another constellation crate to `Cargo.toml`; communicate strictly over wire protocols (REST, WebSocket/WSS, gRPC).
- Keep every source and documentation file at or below **500 lines**.

## 4. Commit, Dependency & License Policy

- Set Git Author and Committer identically to the repository maintainer account using a GitHub noreply email.
- Format commits as `type(scope): description` (3 to 6 lowercase words, no trailing period, max 100 chars), a single blank line, and 3+ consecutive `- **Label**: text` bullets (3 to 10 words each) without trailers.
- External dependencies must pass the 3-day publish-age cooldown (`resolver.min-publish-age="3 days"`); run `cargo xtask notices` after dependency edits and keep `.env.example` restricted to non-secret placeholders.
- Code and documentation are released under the Apache License 2.0 (`Copyright (c) 2026 Natuleadan`).
