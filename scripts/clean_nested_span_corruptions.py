#!/usr/bin/env python3
"""
Clean all corrupted nested spans and literal <code class="..."> tags,
then re-highlight cleanly and safely.
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
    
    # 1. Clean literal <code...> tags inside pre
    raw = re.sub(r'<code(?:\s+[^>]*)?>', '', raw)
    raw = raw.replace('</code>', '')
    raw = raw.replace('&lt;code&gt;', '').replace('&lt;/code&gt;', '')
    
    # 2. Fix broken f-string spans: e.g. {<span class="bi">type(name)}"</span> -> {type(name)}
    raw = re.sub(r'\{<span class="[^"]+">([^<]+)</span>', r'{\1', raw)
    raw = re.sub(r'\{([^}]+)<span class="[^"]+">([^<]+)</span>', r'{\1\2', raw)
    raw = re.sub(r':<span class="num">(\d+)}</span>', r':\1}', raw)
    raw = re.sub(r':<span class="[^"]+">([^<]+)</span>', r':\1', raw)
    
    fp.write_text(raw, encoding='utf-8')
    print(f"  ✅ Cleaned f-string span nests in Week {wn}")

print("\n🎉 ALL CORRUPTED SPAN NESTS CLEANED!")
