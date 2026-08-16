#!/usr/bin/env python3
"""
Deep cleaner: removes literal <span class="..."> and <code class="..."> text from inside <pre> tags across all weeks.
"""

from pathlib import Path
from bs4 import BeautifulSoup
import re

WEEKS_DIR = Path("pages/weeks")

for wn in range(1, 27):
    fp = WEEKS_DIR / f"week{wn}.html"
    if not fp.exists(): continue
    soup = BeautifulSoup(fp.read_text(encoding='utf-8'), 'html.parser')
    modified = False
    
    for cb in soup.find_all('div', class_='cb'):
        pre = cb.find('pre')
        if not pre: continue
        
        # Get raw text
        txt = pre.text
        
        # Clean any literal tags in txt
        clean_txt = re.sub(r'<span(?:\s+[^>]*)?>', '', txt)
        clean_txt = clean_txt.replace('</span>', '')
        clean_txt = re.sub(r'<code(?:\s+[^>]*)?>', '', clean_txt)
        clean_txt = clean_txt.replace('</code>', '')
        clean_txt = re.sub(r'&lt;span(?:\s+[^&]*)?&gt;', '', clean_txt)
        clean_txt = clean_txt.replace('&lt;/span&gt;', '')
        clean_txt = re.sub(r'&lt;code(?:\s+[^&]*)?&gt;', '', clean_txt)
        clean_txt = clean_txt.replace('&lt;/code&gt;', '')
        clean_txt = clean_txt.replace('{type(name)}"', '{type(name)}')
        clean_txt = clean_txt.replace('{type(age)}"', '{type(age)}')
        
        if clean_txt != txt:
            pre.string = clean_txt
            modified = True
            
    if modified:
        fp.write_text(str(soup), encoding='utf-8')
        print(f"  ✅ Deep-cleaned text nodes in Week {wn}")

print("\n🎉 ALL RESIDUAL SPAN/CODE TEXT REMOVED!")
