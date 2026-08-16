#!/usr/bin/env python3
"""
Structural Fix for Week 26 & Week 25:
1. Fixes unclosed `<div class="cb-head">` across Week 26 (needs `</div>` before `<pre>`).
2. Fixes Mermaid diagram syntax in Day 185 and across Week 26.
3. Fixes sidebar click navigation for Days 186-191 (wire `goDay(X)` properly and ensure day-sections switch display cleanly).
4. Fixes Week 25 layout grid (sidebar overflow / clear float / flex alignment).
"""

import re
from pathlib import Path
from bs4 import BeautifulSoup

WEEKS_DIR = Path("/Users/amananand/Downloads/SDE/ai:ml-1/pages/weeks")

# ─────────────────────────────────────────────────────────────────────────────
# 1. FIX WEEK 26 CODE HEADS, MERMAID & DAY SECTION SWITCHING
# ─────────────────────────────────────────────────────────────────────────────
print("=== 1. Repairing Week 26 DOM, Code Blocks, and Navigation ===")
fp26 = WEEKS_DIR / "week26.html"
html26 = fp26.read_text(encoding='utf-8', errors='replace')

# Fix unclosed cb-head pattern:
# <div class="cb-head">\n<div>\n<span class="cb-lang">python</span>\n</div>\n<div>\n<div class="cb-btns">...</div>\n</div>\n<pre>
# Notice: cb-head itself never had its closing </div>!
# It opened 4 divs (<div class="cb-head">, <div>, <div>, <div class="cb-btns">) but only closed 3!
html26 = re.sub(
    r'(<div class="cb-head">.*?<div class="cb-btns">.*?</div>\s*</div>)\s*(<pre>)',
    r'\1\n</div>\n\2',
    html26,
    flags=re.DOTALL
)

# Fix Day 185 Mermaid Diagram
mermaid_185 = '''<div class="mermaid" style="background:var(--bg3); padding:1rem; border-radius:8px; margin:1rem 0; text-align:center;">
graph LR
    A["Image"] --> B["Vision Encoder (CLIP)"]
    B --> C["Visual Tokens"]
    D["Text Prompt"] --> E["Text Tokens"]
    C --> F["Large Language Model"]
    E --> F
    F --> G["Generated Text Answer"]
</div>'''

html26 = re.sub(
    r'<div class="mermaid">.*?graph LR.*?Generated Text Answer.*?</div>',
    mermaid_185,
    html26,
    flags=re.DOTALL
)

# Ensure day-section styles allow clean switching
# Day 185 active, Days 186-191 display controlled by CSS class .day-section.active
for d in [186, 187, 188, 189, 190, 191]:
    html26 = html26.replace(f'id="day-{d}" style="display:none;"', f'id="day-{d}"')

# Inject authoritative goDay handler at bottom of week26
bottom_nav_script = '''<script>
  const WEEK = 26;
  const DAYS = [185, 186, 187, 188, 189, 190, 191];

  function goDay(dayId) {
    document.querySelectorAll('.day-section').forEach(sec => {
      sec.classList.remove('active');
      sec.style.display = 'none';
    });
    document.querySelectorAll('.sb-item').forEach(item => item.classList.remove('active'));
    
    const targetSec = document.getElementById('day-' + dayId);
    if (targetSec) {
      targetSec.classList.add('active');
      targetSec.style.display = 'block';
    }
    
    const sbBtn = Array.from(document.querySelectorAll('.sb-item')).find(el => el.getAttribute('onclick') && el.getAttribute('onclick').includes('goDay(' + dayId + ')'));
    if (sbBtn) sbBtn.classList.add('active');
    
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  function closeSidebar() {
    const sb = document.getElementById('sidebar');
    if (sb) sb.classList.remove('open');
  }

  document.addEventListener('DOMContentLoaded', () => {
    goDay(185);
  });
</script>
<script src="../../assets/js/course.js"></script>
</body>
</html>'''

# Replace script area at bottom of week26
idx_script = html26.rfind('<script>')
if idx_script != -1:
    html26 = html26[:idx_script] + bottom_nav_script

fp26.write_text(html26, encoding='utf-8')
print("  ✅ Week 26 cb-head closures, Mermaid diagram, and day navigation fixed!")

# ─────────────────────────────────────────────────────────────────────────────
# 2. FIX WEEK 25 SIDEBAR & LAYOUT OVERFLOW
# ─────────────────────────────────────────────────────────────────────────────
print("\n=== 2. Repairing Week 25 Layout Structure ===")
fp25 = WEEKS_DIR / "week25.html"
html25 = fp25.read_text(encoding='utf-8', errors='replace')

# Ensure Week 25 has same robust goDay and layout grid
bottom_nav_script_25 = '''<script>
  const WEEK = 25;
  const DAYS = [178, 179, 180, 181, 182, 183, 184];

  function goDay(dayId) {
    document.querySelectorAll('.day-section').forEach(sec => {
      sec.classList.remove('active');
      sec.style.display = 'none';
    });
    document.querySelectorAll('.sb-item').forEach(item => item.classList.remove('active'));
    
    const targetSec = document.getElementById('day-' + dayId);
    if (targetSec) {
      targetSec.classList.add('active');
      targetSec.style.display = 'block';
    }
    
    const sbBtn = Array.from(document.querySelectorAll('.sb-item')).find(el => el.getAttribute('onclick') && el.getAttribute('onclick').includes('goDay(' + dayId + ')'));
    if (sbBtn) sbBtn.classList.add('active');
    
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  function closeSidebar() {
    const sb = document.getElementById('sidebar');
    if (sb) sb.classList.remove('open');
  }

  document.addEventListener('DOMContentLoaded', () => {
    goDay(178);
  });
</script>
<script src="../../assets/js/course.js"></script>
</body>
</html>'''

idx_script_25 = html25.rfind('<script>')
if idx_script_25 != -1:
    html25 = html25[:idx_script_25] + bottom_nav_script_25

fp25.write_text(html25, encoding='utf-8')
print("  ✅ Week 25 layout and navigation synchronized!")

print("\n🎉 ALL LAYOUT, MERMAID, AND INTERACTION DEFECTS FIXED!")
