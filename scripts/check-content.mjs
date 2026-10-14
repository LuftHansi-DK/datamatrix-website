// Content guard: run before every build/PR. Fails on claims we have decided never to publish
// and on accidental secrets. Deterministic, no network.
import { readFileSync, readdirSync, statSync } from "node:fs";
import { join } from "node:path";

const roots = ["src", "public"];
const banned = [
  [/99[,.]9{3,}/, "uptime claims with 4+ nines"],
  [/fem teknikere|five technicians/i, "team-size claim that is not true"],
  [/garanter\w*\s+(24\/7|døgnet rundt)|guarantee\w*\s+24\/7/i, "24/7 guarantee (we are reachable, we do not guarantee)"],
  [/Einstein/i, "misattributed quote"],
  [/(api[_-]?key|password|passwd|secret|token)\s*[:=]\s*\S{8,}/i, "possible secret"],
  [/ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}/, "GitHub token"],
];
// Customer names are NOT listed here (repo may be public). Optional local, gitignored list:
// one name per line in .private-names.txt → any match fails the check.
import { existsSync } from "node:fs";
if (existsSync(".private-names.txt")) {
  for (const n of readFileSync(".private-names.txt", "utf8").split("\n").map((x) => x.trim()).filter(Boolean)) {
    banned.push([new RegExp(n.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"), "i"), "customer name without written OK (see AGENTS.md)"]);
  }
}
const exts = /\.(astro|md|mdx|json|ts|js|mjs|html|txt|css)$/;
let errors = 0;
function walk(dir) {
  for (const name of readdirSync(dir)) {
    const p = join(dir, name);
    if (statSync(p).isDirectory()) walk(p);
    else if (exts.test(name)) {
      const lines = readFileSync(p, "utf8").split("\n");
      lines.forEach((line, i) => {
        for (const [re, why] of banned) if (re.test(line)) { console.error(`${p}:${i + 1}: ${why}`); errors++; }
      });
    }
  }
}
roots.forEach(walk);
if (errors) { console.error(`\ncheck-content: ${errors} problem(s)`); process.exit(1); }
console.log("check-content: OK");
