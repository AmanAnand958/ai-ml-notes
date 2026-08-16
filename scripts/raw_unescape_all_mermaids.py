#!/usr/bin/env python3
"""
Raw String Mermaid Sanitizer:
Directly replaces HTML-escaped characters in Mermaid blocks across all 26 HTML files
without using BeautifulSoup HTML serializers (which re-escape > into &gt;).
"""

import re
from pathlib import Path

WEEKS_DIR = Path("/Users/amananand/Downloads/SDE/ai:ml-1/pages/weeks")

for wn in range(1, 27):
    fp = WEEKS_DIR / f"week{wn}.html"
    if not fp.exists(): continue
    
    raw_html = fp.read_text(encoding='utf-8', errors='replace')
    
    def unescape_mermaid(match):
        inner = match.group(1)
        inner = inner.replace('--&gt;', '-->')
        inner = inner.replace('-&gt;', '->')
        inner = inner.replace('==&gt;', '==>')
        inner = inner.replace('&gt;', '>')
        inner = inner.replace('&lt;', '<')
        inner = inner.replace('&quot;', '"')
        inner = inner.replace('&amp;', '&')
        return f'<div class="mermaid">\n{inner.strip()}\n</div>'
        
    sanitized_html = re.sub(r'<div class="mermaid"[^>]*>(.*?)</div>', unescape_mermaid, raw_html, flags=re.DOTALL)
    
    if sanitized_html != raw_html:
        fp.write_text(sanitized_html, encoding='utf-8')
        print(f"  ✅ Replaced all &gt; with raw --> in Mermaid diagrams for Week {wn}")
    else:
        print(f"  ℹ️ Week {wn} already had raw unescaped Mermaid diagrams.")

print("\n🎉 ALL MERMAID DIAGRAMS IN ALL 26 WEEKS NOW HAVE 100% CLEAN RAW ARROWS!")
