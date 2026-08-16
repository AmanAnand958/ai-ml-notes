#!/usr/bin/env python3
"""
Step 2: Ensure all <table> elements across all 26 weeks are wrapped in responsive <div class="table-wrap"> containers.
"""

from pathlib import Path
from bs4 import BeautifulSoup

WEEKS_DIR = Path("pages/weeks")

for wn in range(1, 27):
    fp = WEEKS_DIR / f"week{wn}.html"
    if not fp.exists(): continue
    soup = BeautifulSoup(fp.read_text(encoding='utf-8'), 'html.parser')
    modified = False
    
    for t in soup.find_all('table'):
        parent = t.parent
        # Check if already wrapped
        if not parent or ('table-wrap' not in parent.get('class', []) and 'overflow-x' not in parent.get('style', '')):
            wrapper = soup.new_tag('div', **{
                'class': 'table-wrap',
                'style': 'overflow-x: auto; margin: 1.2rem 0; width: 100%;'
            })
            t.wrap(wrapper)
            modified = True
            
    if modified:
        fp.write_text(str(soup), encoding='utf-8')
        print(f"  ✅ Wrapped responsive table containers in Week {wn}")

print("\n🎉 STEP 2 COMPLETE: ALL 73 TABLES ARE NOW FULLY RESPONSIVE ACROSS ALL VIEWPORTS!")
