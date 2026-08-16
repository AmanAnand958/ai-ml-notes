#!/usr/bin/env python3
"""
Surgically fix all corrupted f-strings and code lines across all weeks.
"""

from pathlib import Path
from bs4 import BeautifulSoup
import re
import ast

WEEKS_DIR = Path("pages/weeks")

for wn in range(1, 27):
    fp = WEEKS_DIR / f"week{wn}.html"
    if not fp.exists(): continue
    raw = fp.read_text(encoding='utf-8')
    
    # 1. Clean &lt;span...&gt; and &lt;/span&gt; everywhere
    raw = re.sub(r'&lt;span(?:\s+[^&]*)?&gt;', '', raw)
    raw = re.sub(r'&lt;/span&gt;', '', raw)
    raw = re.sub(r'&lt;code(?:\s+[^&]*)?&gt;', '', raw)
    raw = re.sub(r'&lt;/code&gt;', '', raw)
    raw = re.sub(r'&lt;br\s*/?&gt;', '\n', raw)
    
    # 2. Fix specific corrupted expressions
    raw = raw.replace('{<span class="bi">', '{')
    raw = raw.replace('{&lt;span class="bi"&gt;', '{')
    raw = raw.replace('type(name)}"', 'type(name)}')
    raw = raw.replace('type(age)}"', 'type(age)}')
    raw = raw.replace('len(freq)}"', 'len(freq)}')
    raw = raw.replace('len(students)} records."', 'len(students)} records."')
    
    fp.write_text(raw, encoding='utf-8')

print("✅ Cleaned corrupted f-string expressions!")
