#!/usr/bin/env python3
"""
scripts/deep_all_weeks_audit.py
A comprehensive, rigorous forensic audit across all 26 weeks with deep focus on Weeks 19-26.
"""

import os
import re
import glob
import ast
import json
from bs4 import BeautifulSoup
from collections import defaultdict

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
PAGES_DIR = os.path.join(ROOT_DIR, 'pages/weeks')
DATA_DIR = os.path.join(ROOT_DIR, 'src/data')

findings = []

def add_finding(category, week, day, severity, title, details, snippet=""):
    findings.append({
        "category": category,
        "week": int(week) if str(week).isdigit() else week,
        "day": str(day),
        "severity": severity, # CRITICAL, HIGH, MEDIUM, LOW
        "title": title,
        "details": details,
        "snippet": (snippet[:200] + '...') if len(snippet) > 200 else snippet
    })

print("Starting Deep Forensic Audit across all 26 Weeks (Intensive scan on Weeks 19-26)...")

# ─────────────────────────────────────────────────────────────────────────────
# 1. SCAN ALL WEEKS
# ─────────────────────────────────────────────────────────────────────────────
seen_questions = defaultdict(list)

for w in range(1, 27):
    fpath = os.path.join(PAGES_DIR, f"week{w}.html")
    if not os.path.exists(fpath): continue
    
    html_content = open(fpath, 'r', encoding='utf-8').read()
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # 1. Day Sections
    day_secs = soup.find_all(lambda tag: tag.name in ['div', 'section', 'main', 'article'] and 
                               tag.get('class') and 'day-section' in tag.get('class'))
    
    # Also check pills and sidebar items
    pills = soup.find_all(lambda tag: tag.get('class') and 'day-pill' in tag.get('class'))
    sb_items = soup.find_all(lambda tag: tag.get('class') and 'sb-item' in tag.get('class'))
    
    # Check if number of day sections matches pills (excluding toolkit pill if separate)
    actual_day_pills = [p for p in pills if p.get('data-day') or re.match(r'pill-\d+', p.get('id', ''))]
    if len(day_secs) != len(actual_day_pills):
        add_finding(
            "Navigation Hierarchy",
            w,
            f"Week {w}",
            "MEDIUM",
            f"Day Sections count ({len(day_secs)}) does not match Day Pills count ({len(actual_day_pills)})",
            f"Sections: {[s.get('id') for s in day_secs]}"
        )
        
    for day_sec in day_secs:
        day_id = day_sec.get('id', 'unknown')
        day_num = re.sub(r'day-?', '', day_id)
        
        # ── A. CODE AST & SYNTAX ──
        for pre in day_sec.find_all('pre'):
            code_text = pre.text.strip()
            parent = pre.parent
            classes = (pre.get('class') or []) + ((parent.get('class') or []) if parent else [])
            class_str = " ".join(classes).lower()
            
            if any(k in class_str for k in ['bash', 'sh', 'json', 'yaml', 'yml', 'output', 'terminal', 'mermaid']):
                continue
            
            if any(k in code_text for k in ['def ', 'import ', 'class ', 'return ', 'for ', 'while ', 'print(']):
                clean_code = re.sub(r'^\s*>>>\s?', '', code_text, flags=re.MULTILINE)
                clean_code = re.sub(r'^\s*\.\.\.\s?', '', clean_code, flags=re.MULTILINE)
                clean_code = re.sub(r'&lt;', '<', clean_code)
                clean_code = re.sub(r'&gt;', '>', clean_code)
                clean_code = re.sub(r'&amp;', '&', clean_code)
                
                try:
                    ast.parse(clean_code)
                except SyntaxError as e:
                    # Ignore intentional ellipses in docstrings or placeholders if purely descriptive
                    if not clean_code.startswith("..."):
                        add_finding(
                            "Code AST Syntax Error",
                            w,
                            day_num,
                            "HIGH",
                            f"Python SyntaxError in Day {day_num} code block",
                            f"Line {e.lineno}: {e.msg}",
                            clean_code[:140]
                        )
                        
        # ── B. TASK PROMPT & SOLUTION COMPLETENESS ──
        tasks = day_sec.find_all(lambda tag: tag.get('class') and any('task' in c for c in tag.get('class')))
        solutions = day_sec.find_all(lambda tag: tag.get('class') and any('solution' in c for c in tag.get('class')))
        
        for sol in solutions:
            sol_text = sol.text.strip()
            if re.search(r'# TODO\b|# YOUR CODE HERE|pass\s*#|raise NotImplementedError', sol_text, re.IGNORECASE):
                add_finding(
                    "Task Solution Quality",
                    w,
                    day_num,
                    "HIGH",
                    f"Placeholder/TODO found in Task Solution (Day {day_num})",
                    "Solution contains unimplemented stub markers (TODO, YOUR CODE HERE, or NotImplementedError)",
                    sol_text[:140]
                )
            if "assert True" in sol_text:
                add_finding(
                    "Task Solution Quality",
                    w,
                    day_num,
                    "HIGH",
                    f"Fake 'assert True' assertion in Task Solution (Day {day_num})",
                    "Solution uses trivial non-verifying assertion",
                    sol_text[:140]
                )
                
        # ── C. PREDICT DRILLS ──
        predict_blocks = day_sec.find_all(lambda tag: tag.get('class') and any('predict' in c for c in tag.get('class')))
        for pb in predict_blocks:
            pre = pb.find('pre')
            btn = pb.find('button')
            input_box = pb.find('input')
            if not pre:
                add_finding(
                    "Predict Drill",
                    w,
                    day_num,
                    "MEDIUM",
                    f"Missing code snippet in Predict Block (Day {day_num})",
                    "Predict block container exists but has no code <pre> block"
                )
            if not btn:
                add_finding(
                    "Predict Drill",
                    w,
                    day_num,
                    "MEDIUM",
                    f"Missing submit button in Predict Block (Day {day_num})",
                    "Predict drill lacks check/submit button"
                )
            if btn:
                btn_onclick = btn.get('onclick', '')
                if 'checkPredict' not in btn_onclick:
                    add_finding(
                        "Predict Drill",
                        w,
                        day_num,
                        "HIGH",
                        f"Predict submit button lacks checkPredict handler (Day {day_num})",
                        f"onclick attribute: {btn_onclick}"
                    )

        # ── D. QUIZZES ──
        quiz_items = day_sec.find_all(lambda tag: tag.get('class') and any('quiz-item' in c or 'quiz-card' in c for c in tag.get('class')))
        for q_idx, q in enumerate(quiz_items):
            q_text_el = q.find(class_=re.compile(r'quiz-title|question-text|q-text')) or q.find('p') or q.find('h4')
            q_title = q_text_el.text.strip() if q_text_el else f"Question {q_idx+1}"
            
            normalized_q = re.sub(r'\s+', ' ', q_title).lower()
            if len(normalized_q) > 20:
                seen_questions[normalized_q].append((w, day_num))
            
            # Check options
            options = q.find_all(['div', 'button', 'li'], class_=re.compile(r'quiz-opt|option|choice'))
            if len(options) > 0 and len(options) < 4:
                add_finding(
                    "Quiz Structure",
                    w,
                    day_num,
                    "MEDIUM",
                    f"Quiz question has fewer than 4 options (Day {day_num}, Q#{q_idx+1})",
                    f"Found {len(options)} options instead of required 4",
                    q_title
                )

        # ── E. FLASHCARDS ──
        cards = day_sec.find_all(lambda tag: tag.get('class') and any('flashcard' in c or 'fc-card' in c for c in tag.get('class')))
        for fc_idx, fc in enumerate(cards):
            front = fc.find(class_=re.compile(r'front|fc-front'))
            back = fc.find(class_=re.compile(r'back|fc-back'))
            front_text = front.text.strip() if front else ""
            back_text = back.text.strip() if back else ""
            
            if not front_text or not back_text:
                add_finding(
                    "Flashcard Defect",
                    w,
                    day_num,
                    "HIGH",
                    f"Empty Flashcard Front or Back (Day {day_num}, Card #{fc_idx+1})",
                    f"Front empty: {not front_text}, Back empty: {not back_text}"
                )

        # ── F. THEORY SECTION DEPTH & STRUCTURE ──
        theory_sec = day_sec.find(lambda tag: tag.get('class') and any('theory' in c for c in tag.get('class')))
        if not theory_sec:
            add_finding(
                "Theory Container",
                w,
                day_num,
                "HIGH",
                f"Missing Theory Section in Day {day_num}",
                "Day section lacks an explicit .theory container"
            )
        else:
            theory_text = theory_sec.text.strip()
            word_count = len(theory_text.split())
            
            if word_count < 250 and w >= 18:
                add_finding(
                    "Theory Depth",
                    w,
                    day_num,
                    "MEDIUM",
                    f"Under-density Theory Content (Day {day_num}, Week {w}: {word_count} words)",
                    f"Word count is {word_count} words (target >= 350 words for senior depth)"
                )

        # ── G. PRODUCTION GOTCHAS ──
        gotchas = day_sec.find_all(lambda tag: tag.get('class') and any('gotcha' in c for c in tag.get('class')))
        if not gotchas and w >= 18:
            add_finding(
                "Gotcha Box Missing",
                w,
                day_num,
                "LOW",
                f"No Production Gotcha Box in Day {day_num}",
                "Day section in advanced week lacks a dedicated .gotcha-box"
            )
        for g in gotchas:
            g_text = g.text.strip()
            if any(generic in g_text.lower() for generic in ['always test your code in production', 'make sure to handle errors properly', 'generic error handling']):
                add_finding(
                    "Gotcha Quality",
                    w,
                    day_num,
                    "MEDIUM",
                    f"Generic Gotcha Callout (Day {day_num})",
                    "Gotcha box contains generic boilerplate",
                    g_text[:140]
                )

# Check cross-day duplicate quizzes
for norm_q, locs in seen_questions.items():
    if len(locs) > 1:
        loc_str = ", ".join([f"W{w}D{d}" for w, d in locs])
        add_finding(
            "Duplicate Quiz Question",
            locs[0][0],
            locs[0][1],
            "LOW",
            f"Duplicate Quiz Question across multiple days: {loc_str}",
            f"Question text: {norm_q[:120]}",
            norm_q
        )

# ─────────────────────────────────────────────────────────────────────────────
# SAVE REPORT
# ─────────────────────────────────────────────────────────────────────────────
out_path = os.path.join(ROOT_DIR, "scripts/deep_forensic_all_weeks_findings.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(findings, f, indent=2)

print(f"\nAudit complete! Logged {len(findings)} total findings.")
print(f"Report saved to: {out_path}")

# Breakdown by Category & Severity
by_severity = defaultdict(int)
by_category = defaultdict(int)
by_week = defaultdict(int)

for item in findings:
    by_severity[item['severity']] += 1
    by_category[item['category']] += 1
    by_week[item['week']] += 1

print("\n--- Summary by Severity ---")
for sev in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']:
    if by_severity[sev]:
        print(f"  {sev:10s}: {by_severity[sev]}")

print("\n--- Summary by Category ---")
for cat, count in sorted(by_category.items(), key=lambda x: x[1], reverse=True):
    print(f"  {cat:30s}: {count}")

print("\n--- Findings by Week (Focus on Weeks 19-26) ---")
for wk in range(1, 27):
    print(f"  Week {wk:2d}: {by_week[wk]} findings")
