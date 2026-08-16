#!/usr/bin/env python3
"""
Ensure all HTML pages have the canonical unescaped mermaid markup and correct CDN scripts.
"""

from pathlib import Path
import re

WEEKS_DIR = Path("/Users/amananand/Downloads/SDE/ai:ml-1/pages/weeks")

for wn in range(1, 27):
    fp = WEEKS_DIR / f"week{wn}.html"
    if not fp.exists(): continue
    
    html = fp.read_text(encoding='utf-8', errors='replace')
    
    # Ensure raw unescaped arrows inside <div class="mermaid">
    def clean_mermaid_block(m):
        content = m.group(1)
        content = content.replace('&gt;', '>').replace('&lt;', '<').replace('&quot;', '"').replace('&amp;', '&')
        return f'<div class="mermaid">\n{content.strip()}\n</div>'
    
    html = re.sub(r'<div class="mermaid"[^>]*>(.*?)</div>', clean_mermaid_block, html, flags=re.DOTALL)
    
    # Ensure mermaid CDN is in head
    if 'mermaid@10.2.0' not in html and 'mermaid.min.js' not in html:
        head_idx = html.find('</head>')
        if head_idx != -1:
            mermaid_script = '<script src="https://cdn.jsdelivr.net/npm/mermaid@10.2.0/dist/mermaid.min.js"></script>\n'
            html = html[:head_idx] + mermaid_script + html[head_idx:]
            
    fp.write_text(html, encoding='utf-8')
    print(f"✅ Sanitized Mermaid diagrams in Week {wn}")

print("\n🎉 ALL MERMAID DIAGRAMS SYNCHRONIZED ACROSS ALL 26 WEEKS!")
