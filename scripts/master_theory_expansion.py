#!/usr/bin/env python3
"""
scripts/master_theory_expansion.py
Comprehensive generator expanding all days in Weeks 18 to 26 to full pedagogical depth
(3,500 - 7,000+ characters, 3-5 sections, code blocks with syntax highlighting, formulas, and diagrams).
"""

import os, yaml

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA_DIR = os.path.join(ROOT_DIR, 'src/data')

class LiteralStr(str): pass
def lit_repr(dumper, data):
    if '\n' in data:
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
    return dumper.represent_scalar('tag:yaml.org,2002:str', data)
yaml.add_representer(LiteralStr, lit_repr)

def load_yaml(path):
    with open(path, 'r', encoding='utf-8') as f: return yaml.safe_load(f)

def deep_literal(obj):
    if isinstance(obj, dict): return {k: deep_literal(v) for k,v in obj.items()}
    if isinstance(obj, list): return [deep_literal(v) for v in obj]
    if isinstance(obj, str) and '\n' in obj: return LiteralStr(obj)
    return obj

def save_yaml(path, data):
    data = deep_literal(data)
    with open(path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, allow_unicode=True, default_flow_style=False, sort_keys=False, width=120)

from full_depth_theory_w18 import W18_THEORY
from theory_deep_w19_w20 import W19_W20_THEORY
from full_depth_theory_w21_to_w26 import FULL_DEPTH_THEORY

MASTER_THEORY = {}
MASTER_THEORY.update(W18_THEORY)
MASTER_THEORY.update(W19_W20_THEORY)
MASTER_THEORY.update(FULL_DEPTH_THEORY)

print(f"Loaded {len(MASTER_THEORY)} master theory definitions across Weeks 18-26.")

for w in range(18, 27):
    fpath = os.path.join(DATA_DIR, f"week{w:02d}.yaml")
    if not os.path.exists(fpath): continue
    data = load_yaml(fpath)

    for day in data.get('days', []):
        did = day.get('id')
        try:
            day_num = int(did)
        except (ValueError, TypeError):
            continue

        if day_num in MASTER_THEORY:
            day['theory_html'] = MASTER_THEORY[day_num]
            print(f"  ✓ Updated Day {day_num:03d} ('{day.get('title')[:30]}'): {len(MASTER_THEORY[day_num])} chars")

    save_yaml(fpath, data)
    print(f"  ✓ Saved week{w:02d}.yaml")

print("\n🎉 Master theory expansion successfully applied to all Weeks 18-26!")
