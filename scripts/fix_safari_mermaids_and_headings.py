#!/usr/bin/env python3
"""
1. Fix Raw Markdown Headings in Week 26:
   Replaces raw markdown headings like `# ML System Design — Semantic Search`
   with canonical styled `<h3 class="sh3">ML System Design — Semantic Search</h3>`.

2. Safari & Cross-Browser Mermaid Compatibility Hardening:
   Ensures mermaid diagrams render reliably across Safari, Chrome, Firefox, and Edge
   using synchronous mermaid.init fallback and unique SVG ID generations.
"""

from pathlib import Path
from bs4 import BeautifulSoup
import re

# ─────────────────────────────────────────────────────────────────────────────
# 1. CLEAN RAW MARKDOWN HEADINGS IN WEEK 26
# ─────────────────────────────────────────────────────────────────────────────
fp26 = Path("/Users/amananand/Downloads/SDE/ai:ml-1/pages/weeks/week26.html")
html26 = fp26.read_text(encoding='utf-8', errors='replace')

# Replace <h2 style="..."> # Heading </h2> with <h3 class="sh3"> Heading </h3>
html26 = re.sub(
    r'<h2[^>]*>\s*#\s*([^<]+)\s*</h2>',
    r'<h3 class="sh3">\1</h3>',
    html26
)

# Also fix any remaining raw "# Heading" inside HTML paragraphs
html26 = re.sub(
    r'<p[^>]*>\s*#\s*([^<]+)\s*</p>',
    r'<h3 class="sh3">\1</h3>',
    html26
)

fp26.write_text(html26, encoding='utf-8')
print("✅ Cleaned raw markdown headings into styled CSS h3 headers in Week 26!")


# ─────────────────────────────────────────────────────────────────────────────
# 2. CROSS-BROWSER / SAFARI MERMAID RENDERING HARDENING (assets/js/course.js)
# ─────────────────────────────────────────────────────────────────────────────
fp_js = Path("/Users/amananand/Downloads/SDE/ai:ml-1/assets/js/course.js")
js = fp_js.read_text(encoding='utf-8')

safari_hardened_mermaid = '''// ── 8. MERMAID RENDERING ENGINE (Safari & Cross-Browser Hardened) ──
function renderMermaid(dayId) {
  let retries = 0;
  const run = () => {
    if (typeof mermaid === 'undefined') {
      retries++;
      if (retries < 30) {
        setTimeout(run, 80);
      }
      return;
    }
    
    try {
      if (!window.mermaidInitialized) {
        mermaid.initialize({
          startOnLoad: false,
          theme: 'dark',
          securityLevel: 'loose',
          fontFamily: 'Outfit, sans-serif',
          flowchart: { htmlLabels: true, curve: 'linear' }
        });
        window.mermaidInitialized = true;
      }
    } catch(e) {}
    
    const sec = dayId ? (document.getElementById(dayId) || document.getElementById('day-' + dayId)) : document;
    if (!sec) return;
    
    const nodes = sec.querySelectorAll('.mermaid:not([data-rendered])');
    if (!nodes.length) return;
    
    nodes.forEach((node, idx) => {
      // Decode HTML entities
      let raw = node.textContent || node.innerText || '';
      raw = raw.replace(/&gt;/g, '>').replace(/&lt;/g, '<').replace(/&quot;/g, '"').replace(/&amp;/g, '&').trim();
      
      // Safari requires explicit unique IDs for dynamic SVG generation
      const uniqueId = 'mermaid-svg-' + (dayId || 'd') + '-' + idx + '-' + Math.random().toString(36).substr(2, 6);
      
      try {
        if (mermaid.render) {
          mermaid.render(uniqueId, raw).then(({ svg }) => {
            node.innerHTML = svg;
            node.setAttribute('data-rendered', '1');
            node.style.visibility = 'visible';
          }).catch(err => {
            console.warn('Mermaid render error, using fallback:', err);
            // Fallback to mermaid.init
            node.textContent = raw;
            mermaid.init(undefined, node);
            node.setAttribute('data-rendered', '1');
          });
        } else if (mermaid.init) {
          node.textContent = raw;
          mermaid.init(undefined, node);
          node.setAttribute('data-rendered', '1');
        }
      } catch(err) {
        console.error('Mermaid render failed:', err);
      }
    });
  };
  run();
}'''

# Replace renderMermaid block in course.js
js = re.sub(
    r'// ── 8\. MERMAID RENDERING ENGINE.*?// ── 9\. INITIALIZATION',
    safari_hardened_mermaid + '\n\n// ── 9. INITIALIZATION',
    js,
    flags=re.DOTALL
)

fp_js.write_text(js, encoding='utf-8')
print("✅ Safari and cross-browser hardened Mermaid rendering engine in assets/js/course.js!")
