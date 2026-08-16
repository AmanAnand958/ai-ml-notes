#!/usr/bin/env python3
"""
Deep cleaner for escaped HTML tags inside <pre> blocks:
- Removes `&lt;span class="..."&gt;` and `&lt;/span&gt;` inside <pre> blocks.
- Removes `&lt;code class="..."&gt;` and `&lt;/code&gt;` inside <pre> blocks.
- Cleans any corrupted f-strings.
"""

from pathlib import Path
import re

WEEKS_DIR = Path("pages/weeks")

for wn in range(1, 27):
    fp = WEEKS_DIR / f"week{wn}.html"
    if not fp.exists(): continue
    raw = fp.read_text(encoding='utf-8')
    
    # Clean escaped span tags inside pre
    def clean_escaped_html_in_pre(match):
        attrs = match.group(1) or ""
        code = match.group(2)
        
        # Remove literal / escaped span and code tags
        code = re.sub(r'&lt;span(?:\s+[^&]*)?&gt;', '', code)
        code = re.sub(r'&lt;/span&gt;', '', code)
        code = re.sub(r'&lt;code(?:\s+[^&]*)?&gt;', '', code)
        code = re.sub(r'&lt;/code&gt;', '', code)
        
        # Also clean unescaped span inside f-strings
        code = re.sub(r'\{<span[^>]*>([^<]+)</span>', r'{\1', code)
        code = re.sub(r'<span class="str">f"([^"]*?)(?:<span[^>]*>|</span>)([^"]*?)"</span>', r'<span class="str">f"\1\2"</span>', code)
        
        return f'<pre{attrs}>{code}</pre>'
        
    cleaned = re.sub(r'<pre([^>]*)>([\s\S]*?)</pre>', clean_escaped_html_in_pre, raw)
    
    if cleaned != raw:
        fp.write_text(cleaned, encoding='utf-8')
        print(f"  ✅ Cleaned escaped HTML tags in Week {wn}")

print("\n🎉 ALL ESCAPED HTML TAGS IN PRE BLOCKS CLEANED!")
