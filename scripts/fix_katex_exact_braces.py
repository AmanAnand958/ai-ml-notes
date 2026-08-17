#!/usr/bin/env python3
"""
scripts/fix_katex_exact_braces.py
"""

import yaml

with open('src/data/week05.yaml', 'r', encoding='utf-8') as f:
    d = yaml.safe_load(f)

for day in d['days']:
    if day['day_num'] == 32:
        day['theory_html'] = day['theory_html'].replace(
            r'R^2 = 1 - \frac{SS_{\text{res}}}{SS_{\text{tot}}',
            r'R^2 = 1 - \frac{SS_{\text{res}}}{SS_{\text{tot}}}'
        )
    elif day['day_num'] == 33:
        day['theory_html'] = day['theory_html'].replace(
            r'\text{Precision} = \frac{\text{TP}{\text{TP} + \text{FP}',
            r'\text{Precision} = \frac{\text{TP}}{\text{TP} + \text{FP}}'
        )

with open('src/data/week05.yaml', 'w', encoding='utf-8') as f:
    yaml.dump(d, f, allow_unicode=True, default_flow_style=False, sort_keys=False)

print("Fixed in week05.yaml")

with open('pages/weeks/week5.html', 'r', encoding='utf-8') as f:
    h = f.read()

h = h.replace(
    r'R^2 = 1 - \frac{SS_{\text{res}}}{SS_{\text{tot}}',
    r'R^2 = 1 - \frac{SS_{\text{res}}}{SS_{\text{tot}}}'
)
h = h.replace(
    r'\text{Precision} = \frac{\text{TP}{\text{TP} + \text{FP}',
    r'\text{Precision} = \frac{\text{TP}}{\text{TP} + \text{FP}}'
)

with open('pages/weeks/week5.html', 'w', encoding='utf-8') as f:
    f.write(h)

print("Fixed in week5.html")
