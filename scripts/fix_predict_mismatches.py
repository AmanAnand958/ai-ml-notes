#!/usr/bin/env python3
"""
scripts/fix_predict_mismatches.py
Corrects all 3 execution output mismatches in Predict The Output drills:
- Day 143: answer -> '2'
- Day 150: answer -> '32'
- Day 158: answer -> '40'
"""

import os
from curriculum_utils import load_yaml, save_yaml

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA_DIR = os.path.join(ROOT_DIR, 'src/data')

# Day 143 (Week 20)
w20 = load_yaml(f"{DATA_DIR}/week20.yaml")
for d in w20['days']:
    if d['id'] == 143:
        d['predict']['answer'] = '2'
        d['predict']['explanation'] = "The ReAct loop history contains 2 action events ('Action: db_query()' and 'Action: Final Answer'), so steps equals 2."
save_yaml(f"{DATA_DIR}/week20.yaml", w20)
print("✓ Fixed Day 143 Predict")

# Day 150 (Week 21)
w21 = load_yaml(f"{DATA_DIR}/week21.yaml")
for d in w21['days']:
    if d['id'] == 150:
        d['predict']['answer'] = '32'
        d['predict']['explanation'] = "2 (K and V) * 2 bytes (FP16) * 32 layers * 32 heads * 128 head_dim * 16 batch * 4096 tokens = 34,359,738,368 bytes = 32.0 GB VRAM."
save_yaml(f"{DATA_DIR}/week21.yaml", w21)
print("✓ Fixed Day 150 Predict")

# Day 158 (Week 22)
w22 = load_yaml(f"{DATA_DIR}/week22.yaml")
for d in w22['days']:
    if d['id'] == 158:
        d['predict']['answer'] = '40'
        d['predict']['explanation'] = "int(10 * 0.95) - 1 = 9 - 1 = 8; index 8 in the sorted latencies array corresponds to 40ms."
save_yaml(f"{DATA_DIR}/week22.yaml", w22)
print("✓ Fixed Day 158 Predict")

print("\n🎉 All Predict drill mismatches resolved!")
