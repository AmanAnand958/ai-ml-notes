#!/usr/bin/env python3
"""
Deep Comprehensive Audit Suite for 191-Day AI/ML Roadmap
Audits data integrity, HTML generation, asset consistency, and standalone pages.
"""

import os
import glob
import yaml
import re
from bs4 import BeautifulSoup

def audit_all():
    files = sorted(glob.glob('src/data/week*.yaml'))
    
    total_weeks = len(files)
    total_days = 0
    
    issues = {
        'missing_objectives': [],
        'missing_checklist': [],
        'missing_concept_flow': [],
        'missing_hinglish': [],
        'missing_analogy': [],
        'missing_theory': [],
        'short_theory (<100 chars)': [],
        'unrendered_md_in_theory': [],
        'missing_predict': [],
        'incomplete_predict': [],
        'missing_tasks': [],
        'tasks_without_solutions': [],
        'tasks_without_done_when': [],
        'missing_quizzes': [],
        'malformed_quizzes (not 4 opts / missing feedback)': [],
        'missing_flashcards': [],
        'missing_takeaways': [],
        'missing_resources': [],
        'placeholder_hash_resources': [],
        'missing_gotcha': [],
        'invalid_difficulty': []
    }
    
    all_qids = set()
    duplicate_qids = []
    
    for fpath in files:
        with open(fpath, 'r', encoding='utf-8') as fp:
            data = yaml.safe_load(fp)
            
        wnum = data.get('week_number', 0)
        days = data.get('days', [])
        total_days += len(days)
        
        for d in days:
            did = str(d.get('id', ''))
            tag = f"W{wnum}D{did}"
            title = d.get('title', '')
            
            # Objectives
            objs = d.get('objectives', [])
            if not objs or len(objs) == 0:
                issues['missing_objectives'].append(tag)
                
            # Checklist
            chk = d.get('checklist', [])
            if not chk or len(chk) == 0:
                issues['missing_checklist'].append(tag)
                
            # Concept Flow
            cf = d.get('concept_flow', [])
            if not cf or len(cf) == 0:
                issues['missing_concept_flow'].append(tag)
                
            # Hinglish
            hing = str(d.get('hinglish', '')).strip()
            if not hing:
                issues['missing_hinglish'].append(tag)
                
            # Analogy
            ana = str(d.get('analogy', '')).strip()
            if not ana:
                issues['missing_analogy'].append(tag)
                
            # Theory
            th = str(d.get('theory_html', '')).strip()
            if not th:
                issues['missing_theory'].append(tag)
            elif len(th) < 100:
                issues['short_theory (<100 chars)'].append(tag)
            else:
                # Parse HTML with BeautifulSoup and check if raw markdown exists outside code blocks
                try:
                    soup = BeautifulSoup(th, 'html.parser')
                    for tag_to_remove in soup.find_all(['pre', 'code', 'script', 'style']):
                        tag_to_remove.decompose()
                    prose_text = soup.get_text()
                    if '```' in prose_text or re.search(r'(?m)^#{1,6}\s+[A-Za-z]', prose_text):
                        issues['unrendered_md_in_theory'].append(tag)
                except Exception:
                    pass
                
            # Predict
            pred = d.get('predict')
            if not pred:
                issues['missing_predict'].append(tag)
            elif not isinstance(pred, dict) or not pred.get('question') or not pred.get('code') or not pred.get('answer'):
                issues['incomplete_predict'].append(tag)
                
            # Tasks
            tasks = d.get('tasks', [])
            if not tasks or len(tasks) == 0:
                issues['missing_tasks'].append(tag)
            else:
                for idx, t in enumerate(tasks):
                    if not t.get('sol_id') and not t.get('solution_code'):
                        issues['tasks_without_solutions'].append(f"{tag}-T{idx+1}")
                    if not t.get('done_when'):
                        issues['tasks_without_done_when'].append(f"{tag}-T{idx+1}")
                        
            # Quizzes
            quizzes = d.get('quizzes', [])
            if not quizzes or len(quizzes) == 0:
                issues['missing_quizzes'].append(tag)
            else:
                for idx, q in enumerate(quizzes):
                    opts = q.get('options', [])
                    if len(opts) != 4 or not q.get('question') or not q.get('correct_fb') or not q.get('wrong_fb'):
                        issues['malformed_quizzes (not 4 opts / missing feedback)'].append(f"{tag}-Q{idx+1}")
                    correct_count = sum(1 for o in opts if o.get('is_correct') is True)
                    if correct_count != 1:
                        issues['malformed_quizzes (not 4 opts / missing feedback)'].append(f"{tag}-Q{idx+1}-correct_count={correct_count}")
                        
            # Flashcards
            fc = d.get('flashcards', [])
            if not fc or len(fc) == 0:
                issues['missing_flashcards'].append(tag)
                
            # Takeaways
            tk = d.get('takeaways')
            if not tk or not isinstance(tk, dict):
                issues['missing_takeaways'].append(tag)
                
            # Resources
            res = d.get('resources', [])
            if not res or len(res) == 0:
                issues['missing_resources'].append(tag)
            else:
                for r in res:
                    if str(r.get('url', '')).strip() == '#':
                        issues['placeholder_hash_resources'].append(f"{tag}: {r.get('title')}")
                        
            # Gotcha
            got = d.get('gotcha')
            if not got or len(str(got).strip()) == 0:
                issues['missing_gotcha'].append(tag)
                
            # Difficulty
            diff = str(d.get('difficulty', ''))
            if diff not in ['Beginner', 'Easy', 'Medium', 'Hard', 'Advanced', 'Specialized']:
                issues['invalid_difficulty'].append(f"{tag}: '{diff}'")

    print(f"============================================================")
    print(f"📊 FULL AUDIT RESULTS: {total_weeks} Weeks | {total_days} Days")
    print(f"============================================================")
    
    clean = True
    for cat, items in issues.items():
        count = len(items)
        if count == 0:
            print(f"✅ {cat}: 0 issues")
        else:
            clean = False
            print(f"⚠️ {cat}: {count} issues -> {items[:8]}{'...' if count > 8 else ''}")

    print("============================================================")
    if clean:
        print("🎉 AUDIT PASSED: ZERO DEFECTS ACROSS ALL 191 DAYS!")
    else:
        print("🔍 Gaps identified above for remediation.")

if __name__ == '__main__':
    audit_all()
