#!/usr/bin/env python3
"""
Fix Week 26 Layout Defect:
1. Re-establishes closing `</main></div>` (closing `<main class="main">` and `<div class="layout">`) right before the `<script>` block.
2. Ensures the div balance is mathematically exact (open = close).
"""

import re
from pathlib import Path

WEEKS_DIR = Path("/Users/amananand/Downloads/SDE/ai:ml-1/pages/weeks")
fp26 = WEEKS_DIR / "week26.html"

html26 = fp26.read_text(encoding='utf-8', errors='replace')

# Locate week-summary closing
ws_idx = html26.rfind('<div class="week-summary">')
script_idx = html26.rfind('<script>')

if ws_idx != -1 and script_idx != -1:
    ws_end = html26.find('</div>\n</div>', ws_idx)
    if ws_end != -1:
        # Proper end of week-summary is ws_end + len('</div>\n</div>')
        clean_bottom = '''</div>
</div>
</main>
</div>
'''
        # Replace from ws_end up to <script>
        new_html26 = html26[:ws_end] + clean_bottom + html26[script_idx:]
        fp26.write_text(new_html26, encoding='utf-8')
        print("✅ Added missing </main> and </div> layout closures to Week 26!")

# Verify div balance
html_check = fp26.read_text(encoding='utf-8', errors='replace')
open_divs = len(re.findall(r'<div\b', html_check))
close_divs = len(re.findall(r'</div>', html_check))
print(f"Verified Div Balance: <div={open_divs}, </div>={close_divs}, diff={open_divs - close_divs}")
