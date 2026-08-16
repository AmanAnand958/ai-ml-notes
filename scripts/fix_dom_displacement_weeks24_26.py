#!/usr/bin/env python3
"""
Structural DOM Re-integration and Gotcha Alignment Script for Weeks 24, 25, and 26.
Uses plain string replacement to avoid regex escape collisions.
"""

import re
from pathlib import Path
from bs4 import BeautifulSoup

WEEKS_DIR = Path("/Users/amananand/Downloads/SDE/ai:ml-1/pages/weeks")

# ─────────────────────────────────────────────────────────────────────────────
# 1. FIX WEEK 24 DOM DISPLACEMENT & GOTCHAS
# ─────────────────────────────────────────────────────────────────────────────
print("=== 1. Fixing Week 24 (Day 171 Displacement & Gotchas) ===")
fp24 = WEEKS_DIR / "week24.html"
html24 = fp24.read_text(encoding='utf-8', errors='replace')
soup24 = BeautifulSoup(html24, 'html.parser')

d171_section = soup24.find('div', id='day-171')
if d171_section:
    btn171 = soup24.find('button', id='btn-day-171')
    tasks171 = soup24.find('div', id='tasks-section-171')
    pred171 = soup24.find('div', id='p171-result')
    
    if pred171:
        pred_parent = pred171.find_parent('div', class_='predict-block')
        if pred_parent and pred_parent.parent != d171_section:
            d171_section.append(pred_parent)
            
    if tasks171 and tasks171.parent != d171_section:
        d171_section.append(tasks171)
        
    if btn171 and btn171.parent != d171_section:
        d171_section.append(btn171)
        
    print("  ✅ Re-integrated Day 171 Tasks, Predict Block & Button into day-171 container")

html24_str = str(soup24)

# Replace Gotchas via string matching
old_172 = "Data drift detectors triggered on small sample windows trigger high false-alarm rates; calibrate minimum sample sizes (e.g. \\ge 1000 requests) before triggering automated retraining alerts."
new_172 = "Model registry automated stage promotion without automated canary validation can deploy silent regressions. Always enforce automated shadow testing or threshold checks before promoting models to Production."

old_175 = "Model registry automated stage promotion without automated canary validation can deploy regression models to production. Always require threshold validation tests before promoting models from Staging to Production."
new_175 = "Data drift detectors triggered on small sample windows trigger high false-alarm rates; calibrate minimum sample sizes (e.g. &ge; 1000 inference requests) before triggering automated alerts or retraining pipelines."

html24_str = html24_str.replace(old_172, new_172)
html24_str = html24_str.replace(old_175, new_175)

fp24.write_text(html24_str, encoding='utf-8')
print("  ✅ Realigned Week 24 Gotchas (Days 172 & 175)")

# ─────────────────────────────────────────────────────────────────────────────
# 2. FIX WEEK 25 DOM DISPLACEMENT
# ─────────────────────────────────────────────────────────────────────────────
print("\n=== 2. Fixing Week 25 (Days 179, 180, 181 Displacement) ===")
fp25 = WEEKS_DIR / "week25.html"
html25 = fp25.read_text(encoding='utf-8', errors='replace')
soup25 = BeautifulSoup(html25, 'html.parser')

for day_num in [179, 180, 181]:
    d_sec = soup25.find('div', id=f'day-{day_num}')
    if d_sec:
        btn = soup25.find('button', id=f'btn-day-{day_num}')
        tasks = soup25.find('div', id=f'tasks-section-{day_num}')
        pred = soup25.find('div', id=f'p{day_num}-result')
        
        if pred:
            p_block = pred.find_parent('div', class_='predict-block')
            if p_block and p_block.parent != d_sec:
                d_sec.append(p_block)
                
        if tasks and tasks.parent != d_sec:
            d_sec.append(tasks)
            
        if btn and btn.parent != d_sec:
            d_sec.append(btn)
            
        print(f"  ✅ Re-integrated Day {day_num} Tasks, Predict Block & Button into day-{day_num} container")

fp25.write_text(str(soup25), encoding='utf-8')

# ─────────────────────────────────────────────────────────────────────────────
# 3. FIX WEEK 26 DOM DISPLACEMENT & GOTCHAS
# ─────────────────────────────────────────────────────────────────────────────
print("\n=== 3. Fixing Week 26 (Day 187 Displacement & Gotchas) ===")
fp26 = WEEKS_DIR / "week26.html"
html26 = fp26.read_text(encoding='utf-8', errors='replace')
soup26 = BeautifulSoup(html26, 'html.parser')

d187_sec = soup26.find('div', id='day-187')
if d187_sec:
    btn187 = soup26.find('button', id='btn-day-187')
    tasks187 = soup26.find('div', id='tasks-section-187')
    pred187 = soup26.find('div', id='p187-result')
    
    if pred187:
        p_block187 = pred187.find_parent('div', class_='predict-block')
        if p_block187 and p_block187.parent != d187_sec:
            d187_sec.append(p_block187)
            
    if tasks187 and tasks187.parent != d187_sec:
        d187_sec.append(tasks187)
        
    if btn187 and btn187.parent != d187_sec:
        d187_sec.append(btn187)
        
    print("  ✅ Re-integrated Day 187 Tasks, Predict Block & Button into day-187 container")

html26_str = str(soup26)

old_187 = "Setting Classifier-Free Guidance too high ($w > 12$) results in oversaturated, cartoonish artifacts and high-frequency noise in latent diffusion outputs. Keep guidance scale between 5.0 and 7.5 for photorealistic generation."
new_187 = "Passing long unvoiced silent segments to Whisper causes the autoregressive decoder to hallucinate repetitive phrases. Always use Voice Activity Detection (VAD) to trim silence before transcribing."

old_188 = "Passing long unvoiced silent segments to Whisper causes the autoregressive decoder to loop and hallucinate repetitive phrases. Always use Voice Activity Detection (VAD) preprocessing to trim silence before model inference."
new_188 = "Training recommendation ranking models purely on user clicks creates severe popularity bias and feedback loops. Enforce exploration bandits (&epsilon;-greedy or Thompson Sampling) to surface long-tail relevant content."

html26_str = html26_str.replace(old_187, new_187)
html26_str = html26_str.replace(old_188, new_188)

fp26.write_text(html26_str, encoding='utf-8')
print("  ✅ Realigned Week 26 Gotchas (Days 187 & 188)")

print("\n🎉 ALL WEEKS 24-26 STRUCTURAL & CONTENT FIXES APPLIED SUCCESSFULLY!")
