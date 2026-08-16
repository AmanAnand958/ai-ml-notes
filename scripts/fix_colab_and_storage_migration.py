#!/usr/bin/env python3
"""
Step 3: 
1. Remove Colab buttons from non-Python code cards (bash, shell, sql, yaml, dockerfile).
2. Add automatic legacy wX-state key migration to courseState in assets/js/course.js.
"""

from pathlib import Path
from bs4 import BeautifulSoup
import re

WEEKS_DIR = Path("pages/weeks")
ROOT_DIR = Path(".")

# 1. Clean non-Python Colab buttons
for wn in range(1, 27):
    fp = WEEKS_DIR / f"week{wn}.html"
    if not fp.exists(): continue
    soup = BeautifulSoup(fp.read_text(encoding='utf-8'), 'html.parser')
    modified = False
    
    for cb in soup.find_all('div', class_='cb'):
        lang = cb.find('span', class_='cb-lang')
        lang_text = lang.text.strip().lower() if lang else 'python'
        
        if lang_text in ['bash', 'shell', 'yaml', 'json', 'sql', 'dockerfile', 'pseudocode']:
            colab_btn = cb.find('button', onclick=re.compile(r'openInColab'))
            if colab_btn:
                colab_btn.extract()
                modified = True
                
    if modified:
        fp.write_text(str(soup), encoding='utf-8')
        print(f"  ✅ Removed non-Python Colab buttons in Week {wn}")

# 2. Add legacy migration to courseState in course.js
fp_js = ROOT_DIR / "assets" / "js" / "course.js"
js = fp_js.read_text(encoding='utf-8')

if "migrateLegacyState" not in js:
    migration_logic = """
  // Auto-migrate legacy wX-state keys into canonical courseState
  try {
    for (let i = 1; i <= 26; i++) {
      const legKey = `w${i}-state`;
      const legVal = localStorage.getItem(legKey);
      if (legVal) {
        const parsed = JSON.parse(legVal);
        if (parsed.done && Array.isArray(parsed.done)) {
          parsed.done.forEach(d => {
            const dayKey = String(d);
            if (!this.state.completedDays[dayKey]) {
              this.state.completedDays[dayKey] = {
                completedAt: new Date().toISOString(),
                xpAwarded: 150
              };
            }
          });
        }
        if (typeof parsed.xp === 'number' && parsed.xp > this.state.totalXP) {
          this.state.totalXP = parsed.xp;
        }
      }
    }
  } catch(e) {}
"""
    # Insert inside load() method in courseState
    idx_load = js.find("load() {")
    if idx_load != -1:
        idx_brace = js.find("try {", idx_load)
        if idx_brace != -1:
            js = js[:idx_brace] + migration_logic + js[idx_brace:]
            fp_js.write_text(js, encoding='utf-8')
            print("✅ Injected legacy state auto-migration into assets/js/course.js!")

print("\n🎉 STEP 3 COMPLETE: NON-PYTHON COLAB BUTTONS CLEANED & LEGACY STORAGE FULLY COMPATIBLE!")
