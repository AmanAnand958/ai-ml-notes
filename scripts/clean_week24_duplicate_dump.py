#!/usr/bin/env python3
"""
Remove Duplicate Dump Chunk in Week 24:
Removes the 9KB orphaned duplicate block between Day 171 and Day 172
(which contained the repeated AI Safety callout, flashcards, and math deep-dive).
"""

import re
from pathlib import Path

WEEKS_DIR = Path("/Users/amananand/Downloads/SDE/ai:ml-1/pages/weeks")
fp24 = WEEKS_DIR / "week24.html"
html24 = fp24.read_text(encoding='utf-8', errors='replace')

# Locate duplicate dump start (after Day 171 complete button) and end (before Day 172)
btn_171_idx = html24.find('id="btn-day-171"')
d172_idx = html24.find('id="day-172"')

if btn_171_idx != -1 and d172_idx != -1:
    # Find the closing tag of day-171 right after button
    btn_close = html24.find('</button>', btn_171_idx) + len('</button>')
    # Look for the day-172 opening tag container
    d172_open = html24.rfind('<div class="day-section"', btn_close, d172_idx)
    
    if d172_open != -1:
        # Check if orphaned dump exists between btn_close and d172_open
        dump = html24[btn_close:d172_open]
        print(f"Found orphaned dump between Day 171 and Day 172 ({len(dump)} chars):")
        print(dump[:200].replace('\n', ' '))
        
        # Clean replacement: close day-171 properly with </div>
        clean_transition = '\n</div>\n'
        html24 = html24[:btn_close] + clean_transition + html24[d172_open:]
        fp24.write_text(html24, encoding='utf-8')
        print("✅ Cleaned orphaned duplicate dump from Week 24!")

# Re-verify
html_after = fp24.read_text(encoding='utf-8', errors='replace')
print("AI Safety occurrences after cleanup:", html_after.count('AI Safety, Adversarial Red-Teaming'))
print("day-172 occurrences after cleanup:", html_after.count('id="day-172"'))
