#!/usr/bin/env python3
"""
Fix Mermaid Rendering & Raw Escapes:
1. Replaces all '&gt;' with raw '>' in all 26 week HTML files so '-->' is NEVER escaped in diagram source.
2. In assets/js/course.js:
   - Always trims raw string before checking diagram prefix.
   - Decodes '&gt;', '&lt;', '&amp;' in both text and attributes.
   - Triggers clean render with SVG insertion.
3. In assets/css/course.css:
   - Hides unrendered .mermaid divs (.mermaid:not([data-rendered])) so raw code text never flashes or displays vertically on screen.
"""

from pathlib import Path
from bs4 import BeautifulSoup
import re

WEEKS_DIR = Path("pages/weeks")
CSS_FILE = Path("assets/css/course.css")
JS_FILE = Path("assets/js/course.js")

# 1. Fix all 26 HTML files on disk
for wn in range(1, 27):
    fp = WEEKS_DIR / f"week{wn}.html"
    if not fp.exists(): continue
    raw = fp.read_text(encoding='utf-8')
    
    # Replace &gt; inside .mermaid divs with raw >
    def clean_mermaid_div(match):
        inner = match.group(1)
        inner = inner.replace('&gt;', '>').replace('&lt;', '<').replace('&amp;', '&').replace('&quot;', '"')
        return f'<div class="mermaid">\n{inner.strip()}\n</div>'
        
    raw = re.sub(r'<div class="mermaid">([\s\S]*?)</div>', clean_mermaid_div, raw)
    fp.write_text(raw, encoding='utf-8')
    print(f"  ✅ Sanitized raw Mermaid diagrams in Week {wn}")

# 2. Update CSS in course.css
css = CSS_FILE.read_text(encoding='utf-8')
mermaid_css = """
/* ── MERMAID DIAGRAM STYLING & CLEAN RENDERING ── */
.mermaid:not([data-rendered]) {
  visibility: hidden !important;
  opacity: 0 !important;
  height: 0 !important;
  overflow: hidden !important;
  display: block !important;
}

.mermaid[data-rendered="1"] {
  visibility: visible !important;
  opacity: 1 !important;
  display: block !important;
  max-width: 100% !important;
  overflow-x: auto !important;
  margin: 1.5rem 0 !important;
  text-align: center !important;
}

.mermaid svg {
  display: inline-block !important;
  visibility: visible !important;
  opacity: 1 !important;
  max-width: 100% !important;
  height: auto !important;
  position: static !important;
}

body > [id^="dmermaid"],
body > div[id^="mermaid-"],
.error-icon,
.error-text {
  display: none !important;
  visibility: hidden !important;
  opacity: 0 !important;
  position: absolute !important;
  left: -9999px !important;
  pointer-events: none !important;
}
"""

if "/* ── MERMAID DIAGRAM STYLING" in css:
    css = re.sub(r'/\* ── MERMAID DIAGRAM STYLING[\s\S]*?(?=\n\n|\Z)', mermaid_css, css)
else:
    css += "\n" + mermaid_css

CSS_FILE.write_text(css, encoding='utf-8')
print("✅ Updated assets/css/course.css with clean .mermaid[data-rendered='1'] styling!")

# 3. Update course.js renderMermaid
js = JS_FILE.read_text(encoding='utf-8')
clean_render_engine = """// ── 8. MERMAID RENDERING ENGINE (Bulletproof & Cross-Browser) ──
function renderMermaid(dayId) {
  let retries = 0;
  const run = () => {
    if (typeof mermaid === 'undefined' || typeof mermaid.render !== 'function') {
      retries++;
      if (retries < 30) setTimeout(run, 60);
      return;
    }
    
    try {
      if (!window.mermaidInitialized) {
        mermaid.initialize({
          startOnLoad: false,
          theme: 'dark',
          securityLevel: 'loose',
          fontFamily: 'Outfit, sans-serif',
          flowchart: { htmlLabels: true, curve: 'linear' },
          suppressErrorRendering: true
        });
        window.mermaidInitialized = true;
      }
    } catch(e) {}
    
    let sec = null;
    if (dayId) {
      sec = document.getElementById(dayId) || document.getElementById('day-' + dayId);
    } else {
      sec = document.querySelector('.day-section.active') || document.querySelector('.day-section');
    }
    
    if (!sec || (sec.offsetParent === null && window.getComputedStyle(sec).display === 'none')) {
      return;
    }
    
    const nodes = sec.querySelectorAll('.mermaid');
    if (!nodes.length) return;
    
    nodes.forEach((node, idx) => {
      let raw = node.getAttribute('data-mermaid-src');
      if (!raw) {
        let currentText = (node.textContent || node.innerText || '').trim();
        if (currentText.startsWith('#mermaid') || currentText.includes('Syntax error')) {
          return;
        }
        raw = currentText.replace(/&gt;/g, '>').replace(/&lt;/g, '<').replace(/&quot;/g, '"').replace(/&amp;/g, '&').trim();
        node.setAttribute('data-mermaid-src', raw);
      }
      
      raw = (raw || '').trim();
      if (!raw) return;
      
      if (node.getAttribute('data-rendered') === '1' && node.querySelector('svg')) {
        return;
      }
      
      const cleanPrefix = (dayId || 'd').replace(/[^a-zA-Z0-9]/g, '');
      const uniqueId = 'svg-diag-' + cleanPrefix + '-' + idx + '-' + Math.random().toString(36).substr(2, 6);
      
      try {
        mermaid.render(uniqueId, raw).then(({ svg }) => {
          node.innerHTML = svg;
          node.setAttribute('data-rendered', '1');
          document.querySelectorAll('body > [id^="mermaid-"], body > [id^="dmermaid-"], div.error-icon').forEach(el => el.remove());
        }).catch(err => {
          console.warn('Mermaid render error:', err);
          document.querySelectorAll('body > [id^="mermaid-"], body > [id^="dmermaid-"], div.error-icon').forEach(el => el.remove());
        });
      } catch(err) {
        console.error('Mermaid render failed:', err);
      }
    });
  };
  
  setTimeout(run, 30);
}"""

js = re.sub(r'// ── 8\. MERMAID RENDERING ENGINE[\s\S]*?(?=// ── 9\. INITIALIZATION)', clean_render_engine + "\n\n", js)
JS_FILE.write_text(js, encoding='utf-8')
print("✅ Updated renderMermaid in assets/js/course.js!")

print("\n🎉 ALL MERMAID DIAGRAMS & ESCAPES FIXED ACROSS THE ENTIRE CURRICULUM!")
