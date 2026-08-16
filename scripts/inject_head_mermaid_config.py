#!/usr/bin/env python3
"""
Complete Solution for Mermaid Auto-Run & Error Replacement:
1. Injects <script>window.mermaidConfig = { startOnLoad: false }; window.mermaid = { startOnLoad: false };</script>
   directly into <head> of all 26 weeks (BEFORE any CDN scripts are evaluated).
2. Updates assets/js/course.js:
   - renderMermaid only accepts valid Mermaid syntax (starting with graph, flowchart, etc.).
   - Cleanly cleans up any error elements from document.body.
"""

from pathlib import Path
from bs4 import BeautifulSoup
import re

WEEKS_DIR = Path("pages/weeks")
JS_FILE = Path("assets/js/course.js")

head_config_tag = """<script>
  window.mermaidConfig = { startOnLoad: false, suppressErrorRendering: true };
  window.mermaid = { startOnLoad: false };
</script>"""

# 1. Update <head> in all 26 weeks
for wn in range(1, 27):
    fp = WEEKS_DIR / f"week{wn}.html"
    if not fp.exists(): continue
    raw = fp.read_text(encoding='utf-8')
    soup = BeautifulSoup(raw, 'html.parser')
    head = soup.find('head')
    if head:
        # Check if already present in head
        if 'window.mermaidConfig' not in str(head):
            head.append(BeautifulSoup(head_config_tag, 'html.parser'))
            fp.write_text(str(soup), encoding='utf-8')
            print(f"  ✅ Added mermaidConfig to <head> in Week {wn}")

# 2. Update renderMermaid in course.js
js = JS_FILE.read_text(encoding='utf-8')

clean_render_mermaid = """// ── 8. MERMAID RENDERING ENGINE (Bulletproof & Cross-Browser) ──
function renderMermaid(dayId) {
  let retries = 0;
  const run = () => {
    if (typeof mermaid === 'undefined' || typeof mermaid.render !== 'function') {
      retries++;
      if (retries < 30) setTimeout(run, 80);
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
      // Get raw code
      let raw = node.getAttribute('data-mermaid-src');
      if (!raw) {
        let currentText = (node.textContent || node.innerText || '').trim();
        // If currentText is already contaminated with error text, do not use it
        if (currentText.startsWith('#mermaid') || currentText.includes('Syntax error')) {
          return;
        }
        raw = currentText.replace(/&gt;/g, '>').replace(/&lt;/g, '<').replace(/&quot;/g, '"').replace(/&amp;/g, '&').trim();
        node.setAttribute('data-mermaid-src', raw);
      }
      
      if (!raw || (!raw.startsWith('graph') && !raw.startsWith('flowchart') && !raw.startsWith('subgraph') && !raw.startsWith('sequenceDiagram'))) {
        return;
      }
      
      if (node.getAttribute('data-rendered') === '1' && node.querySelector('svg')) {
        return;
      }
      
      const cleanPrefix = (dayId || 'd').replace(/[^a-zA-Z0-9]/g, '');
      const uniqueId = 'svg-diag-' + cleanPrefix + '-' + idx + '-' + Math.random().toString(36).substr(2, 6);
      
      try {
        mermaid.render(uniqueId, raw).then(({ svg }) => {
          node.innerHTML = svg;
          node.setAttribute('data-rendered', '1');
          node.style.visibility = 'visible';
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
  
  setTimeout(run, 40);
}"""

# Replace renderMermaid in course.js
js = re.sub(r'// ── 8\. MERMAID RENDERING ENGINE[\s\S]*?(?=// ── 9\. INITIALIZATION)', clean_render_mermaid + "\n\n", js)
JS_FILE.write_text(js, encoding='utf-8')
print("✅ Updated renderMermaid engine in assets/js/course.js")
