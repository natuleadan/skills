#!/usr/bin/env node
// Generates ThirdPartyNotices.txt from the direct development dependencies.
// Usage: pnpm notices           write the file
//        pnpm notices --check   fail when the file is out of date
import { existsSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const OUTPUT = join(ROOT, "ThirdPartyNotices.txt");

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
  return {
    name,
    version: pkg.version ?? "",
    license,
    repository: repositoryUrl(pkg),
  };
});

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

const content = [
  "Third Party Notices",
  "",
  "This project uses the following development dependencies. The skills",
  "contain no third-party code; these packages are build and validation",
  "tooling and are not distributed with the skill content.",
  "",
  table,
  "",
  "The full license text of each package is distributed with the package and",
  "available at the repository listed above.",
  "",
].join("\n");

const check = process.argv.includes("--check");
if (check) {
  const current = existsSync(OUTPUT) ? readFileSync(OUTPUT, "utf8") : "";
  if (current !== content) {
    console.error(
      "FAIL: ThirdPartyNotices.txt is out of date. Run `pnpm notices`.",
    );
    process.exit(1);
  }
  console.log("PASS: ThirdPartyNotices.txt is up to date.");
} else {
  writeFileSync(OUTPUT, content);
  console.log(`Wrote ${rows.length} packages to ThirdPartyNotices.txt`);
}
