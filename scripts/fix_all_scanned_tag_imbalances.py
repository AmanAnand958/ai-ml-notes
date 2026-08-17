#!/usr/bin/env python3
"""
scripts/fix_all_scanned_tag_imbalances.py
Fixes:
1. week03.yaml Day 19 theory Plotly section sync (unclosed <div>)
2. week05.yaml and week5.html orphaned </span> tags in Day 35 and Day 37
"""

import yaml, re

print("=== REMEDIATING ALL IDENTIFIED TAG DISCREPANCIES ===")

# 1. FIX week03.yaml Day 19
with open('pages/weeks/week3.html', 'r', encoding='utf-8') as f:
    h3_text = f.read()

# Extract Day 19 theory from week3.html
m = re.search(r'<div id="day-19-theory" class="theory">([\s\S]*?)(?=<div class="predict-block")', h3_text)
if m:
    day19_theory = m.group(1).strip()
    with open('src/data/week03.yaml', 'r', encoding='utf-8') as f:
        w3 = yaml.safe_load(f)
    for day in w3['days']:
        if day['day_num'] == 19:
            day['theory_html'] = day19_theory
    with open('src/data/week03.yaml', 'w', encoding='utf-8') as f:
        yaml.dump(w3, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
    print("✓ Fixed src/data/week03.yaml Day 19 theory")

# 2. FIX week05.yaml & week5.html
with open('pages/weeks/week5.html', 'r', encoding='utf-8') as f:
    h5_text = f.read()

h5_text = h5_text.replace(
'''param_grid = {
    "knn__n_neighbors": [3, 5, 7, 9, 11],
    "knn__weights": ["uniform", "distance"],
    "knn__metric": ["euclidean", "manhattan"]
}</span>''',
'''param_grid = {
    "knn__n_neighbors": [3, 5, 7, 9, 11],
    "knn__weights": ["uniform", "distance"],
    "knn__metric": ["euclidean", "manhattan"]
}'''
)

with open('pages/weeks/week5.html', 'w', encoding='utf-8') as f:
    f.write(h5_text)
print("✓ Fixed pages/weeks/week5.html orphaned </span> tags")

with open('src/data/week05.yaml', 'r', encoding='utf-8') as f:
    w5_text = f.read()

w5_text = w5_text.replace(
'''param_grid = {\\n    \\"knn__n_neighbors\\": [3, 5, 7, 9, 11],\\n    \\"knn__weights\\": [\\"uniform\\", \\"distance\\"],\\n    \\"knn__metric\\": [\\"euclidean\\", \\"manhattan\\"]\\n}</span>''',
'''param_grid = {\\n    \\"knn__n_neighbors\\": [3, 5, 7, 9, 11],\\n    \\"knn__weights\\": [\\"uniform\\", \\"distance\\"],\\n    \\"knn__metric\\": [\\"euclidean\\", \\"manhattan\\"]\\n}'''
)
# Also standard regex replace in case formatting varies
w5_text = re.sub(r'(\"knn__metric\": \[\"euclidean\", \"manhattan\"\]\\n\})</span>', r'\1', w5_text)

with open('src/data/week05.yaml', 'w', encoding='utf-8') as f:
    f.write(w5_text)
print("✓ Fixed src/data/week05.yaml orphaned </span> tags")
