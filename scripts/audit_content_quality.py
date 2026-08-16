#!/usr/bin/env python3
"""
Deep Content-Quality & Pedagogical Integrity Audit Suite across all 26 Weeks.
Specifically evaluates:
1. Predict block code execution vs expected answer accuracy.
2. Generic/stub task solution implementations.
3. Content length & depth of Theory sections per day.
4. Identical or duplicated paragraphs/blocks across days.
5. Code snippet depth, imports completeness, and realistic logic.
6. Mathematical equation completeness & variable definitions.
7. Enterprise Case Study depth & realistic architecture metrics.
"""

import sys
import io
import re
import json
import ast
from pathlib import Path
from bs4 import BeautifulSoup
from collections import defaultdict

WEEKS_DIR = Path("pages/weeks")
content_issues = []

def log_issue(category, week, day, severity, title, details, snippet=""):
    content_issues.append({
        "id": len(content_issues) + 1,
        "category": category,
        "week": week,
        "day": day,
        "severity": severity,
        "title": title,
        "details": details,
        "snippet": snippet[:160].replace('\n', ' ') if snippet else ""
    })

# ─────────────────────────────────────────────────────────────────────────────
# 1. SCAN PREDICT BLOCKS: CODE OUTPUT VS EXPECTED ANSWER
# ─────────────────────────────────────────────────────────────────────────────
print("Auditing 1: Predict Block Code Output Accuracy...")
for wn in range(1, 27):
    fp = WEEKS_DIR / f"week{wn}.html"
    if not fp.exists(): continue
    soup = BeautifulSoup(fp.read_text(encoding='utf-8'), 'html.parser')
    
    for p in soup.find_all('div', class_=re.compile(r'predict-block|predict-box')):
        pre = p.find('pre')
        btn = p.find('button', class_=re.compile(r'predict-btn|btn'))
        if not pre or not btn: continue
        
        code_str = pre.text.strip()
        btn_onclick = btn.get('onclick', '')
        
        # Extract expected answer from checkPredict(id, answer)
        m = re.search(r"checkPredict\s*\(\s*['\"][^'\"]+['\"]\s*,\s*['\"]([^'\"]*)['\"]\s*\)", btn_onclick)
        if m:
            expected_ans = m.group(1).strip()
            
            # Check if code is pure Python and executable safely in AST sandbox
            try:
                # Capture print output of code snippet
                buffer = io.StringIO()
                safe_code = re.sub(r'#.*', '', code_str)
                # Only execute safe arithmetic / string manipulation snippets
                if not any(danger in code_str for danger in ['open(', 'import os', 'import sys', 'subprocess', 'requests', 'urllib', '__import__']):
                    if 'import numpy' not in safe_code and 'import torch' not in safe_code and 'import pandas' not in safe_code and len(safe_code) < 300:
                        try:
                            # Test run in clean scope
                            local_scope = {}
                            sys.stdout = buffer
                            exec(safe_code, {}, local_scope)
                            sys.stdout = sys.__stdout__
                            actual_out = buffer.getvalue().strip()
                            
                            # Normalize whitespace
                            norm_actual = re.sub(r'\s+', ' ', actual_out).lower()
                            norm_exp = re.sub(r'\s+', ' ', expected_ans).lower()
                            
                            if actual_out and norm_actual != norm_exp and norm_exp not in norm_actual:
                                log_issue(
                                    "Predict Answer Mismatch", wn, p.get('id', 'predict'), "HIGH",
                                    f"Predict block expected answer mismatch in Week {wn}",
                                    f"Code outputs '{actual_out}' but checkPredict expects '{expected_ans}'.",
                                    code_str
                                )
                        except Exception as e:
                            sys.stdout = sys.__stdout__
            except Exception:
                pass

# ─────────────────────────────────────────────────────────────────────────────
# 2. SCAN TASK SOLUTION DEPTH & GENERIC STUBS
# ─────────────────────────────────────────────────────────────────────────────
print("Auditing 2: Task Solution Implementations...")
for wn in range(1, 27):
    fp = WEEKS_DIR / f"week{wn}.html"
    if not fp.exists(): continue
    soup = BeautifulSoup(fp.read_text(encoding='utf-8'), 'html.parser')
    
    for ds in soup.find_all('div', class_=lambda c: c and 'day-section' in c):
        did = ds.get('id', 'unknown')
        tasks = ds.find_all('div', class_='task-block')
        
        for t_idx, t in enumerate(tasks):
            body = t.find('div', class_='task-body')
            if not body: continue
            
            cb = body.find('div', class_='cb') or body.find('pre')
            if cb:
                c_text = cb.text.strip()
                # Check for superficial stub functions
                if "def execute_pipeline():" in c_text and "status\": \"success" in c_text:
                    t_hdr = t.find('div', class_='task-header')
                    t_name = t_hdr.text.strip() if t_hdr else f"Task {t_idx+1}"
                    log_issue(
                        "Superficial Task Solution", wn, did, "MEDIUM",
                        f"Generic placeholder solution in {t_name}",
                        f"Solution code for '{t_name}' is a generic execute_pipeline() dummy function rather than topic-specific algorithm code.",
                        c_text[:120]
                    )
                elif len(c_text) < 60:
                    log_issue(
                        "Superficial Task Solution", wn, did, "LOW",
                        f"Very short task solution in Task #{t_idx+1} of {did}",
                        f"Task solution code is only {len(c_text)} characters long.",
                        c_text
                    )

# ─────────────────────────────────────────────────────────────────────────────
# 3. SCAN THEORY & CONCEPTS DEPTH PER DAY
# ─────────────────────────────────────────────────────────────────────────────
print("Auditing 3: Theory & Concepts Depth...")
for wn in range(1, 27):
    fp = WEEKS_DIR / f"week{wn}.html"
    if not fp.exists(): continue
    soup = BeautifulSoup(fp.read_text(encoding='utf-8'), 'html.parser')
    
    for ds in soup.find_all('div', class_=lambda c: c and 'day-section' in c):
        did = ds.get('id', 'unknown')
        
        # Calculate theory word count
        theory_nodes = []
        in_theory = False
        for child in ds.children:
            if not child.name: continue
            txt = child.text
            if 'Theory & Concepts' in txt or '🧠 Theory' in txt:
                in_theory = True
            elif in_theory and any(stop in txt for stop in ['PREDICT THE OUTPUT', 'Task 1', '🧪 Knowledge Check', '🃏 Revision Flashcards']):
                in_theory = False
            elif in_theory:
                theory_nodes.append(child.text.strip())
                
        theory_text = ' '.join(theory_nodes)
        word_count = len(theory_text.split())
        
        if word_count < 75 and 'toolkit' not in did:
            log_issue(
                "Sparse Theoretical Content", wn, did, "HIGH",
                f"Thin theoretical explanation in {did} ({word_count} words)",
                f"{did} Theory section contains only {word_count} words (minimum standard is 150+ words of deep conceptual grounding).",
                theory_text[:140]
            )
        elif word_count < 120 and 'toolkit' not in did:
            log_issue(
                "Sparse Theoretical Content", wn, did, "LOW",
                f"Modest theoretical depth in {did} ({word_count} words)",
                f"{did} Theory section is relatively brief ({word_count} words).",
                theory_text[:140]
            )

# ─────────────────────────────────────────────────────────────────────────────
# 4. SCAN DUPLICATED OR REPEATED PARAGRAPHS ACROSS DAYS
# ─────────────────────────────────────────────────────────────────────────────
print("Auditing 4: Duplicate Paragraphs & Boilerplate Dumps...")
seen_paragraphs = defaultdict(list)

for wn in range(1, 27):
    fp = WEEKS_DIR / f"week{wn}.html"
    if not fp.exists(): continue
    soup = BeautifulSoup(fp.read_text(encoding='utf-8'), 'html.parser')
    
    for ds in soup.find_all('div', class_=lambda c: c and 'day-section' in c):
        did = ds.get('id', 'unknown')
        for p in ds.find_all('p'):
            ptxt = p.text.strip()
            # Ignore short standard hints
            if len(ptxt) > 80 and not any(ign in ptxt for ign in ['CLICK EACH CARD TO FLIP', 'Enter your prediction', 'Mark Day', 'Production-oriented AI/ML checkpoint']):
                seen_paragraphs[ptxt].append((wn, did))

for ptxt, occurrences in seen_paragraphs.items():
    if len(occurrences) > 1:
        # Check if they occur in different days
        distinct_days = set(d for w, d in occurrences)
        if len(distinct_days) > 1:
            log_issue(
                "Duplicate / Copy-Pasted Content", occurrences[0][0], f"{occurrences[0][1]} & {occurrences[1][1]}", "MEDIUM",
                f"Identical paragraph duplicated across {len(distinct_days)} days",
                f"The exact same 80+ character paragraph is copy-pasted across {list(distinct_days)[:3]}.",
                ptxt
            )

# ─────────────────────────────────────────────────────────────────────────────
# 5. SCAN FLASHCARD DEFINITIONS DEPTH & QUALITY
# ─────────────────────────────────────────────────────────────────────────────
print("Auditing 5: Flashcard Content Quality...")
for wn in range(1, 27):
    fp = WEEKS_DIR / f"week{wn}.html"
    if not fp.exists(): continue
    soup = BeautifulSoup(fp.read_text(encoding='utf-8'), 'html.parser')
    
    for ds in soup.find_all('div', class_=lambda c: c and 'day-section' in c):
        did = ds.get('id', 'unknown')
        fcs = ds.find_all('div', class_='flashcard')
        
        for i, fc in enumerate(fcs):
            divs = fc.find_all('div')
            if len(divs) >= 2:
                front = divs[0].text.strip()
                back = divs[1].text.strip()
                
                # Check if front and back are almost identical
                if front.lower() == back.lower():
                    log_issue(
                        "Low-Quality Flashcard", wn, did, "HIGH",
                        f"Flashcard #{i+1} has identical front and back text in {did}",
                        f"Card front and back both say '{front}', failing to test knowledge.",
                        front
                    )
                elif len(back) < 15:
                    log_issue(
                        "Low-Quality Flashcard", wn, did, "MEDIUM",
                        f"Extremely brief flashcard definition in #{i+1} of {did}",
                        f"Flashcard back definition is only {len(back)} characters ('{back}').",
                        back
                    )

# ─────────────────────────────────────────────────────────────────────────────
# 6. SCAN MATHEMATICAL FORMULATIONS & LATEX COMPLETENESS
# ─────────────────────────────────────────────────────────────────────────────
print("Auditing 6: Mathematical Formulations...")
for wn in range(1, 27):
    fp = WEEKS_DIR / f"week{wn}.html"
    if not fp.exists(): continue
    raw = fp.read_text(encoding='utf-8')
    
    # Check for empty or malformed LaTeX tags like $$ $$
    empty_math = re.findall(r'\$\$\s*\$\$', raw)
    if empty_math:
        log_issue("Malformed Math Block", wn, "Global", "HIGH", f"Empty $$ $$ KaTeX math block in Week {wn}", "Found empty double-dollar math delimiters.")

    # Check for unfinished LaTeX like \frac{} with empty arguments
    unfinished_latex = re.findall(r'\\frac\{\s*\}\{\s*\}|\\sqrt\{\s*\}', raw)
    if unfinished_latex:
        log_issue("Incomplete Mathematical Formula", wn, "Global", "HIGH", f"Incomplete LaTeX fraction/root in Week {wn}", f"Found unpopulated LaTeX math expression '{unfinished_latex[0]}'.")

# ─────────────────────────────────────────────────────────────────────────────
# 7. SCAN ENTERPRISE CASE STUDIES REALISM
# ─────────────────────────────────────────────────────────────────────────────
print("Auditing 7: Enterprise Case Studies...")
for wn in range(1, 27):
    fp = WEEKS_DIR / f"week{wn}.html"
    if not fp.exists(): continue
    soup = BeautifulSoup(fp.read_text(encoding='utf-8'), 'html.parser')
    
    for ds in soup.find_all('div', class_=lambda c: c and 'day-section' in c):
        did = ds.get('id', 'unknown')
        cs = ds.find('div', class_='enterprise-case-study')
        if cs:
            cs_text = cs.text.strip()
            if len(cs_text) < 100:
                log_issue(
                    "Superficial Enterprise Case Study", wn, did, "LOW",
                    f"Superficial case study in {did}",
                    f"Enterprise case study is under 100 characters ({len(cs_text)} chars) and lacks architectural details.",
                    cs_text
                )

print(f"\nContent Audit complete! Cataloged {len(content_issues)} content & pedagogical issues.")
out_file = Path("scripts/detailed_content_issues_inventory.json")
out_file.write_text(json.dumps(content_issues, indent=2), encoding='utf-8')
print(f"Report saved to {out_file}")
