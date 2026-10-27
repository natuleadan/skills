#!/usr/bin/env node
// Computes the next version from conventional commits since the last tag.
//
// Usage:
//   pnpm release:plan       print the next version
//   pnpm release:prepare    write version, manifests and changelog
//   pnpm release:check      fail if the version does not match the commits
import { execFileSync } from "node:child_process";
import { readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const PACKAGE = join(ROOT, "package.json");
const CHANGELOG = join(ROOT, "CHANGELOG.md");

type Bump = "major" | "minor" | "patch";
type Commit = {
  type: string;
  scope?: string;
  subject: string;
  body: string;
  breaking: boolean;
};

function git(args: string[]): string {
  return execFileSync("git", args, { cwd: ROOT, encoding: "utf8" }).trim();
}

function lastTag(): string {
  try {
    return git(["describe", "--tags", "--abbrev=0", "--match", "v[0-9]*"]);
  } catch {
    return "v0.0.0";
  }
}

function versionParts(tag: string): [number, number, number] {
  const match = /^v?(\d+)\.(\d+)\.(\d+)$/.exec(tag);
  if (!match) throw new Error(`invalid version tag: ${tag}`);
  return [Number(match[1]), Number(match[2]), Number(match[3])];
}

function nextVersion(base: string, bump: Bump): string {
  let [major, minor, patch] = versionParts(base);
  if (bump === "major") {
    major += 1;
    minor = 0;
    patch = 0;
  } else if (bump === "minor") {
    minor += 1;
    patch = 0;
  } else {
    patch += 1;
  }
  return `${major}.${minor}.${patch}`;
}

function commitsSince(tag: string): Commit[] {
  const raw = git(["log", `${tag}..HEAD`, "--reverse", "--format=%s%x00%b%x00"]);
  if (!raw) return [];
  const parts = raw.split("\0");
  const commits: Commit[] = [];
  for (let index = 0; index + 1 < parts.length; index += 2) {
    const subject = parts[index].trim();
    const body = parts[index + 1].trim();
    if (!subject || subject.startsWith("Merge ")) continue;
    const match = /^([a-z]+)(?:\(([^)]+)\))?(!)?:\s+(.+)$/.exec(subject);
    if (!match) continue;
    commits.push({
      type: match[1],
      scope: match[2],
      subject: match[4],
      body,
      breaking:
        match[3] === "!" ||
        /BREAKING[ -]CHANGE:/.test(body) ||
        match[1] === "upgrade",
    });
  }
  return commits;
}

function bumpFor(commits: Commit[]): Bump | null {
  if (commits.some((commit) => commit.breaking)) return "major";
  if (commits.some((commit) => commit.type === "feat")) return "minor";
  if (
    commits.some(
      (commit) => commit.type === "fix" || commit.type === "perf",
    )
  ) {
    return "patch";
  }
  return null;
}

function changelogEntry(version: string, commits: Commit[]): string {
  const sections: string[] = [];
  const add = (title: string, predicate: (commit: Commit) => boolean) => {
    const items = commits
      .filter(predicate)
      .map((commit) => `- ${commit.subject}`);
    if (items.length > 0) sections.push(`### ${title}\n\n${items.join("\n")}`);
  };

  add("Breaking Changes", (commit) => commit.breaking);
  add(
    "Features",
    (commit) => !commit.breaking && commit.type === "feat",
  );
  add("Fixes", (commit) => !commit.breaking && commit.type === "fix");
  add(
    "Performance",
    (commit) => !commit.breaking && commit.type === "perf",
  );
  add(
    "Documentation",
    (commit) => !commit.breaking && commit.type === "docs",
  );
  add(
    "Maintenance",
    (commit) =>
      !commit.breaking &&
      ["ci", "chore", "test", "style", "refactor", "build"].includes(
        commit.type,
      ),
  );
  add("Reverts", (commit) => !commit.breaking && commit.type === "revert");

  const known = new Set([
    "feat",
    "fix",
    "perf",
    "docs",
    "ci",
    "chore",
    "test",
    "style",
    "refactor",
    "build",
    "revert",
    "upgrade",
  ]);
  add(
    "Other",
    (commit) => !commit.breaking && !known.has(commit.type),
  );

  return `## ${version}\n\n${sections.join("\n\n")}`;
}

const tag = lastTag();
const base = tag.replace(/^v/, "");
const commits = commitsSince(tag);
const bump = bumpFor(commits);
const expected = bump ? nextVersion(base, bump) : base;
const packageJson = JSON.parse(readFileSync(PACKAGE, "utf8")) as {
  version: string;
};
const check = process.argv.includes("--check");
const apply = process.argv.includes("--apply");

if (check) {
  if (packageJson.version !== expected) {
    console.error(
      `FAIL: package.json is ${packageJson.version}, expected ${expected}. Run pnpm release:prepare.`,
    );
    process.exit(1);
  }
  if (bump && !readFileSync(CHANGELOG, "utf8").includes(`## ${expected}`)) {
    console.error(
      `FAIL: CHANGELOG.md has no entry for ${expected}. Run pnpm release:prepare.`,
    );
    process.exit(1);
  }
  console.log(
    `PASS: release ${expected} (${bump ?? "no bump"}) from ${tag}.`,
  );
  process.exit(0);
}

if (!bump) {
  console.log(`No release: no feat, fix, perf or breaking commits since ${tag}.`);
  process.exit(0);
}

if (!apply) {
  console.log(
    `Next release: ${expected} (${bump}) from ${tag}. ${commits.length} commit(s).`,
  );
  process.exit(0);
}

packageJson.version = expected;
writeFileSync(PACKAGE, `${JSON.stringify(packageJson, null, 2)}\n`);
execFileSync(process.execPath, [join(ROOT, "scripts", "sync-plugin-version.mjs")], {
  cwd: ROOT,
  stdio: "inherit",
});

const changelog = readFileSync(CHANGELOG, "utf8");
if (!changelog.includes(`## ${expected}`)) {
  const entry = changelogEntry(expected, commits);
  const next = changelog
    .replace(/^(# natuleadan-skills\n\n)/, `$1${entry}\n\n`)
    .replace(/\n{3,}/g, "\n\n");
  writeFileSync(CHANGELOG, next);
}

console.log(`Prepared release ${expected} (${bump}) from ${tag}.`);
