#!/usr/bin/env node
// Copies package.json's version into .claude-plugin/plugin.json and marketplace.json.
// Runs as part of `npm run version`, immediately after `changeset version`.
// With --check it changes nothing and exits 1 if the two versions differ.

import { readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const repo = join(dirname(fileURLToPath(import.meta.url)), "..");
const pluginPath = join(repo, ".claude-plugin", "plugin.json");
const marketplacePath = join(repo, ".claude-plugin", "marketplace.json");

const { version } = JSON.parse(readFileSync(join(repo, "package.json"), "utf8"));

// Sync plugin.json
if (pluginPath) {
  try {
    const pluginSource = readFileSync(pluginPath, "utf8");
    const plugin = JSON.parse(pluginSource);

    if (plugin.version !== version) {
      if (process.argv.includes("--check")) {
        console.error(
          `plugin.json version is ${plugin.version}, package.json is ${version}. Run \`npm run version\`.`,
        );
        process.exit(1);
      }

      const updated = pluginSource.replace(
        /("version"\s*:\s*")[^"]*(")/,
        `$1${version}$2`,
      );

      writeFileSync(pluginPath, updated);
      console.log(`plugin.json version ${plugin.version} -> ${version}`);
    } else {
      console.log(`plugin.json version is ${version} (already in sync)`);
    }
  } catch (e) {
    if (e.code !== "ENOENT") throw e;
    console.log("plugin.json not found, skipping");
  }
}

// Sync marketplace.json
if (marketplacePath) {
  try {
    const marketSource = readFileSync(marketplacePath, "utf8");
    const market = JSON.parse(marketSource);

    // Update plugin version in marketplace
    if (market.plugins && market.plugins[0]) {
      const currentPluginVersion = market.plugins[0].version;
      if (currentPluginVersion !== version) {
        if (process.argv.includes("--check")) {
          console.error(
            `marketplace.json plugin version is ${currentPluginVersion}, package.json is ${version}. Run \`npm run version\`.`,
          );
          process.exit(1);
        }

        const updated = marketSource.replace(
          /("version"\s*:\s*")[^"]*(")/g,
          `$1${version}$2`,
        );

        writeFileSync(marketplacePath, updated);
        console.log(`marketplace.json version ${currentPluginVersion} -> ${version}`);
      } else {
        console.log(`marketplace.json version is ${version} (already in sync)`);
      }
    }
  } catch (e) {
    if (e.code !== "ENOENT") throw e;
    console.log("marketplace.json not found, skipping");
  }
}

// Sync metadata.version in marketplace
if (marketplacePath) {
  try {
    const marketSource = readFileSync(marketplacePath, "utf8");
    const market = JSON.parse(marketSource);

    if (market.metadata && market.metadata.version !== version) {
      const updated = marketSource.replace(
        /("version"\s*:\s*")[^"]*(")/g,
        `$1${version}$2`,
      );
      writeFileSync(marketplacePath, updated);
      console.log(`marketplace.json metadata version -> ${version}`);
    }
  } catch (e) {
    if (e.code !== "ENOENT") throw e;
  }
}

console.log(`Version sync complete: ${version}`);
