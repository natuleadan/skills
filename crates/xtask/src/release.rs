//! Native semantic version planner, `RELEASE_NOTES` generator, and CHANGELOG verifier.

use std::fmt::Write as _;
use std::fs;
use std::path::Path;
use std::process::Command;

#[derive(Clone, Copy, PartialEq, Eq)]
pub(crate) enum ReleaseMode {
    Status,
    Check,
    Apply,
}

#[derive(Clone, Copy, PartialEq, Eq)]
enum Bump {
    Major,
    Minor,
    Patch,
}

pub(crate) fn run(root: &Path, mode: ReleaseMode, notes_out: Option<&Path>) -> bool {
    let cargo_toml_path = root.join("Cargo.toml");
    let Ok(cargo_toml) = fs::read_to_string(&cargo_toml_path) else {
        println!("FAIL release: cannot read Cargo.toml");
        return false;
    };
    let Some(current_ver) = extract_version(&cargo_toml) else {
        println!("FAIL release: cannot find workspace version in Cargo.toml");
        return false;
    };

    let last_tag = latest_v_tag(root);
    let commits = commits_since(root, last_tag.as_deref());
    if let Some(out_path) = notes_out {
        let notes = build_release_notes(&current_ver, &commits);
        if fs::write(out_path, notes).is_err() {
            println!("FAIL release: cannot write release notes");
            return false;
        }
        println!("PASS release: wrote notes to {}", out_path.display());
        return true;
    }

    let bump = compute_bump(&commits);
    let expected = if let Some(ref tag) = last_tag {
        let base = tag.strip_prefix('v').unwrap_or(tag);
        match bump {
            Some(b) => next_version(base, b),
            None => base.to_string(),
        }
    } else {
        current_ver.clone()
    };

    let changelog_path = root.join("CHANGELOG.md");
    let changelog = fs::read_to_string(&changelog_path).unwrap_or_default();

    if mode == ReleaseMode::Apply && expected != current_ver {
        let updated_toml = cargo_toml.replacen(
            &format!("version = \"{current_ver}\""),
            &format!("version = \"{expected}\""),
            1,
        );
        if fs::write(&cargo_toml_path, updated_toml).is_err() {
            println!("FAIL release: failed to update Cargo.toml");
            return false;
        }
        let mut bullets = String::new();
        for c in commits.iter().filter(|c| !c.starts_with("Merge ")) {
            let _ = writeln!(bullets, "- {c}");
        }
        let body = if bullets.is_empty() {
            "- Automated release preparation.\n".to_string()
        } else {
            bullets
        };
        let section = format!("## {expected}\n\n{body}\n");
        let updated_log = if changelog.contains(&format!("## {expected}")) {
            changelog
        } else {
            format!(
                "# Changelog\n\n{section}{}",
                changelog.trim_start_matches("# Changelog\n\n")
            )
        };
        if fs::write(&changelog_path, updated_log).is_err() {
            println!("FAIL release: failed to update CHANGELOG.md");
            return false;
        }
        let _ = Command::new("cargo")
            .args(["generate-lockfile", "--offline"])
            .current_dir(root)
            .output();
        println!("PASS release: prepared {expected}");
        return true;
    }

    if mode == ReleaseMode::Check {
        if current_ver != expected {
            println!("FAIL release: Cargo.toml version {current_ver} != expected {expected}");
            return false;
        }
        if !changelog.contains(&format!("## {current_ver}")) {
            println!("FAIL release: CHANGELOG.md missing section '## {current_ver}'");
            return false;
        }
        println!("PASS release ({current_ver})");
        return true;
    }

    println!("PASS release: current={current_ver} expected={expected}");
    true
}

fn build_release_notes(version: &str, commits: &[String]) -> String {
    let mut notes = format!("# Release v{version}\n\n");
    for kind in ["feat", "fix", "perf", "refactor", "docs", "ci", "chore", "upgrade"] {
        let items: Vec<&String> = commits
            .iter()
            .filter(|c| c.starts_with(&format!("{kind}(")))
            .collect();
        if !items.is_empty() {
            let _ = write!(notes, "## {kind}\n\n");
            for item in items {
                let _ = writeln!(notes, "- {item}");
            }
            notes.push('\n');
        }
    }
    notes
}

fn extract_version(toml: &str) -> Option<String> {
    for line in toml.lines() {
        let trimmed = line.trim();
        if let Some(rest) = trimmed.strip_prefix("version = \"")
            && let Some(ver) = rest.strip_suffix('"')
        {
            return Some(ver.to_string());
        }
    }
    None
}

fn latest_v_tag(root: &Path) -> Option<String> {
    let out = Command::new("git")
        .args(["describe", "--tags", "--abbrev=0", "--match", "v[0-9]*"])
        .current_dir(root)
        .output()
        .ok()?;
    if !out.status.success() {
        return None;
    }
    let tag = String::from_utf8_lossy(&out.stdout).trim().to_string();
    if tag.is_empty() { None } else { Some(tag) }
}

fn commits_since(root: &Path, tag: Option<&str>) -> Vec<String> {
    let range = tag.map_or_else(|| "HEAD".to_string(), |t| format!("{t}..HEAD"));
    let Ok(out) = Command::new("git")
        .args(["log", &range, "--format=%s"])
        .current_dir(root)
        .output()
    else {
        return Vec::new();
    };
    String::from_utf8_lossy(&out.stdout)
        .lines()
        .map(str::to_string)
        .collect()
}

fn compute_bump(subjects: &[String]) -> Option<Bump> {
    if subjects
        .iter()
        .any(|s| s.starts_with("upgrade(") || s.contains("!:"))
    {
        return Some(Bump::Major);
    }
    if subjects.iter().any(|s| s.starts_with("feat(")) {
        return Some(Bump::Minor);
    }
    if subjects
        .iter()
        .any(|s| s.starts_with("fix(") || s.starts_with("perf(") || s.starts_with("revert("))
    {
        return Some(Bump::Patch);
    }
    None
}

fn next_version(base: &str, bump: Bump) -> String {
    let parts: Vec<u64> = base.split('.').filter_map(|p| p.parse().ok()).collect();
    if parts.len() != 3 {
        return base.to_string();
    }
    match bump {
        Bump::Major => format!("{}.0.0", parts[0] + 1),
        Bump::Minor => format!("{}.{}.0", parts[0], parts[1] + 1),
        Bump::Patch => format!("{}.{}.{}", parts[0], parts[1], parts[2] + 1),
    }
}
