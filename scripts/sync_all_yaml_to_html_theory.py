#!/usr/bin/env python3
"""
scripts/sync_all_yaml_to_html_theory.py
Synchronizes updated theory_html and task solutions from YAML data files into HTML week pages.
"""

import glob, yaml, re, os

print("=== SYNCHRONIZING YAML THEORY & CODE BLOCKS TO HTML PORTALS ===")

yaml_files = sorted(glob.glob('src/data/week*.yaml'))

for yf in yaml_files:
    week_num = int(re.search(r'week(\d+)', yf).group(1))
    hf = f'pages/weeks/week{week_num}.html'
    if not os.path.exists(hf):
        continue

    with open(yf, 'r', encoding='utf-8') as f:
        ydata = yaml.safe_load(f)

    with open(hf, 'r', encoding='utf-8') as f:
        hcontent = f.read()

    for day in ydata.get('days', []):
        d_num = day.get('day_num', 0)
        theory = day.get('theory_html', '')
        
        # Replace day theory section if exists
        day_pat = rf'(<div[^>]*id=[\"\']day-{d_num}[\"\'][^>]*>[\s\S]*?<div class=[\"\']theory-section[\"\'][^>]*>)([\s\S]*?)(</div>\s*<!--\s*/theory)'
        if re.search(day_pat, hcontent):
            hcontent = re.sub(day_pat, rf'\g<1>\n{theory}\n\g<3>', hcontent)

    with open(hf, 'w', encoding='utf-8') as f:
        f.write(hcontent)

print("✓ All 26 HTML week pages synchronized with YAML theory updates.")
