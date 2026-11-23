//! Pure Rust repository automation and validation runner.

#![expect(clippy::print_stdout, reason = "xtask CLI prints gate validation output to stdout")]
#![expect(clippy::print_stderr, reason = "xtask CLI prints diagnostic errors to stderr")]

mod commit;
mod hygiene;
mod notices;
mod release;

use notices::NoticesMode;
use release::ReleaseMode;

use std::env;
use std::path::{Path, PathBuf};
use std::process::{Command, ExitCode};

/// One external command executed as part of a validation gate.
struct Step<'a> {
    cmd: &'a str,
    args: &'a [&'a str],
    envs: &'a [(&'a str, &'a str)],
}

fn repo_root() -> PathBuf {
    let manifest_dir = env!("CARGO_MANIFEST_DIR");
    PathBuf::from(manifest_dir)
        .parent()
        .and_then(|p| p.parent())
        .map_or_else(|| PathBuf::from("."), PathBuf::from)
}

fn run_gate(name: &str, steps: &[Step<'_>], root: &Path) -> bool {
    for step in steps {
        let out = Command::new(step.cmd)
            .args(step.args)
            .envs(step.envs.iter().copied())
            .current_dir(root)
            .output();
        match out {
            Ok(res) if res.status.success() => {}
            Ok(res) => {
                println!("FAIL {name}");
                let stderr = String::from_utf8_lossy(&res.stderr);
                let stdout = String::from_utf8_lossy(&res.stdout);
                if !stdout.trim().is_empty() {
                    println!("{}", stdout.trim());
                }
                if !stderr.trim().is_empty() {
                    println!("{}", stderr.trim());
                }
                return false;
            }
            Err(err) => {
                println!("FAIL {name}: {err}");
                return false;
            }
        }
    }
    println!("PASS {name}");
    true
}

fn cmd_validate(root: &Path) -> ExitCode {
    let checks = [
        run_gate(
            "lint",
            &[
                Step {
                    cmd: "cargo",
                    args: &[
                        "clippy",
                        "--workspace",
                        "--all-targets",
                        "--all-features",
                        "--",
                        "-D",
                        "warnings",
                    ],
                    envs: &[],
                },
                Step {
                    cmd: "cargo",
                    args: &["doc", "--workspace", "--no-deps", "--all-features"],
                    envs: &[("RUSTDOCFLAGS", "-D warnings")],
                },
            ],
            root,
        ),
        run_gate(
            "typecheck",
            &[Step {
                cmd: "cargo",
                args: &["check", "--workspace", "--all-targets"],
                envs: &[],
            }],
            root,
        ),
        run_gate(
            "unit tests",
            &[
                Step {
                    cmd: "cargo",
                    args: &["test", "--workspace", "--lib"],
                    envs: &[],
                },
                Step {
                    cmd: "cargo",
                    args: &["test", "--workspace", "--doc"],
                    envs: &[],
                },
            ],
            root,
        ),
        run_gate(
            "integration and architecture tests",
            &[Step {
                cmd: "cargo",
                args: &["test", "--workspace", "--test", "*"],
                envs: &[],
            }],
            root,
        ),
        run_gate(
            "cooldown",
            &[Step {
                cmd: "cargo",
                args: &[
                    "--config",
                    "resolver.min-publish-age=\"3 days\"",
                    "check",
                    "--workspace",
                ],
                envs: &[],
            }],
            root,
        ),
        hygiene::check(root),
        notices::run(root, NoticesMode::Check),
        release::run(root, ReleaseMode::Check, None),
    ];

    let passed = checks.iter().filter(|ok| **ok).count();
    let failed = checks.len() - passed;
    println!("TOTAL PASS={passed} FAIL={failed}");
    if failed == 0 {
        ExitCode::SUCCESS
    } else {
        ExitCode::FAILURE
    }
}

fn main() -> ExitCode {
    let root = repo_root();
    let args: Vec<String> = env::args().skip(1).collect();
    match args.first().map(String::as_str) {
        Some("validate") => cmd_validate(&root),
        Some("commit-check") => commit::run(&root, &args[1..]),
        Some("notices") => {
            let mode = if args.iter().any(|a| a == "--check") {
                NoticesMode::Check
            } else {
                NoticesMode::Write
            };
            if notices::run(&root, mode) {
                ExitCode::SUCCESS
            } else {
                ExitCode::FAILURE
            }
        }
        Some("release") => {
            let mode = if args.iter().any(|a| a == "--apply") {
                ReleaseMode::Apply
            } else if args.iter().any(|a| a == "--check") {
                ReleaseMode::Check
            } else {
                ReleaseMode::Status
            };
            let notes_path = args
                .windows(2)
                .find(|w| w[0] == "--notes")
                .map(|w| PathBuf::from(&w[1]));
            if release::run(&root, mode, notes_path.as_deref()) {
                ExitCode::SUCCESS
            } else {
                ExitCode::FAILURE
            }
        }
        _ => {
            eprintln!(
                "Usage: cargo xtask <validate|commit-check|notices [--check]|release [--check|--apply|--notes <path>]>"
            );
            ExitCode::FAILURE
        }
    }
}
