#!/usr/bin/env python3
"""
Deep Forensic Scan — Vector Audit:
1. Colab & Compiler Integration (openInColab, runCode, copyCode)
2. Index.html Hero Metrics & Consistency (191 vs 198 days, total XP, week links)
3. Code Imports Completeness (missing imports like pandas, matplotlib, torch, numpy)
4. Gamification Namespace & Storage Key Compatibility (wX-state vs courseState)
5. A11y & Keyboard Navigation (tabindex, role, onkeydown on all interactive widgets)
6. Mobile Viewport & Table Wrap Overflow
7. Protocol & Link Safety (http vs https, target=_blank security with rel="noopener")
"""

import re
import json
from pathlib import Path
from bs4 import BeautifulSoup
import ast

WEEKS_DIR = Path("pages/weeks")
ROOT_DIR = Path(".")

findings = []

def add_finding(vector, week, location, severity, title, details, snippet=""):
    findings.append({
        "id": len(findings) + 1,
        "vector": vector,
        "week": week,
        "location": location,
        "severity": severity,
        "title": title,
        "details": details,
        "snippet": snippet[:160].replace('\n', ' ') if snippet else ""
    })

# ─────────────────────────────────────────────────────────────────────────────
# 1. AUDIT OPENINCOLAB & RUNCODE BUTTONS ACROSS ALL WEEKS
# ─────────────────────────────────────────────────────────────────────────────
print("Auditing Vector 1: Colab & Compiler Runner...")
js_course = (ROOT_DIR / "assets" / "js" / "course.js").read_text(encoding='utf-8')

has_open_in_colab = "function openInColab" in js_course
has_run_code = "function runCode" in js_course
has_copy_code = "function copyCode" in js_course

if not has_open_in_colab:
    add_finding("Compiler & Colab", 0, "assets/js/course.js", "HIGH", "Missing openInColab() implementation in course.js", "course.js does not define openInColab(), causing Colab buttons to fail if clicked.")
if not has_run_code:
    add_finding("Compiler & Colab", 0, "assets/js/course.js", "HIGH", "Missing runCode() implementation in course.js", "course.js does not define runCode().")
if not has_copy_code:
    add_finding("Compiler & Colab", 0, "assets/js/course.js", "HIGH", "Missing copyCode() implementation in course.js", "course.js does not define copyCode().")

# Check each week's code block buttons
for wn in range(1, 27):
    fp = WEEKS_DIR / f"week{wn}.html"
    if not fp.exists(): continue
    soup = BeautifulSoup(fp.read_text(encoding='utf-8'), 'html.parser')
    
    cbs = soup.find_all('div', class_='cb')
    for i, cb in enumerate(cbs):
        lang = cb.find('span', class_='cb-lang')
        lang_text = lang.text.strip().lower() if lang else 'python'
        
        # Check if non-python block has colab button
        colab_btn = cb.find('button', onclick=re.compile(r'openInColab'))
        if colab_btn and lang_text in ['bash', 'shell', 'yaml', 'json', 'sql', 'dockerfile', 'pseudocode']:
            add_finding(
                "Compiler & Colab", wn, f"Week {wn} (CB #{i+1})", "LOW",
                f"Colab button present on non-Python code ({lang_text})",
                f"Code block #{i+1} has language '{lang_text}' but offers '⚡ Run on Colab', which may fail to execute as valid Python.",
                str(cb)[:100]
            )

# ─────────────────────────────────────────────────────────────────────────────
# 2. AUDIT INDEX.HTML HERO METRICS & LINKS
# ─────────────────────────────────────────────────────────────────────────────
print("Auditing Vector 2: Index.html Hero Metrics...")
fp_index = ROOT_DIR / "index.html"
if fp_index.exists():
    index_html = fp_index.read_text(encoding='utf-8')
    index_soup = BeautifulSoup(index_html, 'html.parser')
    
    # Check total days mention
    m_days = re.findall(r'(\d+)[-\s]Day', index_html)
    for md in m_days:
        if md not in ['191', '198']:
            add_finding("Landing Page Inconsistency", 0, "index.html", "MEDIUM", f"Outdated day count in index.html ({md} Days)", f"index.html mentions '{md} Days' (curriculum is 191 core days / 198 modules).")
            
    # Check week links in index.html
    week_links = index_soup.find_all('a', href=lambda h: h and 'week' in h)
    for wl in week_links:
        target = wl.get('href')
        resolved = (ROOT_DIR / target).resolve()
        if not resolved.exists():
            add_finding("Broken Navigation Link", 0, "index.html", "HIGH", f"Broken week link in index.html: {target}", f"Link '{target}' does not exist.")

# ─────────────────────────────────────────────────────────────────────────────
# 3. AUDIT CODE IMPORTS COMPLETENESS (Missing imports)
# ─────────────────────────────────────────────────────────────────────────────
print("Auditing Vector 3: Code Block Imports Completeness...")
for wn in range(1, 27):
    fp = WEEKS_DIR / f"week{wn}.html"
    if not fp.exists(): continue
    soup = BeautifulSoup(fp.read_text(encoding='utf-8'), 'html.parser')
    
    for i, pre in enumerate(soup.find_all('pre')):
        code_text = pre.text
        # Check for unimported common libraries
        if re.search(r'\bnp\.[a-zA-Z]', code_text) and 'import numpy' not in code_text:
            add_finding("Missing Library Import", wn, f"Week {wn} (Pre #{i+1})", "MEDIUM", "np. used without 'import numpy as np'", f"Snippet references NumPy functions without importing numpy.", code_text[:100])
        if re.search(r'\bpd\.[a-zA-Z]', code_text) and 'import pandas' not in code_text:
            add_finding("Missing Library Import", wn, f"Week {wn} (Pre #{i+1})", "MEDIUM", "pd. used without 'import pandas as pd'", f"Snippet references Pandas functions without importing pandas.", code_text[:100])
        if re.search(r'\bplt\.[a-zA-Z]', code_text) and 'import matplotlib' not in code_text:
            add_finding("Missing Library Import", wn, f"Week {wn} (Pre #{i+1})", "MEDIUM", "plt. used without 'import matplotlib.pyplot as plt'", f"Snippet references Matplotlib functions without importing pyplot.", code_text[:100])
        if re.search(r'\btorch\.[a-zA-Z]', code_text) and 'import torch' not in code_text:
            add_finding("Missing Library Import", wn, f"Week {wn} (Pre #{i+1})", "MEDIUM", "torch. used without 'import torch'", f"Snippet references PyTorch functions without importing torch.", code_text[:100])

# ─────────────────────────────────────────────────────────────────────────────
# 4. AUDIT GAMIFICATION STORAGE COMPATIBILITY
# ─────────────────────────────────────────────────────────────────────────────
print("Auditing Vector 4: Storage Compatibility...")
# Check if courseState in course.js migrates legacy wX-state keys
if "localStorage.getItem('w' + weekNum + '-state')" not in js_course and "localStorage.getItem(`w${" not in js_course:
    add_finding("Storage Legacy Migration", 0, "assets/js/course.js", "LOW", "course.js lacks auto-migration for legacy wX-state keys", "course.js does not automatically migrate older wX-state format into canonical courseState.")

# ─────────────────────────────────────────────────────────────────────────────
# 5. AUDIT A11Y & KEYBOARD ACCESSIBILITY
# ─────────────────────────────────────────────────────────────────────────────
print("Auditing Vector 5: Accessibility & Keyboard Navigation...")
for wn in range(1, 27):
    fp = WEEKS_DIR / f"week{wn}.html"
    if not fp.exists(): continue
    soup = BeautifulSoup(fp.read_text(encoding='utf-8'), 'html.parser')
    
    # Check flashcards accessibility
    for i, fc in enumerate(soup.find_all('div', class_='flashcard')):
        if not fc.get('tabindex'):
            add_finding("Accessibility Gap", wn, f"Week {wn} (Flashcard #{i+1})", "LOW", f"Flashcard #{i+1} missing tabindex='0'", "Interactive flashcard cannot be focused via keyboard navigation.")
            break
            
    # Check quiz options accessibility
    for i, opt in enumerate(soup.find_all('div', class_='quiz-opt')):
        if not opt.get('role'):
            add_finding("Accessibility Gap", wn, f"Week {wn} (Quiz option)", "LOW", "Quiz option missing role='button'", "Interactive quiz option lacks semantic ARIA role='button'.")
            break

# ─────────────────────────────────────────────────────────────────────────────
# 6. AUDIT MOBILE VIEWPORT & TABLE OVERFLOW
# ─────────────────────────────────────────────────────────────────────────────
print("Auditing Vector 6: Table Wrappers & Viewport...")
for wn in range(1, 27):
    fp = WEEKS_DIR / f"week{wn}.html"
    if not fp.exists(): continue
    soup = BeautifulSoup(fp.read_text(encoding='utf-8'), 'html.parser')
    
    tables = soup.find_all('table')
    for i, t in enumerate(tables):
        parent = t.parent
        if not parent or ('table-wrap' not in parent.get('class', []) and 'overflow-x' not in parent.get('style', '')):
            add_finding(
                "Mobile Responsive Risk", wn, f"Week {wn} (Table #{i+1})", "MEDIUM",
                f"Table #{i+1} not wrapped in responsive .table-wrap container",
                "Table lacks an overflow-x scroll container, which can cause horizontal blowout on mobile viewports.",
                str(t)[:100]
            )

# ─────────────────────────────────────────────────────────────────────────────
# 7. AUDIT EXTERNAL LINK PROTOCOL & SECURITY
# ─────────────────────────────────────────────────────────────────────────────
print("Auditing Vector 7: Link Security & Protocols...")
for wn in range(1, 27):
    fp = WEEKS_DIR / f"week{wn}.html"
    if not fp.exists(): continue
    soup = BeautifulSoup(fp.read_text(encoding='utf-8'), 'html.parser')
    
    for a in soup.find_all('a'):
        href = a.get('href', '')
        if href.startswith('http://'):
            add_finding("Insecure Protocol", wn, f"Week {wn}", "LOW", f"Insecure HTTP link: {href}", f"Resource link uses unencrypted http:// protocol instead of https://.", href)
        if href.startswith('http') and a.get('target') == '_blank':
            rel = a.get('rel', '')
            if 'noopener' not in str(rel):
                add_finding("Security Best Practice", wn, f"Week {wn}", "LOW", f"Target _blank link missing rel='noopener': {href}", "External link opening in a new tab lacks rel='noopener' security attribute.", href)

print(f"\nVector Audit complete! Cataloged {len(findings)} issues across the 7 vectors.")
out_file = ROOT_DIR / "scripts" / "vector_audit_issues_inventory.json"
out_file.write_text(json.dumps(findings, indent=2), encoding='utf-8')
print(f"Report saved to {out_file}")
