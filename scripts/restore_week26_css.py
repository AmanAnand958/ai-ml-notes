#!/usr/bin/env python3
"""
Restore Full Production CSS to Week 26:
Copies the complete 44KB+ theme style block and layout rules from Week 25 to Week 26.
"""

from pathlib import Path
from bs4 import BeautifulSoup

WEEKS_DIR = Path("/Users/amananand/Downloads/SDE/ai:ml-1/pages/weeks")

print("=== Restoring Full CSS to Week 26 ===")
fp25 = WEEKS_DIR / "week25.html"
fp26 = WEEKS_DIR / "week26.html"

html25 = fp25.read_text(encoding='utf-8', errors='replace')
html26 = fp26.read_text(encoding='utf-8', errors='replace')

# Extract full <style>...</style> block from week25
style_start = html25.find('<style>')
style_end = html25.find('</style>') + len('</style>')
full_style_css = html25[style_start:style_end]

# In week26, replace whatever truncated <style> tag exists with the full style block
soup26 = BeautifulSoup(html26, 'html.parser')
head26 = soup26.find('head')

# Remove existing style tags in week26
for st in head26.find_all('style'):
    st.decompose()

# Insert full style block into head
head26.append(BeautifulSoup(full_style_css, 'html.parser'))

fp26.write_text(str(soup26), encoding='utf-8')
print(f"✅ Restored full {len(full_style_css)} bytes CSS stylesheet to Week 26!")
