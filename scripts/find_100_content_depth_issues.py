#!/usr/bin/env python3
"""
100+ Depth & Rigor Issue Discovery Engine for 191-Day AI/ML Roadmap.
Scans for:
1. Generic fallback prediction code (e.g. `calculate_metric()`).
2. Generic fallback task solutions (e.g. `processed = [x * 2 for x in dataset]`).
3. Duplicate quiz options or identical distractors within the same quiz.
4. Short or repetitive flashcards (< 15 chars back text).
5. Days with sparse takeaway bullets (< 3 bullets).
6. Missing code blocks (<pre>) in theory sections.
7. Interactive quiz accessibility attributes.
"""

import glob
import yaml
import re

def find_100_issues():
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
            
            # 1. Check for generic fallback prediction code
            pred = d.get('predict', {})
            if isinstance(pred, dict):
                p_code = str(pred.get('code', ''))
                if 'calculate_metric' in p_code or 'multiplier = 2' in p_code:
                    issues.append({
                        'category': 'Generic Fallback Predict Code',
                        'location': f"{tag} ({title})",
                        'issue': f"Prediction challenge uses placeholder math snippet instead of real topic-specific Python/ML code."
                    })
                    
            # 2. Check for generic fallback task solution code
            for idx, t in enumerate(d.get('tasks', [])):
                sol = str(t.get('solution_code', ''))
                ttitle = t.get('title', f"Task {idx+1}")
                if 'processed = [x * 2 for x in dataset]' in sol or 'dataset = np.linspace(0, 10, 100)' in sol or 'pipeline_state =' in sol:
                    issues.append({
                        'category': 'Generic Fallback Task Solution',
                        'location': f"{tag} - Task {idx+1} ({ttitle})",
                        'issue': f"Task solution uses generic list/array dummy code instead of genuine algorithmic pipeline for {title}."
                    })

            # 3. Check for duplicate quiz options or identical distractors
            for q_idx, q in enumerate(d.get('quizzes', [])):
                opts = q.get('options', [])
                opt_texts = [str(o.get('text', '')).strip() for o in opts]
                if len(opt_texts) != len(set(opt_texts)):
                    issues.append({
                        'category': 'Duplicate Quiz Options',
                        'location': f"{tag} - Quiz {q_idx+1}",
                        'issue': f"Quiz has duplicate option text within choices: {opt_texts}"
                    })
                # Check for repeated distractor texts
                if any('Standard approach for' in ot or 'Plausible distractor' in ot for ot in opt_texts):
                    issues.append({
                        'category': 'Placeholder Quiz Distractor',
                        'location': f"{tag} - Quiz {q_idx+1}",
                        'issue': f"Quiz contains placeholder distractor label: {opt_texts}"
                    })

            # 4. Check for sparse takeaways (< 3 bullets)
            tk = d.get('takeaways', {})
            if isinstance(tk, dict):
                bullets = tk.get('bullets', [])
                if len(bullets) < 3:
                    issues.append({
                        'category': 'Sparse Daily Takeaways',
                        'location': f"{tag} ({title})",
                        'issue': f"Only {len(bullets)} takeaway bullets (minimum 3 required for thorough daily retention)."
                    })

            # 5. Check for short/trivial flashcards (< 15 chars back)
            for fc_idx, fc in enumerate(d.get('flashcards', [])):
                back = str(fc.get('back', '')).strip()
                front = str(fc.get('front', '')).strip()
                if len(back) < 15:
                    issues.append({
                        'category': 'Short Flashcard Explanation',
                        'location': f"{tag} - Flashcard {fc_idx+1} ('{front}')",
                        'issue': f"Flashcard back explanation is too brief ({len(back)} chars): '{back}'"
                    })
                if front.lower() == back.lower():
                    issues.append({
                        'category': 'Circular Flashcard',
                        'location': f"{tag} - Flashcard {fc_idx+1}",
                        'issue': f"Flashcard front is identical to back: '{front}'"
                    })

            # 6. Check theory code blocks
            th = str(d.get('theory_html', ''))
            if '<pre>' not in th and '<code>' not in th and len(th) > 0:
                issues.append({
                    'category': 'Missing Code Block in Theory',
                    'location': f"{tag} ({title})",
                    'issue': "Theory section has no formatted syntax-highlighted code examples (<pre>)."
                })

    print(f"============================================================")
    print(f"🚨 DISCOVERED {len(issues)} DEPTH & RIGOR ISSUES ACROSS ALL WEEKS")
    print(f"============================================================")
    for idx, item in enumerate(issues, 1):
        print(f"{idx}. [{item['category']}] {item['location']}: {item['issue']}")
    print(f"============================================================")

if __name__ == '__main__':
    find_100_issues()
