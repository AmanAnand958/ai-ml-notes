#!/usr/bin/env python3
"""
Final CSS Polish:
1. Removes all redundant large <style> blocks from week26 and all remaining weeks (all styling is in assets/css/course.css).
2. Cleans remaining hardcoded hex colors in inline style attributes.
"""

from pathlib import Path
from bs4 import BeautifulSoup
import re

WEEKS_DIR = Path("pages/weeks")

for wn in range(1, 27):
    fp = WEEKS_DIR / f"week{wn}.html"
    if not fp.exists(): continue
    raw = fp.read_text(encoding='utf-8', errors='replace')
    soup = BeautifulSoup(raw, 'html.parser')
    
    # Remove any style tags in head or body that duplicate course.css
    for s in soup.find_all('style'):
        if len(s.text) > 1000:
            s.decompose()
            
    doc_str = str(soup)
    
    # Replace any residual hex colors in inline styles
    doc_str = re.sub(r'#24292e\b', 'var(--bg)', doc_str)
    doc_str = re.sub(r'#1b1f23\b', 'var(--bg)', doc_str)
    doc_str = re.sub(r'#0d1117\b', 'var(--bg)', doc_str)
    doc_str = re.sub(r'#161b22\b', 'var(--bg2)', doc_str)
    doc_str = re.sub(r'#21262d\b', 'var(--bg3)', doc_str)
    doc_str = re.sub(r'#30363d\b', 'var(--border)', doc_str)
    doc_str = re.sub(r'#e1e4e8\b', 'var(--border)', doc_str)
    doc_str = re.sub(r'#2f363d\b', 'var(--border)', doc_str)
    doc_str = re.sub(r'#c9d1d9\b', 'var(--text)', doc_str)
    doc_str = re.sub(r'#8b949e\b', 'var(--text2)', doc_str)
    doc_str = re.sub(r'#58a6ff\b', 'var(--blue, #82aaff)', doc_str)
    doc_str = re.sub(r'#3fb950\b', 'var(--green, #49e9a6)', doc_str)
    doc_str = re.sub(r'#f85149\b', 'var(--accent)', doc_str)
    doc_str = re.sub(r'#d73a49\b', 'var(--accent)', doc_str)
    doc_str = re.sub(r'#6f42c1\b', 'var(--purple, #c792ea)', doc_str)
    doc_str = re.sub(r'#005cc5\b', 'var(--blue, #82aaff)', doc_str)
    doc_str = re.sub(r'#22863a\b', 'var(--green, #49e9a6)', doc_str)
    doc_str = re.sub(r'#032f62\b', 'var(--text)', doc_str)
    doc_str = re.sub(r'#b392f0\b', 'var(--purple, #c792ea)', doc_str)
    doc_str = re.sub(r'#e36209\b', 'var(--yellow, #ffcb6b)', doc_str)

    fp.write_text(doc_str, encoding='utf-8')

print("✅ Final CSS Polish Complete!")
