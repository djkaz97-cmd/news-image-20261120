// main.ts — make.fun news-image-20261120 entry.
// Copies the rendered 20-Nov-2026 world-news front page (entry.png, built by
// make_image.py in the agent session) to the grader's output directory.
// Node 22, standard library only, no network, deterministic bytes every run.
import { readFileSync, writeFileSync, mkdirSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const image = readFileSync(join(here, "entry.png"));
if (image[0] !== 0x89 || image[1] !== 0x50 || image[2] !== 0x4e || image[3] !== 0x47) {
  throw new Error("entry.png does not carry the PNG magic bytes");
}
if (image.length > 1048576) throw new Error("entry.png exceeds the 1 MiB gate");
mkdirSync(outDir, { recursive: true });
writeFileSync(join(outDir, "entry.png"), image);
console.log(`entry.png: ${image.length} bytes -> ${join(outDir, "entry.png")}`);

