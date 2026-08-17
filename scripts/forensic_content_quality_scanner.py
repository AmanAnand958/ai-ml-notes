#!/usr/bin/env python3
"""
Forensic Content Quality Scanner
Detects generic boilerplate, templated filler, short explanations, and repetitive patterns
across all 191 days in all 26 YAML files.
"""

import glob
import yaml
import re

def scan_curriculum_quality():
    files = sorted(glob.glob('src/data/week*.yaml'))
    
    issues = {
        'generic_checklists': [],
        'generic_tasks_or_solutions': [],
        'generic_predictions': [],
        'generic_flashcards': [],
        'generic_analogies': [],
        'generic_gotchas': [],
        'generic_resources': [],
        'empty_takeaway_hinglish': []
    }
    
    for fpath in files:
        with open(fpath, 'r', encoding='utf-8') as fp:
            data = yaml.safe_load(fp)
            
        wnum = data.get('week_number', 0)
        
        for d in data.get('days', []):
            did = str(d.get('id', ''))
            tag = f"W{wnum}D{did}"
            title = d.get('title', '')
            
            # 1. Checklist quality
            chks = d.get('checklist', [])
            for c in chks:
                text = c.get('text', '') if isinstance(c, dict) else str(c)
                if 'Study the core mathematical and architectural principles' in text or 'Implement the hands-on code exercises and verify' in text:
                    issues['generic_checklists'].append(tag)
                    break
                    
            # 2. Tasks / Solutions quality
            tasks = d.get('tasks', [])
            for idx, t in enumerate(tasks):
                code = str(t.get('solution_code', ''))
                prompt = str(t.get('prompt_html', ''))
                if 'metric = 0.98' in code or 'execute_task_' in code or 'TODO' in prompt or 'TBD' in prompt:
                    issues['generic_tasks_or_solutions'].append(f"{tag}-T{idx+1}")
                    
            # 3. Predict quality
            pred = d.get('predict', {})
            if isinstance(pred, dict):
                p_code = str(pred.get('code', ''))
                p_q = str(pred.get('question', ''))
                if 'x = 10' in p_code or 'predict the exact output' in p_q.lower() and len(p_code.strip()) < 30:
                    issues['generic_predictions'].append(tag)
                    
            # 4. Flashcards quality
            fcs = d.get('flashcards', [])
            for idx, fc in enumerate(fcs):
                front = str(fc.get('front', ''))
                back = str(fc.get('back', ''))
                if 'Key principle of' in front or 'Core Objective of' in front or 'Common failure mode in' in front or 'When to use' in front:
                    issues['generic_flashcards'].append(f"{tag}-FC{idx+1}")
                    
            # 5. Analogy quality
            ana = str(d.get('analogy', ''))
            if 'is like an essential foundational building block' in ana:
                issues['generic_analogies'].append(tag)
                
            # 6. Gotcha quality
            got = str(d.get('gotcha', ''))
            if 'never assume default configurations work out of the box' in got:
                issues['generic_gotchas'].append(tag)
                
            # 7. Resources quality
            res = d.get('resources', [])
            for r in res:
                rtitle = str(r.get('title', ''))
                if 'Reference Guide' in rtitle and 'Official documentation and API reference for Day' in str(r.get('desc', '')):
                    issues['generic_resources'].append(f"{tag}: {rtitle}")
                    
            # 8. Takeaways hinglish
            tk = d.get('takeaways', {})
            if isinstance(tk, dict):
                if not tk.get('hinglish_line') or len(str(tk.get('hinglish_line')).strip()) == 0:
                    issues['empty_takeaway_hinglish'].append(tag)

    print("============================================================")
    print("🔍 DETAILED FORENSIC CONTENT QUALITY SCAN")
    print("============================================================")
    for k, v in issues.items():
        print(f"📌 {k}: {len(v)} occurrences")
        if v:
            print(f"   Sample: {v[:6]}{'...' if len(v)>6 else ''}")
    print("============================================================")

if __name__ == '__main__':
    scan_curriculum_quality()
