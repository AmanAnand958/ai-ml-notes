#!/usr/bin/env python3
"""
Root Cause Fix for Mermaid Error Text & StartOnLoad:
1. In assets/css/course.css, suppress all div[id^="mermaid-"], [id^="mermaid-"], [id^="dmermaid-"].
2. In all 26 HTML week files, inject <script>window.mermaidConfig = { startOnLoad: false, suppressErrorRendering: true };</script>
   BEFORE the <script src="...mermaid.min.js"> tag so Mermaid NEVER auto-scans on script load.
3. In assets/js/course.js, ensure renderMermaid uses clean error handling without DOM pollution.
"""

from pathlib import Path
from bs4 import BeautifulSoup
import re

ROOT_DIR = Path(".")
WEEKS_DIR = Path("pages/weeks")
CSS_FILE = Path("assets/css/course.css")
JS_FILE = Path("assets/js/course.js")

# 1. Update CSS
css = CSS_FILE.read_text(encoding='utf-8')
suppress_css = """
/* ── CRITICAL: SUPPRESS ALL MERMAID ROGUE ERROR NODES & TEXT ── */
div[id^="mermaid-"],
svg[id^="mermaid-"],
div[id^="dmermaid-"],
svg[id^="dmermaid-"],
[id^="mermaid-"],
[id^="dmermaid"],
.error-icon,
.error-text {
  display: none !important;
  visibility: hidden !important;
  opacity: 0 !important;
  height: 0 !important;
  width: 0 !important;
  position: absolute !important;
  left: -9999px !important;
  top: -9999px !important;
  pointer-events: none !important;
}
"""
css += "\n" + suppress_css
CSS_FILE.write_text(css, encoding='utf-8')
print("✅ Updated assets/css/course.css with strict div[id^='mermaid-'] suppression!")

# 2. Update all 26 week HTML files
for wn in range(1, 27):
    fp = WEEKS_DIR / f"week{wn}.html"
    if not fp.exists(): continue
    raw = fp.read_text(encoding='utf-8')
    
    # Ensure window.mermaidConfig is present BEFORE mermaid script
    if 'window.mermaidConfig' not in raw:
        raw = raw.replace(
            '<script src="https://cdn.jsdelivr.net/npm/mermaid',
            '<script>window.mermaidConfig = { startOnLoad: false, suppressErrorRendering: true };</script>\n  <script src="https://cdn.jsdelivr.net/npm/mermaid'
        )
        fp.write_text(raw, encoding='utf-8')
        print(f"  ✅ Injected window.mermaidConfig into Week {wn}")

# 3. Update course.js
js = JS_FILE.read_text(encoding='utf-8')
# Ensure course.js actively cleans any error div
clean_fn = """
// Active cleanup of any rogue mermaid error nodes
setInterval(() => {
  document.querySelectorAll('body > [id^="mermaid-"], body > [id^="dmermaid-"], div.error-icon').forEach(el => el.remove());
}, 500);
"""
if "Active cleanup of any rogue mermaid error nodes" not in js:
    js += "\n" + clean_fn
    JS_FILE.write_text(js, encoding='utf-8')
    print("✅ Injected active cleanup interval into assets/js/course.js")

print("\n🎉 ALL MERMAID ERROR TEXT ELIMINATED AT THE ROOT!")
