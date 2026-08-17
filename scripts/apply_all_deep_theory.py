#!/usr/bin/env python3
"""
scripts/apply_all_deep_theory.py
Merges all four deep theory modules and updates all 56 days in Weeks 19 to 26.
"""

import os, yaml
from theory_deep_w19_w20 import W19_W20_THEORY
from theory_deep_w21_w22 import W21_W22_THEORY
from theory_deep_w23_w24 import W23_W24_THEORY
from theory_deep_w25_w26 import W25_W26_THEORY

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA_DIR = os.path.join(ROOT_DIR, 'src/data')

ALL_THEORY = {}
ALL_THEORY.update(W19_W20_THEORY)
ALL_THEORY.update(W21_W22_THEORY)
ALL_THEORY.update(W23_W24_THEORY)
ALL_THEORY.update(W25_W26_THEORY)

print(f"Loaded a total of {len(ALL_THEORY)} deep theory day modules.")

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

for w in range(19, 27):
    fpath = os.path.join(DATA_DIR, f"week{w:02d}.yaml")
    if not os.path.exists(fpath): continue
    data = load_yaml(fpath)

    for day in data.get('days', []):
        did = day.get('id')
        try:
            day_num = int(did)
        except (ValueError, TypeError):
            continue

        if day_num in ALL_THEORY:
            day['theory_html'] = ALL_THEORY[day_num]
            print(f"  ✓ Enriched Day {day_num:03d} ('{day.get('title')[:30]}'): {len(ALL_THEORY[day_num])} chars")

    save_yaml(fpath, data)
    print(f"  ✓ Updated week{w:02d}.yaml")

print("\n🎉 All 56 days across Weeks 19-26 enriched with deep multi-section theory!")
