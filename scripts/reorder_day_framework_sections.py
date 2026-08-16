#!/usr/bin/env python3
"""
Canonical Section Ordering Engine:
Reorders the DOM elements inside every day section across all 26 weeks to strictly match the canonical standard:
1. Header & Title (h1, badges)
2. 🎯 Daily Objectives
3. 🧠 Theory & Concepts (h2 theory, prose, math, tables, diagrams)
4. ⚠️ Common Pitfalls & Gotchas (.gotcha-box)
5. 💻 Code Implementations & Walkthroughs (.cb)
6. 🔮 Predict the Output (.predict-box)
7. 📝 Practice Tasks & Solutions (.task-block, .task-item, .solution-drawer)
8. 🃏 Revision Flashcards (.flashcard, .flashcards-grid)
9. ✅ Self-Assessment Quizzes (.quiz-block)
10. 🔘 Complete Day Button (.complete-btn)
"""

from pathlib import Path
from bs4 import BeautifulSoup
import re

WEEKS_DIR = Path("pages/weeks")

for wn in range(1, 27):
    fp = WEEKS_DIR / f"week{wn}.html"
    if not fp.exists(): continue
    soup = BeautifulSoup(fp.read_text(encoding='utf-8'), 'html.parser')
    modified = False
    
    for ds in soup.find_all('div', class_=lambda c: c and 'day-section' in c):
        did = ds.get('id', '')
        if 'toolkit' in did: continue
        
        # Collect elements by category
        header_nodes = []
        obj_nodes = []
        theory_nodes = []
        gotcha_nodes = []
        code_nodes = []
        predict_nodes = []
        task_nodes = []
        flashcard_nodes = []
        quiz_nodes = []
        btn_nodes = []
        
        for child in list(ds.children):
            if isinstance(child, str) and not child.strip():
                continue
            
            c_text = child.text if hasattr(child, 'text') else str(child)
            c_classes = child.get('class', []) if hasattr(child, 'get') else []
            
            # Classification
            if hasattr(child, 'name') and child.name == 'h1':
                header_nodes.append(child)
            elif 'badge' in c_classes or 'day-meta' in c_classes or 'phase-tag' in c_classes:
                header_nodes.append(child)
            elif 'objective' in str(c_classes).lower() or '🎯' in c_text or 'Daily Objectives' in c_text:
                obj_nodes.append(child)
            elif 'gotcha' in str(c_classes).lower() or '⚠️' in c_text or 'Pitfall' in c_text:
                gotcha_nodes.append(child)
            elif 'predict' in str(c_classes).lower() or '🔮' in c_text or 'Predict the Output' in c_text:
                predict_nodes.append(child)
            elif 'task' in str(c_classes).lower() or 'practice' in str(c_classes).lower() or 'solution' in str(c_classes).lower() or '📝' in c_text:
                task_nodes.append(child)
            elif 'flashcard' in str(c_classes).lower() or '🃏' in c_text:
                flashcard_nodes.append(child)
            elif 'quiz' in str(c_classes).lower() or '✅' in c_text:
                quiz_nodes.append(child)
            elif 'complete' in str(c_classes).lower() or 'completeDay' in str(child):
                btn_nodes.append(child)
            elif 'cb' in c_classes or (hasattr(child, 'name') and child.name == 'pre'):
                code_nodes.append(child)
            else:
                theory_nodes.append(child)

        # Re-assemble in canonical order
        ordered_children = (
            header_nodes +
            obj_nodes +
            theory_nodes +
            gotcha_nodes +
            code_nodes +
            predict_nodes +
            task_nodes +
            flashcard_nodes +
            quiz_nodes +
            btn_nodes
        )
        
        # Clear and repopulate
        ds.clear()
        for node in ordered_children:
            ds.append(node)
        modified = True

    if modified:
        fp.write_text(str(soup), encoding='utf-8')
        print(f"  ✅ Reordered canonical sections in Week {wn}")

print("\n🎉 CANONICAL SECTION ORDER STANDARDIZED ACROSS ALL 26 WEEKS!")
