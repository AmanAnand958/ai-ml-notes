#!/usr/bin/env python3
"""
scripts/fix_issue3_corrupted_latex.py
Fixes Issue 3: Corrects corrupted LaTeX backslashes in Week 19 Day 136 Flashcard #2
from `\\\\sum` and `\\\\frac` to `\sum` and `\frac`.
"""

import os, re
from curriculum_utils import load_yaml, save_yaml

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA_DIR = os.path.join(ROOT_DIR, 'src/data')

def fix_latex():
    counts_per_file = {}
    for w in range(13, 27):
        fpath = f"{DATA_DIR}/week{w:02d}.yaml"
        if not os.path.exists(fpath): continue
        data = load_yaml(fpath)
        
        file_count = 0
        for d in data.get('days', []):
            did = d['id']
            for fc in d.get('flashcards', []):
                for key in ['front', 'back']:
                    val = str(fc.get(key, ''))
                    if '\\\\' in val:
                        # Clean up 4 backslashes down to single backslash
                        new_val = val.replace('\\\\\\\\sum', r'\sum').replace('\\\\\\\\frac', r'\frac').replace('\\\\sum', r'\sum').replace('\\\\frac', r'\frac')
                        if new_val != val:
                            fc[key] = new_val
                            file_count += 1
                            
        save_yaml(fpath, data)
        counts_per_file[f"week{w:02d}.yaml"] = file_count
        
    return counts_per_file

if __name__ == '__main__':
    counts = fix_latex()
    print("=" * 60)
    print("Issue 3: Corrupted LaTeX Backslashes Fixed in Flashcards")
    print("=" * 60)
    for fname, cnt in counts.items():
        if cnt > 0 or fname == 'week19.yaml':
            print(f"  • {fname}: {cnt} instances changed")
    print(f"Total instances changed: {sum(counts.values())}")
