#!/usr/bin/env python3
"""
Fix indentation for injected comments in week18 and week24.
"""

from pathlib import Path
from bs4 import BeautifulSoup
import ast

for wn in [18, 24]:
    fp = Path(f"pages/weeks/week{wn}.html")
    soup = BeautifulSoup(fp.read_text(encoding='utf-8'), 'html.parser')
    
    for cb in soup.find_all('div', class_='cb'):
        pre = cb.find('pre')
        if not pre: continue
        code = pre.text
        
        # If AST parse fails, fix comment indentations
        try:
            ast.parse(code)
        except SyntaxError:
            lines = code.split('\n')
            fixed_lines = []
            current_indent = ""
            for l in lines:
                stripped = l.strip()
                if stripped.startswith('with ') or stripped.startswith('for ') or stripped.startswith('def ') or stripped.startswith('class '):
                    # Check leading spaces
                    indent_len = len(l) - len(l.lstrip())
                    current_indent = " " * indent_len
                elif stripped.startswith('# Step'):
                    # Match next statement's indentation if inside a block
                    fixed_lines.append(current_indent + stripped)
                    continue
                fixed_lines.append(l)
            fixed_code = '\n'.join(fixed_lines)
            try:
                ast.parse(fixed_code)
                pre.string = fixed_code
            except SyntaxError:
                pass

    fp.write_text(str(soup), encoding='utf-8')
    print(f"✅ Repaired comment indentations in Week {wn}")

print("\n🎉 COMMENT INDENTATIONS IN WEEKS 18 & 24 FIXED!")
