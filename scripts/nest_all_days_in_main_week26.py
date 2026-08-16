#!/usr/bin/env python3
"""
Structural Fix for Week 26:
Moves Days 186 to 191 (and all associated quizzes/milestones) INSIDE `<main class="main">`
so that ALL 7 days are properly contained within the layout grid alongside the sidebar.
"""

from bs4 import BeautifulSoup
from pathlib import Path

fp26 = Path("/Users/amananand/Downloads/SDE/ai:ml-1/pages/weeks/week26.html")
html = fp26.read_text(encoding='utf-8', errors='replace')
soup = BeautifulSoup(html, 'html.parser')

body = soup.find('body')
layout = soup.find('div', class_='layout')
main = layout.find('main', class_='main') if layout else None

if not layout:
    print("❌ Layout container not found!")
    exit(1)

if not main:
    main = soup.new_tag('main', **{'class': 'main'})
    layout.append(main)

# Collect all top-level children of body that appear after <div class="layout">
# (excluding script tags, toast, nav)
children_to_move = []
for child in list(body.children):
    if child.name in ['div', 'section', 'h2', 'p', 'button'] and child != layout and child.get('id') != 'xp-toast':
        children_to_move.append(child)

print(f"Moving {len(children_to_move)} orphaned top-level elements into <main class='main'>...")
for child in children_to_move:
    main.append(child)

# Write clean DOM back
fp26.write_text(soup.prettify(), encoding='utf-8')
print("✅ Successfully nested all 7 days inside <main class='main'> in Week 26!")
