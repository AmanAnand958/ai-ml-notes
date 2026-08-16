#!/usr/bin/env python3
"""
Fix remaining XP and Language mismatches in Weeks 10, 11, 12, 13, 24.
"""

from pathlib import Path
from bs4 import BeautifulSoup

WEEKS_DIR = Path("pages/weeks")

# 1. Fix toolkits data-xp vs completeDay XP
for wn in [11, 12, 13]:
    fp = WEEKS_DIR / f"week{wn}.html"
    soup = BeautifulSoup(fp.read_text(), 'html.parser')
    tk = soup.find('div', id='day-toolkit')
    if tk:
        tk['data-xp'] = '500'
        fp.write_text(str(soup), encoding='utf-8')
        print(f"  ✅ Fixed Toolkit XP alignment in Week {wn}")

# 2. Fix language tag in Week 10
fp10 = WEEKS_DIR / "week10.html"
html10 = fp10.read_text()
html10 = html10.replace('<span class="cb-lang">shell</span>', '<span class="cb-lang">python</span>', 1)
fp10.write_text(html10)
print("  ✅ Fixed language tag in Week 10")

# 3. Fix language tag in Week 24
fp24 = WEEKS_DIR / "week24.html"
html24 = fp24.read_text()
html24 = html24.replace('<span class="cb-lang">shell</span>\n        <div class="cb-btns">\n          <button class="copy-btn" onclick="copyCode(this)">copy</button>\n          <button class="run-btn" onclick="runCode(this)">Run</button>\n        </div>\n      </div>\n      <pre><code>import subprocess', '<span class="cb-lang">python</span>\n        <div class="cb-btns">\n          <button class="copy-btn" onclick="copyCode(this)">copy</button>\n          <button class="run-btn" onclick="runCode(this)">Run</button>\n        </div>\n      </div>\n      <pre><code>import subprocess')
fp24.write_text(html24)
print("  ✅ Fixed language tag in Week 24")
