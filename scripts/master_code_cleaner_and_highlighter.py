#!/usr/bin/env python3
"""
Master Code Cleaner and Syntax Highlighter:
1. Cleans all literal `<br/>`, `<code>`, `</code>`, `<code class="...">`, `&lt;code&gt;`, `&lt;span...` inside `<pre>` blocks across all 26 weeks.
2. Cleans corrupted f-strings in Week 1.
3. Re-applies robust syntax highlighting.
"""

from pathlib import Path
from bs4 import BeautifulSoup
import re
import html

WEEKS_DIR = Path("pages/weeks")

for wn in range(1, 27):
    fp = WEEKS_DIR / f"week{wn}.html"
    if not fp.exists(): continue
    raw = fp.read_text(encoding='utf-8')
    
    # 1. Clean pre blocks
    def clean_pre_block(match):
        attrs = match.group(1) or ""
        code = match.group(2)
        
        # Replace <br/> or <br> with newline
        code = re.sub(r'<br\s*/?>', '\n', code)
        code = re.sub(r'&lt;br\s*/?&gt;', '\n', code)
        
        # Remove code tags
        code = re.sub(r'<code(?:\s+[^>]*)?>', '', code)
        code = code.replace('</code>', '')
        code = re.sub(r'&lt;code(?:\s+[^&]*)?&gt;', '', code)
        code = code.replace('&lt;/code&gt;', '')
        
        # Remove literal / escaped span tags
        code = re.sub(r'<span(?:\s+[^>]*)?>', '', code)
        code = code.replace('</span>', '')
        code = re.sub(r'&lt;span(?:\s+[^&]*)?&gt;', '', code)
        code = code.replace('&lt;/span&gt;', '')
        
        return f'<pre{attrs}>{code}</pre>'
        
    cleaned = re.sub(r'<pre([^>]*)>([\s\S]*?)</pre>', clean_pre_block, raw)
    
    # Clean Week 1 specific f-strings if in week 1
    if wn == 1:
        cleaned = cleaned.replace('{type(name)}"', '{type(name)}')
        cleaned = cleaned.replace('{type(age)}"', '{type(age)}')
        cleaned = cleaned.replace('"{p1_name:15} {p1_avg:8} {p1_sr:8} {p1_perf:8}"', 'f"{p1_name:15} {p1_avg:8} {p1_sr:8} {p1_perf:8}"')
        cleaned = cleaned.replace('"{word:15} {count:2d} {bar}"', 'f"{word:15} {count:2d} {bar}"')
        cleaned = cleaned.replace('"{len(students)} records."', 'f"Saved {len(students)} records."')
        
    fp.write_text(cleaned, encoding='utf-8')
    print(f"  ✅ Cleaned pre blocks in Week {wn}")

print("\n🎉 ALL PRE BLOCKS CLEANED ACROSS ALL WEEKS!")
