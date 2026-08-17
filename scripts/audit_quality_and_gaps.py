#!/usr/bin/env python3
import glob
import yaml
import re

files = sorted(glob.glob('src/data/week*.yaml'))

report = {
    'total_weeks': len(files),
    'total_days': 0,
    'missing_objectives': [],
    'missing_hinglish': [],
    'missing_predict': [],
    'missing_tasks': [],
    'missing_quizzes': [],
    'missing_flashcards': [],
    'missing_takeaways': [],
    'missing_resources': [],
    'markdown_in_theory': [],
    'empty_theory': []
}

for fpath in files:
    with open(fpath, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
        
    wnum = data['week_number']
    days = data.get('days', [])
    report['total_days'] += len(days)
    
    for d in days:
        did = f"W{wnum}D{d.get('id')}"
        
        if not d.get('objectives'):
            report['missing_objectives'].append(did)
        if not d.get('hinglish'):
            report['missing_hinglish'].append(did)
        if not d.get('predict'):
            report['missing_predict'].append(did)
        if not d.get('tasks'):
            report['missing_tasks'].append(did)
        if not d.get('quizzes'):
            report['missing_quizzes'].append(did)
        if not d.get('flashcards'):
            report['missing_flashcards'].append(did)
        if not d.get('takeaways'):
            report['missing_takeaways'].append(did)
        if not d.get('resources'):
            report['missing_resources'].append(did)
            
        theory = d.get('theory_html', '')
        if not theory or len(theory.strip()) < 50:
            report['empty_theory'].append(did)
        
        if re.search(r'```[a-z]*', theory) or re.search(r'(?m)^#{2,4}\s+', theory):
            report['markdown_in_theory'].append(did)

print(f"Total Weeks: {report['total_weeks']}")
print(f"Total Days: {report['total_days']}")
print(f"Missing Objectives: {len(report['missing_objectives'])} -> {report['missing_objectives'][:8]}")
print(f"Missing Hinglish: {len(report['missing_hinglish'])} -> {report['missing_hinglish'][:8]}")
print(f"Missing Predict: {len(report['missing_predict'])} -> {report['missing_predict'][:8]}")
print(f"Missing Tasks: {len(report['missing_tasks'])} -> {report['missing_tasks'][:8]}")
print(f"Missing Quizzes: {len(report['missing_quizzes'])} -> {report['missing_quizzes'][:8]}")
print(f"Missing Flashcards: {len(report['missing_flashcards'])} -> {report['missing_flashcards'][:8]}")
print(f"Missing Takeaways: {len(report['missing_takeaways'])} -> {report['missing_takeaways'][:8]}")
print(f"Missing Resources: {len(report['missing_resources'])} -> {report['missing_resources'][:8]}")
print(f"Unrendered Markdown in Theory: {len(report['markdown_in_theory'])} -> {report['markdown_in_theory'][:8]}")
print(f"Empty Theory (<50 chars): {len(report['empty_theory'])} -> {report['empty_theory']}")
