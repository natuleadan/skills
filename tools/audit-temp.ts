#!/usr/bin/env node
// Audits the 16 industry skills for neutrality and shape.
//
// Checks:
// 1. no platform concepts (robot, toolset, human-in-the-loop, HIL)
// 2. no vendor mention
// 3. no pricing or commercial vocabulary
// 4. no embedded code except mermaid
// 5. every reference has a mermaid sequenceDiagram
// 6. SKILL.md has frontmatter, exactly one H1 and no mermaid
// 7. metadata.json references match the files on disk
//
// Exit 0 when clean, 1 when there are findings.
import { existsSync, readdirSync, readFileSync } from "node:fs";
import { dirname, join, relative } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const SKILLS = join(ROOT, "skills");

const PLATFORM_WORDS = ["robot", "toolset", "human-in-the-loop", "HIL"];
const VENDOR_WORDS = [
  "natuleadan",
  "nla.run",
  "nla-api",
  "natuleadan.com",
  "natuleadan.app",
];
const COMMERCIAL_WORDS = [
  "credit",
  "usd",
  "invoice",
  "payment",
  "price",
  "pricing",
  "wallet",
  "top-up",
  "subscription",
  "refund",
  "tax",
];
const H1 = /^# /gm;

type Metadata = { references?: string[] };

function wordMatches(text: string, word: string): boolean {
  const escaped = word.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  return new RegExp(`\\b${escaped}\\b`, "i").test(text);
}

function mdFiles(dir: string): string[] {
  const out: string[] = [];
  for (const entry of readdirSync(dir, { withFileTypes: true })) {
    const full = join(dir, entry.name);
    if (entry.isDirectory()) out.push(...mdFiles(full));
    else if (entry.name.endsWith(".md")) out.push(full);
  }
  return out.sort();
}

const findings: string[] = [];

if (!existsSync(SKILLS)) {
  console.error("FAIL: no skills directory");
  process.exit(1);
}

const skills = readdirSync(SKILLS, { withFileTypes: true })
  .filter((entry) => entry.isDirectory() && entry.name.endsWith("-ai-tools"))
  .map((entry) => entry.name)
  .sort();

console.log(`Industry skills audited: ${skills.length}`);

for (const name of skills) {
  const skill = join(SKILLS, name);
  const files = mdFiles(skill);
  console.log(`  ${name}: ${files.length} md files`);

  for (const file of files) {
    const rel = relative(skill, file).split("\\").join("/");
    const text = readFileSync(file, "utf8");

    for (const word of COMMERCIAL_WORDS) {
      if (wordMatches(text, word)) {
        findings.push(`${name}: commercial word '${word}' in ${rel}`);
      }
    }
    for (const word of PLATFORM_WORDS) {
      if (wordMatches(text, word)) {
        findings.push(`${name}: platform word '${word}' in ${rel}`);
      }
    }
    for (const word of VENDOR_WORDS) {
      if (text.toLowerCase().includes(word.toLowerCase())) {
        findings.push(`${name}: vendor word '${word}' in ${rel}`);
      }
    }
    for (const match of text.matchAll(/```(\w+)/g)) {
      if (match[1] !== "mermaid") {
        findings.push(`${name}: non-mermaid code block in ${rel}`);
      }
    }
  }

  for (const file of files.filter((path) =>
    path.split("/").includes("references"),
  )) {
    const rel = relative(skill, file).split("\\").join("/");
    const text = readFileSync(file, "utf8");
    if (!text.includes("```mermaid")) {
      findings.push(`${name}: ${rel} has no mermaid block`);
    } else if (!text.includes("sequenceDiagram")) {
      findings.push(`${name}: ${rel} mermaid is not a sequenceDiagram`);
    }
    if ((text.match(H1) ?? []).length !== 1) {
      findings.push(`${name}: ${rel} must have exactly one H1`);
    }
  }

  const skillMd = join(skill, "SKILL.md");
  if (!existsSync(skillMd)) {
    findings.push(`${name}: missing SKILL.md`);
  } else {
    const text = readFileSync(skillMd, "utf8");
    if (!text.startsWith("---\n")) {
      findings.push(`${name}: SKILL.md missing frontmatter`);
    }
    if (text.includes("mermaid")) {
      findings.push(`${name}: SKILL.md must not contain mermaid`);
    }
    if ((text.match(H1) ?? []).length !== 1) {
      findings.push(`${name}: SKILL.md must have exactly one H1`);
    }
  }

  const metaPath = join(skill, "metadata.json");
  if (!existsSync(metaPath)) {
    findings.push(`${name}: missing metadata.json`);
  } else {
    let metadata: Metadata = {};
    try {
      metadata = JSON.parse(readFileSync(metaPath, "utf8")) as Metadata;
    } catch (error) {
      findings.push(`${name}: metadata.json invalid (${String(error)})`);
    }
    const declared = new Set(metadata.references ?? []);
    const present = new Set(
      files
        .filter((file) => file.split("/").includes("references"))
        .map((file) => file.split("/").pop() as string),
    );
    for (const reference of declared) {
      if (!present.has(reference)) {
        findings.push(`${name}: metadata declares missing '${reference}'`);
      }
    }
    for (const reference of present) {
      if (!declared.has(reference)) {
        findings.push(
          `${name}: reference '${reference}' not declared in metadata`,
        );
      }
    }
  }
}

if (findings.length > 0) {
  console.error("");
  for (const finding of findings) console.error(`FAIL: ${finding}`);
  console.error(`\n${findings.length} finding(s)`);
  process.exit(1);
}

console.log("");
console.log("PASS: industry skills are neutral, uniform and clean.");
