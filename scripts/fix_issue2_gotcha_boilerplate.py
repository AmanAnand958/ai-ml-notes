#!/usr/bin/env python3
"""
scripts/fix_issue2_gotcha_boilerplate.py
Fixes Issue 2: Removes generic boilerplate appended to gotcha.description in Weeks 18-26:
`(Avoid anti-pattern: always validate with strict assertion checks e.g. `assert input_tensor.shape[-1] == expected_dim`)`
Restores authentic, topic-specific gotchas matching Weeks 13-17 standard.
"""

import os, re, yaml
from curriculum_utils import load_yaml, save_yaml

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA_DIR = os.path.join(ROOT_DIR, 'src/data')

BOILERPLATE_PATTERN = r'\s*\(Avoid anti-pattern:\s*always validate with strict assertion checks e\.g\.\s*`assert input_tensor\.shape\[-1\]\s*==\s*expected_dim`\)'

def fix_gotchas():
    counts_per_file = {}
    
    for w in range(18, 27):
        fpath = f"{DATA_DIR}/week{w:02d}.yaml"
        if not os.path.exists(fpath): continue
        data = load_yaml(fpath)
        
        file_count = 0
        for d in data.get('days', []):
            did = d['id']
            gotcha = d.get('gotcha')
            if gotcha and isinstance(gotcha, dict):
                desc = gotcha.get('description', '')
                if 'always validate with strict assertion checks' in desc:
                    # Clean out the boilerplate
                    cleaned_desc = re.sub(BOILERPLATE_PATTERN, '', desc).strip()
                    # Also handle any slight whitespace or formatting variation
                    if 'always validate with strict assertion checks' in cleaned_desc:
                        cleaned_desc = cleaned_desc.split('(Avoid anti-pattern: always validate with strict assertion checks')[0].strip()
                    
                    gotcha['description'] = cleaned_desc
                    file_count += 1
                    
        save_yaml(fpath, data)
        counts_per_file[f"week{w:02d}.yaml"] = file_count
        
    return counts_per_file

if __name__ == '__main__':
    counts = fix_gotchas()
    print("=" * 60)
    print("Issue 2: Generic Gotcha Boilerplate Removed")
    print("=" * 60)
    for fname, cnt in counts.items():
        print(f"  • {fname}: {cnt} instances changed")
    print(f"Total instances changed: {sum(counts.values())}")
