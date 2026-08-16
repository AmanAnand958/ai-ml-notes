#!/usr/bin/env python3
"""
Comprehensive Fix for Week 4 (including Day 26):
Wraps all bare <pre> blocks across all days in Week 4 in <code class="language-python">
and adds standard syntax highlighting tokens (<span class="kw">, <span class="st">, <span class="bi">, <span class="num">, <span class="cm">).
"""

import re
from pathlib import Path
from bs4 import BeautifulSoup

WEEKS_DIR = Path("/Users/amananand/Downloads/SDE/ai:ml-1/pages/weeks")

KEYWORDS = {"import", "from", "def", "class", "return", "if", "else", "elif", "for", "while", "in", "as", "try", "except", "raise", "with", "lambda", "assert", "True", "False", "None", "and", "or", "not", "is"}
BUILTINS = {"print", "len", "sum", "abs", "round", "int", "float", "str", "list", "dict", "set", "super", "range", "min", "max", "array", "dot", "zeros", "ones", "mean", "var", "std"}

def highlight_python(code_str: str) -> str:
    lines = code_str.split("\n")
    hl_lines = []
    for line in lines:
        if line.strip().startswith("#"):
            hl_lines.append(f'<span class="cm">{line}</span>')
            continue
        
        # Strings
        line = re.sub(r'("(?:[^"\\]|\\.)*"|\'(?:[^\'\\]|\\.)*\')', r'<span class="st">\1</span>', line)
        
        # Keywords
        for kw in KEYWORDS:
            line = re.sub(rf'\b({kw})\b(?![^<]*>|[^<>]*<\/span>)', r'<span class="kw">\1</span>', line)
            
        # Builtins
        for bi in BUILTINS:
            line = re.sub(rf'\b({bi})\b(?![^<]*>|[^<>]*<\/span>)', r'<span class="bi">\1</span>', line)
            
        # Numbers
        line = re.sub(r'\b(\d+(?:\.\d+)?)\b(?![^<]*>|[^<>]*<\/span>)', r'<span class="num">\1</span>', line)
        
        hl_lines.append(line)
    return f'<code class="language-python">{"\n".join(hl_lines)}</code>'

print("=== Fixing Bare <pre> and CSS Syntax in Week 4 (including Day 26) ===")
fp4 = WEEKS_DIR / "week4.html"
html4 = fp4.read_text(encoding='utf-8', errors='replace')
soup4 = BeautifulSoup(html4, 'html.parser')

fixed_pres = 0
for pre in soup4.find_all('pre'):
    if not pre.find('code'):
        raw_code = pre.get_text()
        if len(raw_code.strip()) > 5:
            highlighted = highlight_python(raw_code)
            pre.clear()
            pre.append(BeautifulSoup(highlighted, 'html.parser'))
            fixed_pres += 1

fp4.write_text(str(soup4), encoding='utf-8')
print(f"✅ Wrapped and highlighted {fixed_pres} code blocks across Week 4 (Days 22 to 30)!")
