#!/usr/bin/env node
// Generates ThirdPartyNotices.txt from the direct development dependencies.
// Usage: pnpm notices           write the file
//        pnpm notices --check   fail when the file is out of date
import { existsSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const OUTPUT = join(ROOT, "ThirdPartyNotices.txt");
const LICENSE_FILES = [
  "LICENSE",
  "LICENSE.md",
  "LICENSE.txt",
  "license",
  "license.md",
  "COPYING",
  "COPYING.md",
];

type PackageJson = {
  version?: string;
  license?: string;
  repository?: string | { url?: string };
};

type Row = {
  name: string;
  version: string;
  license: string;
  repository: string;
  text: string | null;
};

function repositoryUrl(pkg: PackageJson): string {
  const value =
    typeof pkg.repository === "string" ? pkg.repository : pkg.repository?.url;
  if (!value) return "unknown";
  return value
    .replace(/^git\+/, "")
    .replace(/^git:\/\//, "https://")
    .replace(/\.git$/, "");
}

function readLicense(dir: string): string | null {
  for (const name of LICENSE_FILES) {
    const path = join(dir, name);
    if (existsSync(path)) {
      return readFileSync(path, "utf8").trim();
    }
  }
  return null;
}

function repositoryBase(url: string): string {
  return url.split("/").slice(0, 5).join("/");
}

// Standard texts are never invented: a package must ship a license file, or
// reuse the text of a sibling from the same repository and license.
function licenseFor(rows: Row[], row: Row): string {
  const sibling = rows.find(
    (other) =>
      other.text &&
      other.license === row.license &&
      other.repository !== "unknown" &&
      repositoryBase(other.repository) === repositoryBase(row.repository),
  );
  if (sibling?.text) return sibling.text;
  throw new Error(
    `cannot find the license text for ${row.name} (${row.license}); ` +
      "add the license file to the package or an explicit override",
  );
}

const manifest = JSON.parse(
  readFileSync(join(ROOT, "package.json"), "utf8"),
) as { devDependencies?: Record<string, string> };

const names = Object.keys(manifest.devDependencies ?? {}).sort();
if (names.length === 0) throw new Error("package.json has no devDependencies");

const rows: Row[] = names.map((name) => {
  const dir = join(ROOT, "node_modules", name);
  if (!existsSync(dir)) {
    throw new Error(`missing ${name}; run pnpm install`);
  }
  const pkg = JSON.parse(
    readFileSync(join(dir, "package.json"), "utf8"),
  ) as PackageJson;
  const license = pkg.license ?? "Unknown";
  if (license === "Unknown") {
    throw new Error(`unknown license for ${name}`);
  }
  const repository = repositoryUrl(pkg);
  return {
    name,
    version: pkg.version ?? "",
    license,
    repository,
    text: readLicense(dir),
  };
});

// Reuse the text of a sibling package from the same repository when a package
// ships no license file of its own. A package with no usable text fails below.
for (const row of rows) {
  if (row.text) continue;
  row.text = licenseFor(rows, row);
}

// Group packages by identical license text.
const groups = new Map<string, string[]>();
for (const row of rows) {
  const text = row.text as string;
  if (!groups.has(text)) groups.set(text, []);
  groups.get(text)?.push(row.name);
}

const widths = {
  name: Math.max(7, ...rows.map((row) => row.name.length)),
  version: Math.max(7, ...rows.map((row) => row.version.length)),
  license: Math.max(7, ...rows.map((row) => row.license.length)),
};

const pad = (value: string, width: number) => value.padEnd(width, " ");

const table = [
  `${pad("Package", widths.name)}  ${pad("Version", widths.version)}  ${pad("License", widths.license)}  Repository`,
  `${"-".repeat(widths.name)}  ${"-".repeat(widths.version)}  ${"-".repeat(widths.license)}  ${"-".repeat(40)}`,
  ...rows.map(
    (row) =>
      `${pad(row.name, widths.name)}  ${pad(row.version, widths.version)}  ${pad(row.license, widths.license)}  ${row.repository}`,
  ),
].join("\n");

const licenses = [...groups.entries()]
  .map(([text, packageNames]) => {
    const title = text.split("\n")[0].trim();
    return [
      "==================================================",
      `  ${title}`,
      `  Applies to: ${packageNames.join(", ")}`,
      "==================================================",
      "",
      text,
    ].join("\n");
  })
  .join("\n\n");

const content = [
  "Third Party Notices",
  "",
  "This project uses the following development dependencies. The skills",
  "contain no third-party code; these packages are build and validation",
  "tooling and are not distributed with the skill content.",
  "",
  table,
  "",
  "License texts",
  "",
  licenses,
  "",
].join("\n");

const check = process.argv.includes("--check");
const summary = `${rows.length} packages, ${groups.size} license texts`;
if (check) {
  const current = existsSync(OUTPUT) ? readFileSync(OUTPUT, "utf8") : "";
  if (current !== content) {
    console.error(
      "FAIL: ThirdPartyNotices.txt is out of date. Run `pnpm notices`.",
    );
    process.exit(1);
  }
  console.log(`PASS: ThirdPartyNotices.txt is up to date (${summary}).`);
} else {
  writeFileSync(OUTPUT, content);
  console.log(`Wrote ${summary} to ThirdPartyNotices.txt`);
}
