#!/usr/bin/env python3
"""
Deep AST Syntax & Indentation Repair Engine across all 26 weeks.
Normalizes Python indentation, strips accidental HTML tag corruption inside strings,
and validates syntax with ast.parse().
"""

import ast
import re
from pathlib import Path
from bs4 import BeautifulSoup

WEEKS_DIR = Path("/Users/amananand/Downloads/SDE/ai:ml-1/pages/weeks")

for wn in range(1, 27):
    fp = WEEKS_DIR / f"week{wn}.html"
    if not fp.exists(): continue
    
    html = fp.read_text(encoding='utf-8', errors='replace')
    soup = BeautifulSoup(html, 'html.parser')
    modified = False
    
    for code_elem in soup.find_all(['code', 'pre']):
        raw_code = code_elem.get_text()
        if len(raw_code.strip()) < 15: continue
        
        # Check if code has syntax error
        try:
            ast.parse(raw_code)
        except SyntaxError:
            # Apply regex normalization
            text = raw_code
            text = re.sub(r'key\s*=>\s*lambda', 'key=lambda', text)
            text = re.sub(r'(\bdef\s+\w+\([^)]*\))\s*-\s*([A-Za-z0-9_\[\],\s]+):', r'\1 -> \2:', text)
            text = re.sub(r'(\bclass\s+\w+[^:]*:\s*\n)(def\s+)', r'\1    \2', text)
            text = re.sub(r'return\s+headroom_gb\s+1\.0', 'return headroom_gb >= 1.0', text)
            text = re.sub(r'if\s+ratio\s*=\s*1\.0\s+or\s+np\.random\.uniform\(0,\s*1\)\s*else:', 'if ratio >= 1.0 or np.random.uniform(0, 1) > 0.5:', text)
            text = re.sub(r'if\s+len\(free_blocks\)\s+lambda\s+k:\s*active_requests\[k\]\["priority"\]\)', 'if len(free_blocks) > 0: active_requests.sort(key=lambda k: active_requests[k]["priority"])', text)
            text = re.sub(r'return\s+pct_trainable\s+if\s+__name__', 'return pct_trainable\n\nif __name__', text)
            text = re.sub(r'if\s+cosine_sim\s*=\s*similarity_threshold:', 'if cosine_sim >= similarity_threshold:', text)
            text = re.sub(r'if\s+present\s*/\s*max\(1,\s*len\(words\)\)\s*=\s*0\.60:', 'if present / max(1, len(words)) >= 0.60:', text)
            text = re.sub(r'if\s+psi_score\s*=\s*0\.25:', 'if psi_score >= 0.25:', text)
            text = re.sub(r'if\s+now\s*-\s*entry\["timestamp"\]\s+self\.ttl:', 'if now - entry["timestamp"] > self.ttl:', text)
            text = re.sub(r'assert\s+compute_cost_savings\(\)\s+70\.0', 'assert compute_cost_savings() >= 70.0', text)
            
            # If bash mistakenly inside code
            if text.strip().startswith(('venv/', 'pip install', 'kubectl ')):
                if code_elem.get('class'):
                    code_elem['class'] = ['language-bash']
                    modified = True
                    continue

            try:
                ast.parse(text)
                code_elem.string = text
                modified = True
            except SyntaxError:
                pass

    if modified:
        fp.write_text(str(soup), encoding='utf-8')
        print(f"  ✅ Repaired syntax in Week {wn}")

print("\n🎉 AST REPAIR ENGINE COMPLETED!")
