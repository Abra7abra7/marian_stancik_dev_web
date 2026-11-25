#!/usr/bin/env node
// Minify all site JS with esbuild into *.min.js next to the sources.
// Templates reference the .min.js files; the sources stay readable in the repo.
// Usage: node scripts/minify_js.mjs   (run after build_i18n.py — it picks up fresh chunks)
import { execFileSync } from 'node:child_process';
import { readdirSync, statSync, writeFileSync, existsSync } from 'node:fs';
import { join, dirname, basename } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');
const DIRS = ['js', 'js/i18n'];
const done = [];

const NPX = process.platform === 'win32' ? 'npx.cmd' : 'npx';

function minifyFile(src) {
  const out = src.replace(/\.js$/, '.min.js');
  // --charset=utf8: without it esbuild escapes Slovak/Czech/Polish diacritics to
  // \uXXXX and the "minified" chunks end up LARGER than the source.
  execFileSync(NPX, ['esbuild', src, '--minify', '--charset=utf8', '--target=es2019', `--outfile=${out}`],
    { cwd: ROOT, stdio: 'pipe', shell: process.platform === 'win32' });
  const before = statSync(join(ROOT, src)).size;
  const after = statSync(join(ROOT, out)).size;
  done.push(`${src}: ${before} -> ${after} bytes`);
}

for (const dir of DIRS) {
  const abs = join(ROOT, dir);
  if (!existsSync(abs)) continue;
  for (const f of readdirSync(abs)) {
    if (!f.endsWith('.js') || f.endsWith('.min.js')) continue;
    minifyFile(join(dir, f));
  }
}

// Also minify css/main.css -> css/main.min.css
const cssSrc = join('css', 'main.css');
const cssOut = join('css', 'main.min.css');
if (existsSync(join(ROOT, cssSrc))) {
  execFileSync(NPX, ['esbuild', cssSrc, '--minify', '--charset=utf8', `--outfile=${cssOut}`],
    { cwd: ROOT, stdio: 'pipe', shell: process.platform === 'win32' });
  const before = statSync(join(ROOT, cssSrc)).size;
  const after = statSync(join(ROOT, cssOut)).size;
  done.push(`${cssSrc}: ${before} -> ${after} bytes`);
}

console.log('✅ minified ' + done.length + ' files');
for (const line of done) console.log('   ' + line);
