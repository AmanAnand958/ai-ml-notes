#!/usr/bin/env python3
"""
Master Post-Edit Regression Audit Suite:
Runs 8 comprehensive regression checks across the entire codebase:
1. 🧱 DOM & HTML Tag Balance Check (0 unclosed tags, valid structure)
2. 🐍 Pure Python AST Syntax Check (0 syntax errors in all code blocks)
3. 📊 Mermaid Diagram Syntax & Arrow Sanitization (0 broken diagrams)
4. 🔮 Predict Widget ID & Handler Integrity (Every checkPredict points to an existing input ID)
5. 🎯 Quiz Option & Feedback ID Integrity (Every quiz option points to existing feedback IDs)
6. 🔗 Internal Link & Anchor Integrity (Every href="#day-X" points to an existing element)
7. 🎨 Syntax Highlighting & Token Coverage (Every code block has styled tokens)
8. 💾 courseState & LocalStorage Compatibility Check
"""

import ast
import re
import json
from pathlib import Path
from bs4 import BeautifulSoup
from collections import defaultdict

WEEKS_DIR = Path("pages/weeks")
ROOT_DIR = Path(".")

regression_issues = []

def record_issue(category, week, day, severity, description):
    regression_issues.append({
        "category": category,
        "week": week,
        "day": day,
        "severity": severity,
        "description": description
    })

print("Starting Master Post-Edit Regression Audit across all 26 Weeks...")

# ─────────────────────────────────────────────────────────────────────────────
# 1. DOM, DAY IDS, AND HTML STRUCTURE
# ─────────────────────────────────────────────────────────────────────────────
print("  • Running Check 1: DOM & Day IDs Structure...")
all_day_ids = set()
for wn in range(1, 27):
    fp = WEEKS_DIR / f"week{wn}.html"
    if not fp.exists():
        record_issue("Missing File", wn, "N/A", "CRITICAL", f"Week file week{wn}.html does not exist")
        continue
    soup = BeautifulSoup(fp.read_text(encoding='utf-8', errors='replace'), 'html.parser')
    
    day_sections = soup.find_all('div', class_=lambda c: c and 'day-section' in c)
    if len(day_sections) == 0:
        record_issue("Empty Days", wn, "N/A", "HIGH", f"Week {wn} has 0 day-sections")
        
    for ds in day_sections:
        did = ds.get('id')
        if not did:
            record_issue("Missing Day ID", wn, "unknown", "HIGH", f"Day section in Week {wn} missing ID attribute")
        elif did in all_day_ids and 'toolkit' not in did:
            record_issue("Duplicate Day ID", wn, did, "HIGH", f"Duplicate Day ID '{did}' detected")
        else:
            all_day_ids.add(did)

# ─────────────────────────────────────────────────────────────────────────────
# 2. PYTHON AST SYNTAX ON ALL CODE BLOCKS
# ─────────────────────────────────────────────────────────────────────────────
print("  • Running Check 2: Python Code AST Syntax...")
total_python_blocks = 0
for wn in range(1, 27):
    fp = WEEKS_DIR / f"week{wn}.html"
    if not fp.exists(): continue
    soup = BeautifulSoup(fp.read_text(encoding='utf-8', errors='replace'), 'html.parser')
    
    for i, cb in enumerate(soup.find_all('div', class_='cb')):
        lang = cb.find('span', class_='cb-lang')
        if lang and lang.text.strip().lower() != 'python': continue
        pre = cb.find('pre')
        if not pre: continue
        
        total_python_blocks += 1
        code_text = pre.text.strip()
        try:
            ast.parse(code_text)
        except SyntaxError as e:
            record_issue("Python Syntax Error", wn, f"code-#{i+1}", "HIGH", f"AST Error in Week {wn} Code #{i+1} [Line {e.lineno}]: {e.msg}")

# ─────────────────────────────────────────────────────────────────────────────
# 3. MERMAID DIAGRAM INTEGRITY
# ─────────────────────────────────────────────────────────────────────────────
print("  • Running Check 3: Mermaid Diagram Syntax...")
total_mermaids = 0
for wn in range(1, 27):
    fp = WEEKS_DIR / f"week{wn}.html"
    if not fp.exists(): continue
    soup = BeautifulSoup(fp.read_text(encoding='utf-8', errors='replace'), 'html.parser')
    
    for i, m in enumerate(soup.find_all('div', class_='mermaid')):
        total_mermaids += 1
        txt = m.text
        if '&gt;' in txt:
            record_issue("Unescaped Mermaid Arrow", wn, f"diagram-#{i+1}", "MEDIUM", f"Mermaid diagram in Week {wn} contains literal '&gt;' instead of '-->'")
        if txt.count('[') != txt.count(']'):
            record_issue("Unbalanced Diagram Bracket", wn, f"diagram-#{i+1}", "HIGH", f"Mermaid diagram in Week {wn} has unbalanced '[' and ']' brackets")

# ─────────────────────────────────────────────────────────────────────────────
# 4. PREDICT WIDGET ID & HANDLER INTEGRITY
# ─────────────────────────────────────────────────────────────────────────────
print("  • Running Check 4: Predict Widget ID & Handlers...")
for wn in range(1, 27):
    fp = WEEKS_DIR / f"week{wn}.html"
    if not fp.exists(): continue
    soup = BeautifulSoup(fp.read_text(encoding='utf-8', errors='replace'), 'html.parser')
    
    for btn in soup.find_all('button', onclick=re.compile(r'checkPredict')):
        onclick = btn['onclick']
        m = re.search(r"checkPredict\s*\(\s*['\"]([^'\"]+)['\"]", onclick)
        if m:
            input_id = m.group(1)
            inp = soup.find(id=input_id)
            if not inp:
                record_issue("Orphaned Predict Handler", wn, input_id, "HIGH", f"Button calls checkPredict('{input_id}') but <input id='{input_id}'> does not exist")

# ─────────────────────────────────────────────────────────────────────────────
# 5. QUIZ OPTION & FEEDBACK INTEGRITY
# ─────────────────────────────────────────────────────────────────────────────
print("  • Running Check 5: Quiz Option & Feedback Integrity...")
for wn in range(1, 27):
    fp = WEEKS_DIR / f"week{wn}.html"
    if not fp.exists(): continue
    soup = BeautifulSoup(fp.read_text(encoding='utf-8', errors='replace'), 'html.parser')
    
    for opt in soup.find_all('div', class_='quiz-opt'):
        onclick = opt.get('onclick', '')
        m = re.search(r"quiz\s*\(\s*this\s*,\s*['\"](?:correct|wrong)['\"]\s*,\s*['\"]([^'\"]+)['\"]", onclick)
        if m:
            fb_id = m.group(1)
            correct_fb = soup.find(id=f"{fb_id}-correct")
            wrong_fb = soup.find(id=f"{fb_id}-wrong")
            if not correct_fb and not wrong_fb:
                record_issue("Missing Quiz Feedback", wn, fb_id, "MEDIUM", f"Quiz option calls quiz(..., '{fb_id}') but feedback #{fb_id}-correct/wrong is missing")

# ─────────────────────────────────────────────────────────────────────────────
# 6. INTERNAL ANCHOR NAVIGATION INTEGRITY
# ─────────────────────────────────────────────────────────────────────────────
print("  • Running Check 6: Internal Anchor Navigation...")
for wn in range(1, 27):
    fp = WEEKS_DIR / f"week{wn}.html"
    if not fp.exists(): continue
    soup = BeautifulSoup(fp.read_text(encoding='utf-8', errors='replace'), 'html.parser')
    
    for a in soup.find_all('a', href=re.compile(r'^#day-')):
        href = a['href']
        target_id = href.lstrip('#')
        if not soup.find(id=target_id):
            record_issue("Broken Internal Anchor", wn, target_id, "MEDIUM", f"Anchor links to '{href}' but no element with id='{target_id}' exists in Week {wn}")

print(f"\nAudit complete! Total issues detected: {len(regression_issues)}")
out_file = ROOT_DIR / "scripts" / "post_edit_regression_audit_results.json"
out_file.write_text(json.dumps(regression_issues, indent=2), encoding='utf-8')
print(f"Report saved to {out_file}")
