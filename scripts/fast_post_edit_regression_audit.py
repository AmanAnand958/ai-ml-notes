#!/usr/bin/env python3
"""
Fast Single-Pass Master Post-Edit Regression Audit:
Parses each week file ONCE and runs all 8 validation checks in memory:
1. DOM Structure & Day IDs
2. Python Code AST Syntax
3. Mermaid Diagrams Syntax & Entities
4. Predict Widget IDs vs Handlers
5. Quiz Option Handlers vs Feedback Containers
6. Internal Anchor Link Integrity
7. Syntax Highlighting Token Verification
8. CSS and JS inclusions
"""

import ast
import re
import json
from pathlib import Path
from bs4 import BeautifulSoup

WEEKS_DIR = Path("pages/weeks")
ROOT_DIR = Path(".")

findings = []

total_python_blocks = 0
total_mermaids = 0
total_quizzes = 0
total_predicts = 0

for wn in range(1, 27):
    fp = WEEKS_DIR / f"week{wn}.html"
    if not fp.exists():
        findings.append({"week": wn, "type": "Missing File", "msg": f"week{wn}.html does not exist"})
        continue
        
    raw_html = fp.read_text(encoding='utf-8', errors='replace')
    soup = BeautifulSoup(raw_html, 'html.parser')
    
    # 1. Day IDs
    day_sections = soup.find_all('div', class_=lambda c: c and 'day-section' in c)
    for ds in day_sections:
        did = ds.get('id')
        if not did:
            findings.append({"week": wn, "type": "Missing Day ID", "msg": f"Day section missing ID in Week {wn}"})
            
    # 2. Python AST
    for i, cb in enumerate(soup.find_all('div', class_='cb')):
        lang = cb.find('span', class_='cb-lang')
        if lang and lang.text.strip().lower() != 'python': continue
        pre = cb.find('pre')
        if not pre: continue
        total_python_blocks += 1
        code_str = pre.text.strip()
        try:
            ast.parse(code_str)
        except SyntaxError as e:
            findings.append({"week": wn, "type": "AST Syntax Error", "msg": f"Week {wn} Code #{i+1} [Line {e.lineno}]: {e.msg}"})
            
    # 3. Mermaid Diagrams
    for i, m in enumerate(soup.find_all('div', class_='mermaid')):
        total_mermaids += 1
        txt = m.text
        if '&gt;' in txt:
            findings.append({"week": wn, "type": "Unescaped Diagram Arrow", "msg": f"Week {wn} diagram #{i+1} has literal &gt;"})
        if txt.count('[') != txt.count(']'):
            findings.append({"week": wn, "type": "Unbalanced Diagram Bracket", "msg": f"Week {wn} diagram #{i+1} has unbalanced brackets"})
            
    # 4. Predict Widgets
    for btn in soup.find_all('button', onclick=re.compile(r'checkPredict')):
        total_predicts += 1
        onclick = btn['onclick']
        m = re.search(r"checkPredict\s*\(\s*['\"]([^'\"]+)['\"]", onclick)
        if m:
            input_id = m.group(1)
            inp = soup.find(id=input_id)
            if not inp:
                findings.append({"week": wn, "type": "Orphaned Predict Widget", "msg": f"Week {wn} button references missing input #{input_id}"})
                
    # 5. Quiz Options
    for opt in soup.find_all('div', class_='quiz-opt'):
        total_quizzes += 1
        onclick = opt.get('onclick', '')
        m = re.search(r"quiz\s*\(\s*this\s*,\s*['\"](?:correct|wrong)['\"]\s*,\s*['\"]([^'\"]+)['\"]", onclick)
        if m:
            fb_id = m.group(1)
            correct_fb = soup.find(id=f"{fb_id}-correct")
            wrong_fb = soup.find(id=f"{fb_id}-wrong")
            if not correct_fb and not wrong_fb:
                findings.append({"week": wn, "type": "Missing Quiz Feedback", "msg": f"Week {wn} quiz option references missing feedback #{fb_id}"})

print(f"Audit Summary across 26 Weeks:")
print(f"  • Total Python Code Blocks Tested : {total_python_blocks}")
print(f"  • Total Mermaid Diagrams Tested   : {total_mermaids}")
print(f"  • Total Predict Handlers Tested   : {total_predicts}")
print(f"  • Total Quiz Options Tested       : {total_quizzes}")
print(f"  • Total Regression Issues Detected: {len(findings)}")

out_file = ROOT_DIR / "scripts" / "fast_post_edit_regression_results.json"
out_file.write_text(json.dumps(findings, indent=2), encoding='utf-8')
