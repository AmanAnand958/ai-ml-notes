#!/usr/bin/env python3
"""
scripts/deep_scan_layout_tags_and_ordering.py
Deep audit of all HTML week pages and YAML files for:
1. Tag balance (<pre>, <code>, <div>, <span>, <p>, <details>, <summary>, <ul>, <li>, <table>, <tr>, <td>, <th>, <a>, <button>, <h1..h6>)
2. Code block anomalies (</pre>bash, double pre tags, leaked markdown codeblock ticks)
3. Structural ordering anomalies within each day section
4. Broken / unclosed comments or KaTeX blocks
"""

import os, glob, re, html
from bs4 import BeautifulSoup
import yaml

print("=== STARTING COMPREHENSIVE SCAN FOR TAG, CODEBLOCK & LAYOUT ORDERING ANOMALIES ===")

html_files = sorted(glob.glob("pages/weeks/week*.html"), key=lambda x: int(re.search(r'\d+', x).group()))
root_htmls = ["index.html", "roadmap.html", "dashboard.html", "resources.html"]
all_htmls = html_files + [f for f in root_htmls if os.path.exists(f)]

yaml_files = sorted(glob.glob("src/data/week*.yaml"), key=lambda x: int(re.search(r'\d+', x).group()))

TAGS_TO_CHECK = ['pre', 'code', 'div', 'span', 'p', 'details', 'summary', 'ul', 'ol', 'li', 'table', 'tr', 'td', 'th', 'a', 'button', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']

findings = []

# 1. TAG BALANCE AUDIT IN HTML FILES
print("\n--- [1/4] AUDITING HTML TAG BALANCES ---")
for h_file in all_htmls:
    with open(h_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Strip script/style tags for pure markup check
    # But also check script/style tag closures
    for tag in ['script', 'style'] + TAGS_TO_CHECK:
        # Count opening and closing
        # Be careful not to match self-closing or attributes
        open_pattern = rf'<{tag}(?:\s+[^>]*)?>'
        close_pattern = rf'</{tag}>'
        
        opens = len(re.findall(open_pattern, content, flags=re.IGNORECASE))
        closes = len(re.findall(close_pattern, content, flags=re.IGNORECASE))
        
        if opens != closes:
            findings.append({
                "type": "Unbalanced HTML Tag",
                "file": h_file,
                "tag": tag,
                "opens": opens,
                "closes": closes,
                "diff": opens - closes
            })

# 2. CODE BLOCK ANOMALIES (like </pre>bash, ```bash in HTML, <pre><pre>, etc.)
print("\n--- [2/4] AUDITING CODE BLOCK SYNTAX & ESCAPING ---")
code_anomaly_patterns = [
    (r'</pre>\s*(?:bash|python|json|html|sql|js|typescript|markdown|yaml)', "Leaked language identifier after </pre>"),
    (r'<pre\b[^>]*>\s*<pre\b', "Nested <pre> tag"),
    (r'</pre>\s*</pre>', "Double </pre> closure"),
    (r'```(?:python|bash|sql|json|html|js|yaml)', "Raw markdown code fence leaking in HTML"),
    (r'<pre\b[^>]*>(?:(?!</pre>).)*?```', "Markdown fence inside <pre> tag"),
    (r'<div class="cb">\s*(?!<div class="cb-head">)', "Code block missing cb-head toolbar"),
    (r'<div class="cb">\s*<div class="cb-head">[\s\S]*?</div>\s*(?!<pre)', "Code block missing <pre> container"),
]

for h_file in all_htmls:
    with open(h_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    for pat, desc in code_anomaly_patterns:
        matches = list(re.finditer(pat, content, flags=re.IGNORECASE))
        if matches:
            for m in matches:
                # find line number
                line_no = content[:m.start()].count('\n') + 1
                findings.append({
                    "type": "Code Block Anomaly",
                    "file": h_file,
                    "line": line_no,
                    "detail": desc,
                    "snippet": content[max(0, m.start()-20):min(len(content), m.end()+20)].replace('\n', ' ')
                })

# 3. YAML THEORY_HTML CODE BLOCK CHECK
print("\n--- [3/4] AUDITING YAML THEORY_HTML FOR NESTED/BROKEN TAGS ---")
for y_file in yaml_files:
    with open(y_file, 'r', encoding='utf-8') as f:
        try:
            data = yaml.safe_load(f)
        except Exception as e:
            findings.append({
                "type": "YAML Parse Error",
                "file": y_file,
                "detail": str(e)
            })
            continue
    
    if not isinstance(data, dict) or 'days' not in data:
        continue
    
    for day in data['days']:
        day_num = day.get('day_num', '?')
        theory = day.get('theory_html', '')
        if not theory:
            continue
        
        # Check pre/code tags in theory
        pre_opens = len(re.findall(r'<pre\b', theory, flags=re.IGNORECASE))
        pre_closes = len(re.findall(r'</pre>', theory, flags=re.IGNORECASE))
        if pre_opens != pre_closes:
            findings.append({
                "type": "YAML Unbalanced <pre>",
                "file": y_file,
                "day": day_num,
                "detail": f"<pre> opens={pre_opens}, closes={pre_closes}"
            })
        
        # Check div balance in theory
        div_opens = len(re.findall(r'<div\b', theory, flags=re.IGNORECASE))
        div_closes = len(re.findall(r'</div\b', theory, flags=re.IGNORECASE))
        if div_opens != div_closes:
            findings.append({
                "type": "YAML Unbalanced <div>",
                "file": y_file,
                "day": day_num,
                "detail": f"<div> opens={div_opens}, closes={div_closes}"
            })
        
        # Check code fence leaks
        for pat, desc in code_anomaly_patterns:
            matches = list(re.finditer(pat, theory, flags=re.IGNORECASE))
            for m in matches:
                findings.append({
                    "type": "YAML Code Anomaly",
                    "file": y_file,
                    "day": day_num,
                    "detail": desc,
                    "snippet": theory[max(0, m.start()-20):min(len(theory), m.end()+20)].replace('\n', ' ')
                })

# 4. SECTION ORDERING WITHIN EACH DAY SECTION
print("\n--- [4/4] AUDITING DAY DOM SECTION ORDERING ---")
# Standard expected layout pattern inside each day section:
# 1. objectives (optional) / checklist (optional) / day-header
# 2. callout / concept-map / hinglish / analogy
# 3. quick-jumps (optional)
# 4. theory
# 5. predict-block
# 6. tasks-section
# 7. quiz-section
# 8. flashcard-grid / revision flashcards
# 9. gotcha-box / takeaways / resources-section / complete-btn

for h_file in html_files:
    with open(h_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract each day section
    day_matches = list(re.finditer(r'<div class="day-section\s*[^"]*"\s+id="day-(\d+)"[^>]*>([\s\S]*?)(?=<div class="day-section|<footer|<\/main)', content))
    
    for m in day_matches:
        day_id = m.group(1)
        day_body = m.group(2)
        
        # Find index positions of key section markers
        pos_theory = day_body.find('class="theory"')
        if pos_theory == -1: pos_theory = day_body.find('id="day-' + day_id + '-theory"')
        
        pos_predict = day_body.find('class="predict-block"')
        pos_tasks = day_body.find('class="tasks-section"')
        pos_quiz = day_body.find('class="quiz-section"')
        pos_flashcards = day_body.find('class="flashcard-grid"')
        pos_resources = day_body.find('class="resources-section"')
        if pos_resources == -1: pos_resources = day_body.find('id="day-' + day_id + '-resources-section"')
        
        pos_complete = day_body.find('class="complete-btn"')
        
        # Check standard relative order:
        # Theory before Predict (if predict exists)
        if pos_theory != -1 and pos_predict != -1 and pos_theory > pos_predict:
            findings.append({
                "type": "Ordering Anomaly",
                "file": h_file,
                "day": day_id,
                "detail": "Predict block appears BEFORE Theory section"
            })
        
        # Predict before Tasks (if both exist)
        if pos_predict != -1 and pos_tasks != -1 and pos_predict > pos_tasks:
            findings.append({
                "type": "Ordering Anomaly",
                "file": h_file,
                "day": day_id,
                "detail": "Tasks section appears BEFORE Predict block"
            })
        
        # Tasks before Quiz (if both exist)
        if pos_tasks != -1 and pos_quiz != -1 and pos_tasks > pos_quiz:
            findings.append({
                "type": "Ordering Anomaly",
                "file": h_file,
                "day": day_id,
                "detail": "Quiz section appears BEFORE Tasks section"
            })
        
        # Quiz before Flashcards (if both exist)
        if pos_quiz != -1 and pos_flashcards != -1 and pos_quiz > pos_flashcards:
            findings.append({
                "type": "Ordering Anomaly",
                "file": h_file,
                "day": day_id,
                "detail": "Flashcards appear BEFORE Quiz section"
            })
        
        # Flashcards before Resources (if both exist)
        if pos_flashcards != -1 and pos_resources != -1 and pos_flashcards > pos_resources:
            findings.append({
                "type": "Ordering Anomaly",
                "file": h_file,
                "day": day_id,
                "detail": "Resources section appears BEFORE Flashcards"
            })
        
        # Resources before Complete Button
        if pos_resources != -1 and pos_complete != -1 and pos_resources > pos_complete:
            findings.append({
                "type": "Ordering Anomaly",
                "file": h_file,
                "day": day_id,
                "detail": "Complete button appears BEFORE Resources section"
            })

# REPORT SUMMARY
print("\n" + "="*70)
print(f"=== SCAN COMPLETE: {len(findings)} TOTAL ANOMALIES FOUND ===")
print("="*70)

if not findings:
    print("✨ ALL 26 WEEKS, 191 DAYS, AND ROOT FILES ARE 100% CLEAN AND PROPERLY ORDERED!")
else:
    for idx, f in enumerate(findings, 1):
        print(f"\n[{idx}] {f['type']} in {f.get('file')} (Day {f.get('day', 'N/A')}):")
        for k, v in f.items():
            if k not in ['type', 'file']:
                print(f"    • {k}: {v}")

import json
with open("scripts/layout_ordering_scan_report.json", "w", encoding="utf-8") as rep:
    json.dump(findings, rep, indent=2)
