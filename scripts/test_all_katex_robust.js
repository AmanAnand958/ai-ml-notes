const fs = require('fs');
const path = require('path');
const katex = require('katex');

const weeksDir = path.join(__dirname, '../pages/weeks');
const files = fs.readdirSync(weeksDir).filter(f => f.startsWith('week') && f.endsWith('.html'));

let totalTested = 0;
let errors = 0;

for (const file of files) {
  let content = fs.readFileSync(path.join(weeksDir, file), 'utf-8');
  
  // KaTeX ignores <pre>, <code>, <script>, and <style>
  content = content.replace(/<pre[\s\S]*?<\/pre>/gi, '');
  content = content.replace(/<code[\s\S]*?<\/code>/gi, '');
  content = content.replace(/<script[\s\S]*?<\/script>/gi, '');
  content = content.replace(/<style[\s\S]*?<\/style>/gi, '');

  // Match $$ blocks
  const blockMath = content.match(/\$\$([\s\S]*?)\$\$/g) || [];
  // Match inline $ blocks
  const inlineMath = content.match(/\$([^\$\n]+?)\$/g) || [];
  
  for (const raw of [...blockMath, ...inlineMath]) {
    const isDisplay = raw.startsWith('$$');
    const expr = isDisplay ? raw.slice(2, -2).trim() : raw.slice(1, -1).trim();
    if (!expr) continue;
    
    totalTested++;
    try {
      katex.renderToString(expr, { displayMode: isDisplay, throwOnError: true, strict: false });
    } catch (err) {
      errors++;
      const pos = content.indexOf(raw);
      const snippet = content.slice(Math.max(0, pos - 80), Math.min(content.length, pos + raw.length + 80));
      console.error(`❌ ${file} math error:\n  Raw expr: ${JSON.stringify(raw)}\n  Error: ${err.message}\n  Context:\n${snippet}\n`);
    }
  }
}

console.log(`\n🎉 Tested ${totalTested} actual rendered KaTeX formulas across ${files.length} week files. Errors: ${errors}`);
if (errors > 0) process.exit(1);
