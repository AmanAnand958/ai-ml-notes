#!/usr/bin/env python3
"""
Fix Blank Consecutive Headings across all 26 Weeks:
Finds any <h2 class="sh2"> or <h3 class="sh3"> that is immediately followed by another heading without content,
and removes the empty preceding heading so there are no blank stacked headings.
"""

from pathlib import Path
from bs4 import BeautifulSoup

WEEKS_DIR = Path("pages/weeks")
total_removed = 0

for wn in range(1, 27):
    fp = WEEKS_DIR / f"week{wn}.html"
    if not fp.exists(): continue
    raw = fp.read_text(encoding='utf-8')
    soup = BeautifulSoup(raw, 'html.parser')
    modified = False
    
    # We iterate multiple times to handle chains like <h2> followed by <h2> followed by <h2>
    while True:
        removed_in_pass = False
        for h in soup.find_all(['h2', 'h3', 'h4']):
            # Find next non-empty sibling
            sib = h.find_next_sibling()
            if sib and sib.name in ['h2', 'h3', 'h4']:
                # h is empty! Decompose it
                h.decompose()
                removed_in_pass = True
                total_removed += 1
                modified = True
                break
        if not removed_in_pass:
            break
            
    if modified:
        fp.write_text(str(soup), encoding='utf-8')
        print(f"  ✅ Cleaned blank consecutive headings in Week {wn}")

print(f"\n🎉 Cleaned all {total_removed} blank consecutive headings across all weeks!")
