#!/usr/bin/env node
// Validates CHANGELOG.md: semver order, allowed sections, bullets and tags.
import { execFileSync } from "node:child_process";
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const CHANGELOG = join(ROOT, "CHANGELOG.md");
const PACKAGE = join(ROOT, "package.json");

const ALLOWED_SECTIONS = new Set([
  "Breaking Changes",
  "Features",
  "Fixes",
  "Performance",
  "Documentation",
  "Maintenance",
  "Reverts",
  "Other",
]);

type VersionBlock = {
  version: string;
  sections: string[];
  bullets: string[];
};

function git(args: string[]): string {
  try {
    return execFileSync("git", args, { cwd: ROOT, encoding: "utf8" }).trim();
  } catch {
    return "";
  }
}

function compareVersions(a: string, b: string): number {
  const pa = a.split(".").map(Number);
  const pb = b.split(".").map(Number);
  for (let index = 0; index < 3; index += 1) {
    if (pa[index] !== pb[index]) return pa[index] - pb[index];
  }
  return 0;
}

const text = readFileSync(CHANGELOG, "utf8");
const packageVersion = (
  JSON.parse(readFileSync(PACKAGE, "utf8")) as { version: string }
).version;
const blocks: VersionBlock[] = [];
const rawBlocks = new Map<string, string>();
let current: VersionBlock | null = null;
let currentVersion: string | null = null;

for (const line of text.split("\n")) {
  const versionMatch = /^## (\d+\.\d+\.\d+)$/.exec(line);
  if (versionMatch) {
    current = { version: versionMatch[1], sections: [], bullets: [] };
    blocks.push(current);
    currentVersion = versionMatch[1];
    rawBlocks.set(currentVersion, "");
    continue;
  }
  if (!current || !currentVersion) continue;
  rawBlocks.set(currentVersion, `${rawBlocks.get(currentVersion) ?? ""}${line}\n`);

  const sectionMatch = /^### (.+)$/.exec(line);
  if (sectionMatch) {
    current.sections.push(sectionMatch[1]);
    continue;
  }

  const bulletMatch = /^- (.+)$/.exec(line);
  if (bulletMatch) current.bullets.push(bulletMatch[1]);
}

const errors: string[] = [];

if (blocks.length === 0) {
  errors.push("CHANGELOG.md has no version sections");
}

for (let index = 0; index < blocks.length; index += 1) {
  const block = blocks[index];
  if (block.sections.length === 0) {
    errors.push(`${block.version}: no section`);
  }
  if (block.bullets.length === 0) {
    errors.push(`${block.version}: no bullet`);
  }
  const seen = new Set<string>();
  for (const section of block.sections) {
    if (!ALLOWED_SECTIONS.has(section)) {
      errors.push(`${block.version}: unknown section '${section}'`);
    }
    if (seen.has(section)) {
      errors.push(`${block.version}: duplicate section '${section}'`);
    }
    seen.add(section);
  }
  for (const bullet of block.bullets) {
    if (/^[0-9a-f]{7,}:\s/.test(bullet)) {
      errors.push(`${block.version}: bullet starts with a commit sha`);
    }
    if (bullet.includes(" - ")) {
      errors.push(`${block.version}: bullet has a spaced hyphen`);
    }
  }
  if (index > 0 && compareVersions(blocks[index - 1].version, block.version) <= 0) {
    errors.push(
      `${blocks[index - 1].version} is not greater than ${block.version}`,
    );
  }
}

if (blocks[0]?.version !== packageVersion) {
  errors.push(
    `top version ${blocks[0]?.version ?? "none"} != package.json ${packageVersion}`,
  );
}

for (let index = 1; index < blocks.length; index += 1) {
  const version = blocks[index].version;
  if (!git(["tag", "-l", `v${version}`])) {
    errors.push(`${version}: missing git tag v${version}`);
  }
}

// Completeness: every commit between the previous tag and this release must
// appear in the block. The initial 0.0.1 block is the root release and is
// excluded. The top version may not have a tag yet, so use HEAD.
for (let index = 0; index < blocks.length - 1; index += 1) {
  const version = blocks[index].version;
  const previous = blocks[index + 1].version;
  const tag = `v${version}`;
  const to = git(["tag", "-l", tag]) ? tag : "HEAD";
  const raw = git(["log", `v${previous}..${to}`, "--format=%s"]);
  const block = (rawBlocks.get(version) ?? "").toLowerCase();
  for (const line of raw.split("\n")) {
    const subject = line.trim();
    if (
      !subject ||
      subject.startsWith("Merge ") ||
      subject.startsWith("chore(release):")
    ) {
      continue;
    }
    const match = /^([a-z]+)(?:\([^)]+\))?(!)?:\s+(.+)$/.exec(subject);
    if (!match) continue;
    const text = match[3].toLowerCase();
    if (!block.includes(text)) {
      errors.push(`${version}: missing commit '${text}'`);
    }
  }
}

if (errors.length > 0) {
  for (const error of errors) console.error(`FAIL: ${error}`);
  console.error(`\n${errors.length} changelog error(s)`);
  process.exit(1);
}

console.log(
  `PASS: ${blocks.length} changelog releases, top ${packageVersion}.`,
);
