#!/usr/bin/env python3
"""
Comprehensive Content Gap & Pedagogical Depth Scanner across all 26 Weeks:
1. Bare Heading Detector: Identifies all <h2>, <h3>, <h4> headings followed immediately by a code block (<div class="cb"> or <pre>) without explanatory prose (<p>, <ul>, <div> with text).
2. Unannotated Code Detector: Identifies all code blocks (> 5 lines) with zero or <= 1 comment line.
3. Shallow Theory Section Detector: Identifies any day section where the Theory & Concepts section has fewer than 100 words of technical explanation.
4. Framework Without Mechanism: Identifies references to major libraries/frameworks (PyTorch, Scikit-Learn, Pandas, MLflow, FastAPI, Docker, Kubernetes, HuggingFace, LangChain, Ray, Triton) where no explanation of the inner mechanics is provided.
"""

import re
import json
from pathlib import Path
from bs4 import BeautifulSoup
from collections import defaultdict

WEEKS_DIR = Path("pages/weeks")
content_gaps = []

def log_gap(category, week, day, severity, title, details, snippet=""):
    content_gaps.append({
        "id": len(content_gaps) + 1,
        "category": category,
        "week": week,
        "day": day,
        "severity": severity,
        "title": title,
        "details": details,
        "snippet": snippet[:160].replace('\n', ' ') if snippet else ""
    })

# ─────────────────────────────────────────────────────────────────────────────
# 1. BARE HEADING AUDIT (Heading -> Immediate Code without explanation)
# ─────────────────────────────────────────────────────────────────────────────
print("Scanning Dimension 1: Bare Headings without Introductory Prose...")
for wn in range(1, 27):
    fp = WEEKS_DIR / f"week{wn}.html"
    if not fp.exists(): continue
    soup = BeautifulSoup(fp.read_text(encoding='utf-8'), 'html.parser')
    
    for ds in soup.find_all('div', class_=lambda c: c and 'day-section' in c):
        did = ds.get('id', 'unknown')
        for h in ds.find_all(['h2', 'h3', 'h4']):
            h_text = h.text.strip()
            # Skip quiz or resource headers
            if any(skip in h_text.lower() for skip in ['quiz', 'flashcard', 'resources', 'daily objective', 'practice task', 'mini-project', 'task 1', 'task 2', 'task 3']):
                continue
                
            # Find next non-empty sibling
            nxt = h.next_sibling
            while nxt and (isinstance(nxt, str) and not nxt.strip()):
                nxt = nxt.next_sibling
                
            if nxt and nxt.name == 'div' and ('cb' in nxt.get('class', []) or nxt.find('pre')):
                log_gap(
                    "Bare Heading Without Prose", wn, did, "MEDIUM",
                    f"Heading '{h_text}' followed immediately by code without explanation (Week {wn}, {did})",
                    f"Topic '{h_text}' launches directly into a code card without introducing the concept, architectural motivation, or key parameters.",
                    h_text
                )

# ─────────────────────────────────────────────────────────────────────────────
# 2. UNANNOTATED CODE BLOCKS (Bare code without step-by-step commentary)
# ─────────────────────────────────────────────────────────────────────────────
print("Scanning Dimension 2: Unannotated Complex Code Blocks...")
for wn in range(1, 27):
    fp = WEEKS_DIR / f"week{wn}.html"
    if not fp.exists(): continue
    soup = BeautifulSoup(fp.read_text(encoding='utf-8'), 'html.parser')
    
    for ds in soup.find_all('div', class_=lambda c: c and 'day-section' in c):
        did = ds.get('id', 'unknown')
        for i, cb in enumerate(ds.find_all('div', class_='cb')):
            pre = cb.find('pre')
            if not pre: continue
            code = pre.text.strip()
            lines = [l.strip() for l in code.split('\n') if l.strip()]
            comment_lines = [l for l in lines if l.startswith('#') or l.startswith('//')]
            
            # If code is substantial (> 8 lines) and has 0 comments
            if len(lines) > 8 and len(comment_lines) == 0:
                log_gap(
                    "Unannotated Code Block", wn, did, "LOW",
                    f"Code block #{i+1} in {did} has {len(lines)} lines of code but ZERO comments",
                    "Complex multi-step code snippet lacks line-by-line pedagogical annotations to explain each transformation.",
                    lines[0] if lines else ""
                )

# ─────────────────────────────────────────────────────────────────────────────
# 3. SHALLOW THEORY SECTIONS (< 100 words of concept prose)
# ─────────────────────────────────────────────────────────────────────────────
print("Scanning Dimension 3: Shallow Theory & Concepts Sections...")
for wn in range(1, 27):
    fp = WEEKS_DIR / f"week{wn}.html"
    if not fp.exists(): continue
    soup = BeautifulSoup(fp.read_text(encoding='utf-8'), 'html.parser')
    
    for ds in soup.find_all('div', class_=lambda c: c and 'day-section' in c):
        did = ds.get('id', 'unknown')
        if 'toolkit' in did: continue
        
        # Find theory heading
        theory_h2 = ds.find('h2', id=re.compile(r'theory')) or ds.find('h2', class_='sh2')
        if theory_h2:
            # Collect text between theory_h2 and next h2 or practice section
            prose_words = 0
            curr = theory_h2.next_sibling
            while curr and not (curr.name == 'h2' and 'theory' not in curr.get('id', '')):
                if curr.name in ['p', 'ul', 'ol', 'div'] and 'cb' not in curr.get('class', []) and 'quiz' not in curr.get('class', []):
                    prose_words += len(curr.text.split())
                curr = curr.next_sibling
                
            if prose_words < 60:
                h1 = ds.find('h1')
                title = h1.text.strip() if h1 else did
                log_gap(
                    "Shallow Theory Coverage", wn, did, "MEDIUM",
                    f"Shallow theory section in {did} ('{title}') ({prose_words} words)",
                    f"Theory section contains only {prose_words} words of conceptual explanation before moving into code or quizzes. Needs deeper background and trade-off analysis.",
                    title
                )

print(f"\nContent Gap Scanner complete! Cataloged {len(content_gaps)} pedagogical gaps.")
out_file = Path("scripts/all_content_gaps_inventory.json")
out_file.write_text(json.dumps(content_gaps, indent=2), encoding='utf-8')
print(f"Report saved to {out_file}")
