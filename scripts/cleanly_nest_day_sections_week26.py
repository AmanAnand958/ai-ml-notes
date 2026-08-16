#!/usr/bin/env python3
"""
Proper Structural Ingestion:
Ensures each Day's content (quizzes, flashcards, takeaways, resources, case studies, task blocks, and buttons)
is nested INSIDE its own <div class="day-section" id="day-XXX"> container.
"""

from bs4 import BeautifulSoup
from pathlib import Path
import re

fp26 = Path("/Users/amananand/Downloads/SDE/ai:ml-1/pages/weeks/week26.html")
soup = BeautifulSoup(fp26.read_text(encoding='utf-8', errors='replace'), 'html.parser')
main = soup.find('main', class_='main')

# List of days in order
day_ids = [f"day-{d}" for d in range(185, 192)]

# Collect elements into buckets per day
day_buckets = {did: [] for did in day_ids}
orphan_milestone = []

current_day = None
for child in list(main.children):
    if not child.name: continue
    
    cid = child.get('id', '')
    cclass = child.get('class', [])
    
    if cid in day_buckets:
        current_day = cid
        # Extract children already inside day-section if any
        for sub in list(child.children):
            if sub.name:
                day_buckets[current_day].append(sub)
    elif current_day:
        if cclass and any(c in ['milestone', 'week-summary'] for c in cclass):
            orphan_milestone.append(child)
        else:
            day_buckets[current_day].append(child)

# Clear main and reconstruct cleanly
main.clear()

for did in day_ids:
    day_num = did.replace('day-', '')
    is_active = (did == 'day-185')
    
    day_sec = soup.new_tag('div', id=did, **{
        'class': f'day-section{" active" if is_active else ""}',
        'data-xp': '150'
    })
    
    # Append all children for this day
    for elem in day_buckets[did]:
        day_sec.append(elem)
        
    main.append(day_sec)

# Append milestones at bottom of main
for ms in orphan_milestone:
    main.append(ms)

fp26.write_text(soup.prettify(), encoding='utf-8')
print("✅ Successfully nested all day components inside their respective day-section containers!")
