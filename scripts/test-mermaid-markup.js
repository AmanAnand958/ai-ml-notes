#!/usr/bin/env node

const assert = require('node:assert/strict');
const fs = require('node:fs');

const pages = ['week3.html'];
let diagramCount = 0;

for (const page of pages) {
  const html = fs.readFileSync(`pages/weeks/${page}`, 'utf8');
  for (const match of html.matchAll(/<div class="mermaid"[^>]*>([\s\S]*?)<\/div>/g)) {
    diagramCount++;
    const diagram = match[1];
    assert.ok(!/<br\s*\/?\s*>/i.test(diagram), `${page} Mermaid diagram must not use HTML line breaks`);
    assert.match(diagram.trim(), /^(graph|flowchart)\s+(TD|TB|BT|RL|LR)/, `${page} Mermaid diagram must start with a graph declaration`);
  }
}

assert.ok(diagramCount > 0, 'expected at least one Mermaid diagram');
console.log(`Mermaid markup check passed for ${diagramCount} diagram(s).`);
