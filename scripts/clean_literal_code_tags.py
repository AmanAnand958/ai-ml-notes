#!/usr/bin/env python3
"""
Clean literal `<code>` and `</code>` text strings inside `<pre>` blocks across all weeks.
"""

from pathlib import Path
from bs4 import BeautifulSoup
import re

WEEKS_DIR = Path("pages/weeks")

for wn in range(1, 27):
    fp = WEEKS_DIR / f"week{wn}.html"
    if not fp.exists(): continue
    raw = fp.read_text(encoding='utf-8')
    
    # Clean literal <code> and </code> inside pre tags
    def clean_pre_code_tags(match):
        attrs = match.group(1) or ""
        content = match.group(2)
        content = content.replace('<code>', '').replace('</code>', '')
        content = content.replace('&lt;code&gt;', '').replace('&lt;/code&gt;', '')
        return f'<pre{attrs}>{content}</pre>'
        
    cleaned_raw = re.sub(r'<pre([^>]*)>([\s\S]*?)</pre>', clean_pre_code_tags, raw)
    
    if cleaned_raw != raw:
        fp.write_text(cleaned_raw, encoding='utf-8')
        print(f"  ✅ Cleaned literal code tags in Week {wn}")

print("\n🎉 ALL LITERAL CODE TAGS CLEANED ACROSS ALL WEEKS!")
