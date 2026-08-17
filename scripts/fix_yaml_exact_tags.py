#!/usr/bin/env python3
"""
scripts/fix_yaml_exact_tags.py
"""

import yaml, re

# 1. Week 3 Day 19
with open('src/data/week03.yaml', 'r', encoding='utf-8') as f:
    w3 = yaml.safe_load(f)

for day in w3['days']:
    if day['day_num'] == 19:
        th = day['theory_html'].strip()
        # If it ends with </div> from the outer day-19-theory container, strip it
        if th.endswith('</div>'):
            th = th[:-6].rstrip()
            day['theory_html'] = th

with open('src/data/week03.yaml', 'w', encoding='utf-8') as f:
    yaml.dump(w3, f, allow_unicode=True, default_flow_style=False, sort_keys=False)

# 2. Week 5 Day 35 & 37
with open('src/data/week05.yaml', 'r', encoding='utf-8') as f:
    w5 = yaml.safe_load(f)

for day in w5['days']:
    if day['day_num'] in [35, 37]:
        th = day['theory_html']
        th = th.replace('}</span>', '}')
        day['theory_html'] = th

with open('src/data/week05.yaml', 'w', encoding='utf-8') as f:
    yaml.dump(w5, f, allow_unicode=True, default_flow_style=False, sort_keys=False)

print("Cleaned exact YAML tags in week03 and week05.")
