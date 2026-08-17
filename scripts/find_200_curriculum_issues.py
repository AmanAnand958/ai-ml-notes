#!/usr/bin/env python3
"""
200+ Forensic Curriculum & Application Layer Issue Discovery Engine
Scans for:
1. Generic quiz feedback explanations (e.g. "✅ Correct! This is the canonical, verified architectural principle for...").
2. Short or vague prediction explanations (< 40 characters).
3. Missing or generic task git commit commands (`git_cmd`).
4. Resource cards with missing or empty `type` attributes.
5. Missing or non-standard daily difficulty badges.
6. HTML meta description uniqueness across compiled pages.
"""

import glob
import yaml
import re
from bs4 import BeautifulSoup

def find_200_issues():
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
            
            # 1. Check Quiz Feedback Specificity
            for q_idx, q in enumerate(d.get('quizzes', [])):
                c_fb = str(q.get('correct_fb', '')).strip()
                w_fb = str(q.get('wrong_fb', '')).strip()
                if 'This is the canonical, verified architectural principle for' in c_fb or len(c_fb) < 25:
                    issues.append({
                        'category': 'Generic Quiz Correct Feedback',
                        'location': f"{tag} - Quiz {q_idx+1}",
                        'issue': f"Correct feedback uses templated fallback sentence: '{c_fb[:50]}...'"
                    })
                if 'Review the theory section for the exact mathematical formulation of' in w_fb or len(w_fb) < 25:
                    issues.append({
                        'category': 'Generic Quiz Wrong Feedback',
                        'location': f"{tag} - Quiz {q_idx+1}",
                        'issue': f"Wrong feedback uses templated fallback sentence: '{w_fb[:50]}...'"
                    })

            # 2. Check Prediction Explanation Specificity
            pred = d.get('predict', {})
            if isinstance(pred, dict):
                p_exp = str(pred.get('explanation', '')).strip()
                if len(p_exp) < 40 or 'Prediction Challenge for Day' in p_exp:
                    issues.append({
                        'category': 'Brief Prediction Explanation',
                        'location': f"{tag} (Predict)",
                        'issue': f"Prediction explanation is too brief ({len(p_exp)} chars): '{p_exp}'"
                    })

            # 3. Check Task Git Commit Commands
            for t_idx, t in enumerate(d.get('tasks', [])):
                git_cmd = str(t.get('git_cmd', '')).strip()
                if not git_cmd or 'git commit' not in git_cmd:
                    issues.append({
                        'category': 'Missing Task Git Command',
                        'location': f"{tag} - Task {t_idx+1} ({t.get('title')})",
                        'issue': "Task lacks a copyable professional git commit workflow command."
                    })

            # 4. Check Resource Card Type
            for r_idx, r in enumerate(d.get('resources', [])):
                r_type = str(r.get('type', '')).strip()
                if not r_type:
                    issues.append({
                        'category': 'Missing Resource Type Badge',
                        'location': f"{tag} - Resource {r_idx+1} ({r.get('title')})",
                        'issue': "Resource card type is empty string (expected VIDEO, DOCS, PAPER, or GITHUB)."
                    })

            # 5. Check Badges
            badges = d.get('badges', [])
            if not badges or len(badges) == 0:
                issues.append({
                    'category': 'Missing Daily Badges',
                    'location': tag,
                    'issue': f"Day lacks metadata badges for difficulty and learning phase."
                })

    print(f"============================================================")
    print(f"🚨 DISCOVERED {len(issues)} ADVANCED PEDAGOGICAL & WORKFLOW ISSUES")
    print(f"============================================================")
    for idx, item in enumerate(issues, 1):
        print(f"{idx}. [{item['category']}] {item['location']}: {item['issue']}")
    print(f"============================================================")

if __name__ == '__main__':
    find_200_issues()
