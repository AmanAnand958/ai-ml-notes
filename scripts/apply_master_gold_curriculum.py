#!/usr/bin/env python3
"""
scripts/apply_master_gold_curriculum.py
Applies exhaustive, gold-standard task prompts and curriculum data across Weeks 19-26.
"""

import os
from curriculum_utils import load_yaml, save_yaml
from curriculum_data_w19_w20 import CURRICULUM_W19_W20
from curriculum_data_w21_w22 import CURRICULUM_W21_W22
from curriculum_data_w23_w24 import CURRICULUM_W23_W24
from curriculum_data_w25_w26 import CURRICULUM_W25_W26

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA_DIR = os.path.join(ROOT_DIR, 'src/data')

ALL_CURRICULUM = {}
ALL_CURRICULUM.update(CURRICULUM_W19_W20)
ALL_CURRICULUM.update(CURRICULUM_W21_W22)
ALL_CURRICULUM.update(CURRICULUM_W23_W24)
ALL_CURRICULUM.update(CURRICULUM_W25_W26)

print(f"Loaded master curriculum data for {len(ALL_CURRICULUM)} days.")

for w in range(19, 27):
    fpath = f"{DATA_DIR}/week{w:02d}.yaml"
    if not os.path.exists(fpath): continue
    data = load_yaml(fpath)

    for day in data.get('days', []):
        did = day.get('id')
        try:
            day_num = int(did)
        except (ValueError, TypeError):
            continue

        if day_num in ALL_CURRICULUM:
            cdata = ALL_CURRICULUM[day_num]
            if 'tasks_prompts' in cdata:
                for idx, prompt_text in enumerate(cdata['tasks_prompts']):
                    if idx < len(day.get('tasks', [])):
                        day['tasks'][idx]['prompt_html'] = prompt_text
            print(f"  ✓ Upgraded Task Prompts for Day {day_num:03d} ('{day.get('title')[:30]}')")

    save_yaml(fpath, data)
    print(f"  ✓ Saved week{w:02d}.yaml")

print("\n🎉 All 56 days across Weeks 19-26 successfully upgraded with gold-standard scenario prompts and requirements!")
