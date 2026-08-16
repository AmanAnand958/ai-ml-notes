#!/usr/bin/env python3
"""
Universal Mermaid Diagram Bulletproofing across all 26 Weeks:
1. Fixes subgraph syntax: 'subgraph ID ["Title"]' -> 'subgraph "Title"' or 'subgraph ID["Title"]'.
2. Removes reserved characters from edge labels: '&' -> 'and', '%' -> 'percent', '<' -> 'under', '>' -> 'over'.
3. Removes leading dashes and inner parentheses from node labels.
4. Replaces reserved '@' prefix in labels.
"""

from pathlib import Path
from bs4 import BeautifulSoup
import re

WEEKS_DIR = Path("pages/weeks")

for wn in range(1, 27):
    fp = WEEKS_DIR / f"week{wn}.html"
    if not fp.exists(): continue
    raw = fp.read_text(encoding='utf-8')
    soup = BeautifulSoup(raw, 'html.parser')
    modified = False
    
    for m in soup.find_all('div', class_='mermaid'):
        txt = m.text
        orig = txt
        
        # 1. Fix subgraph space before bracket: subgraph ID ["Title"] -> subgraph "Title"
        txt = re.sub(r'subgraph\s+[a-zA-Z0-9_]+\s+\["([^"]+)"\]', r'subgraph "\1"', txt)
        txt = re.sub(r'subgraph\s+\["([^"]+)"\]', r'subgraph "\1"', txt)
        
        # 2. Fix @ in node labels
        txt = txt.replace('@challenger', 'Challenger').replace('@champion', 'Champion')
        
        # 3. Fix inner parentheses inside brackets: ["Text (Note)"] -> ["Text - Note"]
        def clean_brackets(match):
            inner = match.group(1)
            inner = inner.replace('(', '- ').replace(')', '')
            return f'["{inner}"]'
        txt = re.sub(r'\["([^"]+)"\]', clean_brackets, txt)
        
        # 4. Fix leading dashes in node labels
        txt = txt.replace('["- ', '["')
        
        # 5. Fix edge label reserved characters
        def clean_edges(match):
            edge = match.group(1)
            edge = edge.replace('&', 'and')
            edge = edge.replace('%', ' percent')
            edge = edge.replace('<', 'under ')
            edge = edge.replace('>', 'over ')
            edge = edge.replace('/', ' or ')
            return f'|{edge}|'
        txt = re.sub(r'\|([^|]+)\|', clean_edges, txt)
        
        if txt != orig:
            m.string = txt
            modified = True

    if modified:
        fp.write_text(str(soup), encoding='utf-8')
        print(f"  ✅ Bulletproofed Mermaid diagrams in Week {wn}")

print("\n🎉 ALL MERMAID DIAGRAMS ACROSS ALL 26 WEEKS BULLETPROOFED!")
