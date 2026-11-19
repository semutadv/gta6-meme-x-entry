// Entry helper for the make.fun bounty "Post a GTA 6 meme on X"
// (gta6-meme-x-01).
//
// The entry itself is the X post; this program has exactly one job for the
// grader: take POST.json, which names the post's URL, from the bot
// directory and place a copy in the output directory, creating that
// directory first when it does not exist yet. If the copy fails, it says
// so (naming POST.json) and exits with code 1.
//
// Both directories can be overridden, which is how the local test runs:
//   MAKEFUN_BOT_DIR    folder POST.json is read from   (default: /bot)
//   MAKEFUN_OUTPUT_DIR folder the copy is written to   (default: /output)
//
// Local test:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync } from "node:fs";
import { join } from "node:path";

const botDir = process.env.MAKEFUN_BOT_DIR ?? "/bot";
const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

mkdirSync(outputDir, { recursive: true });

const source = join(botDir, "POST.json");
const target = join(outputDir, "POST.json");

try {
  copyFileSync(source, target);
} catch (err) {
  console.error(
    `Could not copy POST.json from ${source}: ${(err as Error).message}`
  );
  process.exit(1);
}

console.log(`POST.json copied to ${target}`);
