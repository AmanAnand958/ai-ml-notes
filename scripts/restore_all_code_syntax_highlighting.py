#!/usr/bin/env python3
"""
Restore and standardise beautiful IDE syntax highlighting across ALL 26 weeks:
1. Parses all <pre> blocks in all 26 weeks.
2. Identifies:
   - Comments: # ... -> <span class="cm">
   - Strings: "..." / '...' / f"..." / f'...' -> <span class="str">
   - Keywords: def, class, import, from, return, if, for, while, with, as, in, try, except, etc. -> <span class="kw">
   - Numbers: integers, floats -> <span class="num">
   - Function definitions & calls: def my_func() -> <span class="fn">
   - Class definitions: class MyClass -> <span class="cls">
3. Wraps them cleanly without corrupting the raw code copy buffer.
"""

from pathlib import Path
from bs4 import BeautifulSoup
import re
import html

WEEKS_DIR = Path("pages/weeks")

KEYWORDS = {
    'def', 'class', 'import', 'from', 'return', 'if', 'elif', 'else', 'for', 'while',
    'with', 'as', 'in', 'is', 'not', 'and', 'or', 'try', 'except', 'finally', 'raise',
    'lambda', 'yield', 'global', 'nonlocal', 'assert', 'pass', 'break', 'continue',
    'True', 'False', 'None', 'self', 'async', 'await'
}

def highlight_python_code(raw_text):
    # First, decode any existing HTML entities so we work on pure text
    text = html.unescape(raw_text)
    
    # Strip any pre-existing syntax highlight tags to avoid double-wrapping
    text = re.sub(r'<span class="[^"]+">([\s\S]*?)</span>', r'\1', text)
    
    lines = text.split('\n')
    highlighted_lines = []
    
    for line in lines:
        if not line:
            highlighted_lines.append('')
            continue
            
        # Check for comment
        comment_idx = -1
        in_str = False
        str_char = ''
        
        # Simple scan for '#' not in string
        for idx, ch in enumerate(line):
            if ch in ('"', "'") and (idx == 0 or line[idx-1] != '\\'):
                if not in_str:
                    in_str = True
                    str_char = ch
                elif ch == str_char:
                    in_str = False
            elif ch == '#' and not in_str:
                comment_idx = idx
                break
                
        code_part = line if comment_idx == -1 else line[:comment_idx]
        comment_part = "" if comment_idx == -1 else line[comment_idx:]
        
        # Tokenize code part with regex
        # Strings: f?"(?:\\.|[^"\\])*" | f?'(?:\\.|[^'\\])*'
        # Words: \b[a-zA-Z_][a-zA-Z0-9_]*\b
        # Numbers: \b\d+(?:\.\d+)?\b
        
        token_pattern = re.compile(
            r'(?P<STRING>f?[\'"](?:\\.|[^\'\\\n])*[\'"])'
            r'|(?P<NUMBER>\b\d+(?:\.\d+)?(?:e[+-]?\d+)?\b)'
            r'|(?P<DEF_FN>\bdef\s+([a-zA-Z_][a-zA-Z0-9_]*)\b)'
            r'|(?P<DEF_CLS>\bclass\s+([a-zA-Z_][a-zA-Z0-9_]*)\b)'
            r'|(?P<WORD>\b[a-zA-Z_][a-zA-Z0-9_]*\b)'
        )
        
        pos = 0
        hl_code = ""
        
        for m in token_pattern.finditer(code_part):
            start, end = m.span()
            # Append plain text preceding match
            hl_code += html.escape(code_part[pos:start])
            
            if m.group('STRING'):
                hl_code += f'<span class="str">{html.escape(m.group("STRING"))}</span>'
            elif m.group('NUMBER'):
                hl_code += f'<span class="num">{m.group("NUMBER")}</span>'
            elif m.group('DEF_FN'):
                fn_name = m.group(4)
                hl_code += f'<span class="kw">def</span> <span class="fn">{html.escape(fn_name)}</span>'
            elif m.group('DEF_CLS'):
                cls_name = m.group(6)
                hl_code += f'<span class="kw">class</span> <span class="cls">{html.escape(cls_name)}</span>'
            elif m.group('WORD'):
                w = m.group('WORD')
                if w in KEYWORDS:
                    hl_code += f'<span class="kw">{w}</span>'
                elif (end < len(code_part) and code_part[end] == '(') or (end+1 < len(code_part) and code_part[end:end+2] == ' ('):
                    hl_code += f'<span class="fn">{html.escape(w)}</span>'
                else:
                    hl_code += html.escape(w)
            pos = end
            
        hl_code += html.escape(code_part[pos:])
        
        if comment_part:
            hl_code += f'<span class="cm">{html.escape(comment_part)}</span>'
            
        highlighted_lines.append(hl_code)
        
    return '\n'.join(highlighted_lines)

# Process all 26 weeks
for wn in range(1, 27):
    fp = WEEKS_DIR / f"week{wn}.html"
    if not fp.exists(): continue
    raw_html = fp.read_text(encoding='utf-8')
    
    # We can highlight all <pre> tags inside .cb
    def repl_pre(match):
        attrs = match.group(1) or ""
        inner_code = match.group(2)
        hl_code = highlight_python_code(inner_code)
        return f'<pre{attrs}>{hl_code}</pre>'
        
    new_html = re.sub(r'<pre([^>]*)>([\s\S]*?)</pre>', repl_pre, raw_html)
    
    if new_html != raw_html:
        fp.write_text(new_html, encoding='utf-8')
        print(f"  🎨 Restored full-spectrum syntax coloring in Week {wn}")

print("\n🎉 ALL CODE BLOCKS IN ALL 26 WEEKS ARE NOW BEAUTIFULLY SYNTAX-HIGHLIGHTED!")
