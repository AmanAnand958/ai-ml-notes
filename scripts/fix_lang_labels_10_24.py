#!/usr/bin/env python3
"""
Fix the 2 remaining language labels in Week 10 and Week 24.
"""

from pathlib import Path
from bs4 import BeautifulSoup

# 1. Week 10
fp10 = Path("pages/weeks/week10.html")
soup10 = BeautifulSoup(fp10.read_text(), 'html.parser')
for cb in soup10.find_all('div', class_='cb'):
    pre = cb.find('pre')
    if pre and 'class LSTMSentimentClassifier' in pre.text:
        lang = cb.find('span', class_='cb-lang')
        if lang:
            lang.string = 'python'
fp10.write_text(str(soup10), encoding='utf-8')

# 2. Week 24
fp24 = Path("pages/weeks/week24.html")
soup24 = BeautifulSoup(fp24.read_text(), 'html.parser')
for cb in soup24.find_all('div', class_='cb'):
    pre = cb.find('pre')
    if pre and 'def run_dvc_pipeline' in pre.text:
        lang = cb.find('span', class_='cb-lang')
        if lang:
            lang.string = 'python'
fp24.write_text(str(soup24), encoding='utf-8')

print("✅ Fixed language tags in Week 10 and Week 24!")
