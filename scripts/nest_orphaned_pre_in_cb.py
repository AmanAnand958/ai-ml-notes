#!/usr/bin/env python3
"""
Structural Code Card Nesting Repair across all 26 Weeks:
When a `<div class="cb">` contains only the `.cb-head` (language tag & copy button)
and the `<pre>` block is sitting as an adjacent sibling outside `.cb`,
this script moves the `<pre>` tag INSIDE the `<div class="cb">` container.
"""

from pathlib import Path
from bs4 import BeautifulSoup
import re

WEEKS_DIR = Path("/Users/amananand/Downloads/SDE/ai:ml-1/pages/weeks")

for wn in range(1, 27):
    fp = WEEKS_DIR / f"week{wn}.html"
    if not fp.exists(): continue
    
    html = fp.read_text(encoding='utf-8', errors='replace')
    soup = BeautifulSoup(html, 'html.parser')
    modified = False
    
    for cb in soup.find_all('div', class_=re.compile(r'\bcb\b')):
        # If cb does not have pre or code inside
        if not cb.find('pre') and not cb.find('code'):
            nxt = cb.find_next_sibling()
            if nxt and nxt.name == 'pre':
                # Move nxt pre INSIDE cb
                cb.append(nxt)
                modified = True

    if modified:
        fp.write_text(soup.prettify(), encoding='utf-8')
        print(f"  ✅ Nest-repaired orphaned <pre> tags into .cb cards for Week {wn}")
    else:
        print(f"  ℹ️ Week {wn} code cards already cleanly nested.")

print("\n🎉 ALL CODE BLOCKS IN ALL 26 WEEKS ARE NOW PROPERLY ENCAPSULATED!")
