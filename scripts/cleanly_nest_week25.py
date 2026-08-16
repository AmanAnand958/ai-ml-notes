#!/usr/bin/env python3
"""
Structural Encapsulation for Week 25:
Nests all quizzes, flashcards, takeaways, case studies, and complete buttons
INSIDE their respective <div class="day-section" id="day-XXX"> containers,
so that when goDay(X) switches display, each day displays cleanly with its complete button and components.
"""

from bs4 import BeautifulSoup
from pathlib import Path

fp25 = Path("/Users/amananand/Downloads/SDE/ai:ml-1/pages/weeks/week25.html")
soup = BeautifulSoup(fp25.read_text(encoding='utf-8', errors='replace'), 'html.parser')

body = soup.find('body')
layout = soup.find('div', class_='layout')
main = layout.find('main', class_='main') if layout else None

day_ids = [f"day-{d}" for d in range(178, 185)]
day_buckets = {did: [] for did in day_ids}
orphan_milestones = []

# Collect elements currently inside main
current_day = None
for child in list(main.children):
    if not child.name: continue
    cid = child.get('id', '')
    cclass = child.get('class', [])
    
    if cid in day_buckets:
        current_day = cid
        for sub in list(child.children):
            if sub.name:
                day_buckets[current_day].append(sub)
    elif current_day:
        if cclass and any(c in ['milestone', 'week-summary'] for c in cclass):
            orphan_milestones.append(child)
        else:
            day_buckets[current_day].append(child)

# Collect orphaned elements currently in body outside layout
for child in list(body.children):
    if not child.name or child == layout or child.get('id') == 'xp-toast' or child.name in ['nav', 'script']:
        continue
    cclass = child.get('class', [])
    if cclass and any(c in ['milestone', 'week-summary'] for c in cclass):
        orphan_milestones.append(child)
    else:
        # Check text to assign to corresponding day
        txt = child.text
        matched_day = None
        for d in range(178, 185):
            if f"Day {d}" in txt or f"day-{d}" in str(child):
                matched_day = f"day-{d}"
                break
        if matched_day:
            day_buckets[matched_day].append(child)
        elif current_day:
            day_buckets[current_day].append(child)
    child.extract()

# Rebuild main cleanly
main.clear()
for did in day_ids:
    is_active = (did == 'day-178')
    day_sec = soup.new_tag('div', id=did, **{
        'class': f'day-section{" active" if is_active else ""}',
        'data-xp': '150'
    })
    for elem in day_buckets[did]:
        day_sec.append(elem)
    main.append(day_sec)

for ms in orphan_milestones:
    main.append(ms)

fp25.write_text(soup.prettify(), encoding='utf-8')
print("✅ Successfully nested all Day 178-184 elements cleanly inside their day containers in Week 25!")
