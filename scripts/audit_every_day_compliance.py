#!/usr/bin/env python3
"""
Canonical 9-Part Day Compliance & Completeness Scanner:
Audits every single day/module (198 days) across all 26 weeks for:
1. 🏷️ Metadata & Title Header (h1, badges, time, XP)
2. 🎯 Daily Objectives (objectives list)
3. 🧠 Theory & Concepts Section (h2 theory, prose, math/tables)
4. 💻 Code Implementations (.cb code blocks)
5. ⚠️ Production Gotchas / Common Pitfalls (.gotcha-box or callout)
6. 🔮 Predict the Output Interactive Widget (predict block)
7. 📝 Practice Coding Tasks & Solutions (task block or solution drawer)
8. 🃏 Revision Flashcards (.flashcard elements)
9. ✅ Quizzes & Complete Day Button (.quiz-block + complete-btn)
"""

import re
import json
from pathlib import Path
from bs4 import BeautifulSoup
from collections import defaultdict

WEEKS_DIR = Path("pages/weeks")
ROOT_DIR = Path(".")

day_compliance_report = []

for wn in range(1, 27):
    fp = WEEKS_DIR / f"week{wn}.html"
    if not fp.exists(): continue
    raw_html = fp.read_text(encoding='utf-8', errors='replace')
    soup = BeautifulSoup(raw_html, 'html.parser')
    
    for ds in soup.find_all('div', class_=lambda c: c and 'day-section' in c):
        did = ds.get('id', 'unknown')
        is_toolkit = 'toolkit' in did
        
        h1 = ds.find('h1')
        title = h1.text.strip() if h1 else did
        
        # 1. Check Objectives
        has_objectives = bool(ds.find(class_=re.compile(r'objective|daily-obj|objectives')) or '🎯' in ds.text or 'Objectives' in ds.text)
        
        # 2. Check Theory
        has_theory = bool(ds.find('h2', id=re.compile(r'theory')) or ds.find('h2', class_='sh2') or '🧠' in ds.text or 'Theory' in ds.text)
        
        # 3. Check Code Blocks
        code_count = len(ds.find_all('div', class_='cb')) + len(ds.find_all('pre'))
        
        # 4. Check Gotchas
        has_gotchas = bool(ds.find(class_=re.compile(r'gotcha|pitfall|callout-warning')) or '⚠️' in ds.text or 'Gotcha' in ds.text or 'Common Pitfall' in ds.text)
        
        # 5. Check Predict the Output
        has_predict = bool(ds.find(class_=re.compile(r'predict|pred-box')) or '🔮' in ds.text or 'Predict the Output' in ds.text)
        
        # 6. Check Practice Tasks
        has_tasks = bool(ds.find(class_=re.compile(r'task|practice|exercise|solution-drawer')) or '💻' in ds.text or 'Task' in ds.text or 'Coding Task' in ds.text)
        
        # 7. Check Flashcards
        flashcard_count = len(ds.find_all('div', class_='flashcard'))
        
        # 8. Check Quizzes
        quiz_count = len(ds.find_all('div', class_='quiz-block'))
        
        # 9. Check Complete Button
        has_complete_btn = bool(ds.find('button', class_=re.compile(r'complete-btn|btn-complete')) or ds.find('button', onclick=re.compile(r'completeDay')))
        
        # Calculate Compliance Score (out of 9 points)
        score = 0
        missing_components = []
        
        if has_objectives: score += 1
        else: missing_components.append("🎯 Daily Objectives")
        
        if has_theory: score += 1
        else: missing_components.append("🧠 Theory & Concepts")
        
        if code_count > 0: score += 1
        else: missing_components.append("💻 Code Blocks")
        
        if has_gotchas or is_toolkit: score += 1
        else: missing_components.append("⚠️ Gotchas & Pitfalls")
        
        if has_predict or is_toolkit: score += 1
        else: missing_components.append("🔮 Predict Widget")
        
        if has_tasks or is_toolkit: score += 1
        else: missing_components.append("📝 Practice Tasks")
        
        if flashcard_count > 0 or is_toolkit: score += 1
        else: missing_components.append("🃏 Flashcards")
        
        if quiz_count > 0 or is_toolkit: score += 1
        else: missing_components.append("✅ Quizzes")
        
        if has_complete_btn or is_toolkit: score += 1
        else: missing_components.append("🔘 Complete Day Button")
        
        compliance_pct = round((score / 9) * 100, 1)
        
        day_compliance_report.append({
            "week": wn,
            "day": did,
            "title": title,
            "score": score,
            "compliance_pct": compliance_pct,
            "missing": missing_components,
            "code_count": code_count,
            "quiz_count": quiz_count,
            "flashcard_count": flashcard_count
        })

out_file = ROOT_DIR / "scripts" / "every_day_compliance_inventory.json"
out_file.write_text(json.dumps(day_compliance_report, indent=2), encoding='utf-8')

# Print summary
perfect_days = [d for d in day_compliance_report if d['score'] == 9]
imperfect_days = [d for d in day_compliance_report if d['score'] < 9]

print("=== CANONICAL 9-PART DAY COMPLIANCE AUDIT ===")
print(f"Total Days/Modules Scanned: {len(day_compliance_report)}")
print(f"100% Fully Compliant Days : {len(perfect_days)} ({round(len(perfect_days)/len(day_compliance_report)*100, 1)}%)")
print(f"Days Missing Any Component: {len(imperfect_days)}")
print(f"Report saved to {out_file}")
