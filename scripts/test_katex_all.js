const fs = require('fs');
const path = require('path');
const katex = require('katex');

const dir = path.join(process.cwd(), 'pages', 'weeks');
const files = fs.readdirSync(dir).filter(f => f.startsWith('week') && f.endsWith('.html')).sort();

let totalBlocks = 0;
let failedBlocks = 0;
let totalInline = 0;
let failedInline = 0;

for (const f of files) {
  let content = fs.readFileSync(path.join(dir, f), 'utf-8');

  // 1. Check Blocks $$...$$
  const blockRegex = /\$\$([\s\S]*?)\$\$/g;
  let match;
  let bIdx = 0;
  while ((match = blockRegex.exec(content)) !== null) {
    totalBlocks++;
    bIdx++;
    const math = match[1].trim();
    try {
      katex.renderToString(math, { displayMode: true, throwOnError: true });
    } catch (err) {
      failedBlocks++;
      console.log(`Block KaTeX FAILED in ${f} block #${bIdx}: ${err.message}`);
      console.log(`  Math: ${math}\n`);
    }
  }

  // Strip code, pre, script, math-blocks before testing inline
  let cleaned = content.replace(/<script[\s\S]*?<\/script>/gi, '')
                       .replace(/<pre[\s\S]*?<\/pre>/gi, '')
                       .replace(/<code[\s\S]*?<\/code>/gi, '')
                       .replace(/\$\$[\s\S]*?\$\$/g, '');

  const inlineRegex = /\$([^\$\n\r]+?)\$/g;
  let iIdx = 0;
  while ((match = inlineRegex.exec(cleaned)) !== null) {
    totalInline++;
    iIdx++;
    const math = match[1].trim();
    if (/^\d+(\.\d+)?(k|M|B|%|\/day|\/month)?$/i.test(math)) continue; // currency or percentage
    if (/^[a-zA-Z0-9_\-\s]+$/.test(math) && !math.includes('_') && !math.includes('^')) continue; // regular word like $foo
    try {
      katex.renderToString(math, { displayMode: false, throwOnError: true });
    } catch (err) {
      failedInline++;
      console.log(`Inline KaTeX FAILED in ${f} inline #${iIdx}: ${err.message}`);
      console.log(`  Math: ${math}\n`);
    }
  }
}

console.log(`\n========================================`);
console.log(`Total Block Math: ${totalBlocks}, Failed: ${failedBlocks}`);
console.log(`Total Inline Math: ${totalInline}, Failed: ${failedInline}`);
console.log(`========================================`);
