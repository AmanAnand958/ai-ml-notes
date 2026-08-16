#!/usr/bin/env python3
"""
Step 3: Fix link security (target=_blank missing rel=noopener) and Flashcard 3D CSS styling across all HTML files.
"""

from pathlib import Path
from bs4 import BeautifulSoup
import re

WEEKS_DIR = Path("pages/weeks")
ROOT_DIR = Path(".")

all_html_files = [ROOT_DIR / "index.html", ROOT_DIR / "dashboard.html", ROOT_DIR / "resources.html", ROOT_DIR / "roadmap.html"]
all_html_files += list(WEEKS_DIR.glob("week*.html"))

# 1. Add rel="noopener" to target=_blank links
for fp in all_html_files:
    soup = BeautifulSoup(fp.read_text(encoding='utf-8', errors='replace'), 'html.parser')
    modified = False
    
    for a in soup.find_all('a', target='_blank'):
        rel = a.get('rel', [])
        if isinstance(rel, str): rel = rel.split()
        if 'noopener' not in rel:
            rel.append('noopener')
            a['rel'] = ' '.join(rel)
            modified = True
            
    if modified:
        fp.write_text(str(soup), encoding='utf-8')
        print(f"  ✅ Secured external links in {fp.name}")

# 2. Add 3D CSS to flashcards
for fp in all_html_files:
    raw = fp.read_text(encoding='utf-8', errors='replace')
    if "flashcard" in raw and "backface-visibility" not in raw:
        if ".flashcard {" in raw:
            raw = raw.replace(
                ".flashcard {",
                ".flashcard {\n  -webkit-backface-visibility: hidden;\n  backface-visibility: hidden;\n  transform-style: preserve-3d;"
            )
            fp.write_text(raw, encoding='utf-8')
            print(f"  ✅ Added 3D backface visibility CSS in {fp.name}")

print("\n🎉 STEP 3 COMPLETE: LINK SECURITY & FLASHCARD 3D STYLES HARDENED!")
