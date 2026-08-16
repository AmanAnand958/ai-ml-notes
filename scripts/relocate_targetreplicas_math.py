#!/usr/bin/env python3
"""
Fix Misplaced TargetReplicas Math Block in Week 25:
The HPA scaling formula:
$$\text{TargetReplicas} = \left\lceil \text{CurrentReplicas} \times \frac{\text{CurrentMetricValue}}{\text{TargetMetricValue}} \right\rceil$$
was accidentally placed inside the <div class="concept-map-flow"> span list at the top of Day 180.
This script moves the math block to its proper place under Day 180's 🧠 Theory & Concepts section.
"""

from pathlib import Path
from bs4 import BeautifulSoup
import re

fp25 = Path("/Users/amananand/Downloads/SDE/ai:ml-1/pages/weeks/week25.html")
html25 = fp25.read_text(encoding='utf-8', errors='replace')
soup25 = BeautifulSoup(html25, 'html.parser')

d180 = soup25.find('div', id='day-180')
if d180:
    cmap = d180.find('div', class_='concept-map-flow')
    if cmap:
        math_in_cmap = cmap.find('div', class_='math-block')
        if math_in_cmap and 'TargetReplicas' in math_in_cmap.text:
            math_in_cmap.extract()
            print("Extracted misplaced TargetReplicas from concept-map-flow.")
            
            # Place it under Theory & Concepts header in Day 180
            theory_h2 = d180.find('h2', class_='sh2', id='day-180-theory') or d180.find('h2', class_='sh2')
            if theory_h2:
                theory_h2.insert_after(math_in_cmap)
                print("✅ Successfully relocated TargetReplicas math block into Theory & Concepts section!")

fp25.write_text(soup25.prettify(), encoding='utf-8')
print("✅ Saved week25.html with clean concept-map-flow and properly placed HPA formula.")
