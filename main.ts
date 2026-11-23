// news-image-20261123 — "The World in One Day".
// The entry is a front page (entry.png) summing up the world's news of
// Monday 23 November 2026: Russian missiles in Poland and NATO's emergency
// session, Ukraine sinking a Russian warship in Libya, COP31 collapsing
// with no deal, Iran vowing "all available means" over the U.S. blockade, and the
// rest of the day.
// This program only puts that image where the grader reads it, as
// /output/entry.png (or $MAKEFUN_OUTPUT_DIR/entry.png when set).
// It copies bytes and nothing else, so two runs write identical output.

import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

mkdirSync(outDir, { recursive: true });
const image = readFileSync(join(here, "entry.png"));
writeFileSync(join(outDir, "entry.png"), image);
