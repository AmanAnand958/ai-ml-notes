#!/usr/bin/env python3
"""
Deep Forensic Verification across Weeks 18-26 for newly highlighted issues:
1. Week 18 Day count (11 days vs 7 days: Days 125-135).
2. Week 18 "Dockerfile RAG" loop across days 129-134.
3. Week 19 Shifted Hinglish (Days 137, 139, 140).
4. Week 22 Shifted Hinglish (Days 159, 160, 161, 162).
5. Week 26 Shifted Hinglish & Tables (Day 187 Stable Diffusion vs Whisper, Day 188 RecSys vs DSPy).
6. Week 21 Day 154 Quiz (DPO vs Speculative Decoding).
7. Week 23 Day 166 Quiz Q3 & Q4 correct answer text match.
8. Task 2 Click-to-Expand interactive header structure across all weeks.
"""

import re
from pathlib import Path
from bs4 import BeautifulSoup

WEEKS_DIR = Path("/Users/amananand/Downloads/SDE/ai:ml-1/pages/weeks")

print("==================================================")
print("1. CHECKING WEEK 18 DAY COUNT & DOCKERFILE CODE")
print("==================================================")
fp18 = WEEKS_DIR / "week18.html"
if fp18.exists():
    html18 = fp18.read_text(encoding='utf-8', errors='replace')
    soup18 = BeautifulSoup(html18, 'html.parser')
    days18 = [d.get('id') for d in soup18.find_all('div', class_=re.compile(r'day-section'))]
    print(f"Week 18 day count: {len(days18)} days -> {days18}")
    
    docker_rag_matches = re.findall(r'Dockerfile for RAG Application', html18)
    print(f"Occurrences of 'Dockerfile for RAG Application': {len(docker_rag_matches)}")
else:
    print("week18.html not found")

print("\n==================================================")
print("2. CHECKING WEEK 19 HINGLISH SHIFTS")
print("==================================================")
fp19 = WEEKS_DIR / "week19.html"
if fp19.exists():
    html19 = fp19.read_text(encoding='utf-8', errors='replace')
    soup19 = BeautifulSoup(html19, 'html.parser')
    for ds in soup19.find_all('div', class_=re.compile(r'day-section')):
        did = ds.get('id')
        h1 = ds.find('h1')
        title = h1.text.strip() if h1 else ''
        # Find Hinglish callout text
        callout = ds.find(class_=re.compile(r'callout|theory-callout|hinglish', re.I))
        callout_text = callout.text.strip()[:100] if callout else 'None'
        print(f"  {did} ({title}): {callout_text}")

print("\n==================================================")
print("3. CHECKING WEEK 22 HINGLISH SHIFTS")
print("==================================================")
fp22 = WEEKS_DIR / "week22.html"
if fp22.exists():
    html22 = fp22.read_text(encoding='utf-8', errors='replace')
    soup22 = BeautifulSoup(html22, 'html.parser')
    for ds in soup22.find_all('div', class_=re.compile(r'day-section')):
        did = ds.get('id')
        h1 = ds.find('h1')
        title = h1.text.strip() if h1 else ''
        callout = ds.find(class_=re.compile(r'callout|theory-callout|hinglish', re.I))
        callout_text = callout.text.strip()[:100] if callout else 'None'
        print(f"  {did} ({title}): {callout_text}")

print("\n==================================================")
print("4. CHECKING WEEK 26 DAY 187 TABLE & DAY 188 HINGLISH")
print("==================================================")
fp26 = WEEKS_DIR / "week26.html"
if fp26.exists():
    html26 = fp26.read_text(encoding='utf-8', errors='replace')
    soup26 = BeautifulSoup(html26, 'html.parser')
    d187 = soup26.find('div', id='day-187')
    if d187:
        table187 = d187.find('table')
        print(f"Day 187 Table Content Preview: {table187.text[:150] if table187 else 'No Table'}")
    
    d188 = soup26.find('div', id='day-188')
    if d188:
        callout188 = d188.find(class_=re.compile(r'callout|theory-callout|hinglish', re.I))
        print(f"Day 188 Hinglish Preview: {callout188.text[:150] if callout188 else 'No Callout'}")

print("\n==================================================")
print("5. CHECKING WEEK 21 DAY 154 QUIZ TOPIC")
print("==================================================")
fp21 = WEEKS_DIR / "week21.html"
if fp21.exists():
    html21 = fp21.read_text(encoding='utf-8', errors='replace')
    soup21 = BeautifulSoup(html21, 'html.parser')
    d154 = soup21.find('div', id='day-154')
    if d154:
        quiz_qs = [q.text.strip() for q in d154.find_all('div', class_='quiz-q')]
        print(f"Day 154 Quiz Questions: {quiz_qs}")

print("\n==================================================")
print("6. CHECKING TASK 2 CLICK-TO-EXPAND ACCORDION HEADERS")
print("==================================================")
for wn in range(19, 27):
    html = Path(f"pages/weeks/week{wn}.html").read_text(encoding='utf-8', errors='replace')
    # Count task-header buttons vs raw text
    t_headers = len(re.findall(r'class="task-header"', html))
    t_toggles = len(re.findall(r'toggleTask\(this\)', html))
    print(f"Week {wn}: task-headers={t_headers}, toggleTask(this) onclicks={t_toggles}")
