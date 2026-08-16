#!/usr/bin/env python3
"""
Fix Code Block DOM Structure across all 26 weeks:
The canonical DOM structure for a code card must be:
<div class="cb">
  <div class="cb-head">
    <span class="cb-lang">python</span>
    <div class="cb-btns">
      <button class="copy-btn" onclick="copyCode(this)">copy</button>
      <button class="run-btn" onclick="runCode(this)">Run</button>
    </div>
  </div>
  <pre>...</pre>
</div>

Notice: <pre> MUST be a sibling of <div class="cb-head"> INSIDE <div class="cb">,
NOT nested inside <div class="cb-head"> or <div class="cb-btns">!
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
        # Find any <pre> anywhere inside cb
        pre = cb.find('pre')
        head = cb.find('div', class_='cb-head')
        
        if pre and head:
            # If pre is nested inside head, move it to be a direct child of cb (after head)
            if pre.parent != cb:
                pre.extract()
                cb.append(pre)
                modified = True
                
        # If pre is an adjacent sibling right after cb
        elif not pre and head:
            nxt = cb.find_next_sibling()
            if nxt and nxt.name == 'pre':
                nxt.extract()
                cb.append(nxt)
                modified = True
                
        # Clean up any nested divs inside cb-head so that it only has .cb-lang and .cb-btns
        if head:
            lang_span = head.find('span', class_='cb-lang')
            btns_div = head.find('div', class_='cb-btns')
            
            # If buttons are not wrapped in .cb-btns, collect buttons
            buttons = head.find_all('button')
            
            new_head = soup.new_tag('div', **{'class': 'cb-head'})
            if lang_span:
                lang_span.extract()
                new_head.append(lang_span)
            else:
                s = soup.new_tag('span', **{'class': 'cb-lang'})
                s.string = 'python'
                new_head.append(s)
                
            new_btns = soup.new_tag('div', **{'class': 'cb-btns'})
            for b in buttons:
                b.extract()
                new_btns.append(b)
            new_head.append(new_btns)
            
            head.replace_with(new_head)
            modified = True

    if modified:
        fp.write_text(soup.prettify(), encoding='utf-8')
        print(f"  ✅ Corrected code block flex hierarchy in Week {wn}")

print("\n🎉 ALL CODE CARDS NOW HAVE HEADER ABOVE CODE BLOCK!")
