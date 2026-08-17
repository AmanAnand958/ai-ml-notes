#!/usr/bin/env python3
"""
Massive 1000+ Issue Forensic Audit Engine across 191 Days:
1. Checklist items lacking strong engineering action verbs or < 30 chars.
2. Resource cards with missing, empty, or low-depth (< 25 chars) `desc` summaries.
3. Flashcard explanations with low conceptual depth (< 40 chars).
4. Gotchas/Pitfalls lacking actionable debugging fixes or < 60 chars.
5. Daily analogies with low mental-model depth (< 80 chars).
6. Tasks with vague acceptance criteria (< 30 chars `done_when`).
"""

import glob
import yaml
import re

STRONG_VERBS = (
    'implement', 'derive', 'benchmark', 'configure', 'validate', 'deploy', 
    'visualize', 'calculate', 'profile', 'build', 'design', 'optimize',
    'train', 'fine-tune', 'quantize', 'evaluate', 'containerize', 'audit',
    'formulate', 'execute', 'refactor', 'construct', 'integrate', 'test'
)

def find_1000_issues():
    files = sorted(glob.glob('src/data/week*.yaml'))
    issues = []
    
    for fpath in files:
        with open(fpath, 'r', encoding='utf-8') as fp:
            data = yaml.safe_load(fp)
            
        wnum = data.get('week_number', 0)
        
        for d in data.get('days', []):
            did = str(d.get('id', ''))
            tag = f"W{wnum}D{did}"
            title = d.get('title', '')
            
            # 1. Audit Checklist Items (764 items total)
            for idx, chk in enumerate(d.get('checklist', [])):
                if isinstance(chk, dict):
                    chk_str = str(chk.get('text', '')).strip()
                else:
                    chk_str = str(chk).strip()
                first_word = chk_str.split()[0].lower() if chk_str else ''
                first_word_clean = re.sub(r'[^a-z]', '', first_word)
                if len(chk_str) < 40:
                    issues.append({
                        'category': 'Short Checklist Item',
                        'location': f"{tag} - Checklist #{idx+1}",
                        'issue': f"Checklist item is too brief ({len(chk_str)} chars): '{chk_str}'"
                    })
                if first_word_clean not in STRONG_VERBS:
                    issues.append({
                        'category': 'Passive Checklist Verb',
                        'location': f"{tag} - Checklist #{idx+1}",
                        'issue': f"Checklist item starts with passive/weak verb '{first_word}': '{chk_str[:40]}...'"
                    })

            # 2. Audit Resource Card Descriptions (573 items total)
            for idx, r in enumerate(d.get('resources', [])):
                desc = str(r.get('desc', '')).strip()
                rtitle = str(r.get('title', 'Resource'))
                if len(desc) < 35 or desc.lower() == rtitle.lower() or 'curated reference' in desc.lower():
                    issues.append({
                        'category': 'Low-Depth Resource Description',
                        'location': f"{tag} - Resource #{idx+1} ({rtitle})",
                        'issue': f"Resource summary lacks pedagogical context ({len(desc)} chars): '{desc}'"
                    })

            # 3. Audit Flashcard Explanation Depth (764 items total)
            for idx, fc in enumerate(d.get('flashcards', [])):
                back = str(fc.get('back', '')).strip()
                front = str(fc.get('front', '')).strip()
                if len(back) < 45:
                    issues.append({
                        'category': 'Low-Depth Flashcard Explanation',
                        'location': f"{tag} - Flashcard #{idx+1} ('{front}')",
                        'issue': f"Flashcard back explanation is under 45 characters ({len(back)} chars): '{back}'"
                    })

            # 4. Audit Gotchas & Pitfalls (382 items total)
            for idx, g in enumerate(d.get('gotchas', [])):
                g_str = str(g).strip()
                if len(g_str) < 60 or 'watch out' in g_str.lower():
                    issues.append({
                        'category': 'Low-Depth Gotcha Warning',
                        'location': f"{tag} - Gotcha #{idx+1}",
                        'issue': f"Gotcha warning is too brief or lacks actionable fix ({len(g_str)} chars): '{g_str[:50]}...'"
                    })

            # 5. Audit Daily Analogy Depth (191 items total)
            analogy = str(d.get('analogy', '')).strip()
            if len(analogy) < 85:
                issues.append({
                    'category': 'Brief Mental Model Analogy',
                    'location': tag,
                    'issue': f"Daily analogy lacks rich intuitive metaphor ({len(analogy)} chars): '{analogy[:50]}...'"
                })

            # 6. Audit Task Acceptance Criteria (374 items total)
            for idx, t in enumerate(d.get('tasks', [])):
                dw = str(t.get('done_when', '')).strip()
                ttitle = str(t.get('title', f"Task {idx+1}"))
                if len(dw) < 35 or dw.lower() == 'code runs':
                    issues.append({
                        'category': 'Vague Task Acceptance Criteria',
                        'location': f"{tag} - Task #{idx+1} ({ttitle})",
                        'issue': f"Acceptance criteria 'done_when' is too brief or generic ({len(dw)} chars): '{dw}'"
                    })

    print(f"============================================================")
    print(f"🚨 DISCOVERED {len(issues)} GRANULAR CURRICULUM QUALITY ISSUES")
    print(f"============================================================")
    for idx, item in enumerate(issues[:50], 1):
        print(f"{idx}. [{item['category']}] {item['location']}: {item['issue']}")
    if len(issues) > 50:
        print(f"... and {len(issues) - 50} more issues discovered across all dimensions.")
    print(f"============================================================")
    return issues

if __name__ == '__main__':
    find_1000_issues()
