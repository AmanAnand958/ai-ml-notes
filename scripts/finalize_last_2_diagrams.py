#!/usr/bin/env python3
"""
Final 2 diagram sanitization:
1. Week 18 Diagram #5: "Accuracy > SLA?" -> "Accuracy exceeds SLA?"
2. Week 24 Diagram #5: "PSI >= 0.25" -> "PSI exceeds 0.25"
"""

from pathlib import Path
from bs4 import BeautifulSoup

# Week 18
fp18 = Path("pages/weeks/week18.html")
soup18 = BeautifulSoup(fp18.read_text(encoding='utf-8'), 'html.parser')
for m in soup18.find_all('div', class_='mermaid'):
    txt = m.text
    if 'Accuracy > SLA?' in txt:
        m.string = txt.replace('Accuracy > SLA?', 'Accuracy exceeds SLA?')
fp18.write_text(str(soup18), encoding='utf-8')
print("✅ Fixed Week 18 Diagram #5!")

# Week 24
fp24 = Path("pages/weeks/week24.html")
soup24 = BeautifulSoup(fp24.read_text(encoding='utf-8'), 'html.parser')
for m in soup24.find_all('div', class_='mermaid'):
    txt = m.text
    if 'PSI >= 0.25' in txt:
        m.string = txt.replace('PSI >= 0.25', 'PSI exceeds 0.25')
fp24.write_text(str(soup24), encoding='utf-8')
print("✅ Fixed Week 24 Diagram #5 (Day 175)!")
