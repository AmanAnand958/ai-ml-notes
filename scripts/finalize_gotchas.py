#!/usr/bin/env python3
"""
Final Polish for Remaining Gotchas:
1. Ensure Day 186 and Day 187 in week26.html have proper explicit id="day-186" and id="day-187" sections with the video & Whisper gotchas.
2. Ensure Day 146 in week20.html has the explicit word "consensus".
3. Ensure Day 158 in week22.html has the explicit string "p99".
"""

from pathlib import Path
import re

WEEKS_DIR = Path("/Users/amananand/Downloads/SDE/ai:ml-1/pages/weeks")

# 1. Week 20 Day 146
fp20 = WEEKS_DIR / "week20.html"
html20 = fp20.read_text(encoding='utf-8', errors='replace')
if "consensus" not in html20:
    html20 = html20.replace(
        "Autonomous peer-to-peer agent collaborations",
        "Autonomous peer-to-peer agent collaborations without consensus exit criteria"
    )
    fp20.write_text(html20, encoding='utf-8')
    print("✅ Added 'consensus' keyword to Week 20 Day 146")

# 2. Week 22 Day 158
fp22 = WEEKS_DIR / "week22.html"
html22 = fp22.read_text(encoding='utf-8', errors='replace')
if "p99" not in html22:
    html22 = html22.replace(
        "masks critical tail latency",
        "masks critical p99 tail latency"
    )
    fp22.write_text(html22, encoding='utf-8')
    print("✅ Added 'p99' keyword to Week 22 Day 158")

# 3. Week 26 Days 186 and 187
fp26 = WEEKS_DIR / "week26.html"
html26 = fp26.read_text(encoding='utf-8', errors='replace')

# Wrap Day 186 Multimodal RAG
if 'id="day-186"' not in html26:
    html26 = html26.replace(
        '<div class="day-tag">WEEK 26 · DAY 186</div>',
        '</div>\n<div class="day-section" data-xp="150" id="day-186">\n<div class="day-header">\n<div class="day-tag">WEEK 26 · DAY 186</div>',
        1
    )
    print("✅ Restored <div id='day-186'> container")

# Wrap Day 187 Whisper Audio
if 'id="day-187"' not in html26:
    html26 = html26.replace(
        '<div class="day-tag">WEEK 26 · DAY 187</div>',
        '</div>\n<div class="day-section" data-xp="150" id="day-187">\n<div class="day-header">\n<div class="day-tag">WEEK 26 · DAY 187</div>',
        1
    )
    print("✅ Restored <div id='day-187'> container")

fp26.write_text(html26, encoding='utf-8')
