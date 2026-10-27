#!/usr/bin/env node
// Smoke tests for every skill script: help, version, known command and unknown
// command. Exits 1 when any skill fails.
import { existsSync, readFileSync, readdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const SKILLS = join(ROOT, "skills");

type Metadata = { version: string; abstract: string; references?: string[] };

const skills = readdirSync(SKILLS, { withFileTypes: true })
  .filter((entry) => entry.isDirectory())
  .map((entry) => entry.name)
  .filter((name) => existsSync(join(SKILLS, name, "metadata.json")))
  .sort();

function run(skill: string, args: string[]) {
  const dir = join(SKILLS, skill);
  return spawnSync(
    process.execPath,
    [join(dir, "scripts", "main.ts"), ...args],
    { cwd: dir, encoding: "utf8" },
  );
}

let failures = 0;

for (const skill of skills) {
  const dir = join(SKILLS, skill);
  const metadata = JSON.parse(
    readFileSync(join(dir, "metadata.json"), "utf8"),
  ) as Metadata;
  const problems: string[] = [];

  if (!existsSync(join(dir, "scripts", "main.ts"))) {
    problems.push("missing scripts/main.ts");
  } else {
    const help = run(skill, ["--help"]);
    if (help.status !== 0) {
      problems.push(`--help exited ${help.status}`);
    } else {
      if (!help.stdout.includes(skill)) problems.push("--help misses the name");
      if (!help.stdout.includes(metadata.abstract)) {
        problems.push("--help misses the abstract");
      }
    }

    const version = run(skill, ["--version"]);
    if (version.status !== 0) {
      problems.push(`--version exited ${version.status}`);
    } else if (version.stdout.trim() !== metadata.version) {
      problems.push("--version does not match metadata");
    }

    const commands = (metadata.references ?? []).map((reference) =>
      reference.replace(/\.md$/, ""),
    );
    if (commands.length > 0) {
      const command = commands[0];
      const result = run(skill, [command]);
      if (result.status !== 0) {
        problems.push(`command ${command} exited ${result.status}`);
      } else {
        try {
          const output = JSON.parse(result.stdout) as {
            status?: string;
            skill?: string;
            command?: string;
          };
          if (output.status !== "stub") problems.push("command is not a stub");
          if (output.skill !== skill) problems.push("command returned wrong skill");
          if (output.command !== command) {
            problems.push("command returned wrong command");
          }
        } catch {
          problems.push(`command ${command} did not return JSON`);
        }
      }
    }

    const unknown = run(skill, ["not-a-command"]);
    if (unknown.status !== 2) {
      problems.push(`unknown command exited ${unknown.status}, expected 2`);
    }
  }

  if (problems.length === 0) {
    console.log(`PASS  ${skill}`);
  } else {
    failures += 1;
    console.error(`FAIL  ${skill}: ${problems.join("; ")}`);
  }
}

if (failures > 0) {
  console.error(`\n${failures} skill script(s) failed`);
  process.exit(1);
}

console.log(`\nPASS: ${skills.length} skill scripts respond correctly.`);
