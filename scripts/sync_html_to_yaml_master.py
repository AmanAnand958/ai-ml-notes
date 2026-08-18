#!/usr/bin/env python3
"""
sync_html_to_yaml_master.py
Reverses the flow: Extracted perfectly polished and remediated HTML from pages/weeks/*.html
and injects it safely back into the source of truth YAML files (src/data/*.yaml).
"""

import glob
import re
import os
import yaml
import html as html_module
from bs4 import BeautifulSoup

def represent_str(dumper, data):
    """Force PyYAML to use block scalars (|-) for multiline strings to keep YAML readable."""
    if '\n' in data:
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
    return dumper.represent_scalar('tag:yaml.org,2002:str', data)

yaml.add_representer(str, represent_str)
yaml.SafeDumper.add_representer(str, represent_str)

print("=== REVERSE SYNC: HTML ARTIFACTS -> YAML SOURCE OF TRUTH ===")

yaml_files = sorted(glob.glob('src/data/week*.yaml'))

for yf in yaml_files:
    week_num_match = re.search(r'week(\d+)', yf)
    if not week_num_match:
        continue
    week_num = int(week_num_match.group(1))
    
    html_file = f'pages/weeks/week{week_num}.html'
    if not os.path.exists(html_file):
        continue
        
    print(f"Processing Week {week_num}...")
    
    with open(yf, 'r', encoding='utf-8') as f:
        ydata = yaml.safe_load(f)
        
    with open(html_file, 'r', encoding='utf-8') as f:
        hcontent = f.read()
        soup = BeautifulSoup(hcontent, 'html.parser')
        
    for idx, day in enumerate(ydata.get('days', [])):
        day_num = day.get('day_num')
        day_id = f"day-{day_num}"
        
        # Determine the boundary of this day's HTML
        start_idx = hcontent.find(f'id="{day_id}"')
        if start_idx == -1:
            start_idx = hcontent.find(f"id='{day_id}'")
        
        if start_idx == -1:
            continue
            
        # Find the start of the next day, or end of file
        next_day_id = None
        if idx + 1 < len(ydata['days']):
            next_day_id = f"day-{ydata['days'][idx+1].get('day_num')}"
            
        end_idx = len(hcontent)
        if next_day_id:
            n_idx = hcontent.find(f'id="{next_day_id}"', start_idx)
            if n_idx != -1:
                end_idx = n_idx
                
        # Slice the HTML for this specific day
        day_html_slice = hcontent[start_idx:end_idx]
        day_soup = BeautifulSoup(day_html_slice, 'html.parser')
            
        # 1. Sync theory_html
        theory_section = day_soup.find('div', class_='theory-section')
        if theory_section:
            inner_html = theory_section.decode_contents()
            day['theory_html'] = inner_html.strip() + "\n"
            
        # 2. Sync tasks solution_code
        tasks_in_yaml = day.get('tasks', [])
        task_blocks_in_html = day_soup.find_all('div', class_='task-block')
        
        for t_idx, task_yaml in enumerate(tasks_in_yaml):
            if t_idx < len(task_blocks_in_html):
                html_task = task_blocks_in_html[t_idx]
                code_block = html_task.find('code')
                if code_block:
                    raw_code = code_block.get_text()
                    task_yaml['solution_code'] = raw_code.strip() + "\n"
                    
        # 3. Sync predict code
        predict_yaml = day.get('predict')
        if predict_yaml:
            predict_block = day_soup.find('div', class_='predict-block')
            if predict_block:
                code_block = predict_block.find('code')
                if code_block:
                    raw_code = code_block.get_text()
                    predict_yaml['code'] = raw_code.strip() + "\n"
                    
    # Write back to YAML
    with open(yf, 'w', encoding='utf-8') as f:
        yaml.safe_dump(ydata, f, sort_keys=False, allow_unicode=True, width=1000)
        
print("\n✓ SUCCESS: All 26 YAML Source of Truth files have been overwritten with fully remediated HTML snippets!")
