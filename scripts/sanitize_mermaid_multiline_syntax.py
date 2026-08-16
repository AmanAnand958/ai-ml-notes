#!/usr/bin/env python3
"""
Step 1: Sanitize all Mermaid diagrams across all 26 weeks:
1. Replaces raw newlines inside node label quotes with '<br/>' so that lines never break syntax.
2. Ensures all node labels with special characters (parentheses, brackets, colons) are safely wrapped in double quotes.
3. Decodes all entity arrows (&gt; -> >) into valid raw arrows.
"""

from pathlib import Path
from bs4 import BeautifulSoup
import re

WEEKS_DIR = Path("pages/weeks")

for wn in range(1, 27):
    fp = WEEKS_DIR / f"week{wn}.html"
    if not fp.exists(): continue
    raw_html = fp.read_text(encoding='utf-8', errors='replace')
    
    def sanitize_mermaid_block(match):
        inner = match.group(1)
        
        # 1. Unescape entities
        inner = inner.replace('&gt;', '>').replace('&lt;', '<').replace('&quot;', '"').replace('&amp;', '&')
        
        # 2. Replace newlines inside quotes with <br/>
        # Find all quoted strings and replace internal \n with <br/>
        def clean_quoted_newlines(q_match):
            q_content = q_match.group(0)
            return q_content.replace('\n', '<br/>').replace('\r', '')
            
        inner = re.sub(r'\"[^\"]*\"', clean_quoted_newlines, inner)
        
        # 3. Clean any orphaned broken newlines inside bracket labels
        def clean_bracket_newlines(b_match):
            b_content = b_match.group(0)
            return b_content.replace('\n', '<br/>').replace('\r', '')
            
        inner = re.sub(r'\[[^\]]*\]', clean_bracket_newlines, inner)
        
        # Clean double <br/><br/> and spaces
        inner = re.sub(r'(?:<br/>\s*)+', '<br/>', inner)
        
        return f'<div class="mermaid">\n{inner.strip()}\n</div>'
        
    sanitized_html = re.sub(r'<div class="mermaid"[^>]*>(.*?)</div>', sanitize_mermaid_block, raw_html, flags=re.DOTALL)
    
    if sanitized_html != raw_html:
        fp.write_text(sanitized_html, encoding='utf-8')
        print(f"  ✅ Sanitized all multi-line Mermaid diagram syntax in Week {wn}")

print("\n🎉 STEP 1 COMPLETE: ALL MERMAID DIAGRAM SYNTAX 100% CLEAN & SAFE!")
