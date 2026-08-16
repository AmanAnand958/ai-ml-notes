#!/usr/bin/env python3
"""
Fix quiz feedback ID bindings in Week 26:
Ensures that the third argument in onclick="quiz(this, 'correct/wrong', 'ID')"
matches the feedback container IDs (<div class="quiz-feedback" id="ID-correct"> / id="ID-wrong">).
"""

from pathlib import Path
from bs4 import BeautifulSoup
import re

fp26 = Path("pages/weeks/week26.html")
soup26 = BeautifulSoup(fp26.read_text(encoding='utf-8'), 'html.parser')

for qb in soup26.find_all('div', class_='quiz-block'):
    # Find all options
    opts = qb.find_all('div', class_='quiz-opt')
    if not opts: continue
    
    # Extract the ID used in the first option
    first_opt = opts[0]
    m = re.search(r"quiz\s*\(\s*this\s*,\s*['\"](?:correct|wrong)['\"]\s*,\s*['\"]([^'\"]+)['\"]", first_opt.get('onclick', ''))
    if m:
        target_id = m.group(1)
        
        # Ensure feedback containers in this quiz block have this exact target_id
        fb_correct = qb.find(class_=re.compile(r'correct'))
        for fb in qb.find_all('div', class_='quiz-feedback'):
            if 'correct' in str(fb.get('class', '')) or 'correct' in fb.get('id', ''):
                fb['id'] = f"{target_id}-correct"
            elif 'wrong' in str(fb.get('class', '')) or 'wrong' in fb.get('id', ''):
                fb['id'] = f"{target_id}-wrong"

fp26.write_text(str(soup26), encoding='utf-8')
print("✅ Fixed Week 26 quiz feedback IDs!")
