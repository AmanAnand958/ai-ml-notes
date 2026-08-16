#!/usr/bin/env python3
"""
Fix remaining accessibility tabindex on all flashcards across all 26 weeks.
"""

from pathlib import Path
from bs4 import BeautifulSoup

WEEKS_DIR = Path("pages/weeks")

for wn in range(1, 27):
    fp = WEEKS_DIR / f"week{wn}.html"
    if not fp.exists(): continue
    soup = BeautifulSoup(fp.read_text(encoding='utf-8'), 'html.parser')
    modified = False
    
    for fc in soup.find_all('div', class_='flashcard'):
        if not fc.get('tabindex'):
            fc['tabindex'] = '0'
            fc['role'] = 'button'
            fc['aria-label'] = 'Revision Flashcard, click to flip'
            if not fc.get('onkeydown'):
                fc['onkeydown'] = "if(event.key==='Enter'||event.key===' ')this.click()"
            modified = True
            
    if modified:
        fp.write_text(str(soup), encoding='utf-8')
        print(f"  ✅ Added keyboard a11y attributes to all flashcards in Week {wn}")

print("\n🎉 ALL FLASHCARDS ARE NOW FULLY KEYBOARD ACCESSIBLE (A11Y) ACROSS ALL WEEKS!")
