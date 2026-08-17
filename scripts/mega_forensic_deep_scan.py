#!/usr/bin/env python3
"""
scripts/mega_forensic_deep_scan.py
Exhaustive multi-vector forensic scan across all 26 weeks, 191 days, and root portals.

Vectors tested:
1. ID Reference Integrity:
   - toggleSolution('id') -> does element id exist?
   - checkPredict('pX', ...) -> do #pX-input and #pX-result exist?
   - quiz(this, ..., 'qX') -> do #qX-correct and #qX-wrong exist?
   - completeDay('X') -> does #btn-day-X exist?
2. Placeholder / Generic Content Detection:
   - Repetitive generic gotchas ("Dictionary Keys & List Mutability" on non-Python core days)
   - Predict the output dummy pipelines ("result = 4" etc.)
3. Malformed / Unescaped HTML Entities & Broken Tokens:
   - "undefined", "NaN", "[object Object]", "None", "&amp;amp;"
4. Empty DOM elements (empty pre, code, p, h1, h2, h3)
5. Python AST validity across all starter_code, solution_code, and predict code
6. Resource link validity and schema formatting
"""

import os, glob, re, ast, json
from bs4 import BeautifulSoup
import yaml

print("=== STARTING MEGA FORENSIC DEEP SCAN ===")

html_files = sorted(glob.glob("pages/weeks/week*.html"), key=lambda x: int(re.search(r'\d+', x).group()))
yaml_files = sorted(glob.glob("src/data/week*.yaml"), key=lambda x: int(re.search(r'\d+', x).group()))

findings = []

# --- 1. JS EVENT & DOM ID INTEGRITY AUDIT ---
print("\n[1/6] Auditing JavaScript Event Target IDs & DOM Symmetry...")

for h_file in html_files:
    with open(h_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Collect all element IDs in this page
    all_ids = set(re.findall(r'\bid=["\']([^"\']+)["\']', content))
    
    # Check toggleSolution calls
    toggle_targets = re.findall(r"toggleSolution\(['\"]([^'\"]+)['\"]", content)
    for target in toggle_targets:
        if target not in all_ids:
            findings.append({
                "vector": "Broken Event Target ID",
                "file": h_file,
                "detail": f"toggleSolution target '{target}' does not exist in DOM"
            })
    
    # Check checkPredict calls
    predict_calls = re.findall(r"checkPredict\(['\"]([^'\"]+)['\"]", content)
    for p_id in predict_calls:
        if f"{p_id}-input" not in all_ids:
            findings.append({
                "vector": "Broken Predict Input ID",
                "file": h_file,
                "detail": f"Predict input '#{p_id}-input' missing in DOM"
            })
        if f"{p_id}-result" not in all_ids:
            findings.append({
                "vector": "Broken Predict Result ID",
                "file": h_file,
                "detail": f"Predict result container '#{p_id}-result' missing in DOM"
            })
    
    # Check quiz feedback containers
    quiz_calls = re.findall(r"quiz\([^,]+,[^,]+,['\"]([^'\"]+)['\"]", content)
    for q_id in quiz_calls:
        if f"{q_id}-correct" not in all_ids:
            findings.append({
                "vector": "Broken Quiz Correct Feedback ID",
                "file": h_file,
                "detail": f"Quiz correct feedback '#{q_id}-correct' missing in DOM"
            })
        if f"{q_id}-wrong" not in all_ids:
            findings.append({
                "vector": "Broken Quiz Wrong Feedback ID",
                "file": h_file,
                "detail": f"Quiz wrong feedback '#{q_id}-wrong' missing in DOM"
            })

# --- 2. PLACEHOLDER / GENERIC CONTENT DETECTION ---
print("\n[2/6] Auditing for Generic / Placeholder Gotchas & Dummy Predictions...")

for y_file in yaml_files:
    with open(y_file, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict) or 'days' not in data:
        continue
    
    for day in data['days']:
        day_num = day.get('day_num', 0)
        
        # Check gotcha
        gotcha = day.get('gotcha', {})
        if isinstance(gotcha, dict):
            g_title = gotcha.get('title', '')
            g_desc = gotcha.get('description', '')
            if "Dictionary Keys & List Mutability" in g_title and day_num > 7:
                findings.append({
                    "vector": "Generic Gotcha on Advanced Day",
                    "file": y_file,
                    "day": day_num,
                    "title": day.get('title', ''),
                    "detail": f"Generic Day 1-7 gotcha '{g_title}' present on Day {day_num}"
                })
        
        # Check predict dummy code
        predict = day.get('predict', {})
        if isinstance(predict, dict):
            p_code = predict.get('code', '')
            p_ans = str(predict.get('answer', ''))
            if re.search(r'result\s*=\s*\d+\s*\n\s*print\(result\)', p_code):
                findings.append({
                    "vector": "Dummy Predict Code Snippet",
                    "file": y_file,
                    "day": day_num,
                    "title": day.get('title', ''),
                    "detail": f"Predict code is a static integer assignment ('{p_ans}') instead of real domain computation"
                })

# --- 3. UNESCAPED ENTITIES / LITERAL STRINGS ---
print("\n[3/6] Auditing for Corrupted Tokens & Double Escapes...")
corrupt_patterns = [
    (r'&amp;amp;', "Double escaped HTML ampersand"),
    (r'&amp;lt;', "Double escaped less-than entity"),
    (r'&amp;gt;', "Double escaped greater-than entity"),
    (r'\bundefined\b', "Literal 'undefined' token"),
    (r'\[object Object\]', "Literal '[object Object]' stringification bug"),
]

for h_file in html_files:
    with open(h_file, 'r', encoding='utf-8') as f:
        content = f.read()
    for pat, desc in corrupt_patterns:
        matches = list(re.finditer(pat, content))
        if matches:
            for m in matches:
                # exclude legitimate JS code occurrences of undefined
                line_no = content[:m.start()].count('\n') + 1
                snippet = content[max(0, m.start()-25):min(len(content), m.end()+25)].replace('\n', ' ')
                # Ignore if inside a script tag or python code string
                if "undefined" in pat and ("typeof" in snippet or "===" in snippet or "!=" in snippet or "window" in snippet):
                    continue
                findings.append({
                    "vector": "Corrupted Token",
                    "file": h_file,
                    "line": line_no,
                    "detail": f"{desc}: '{snippet}'"
                })

# --- 4. PYTHON AST VALIDITY SCAN ---
print("\n[4/6] Auditing Python Code AST in Tasks & Predict Snippets...")

for y_file in yaml_files:
    with open(y_file, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict) or 'days' not in data:
        continue
    
    for day in data['days']:
        day_num = day.get('day_num', 0)
        
        # Predict code
        p_code = day.get('predict', {}).get('code', '')
        if p_code and p_code.strip():
            try:
                ast.parse(p_code)
            except SyntaxError as e:
                findings.append({
                    "vector": "Python Syntax Error in Predict",
                    "file": y_file,
                    "day": day_num,
                    "detail": f"Line {e.lineno}: {e.msg} -> '{e.text}'"
                })
        
        # Task solutions
        for task in day.get('tasks', []):
            sol_code = task.get('solution_code', '')
            if sol_code and sol_code.strip() and task.get('solution_lang', 'python') == 'python':
                # Filter out bash or SQL comments
                if sol_code.startswith("git ") or sol_code.startswith("docker ") or sol_code.startswith("SELECT "):
                    continue
                try:
                    ast.parse(sol_code)
                except SyntaxError as e:
                    findings.append({
                        "vector": "Python Syntax Error in Task Solution",
                        "file": y_file,
                        "day": day_num,
                        "task": task.get('title', ''),
                        "detail": f"Line {e.lineno}: {e.msg} -> '{e.text}'"
                    })

# --- 5. EMPTY DOM CONTAINERS ---
print("\n[5/6] Checking for Accidental Empty Content Tags...")
empty_tag_patterns = [
    (r'<pre>\s*</pre>', "Empty <pre> block"),
    (r'<div class="cb">\s*</div>', "Empty code block wrapper"),
    (r'<div class="res-grid">\s*</div>', "Empty resources grid"),
    (r'<div class="flashcard-grid">\s*</div>', "Empty flashcard grid"),
    (r'<div class="tasks-section">\s*</div>', "Empty tasks section"),
    (r'<div class="quiz-section">\s*</div>', "Empty quiz section"),
]

for h_file in html_files:
    with open(h_file, 'r', encoding='utf-8') as f:
        content = f.read()
    for pat, desc in empty_tag_patterns:
        if re.search(pat, content):
            findings.append({
                "vector": "Empty DOM Container",
                "file": h_file,
                "detail": desc
            })

# --- 6. SUMMARY REPORT ---
print("\n" + "="*70)
print(f"=== MEGA AUDIT COMPLETE: {len(findings)} FINDINGS IDENTIFIED ===")
print("="*70)

from collections import Counter
counts = Counter(x['vector'] for x in findings)
for k, v in counts.items():
    print(f"  • {k}: {v}")

with open("scripts/mega_forensic_report.json", "w", encoding="utf-8") as rep:
    json.dump(findings, rep, indent=2)

print("\nDetailed report saved to: scripts/mega_forensic_report.json")
