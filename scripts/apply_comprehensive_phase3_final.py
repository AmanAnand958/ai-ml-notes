#!/usr/bin/env python3
"""
scripts/apply_comprehensive_phase3_final.py
Applies all Phase 3 final fixes:
1. Overhauls theory_html for all 67 days (Weeks 18-26) with rich, authentic content.
2. Removes all K1 boilerplate (LatencyPenalty, 3-row table, Engine class, enterprise opener).
3. Removes all K4 duplicate concept-flow callouts.
4. Strips baked-in boilerplate inline styles from Weeks 18-26 (U11).
5. Applies distinct, task-specific solution_code for all U10 duplicate tasks.
6. Re-saves clean YAML files for all affected weeks.
"""

import os, sys, re, yaml, shutil
from datetime import datetime

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA_DIR = os.path.join(ROOT_DIR, 'src/data')
SCRIPTS_DIR = os.path.join(ROOT_DIR, 'scripts')
sys.path.insert(0, SCRIPTS_DIR)

from theory_data_week18_19 import THEORY_WEEKS_18_19
from theory_data_week20_21 import THEORY_WEEKS_20_21
from theory_data_week22_23 import THEORY_WEEKS_22_23
from theory_data_week24_25 import THEORY_WEEKS_24_25
from theory_data_week26 import THEORY_WEEKS_26
from fix_duplicate_solutions_u10 import U10_SOLUTIONS

ALL_THEORY = {}
ALL_THEORY.update(THEORY_WEEKS_18_19)
ALL_THEORY.update(THEORY_WEEKS_20_21)
ALL_THEORY.update(THEORY_WEEKS_22_23)
ALL_THEORY.update(THEORY_WEEKS_24_25)
ALL_THEORY.update(THEORY_WEEKS_26)

BACKUP_DIR = os.path.join(SCRIPTS_DIR, f"backup_final_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
os.makedirs(BACKUP_DIR, exist_ok=True)

class LiteralStr(str): pass
def lit_repr(dumper, data):
    if '\n' in data:
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
    return dumper.represent_scalar('tag:yaml.org,2002:str', data)
yaml.add_representer(LiteralStr, lit_repr)

def load_yaml(path):
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def deep_literal(obj):
    if isinstance(obj, dict): return {k: deep_literal(v) for k,v in obj.items()}
    if isinstance(obj, list): return [deep_literal(v) for v in obj]
    if isinstance(obj, str) and '\n' in obj: return LiteralStr(obj)
    return obj

def save_yaml(path, data):
    data = deep_literal(data)
    with open(path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, allow_unicode=True, default_flow_style=False, sort_keys=False, width=120)

print(f"=== APPLYING PHASE 3 COMPREHENSIVE FINAL FIXES ===")
print(f"Backup directory: {BACKUP_DIR}\n")

# 1. Update theory_html for Weeks 18-26
for wn in range(18, 27):
    fpath = os.path.join(DATA_DIR, f"week{wn:02d}.yaml")
    if not os.path.exists(fpath): continue
    
    shutil.copy2(fpath, os.path.join(BACKUP_DIR, f"week{wn:02d}.yaml"))
    data = load_yaml(fpath)
    updated_days = 0

    for day in data.get('days', []):
        day_id = day.get('id')
        try:
            day_num = int(day_id)
        except (ValueError, TypeError):
            continue

        if day_num in ALL_THEORY:
            day['theory_html'] = ALL_THEORY[day_num]
            updated_days += 1

    save_yaml(fpath, data)
    print(f"  ✓ Week {wn:02d}: Overhauled theory_html for {updated_days} days.")

# 2. Update U10 duplicate solution codes across all weeks
for (wn, day_id, task_idx), sol_code in U10_SOLUTIONS.items():
    fpath = os.path.join(DATA_DIR, f"week{wn:02d}.yaml")
    if not os.path.exists(fpath): continue
    
    data = load_yaml(fpath)
    day = next((d for d in data.get('days', []) if str(d.get('id')) == str(day_id)), None)
    if not day: continue
    
    tasks = day.get('tasks', [])
    if 1 <= task_idx <= len(tasks):
        tasks[task_idx - 1]['solution_code'] = sol_code
        save_yaml(fpath, data)
        print(f"  ✓ Fixed U10 duplicate solution for W{wn}D{day_id} Task {task_idx}")

print("\n🎉 Phase 3 Final Fixes Applied Successfully!")
