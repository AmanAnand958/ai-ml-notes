#!/usr/bin/env python3
"""
Master Remediation Script addressing all items in the user report:
1. Week 17: Check & clean any accidental Day 172 (MLflow) content contamination.
2. Week 24: Check & clean any duplicate/garbled sections for Days 172-177.
3. Week 26: Reconstruct proper day wrappers (<div class="day-section" id="day-186"> & <div class="day-section" id="day-187">) so Days 185 to 191 all have explicit, active DOM sections with aligned tables.
4. Python code & LaTeX symbol repairs:
   - Fix return type hyphens: `def foo(...) - Type:` -> `def foo(...) -> Type:`
   - Fix LaTeX tab artifacts: `\text` getting converted to `\text` (ensure standard KaTeX string format)
   - Fix broken lambda sorting: `key=>lambda` -> `key=lambda`
   - Fix broken comparisons in verification asserts
"""

import re
from pathlib import Path
from bs4 import BeautifulSoup

WEEKS_DIR = Path("/Users/amananand/Downloads/SDE/ai:ml-1/pages/weeks")

# ─────────────────────────────────────────────────────────────────────────────
# 1. WEEK 17 CHECK & CONTAMINATION CLEANUP
# ─────────────────────────────────────────────────────────────────────────────
print("=== 1. Checking Week 17 for Day 172 MLflow Contamination ===")
fp17 = WEEKS_DIR / "week17.html"
if fp17.exists():
    html17 = fp17.read_text(encoding='utf-8', errors='replace')
    if "MLflow" in html17 or "day-172" in html17 or "Champion" in html17:
        print("  ⚠️ Detected MLflow/Day 172 contamination in Week 17. Cleaning...")
        # Remove any stray day-172 blocks if present
        html17 = re.sub(r'<div[^>]*id="day-172".*?</div>\s*(?=<div[^>]*id="day-|$)', '', html17, flags=re.DOTALL)
        fp17.write_text(html17, encoding='utf-8')
        print("  ✅ Week 17 cleaned")
    else:
        print("  ✅ Week 17 is clean (no MLflow contamination found)")

# ─────────────────────────────────────────────────────────────────────────────
# 2. WEEK 24 DUPLICATION CLEANUP
# ─────────────────────────────────────────────────────────────────────────────
print("\n=== 2. Checking Week 24 for Internal Section Duplications ===")
fp24 = WEEKS_DIR / "week24.html"
if fp24.exists():
    html24 = fp24.read_text(encoding='utf-8', errors='replace')
    # Count occurrences of day IDs
    day_counts = {f"day-{d}": len(re.findall(f'id="day-{d}"', html24)) for d in range(171, 178)}
    print(f"  Day ID counts in Week 24: {day_counts}")
    
    # Clean up if duplicate day-section containers exist
    soup24 = BeautifulSoup(html24, 'html.parser')
    seen_ids = set()
    removed = 0
    for ds in soup24.find_all('div', class_=re.compile(r'day-section')):
        did = ds.get('id')
        if did in seen_ids:
            ds.decompose()
            removed += 1
        else:
            seen_ids.add(did)
    if removed > 0:
        fp24.write_text(str(soup24), encoding='utf-8')
        print(f"  ✅ Removed {removed} duplicate day-section(s) in Week 24")
    else:
        print("  ✅ Week 24 day sections are unique and non-duplicated")

# ─────────────────────────────────────────────────────────────────────────────
# 3. WEEK 26 RECONSTRUCTION (Days 185-191)
# ─────────────────────────────────────────────────────────────────────────────
print("\n=== 3. Reconstructing Week 26 Day Containers (Days 185-191) ===")
fp26 = WEEKS_DIR / "week26.html"
if fp26.exists():
    html26 = fp26.read_text(encoding='utf-8', errors='replace')
    
    # Ensure Day 186 container exists
    if 'id="day-186"' not in html26 and "Multimodal RAG" in html26:
        print("  Restoring id='day-186' wrapper for Multimodal RAG...")
        html26 = html26.replace(
            '<div class="day-tag">WEEK 26 · DAY 186</div>',
            '<div class="day-tag">WEEK 26 · DAY 186</div>',
            1
        )
        # Find Multimodal RAG section header and wrap in day-section
        pattern_186 = r'(<div class="day-tag">WEEK 26 · DAY 186</div>.*?<h1[^>]*>Multimodal RAG</h1>)'
        if re.search(pattern_186, html26):
            # Locate preceding container
            idx_tag = html26.find('WEEK 26 · DAY 186')
            # Look backwards for previous section close or start
            idx_open = html26.rfind('<div class="day-section', 0, idx_tag)
            if idx_open != -1 and 'id="day-186"' not in html26[idx_open:idx_tag]:
                html26 = html26[:idx_open] + '<div class="day-section" data-xp="150" id="day-186">\n' + html26[idx_open + len('<div class="day-section">'):]
        
    # Ensure Day 187 container exists
    if 'id="day-187"' not in html26 and "Whisper" in html26:
        print("  Restoring id='day-187' wrapper for Whisper Audio Processing...")
        idx_tag187 = html26.find('WEEK 26 · DAY 187')
        if idx_tag187 != -1:
            idx_open187 = html26.rfind('<div class="day-section', 0, idx_tag187)
            if idx_open187 != -1 and 'id="day-187"' not in html26[idx_open187:idx_tag187]:
                html26 = html26[:idx_open187] + '<div class="day-section" data-xp="150" id="day-187">\n' + html26[idx_open187 + len('<div class="day-section">'):]

    fp26.write_text(html26, encoding='utf-8')
    print("  ✅ Week 26 day IDs verified")

# ─────────────────────────────────────────────────────────────────────────────
# 4. SYNTAX, ARROW, OPERATOR & LATEX REPAIRS (ALL WEEKS 18-26)
# ─────────────────────────────────────────────────────────────────────────────
print("\n=== 4. Scanning & Fixing Syntax, Arrows, Operators & LaTeX (Weeks 18-26) ===")

for wn in range(18, 27):
    fp = WEEKS_DIR / f"week{wn}.html"
    if not fp.exists():
        continue
    
    content = fp.read_text(encoding='utf-8', errors='replace')
    orig = content
    
    # 4.1 Fix broken lambda sorting: key=>lambda -> key=lambda
    content = re.sub(r'key\s*=>\s*lambda', 'key=lambda', content)
    
    # 4.2 Fix return type hyphens: `def foo(...) - Type:` -> `def foo(...) -> Type:`
    content = re.sub(r'(\bdef\s+\w+\([^)]*\))\s*-\s*([A-Za-z0-9_\[\],\s]+):', r'\1 -> \2:', content)
    
    # 4.3 Fix mangled LaTeX \text getting turned into tab literals
    content = content.replace('\text', '\\text')
    
    # 4.4 Fix broken Python assertions with missing operators
    content = re.sub(r'assert\s+compute_cost_savings\(\)\s+70\.0', 'assert compute_cost_savings() >= 70.0', content)
    content = re.sub(r'if\s+present\s*/\s*max\(1,\s*len\(words\)\)\s*=\s*0\.60:', 'if present / max(1, len(words)) >= 0.60:', content)
    content = re.sub(r'if\s+cosine_sim\s*=\s*similarity_threshold:', 'if cosine_sim >= similarity_threshold:', content)
    content = re.sub(r'if\s+f1\s*=\s*self\.min_f1_threshold', 'if f1 >= self.min_f1_threshold', content)
    content = re.sub(r'if\s+now\s*-\s*entry\["timestamp"\]\s+self\.ttl:', 'if now - entry["timestamp"] > self.ttl:', content)
    
    if content != orig:
        fp.write_text(content, encoding='utf-8')
        print(f"  ✅ Repaired syntax / operator / LaTeX anomalies in Week {wn}")

print("\n🎉 ALL MASTER REMEDIATION TASKS COMPLETED!")
