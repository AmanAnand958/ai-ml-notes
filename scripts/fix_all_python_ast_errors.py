#!/usr/bin/env python3
"""
Fix all Python AST Syntax Errors across Weeks 1, 4, 5, 6, 9:
1. Fix missing exponentiation operator (**): `(1 + monthly_rate) ** tenure_months`, `(y - y_pred)**2`, `w[0]**2`.
2. Fix un-commented task titles in code blocks: prepend `# ` to raw text headers.
3. Fix multi-line string print in Week 9 Day 60.
"""

from pathlib import Path
from bs4 import BeautifulSoup
import ast
import re

WEEKS_DIR = Path("pages/weeks")

# ─────────────────────────────────────────────────────────────────────────────
# 1. FIX WEEK 1 (EMI Formula Exponentiation)
# ─────────────────────────────────────────────────────────────────────────────
fp1 = WEEKS_DIR / "week1.html"
if fp1.exists():
    html1 = fp1.read_text(encoding='utf-8')
    html1 = html1.replace(
        "(1 + monthly_rate)  tenure_months",
        "(1 + monthly_rate) ** tenure_months"
    )
    fp1.write_text(html1, encoding='utf-8')
    print("✅ Fixed exponentiation syntax in Week 1")

# ─────────────────────────────────────────────────────────────────────────────
# 2. FIX WEEK 4 (Square Exponentiation)
# ─────────────────────────────────────────────────────────────────────────────
fp4 = WEEKS_DIR / "week4.html"
if fp4.exists():
    html4 = fp4.read_text(encoding='utf-8')
    html4 = html4.replace("(y - y_pred)2", "(y - y_pred)**2")
    html4 = html4.replace("(y - np.mean(y))2", "(y - np.mean(y))**2")
    html4 = html4.replace("w[0]2 + 2*w[1]**2", "w[0]**2 + 2*w[1]**2")
    fp4.write_text(html4, encoding='utf-8')
    print("✅ Fixed square exponentiation syntax in Week 4")

# ─────────────────────────────────────────────────────────────────────────────
# 3. FIX WEEK 5 (Distance & Task Headers)
# ─────────────────────────────────────────────────────────────────────────────
fp5 = WEEKS_DIR / "week5.html"
if fp5.exists():
    html5 = fp5.read_text(encoding='utf-8')
    html5 = html5.replace("(4 - 1)2 + (6 - 2)2", "(4 - 1)**2 + (6 - 2)**2")
    soup5 = BeautifulSoup(html5, 'html.parser')
    for pre in soup5.find_all('pre'):
        lines = pre.text.split('\n')
        new_lines = []
        for l in lines:
            if l.strip() and not l.strip().startswith('#') and not any(kw in l for kw in ['import', 'def', 'class', 'from', 'return', 'print', '=', 'if', 'for', 'while']):
                new_lines.append('# ' + l.strip())
            else:
                new_lines.append(l)
        pre.string = '\n'.join(new_lines)
    fp5.write_text(str(soup5), encoding='utf-8')
    print("✅ Fixed AST syntax in Week 5")

# ─────────────────────────────────────────────────────────────────────────────
# 4. FIX WEEK 6 (R2 Score Exponentiation)
# ─────────────────────────────────────────────────────────────────────────────
fp6 = WEEKS_DIR / "week6.html"
if fp6.exists():
    html6 = fp6.read_text(encoding='utf-8')
    html6 = html6.replace("(y - y_pred)  2", "(y - y_pred) ** 2")
    html6 = html6.replace("(y - y.mean())  2", "(y - y.mean()) ** 2")
    fp6.write_text(html6, encoding='utf-8')
    print("✅ Fixed exponentiation syntax in Week 6")

# ─────────────────────────────────────────────────────────────────────────────
# 5. FIX WEEK 9 (Un-commented Headers & Split Strings)
# ─────────────────────────────────────────────────────────────────────────────
fp9 = WEEKS_DIR / "week9.html"
if fp9.exists():
    html9 = fp9.read_text(encoding='utf-8')
    html9 = html9.replace('print("Pooled 2x2 Feature Map:\n",', 'print("Pooled 2x2 Feature Map:\\n",')
    soup9 = BeautifulSoup(html9, 'html.parser')
    for pre in soup9.find_all('pre'):
        lines = pre.text.split('\n')
        new_lines = []
        for l in lines:
            if l.strip() and not l.strip().startswith('#') and not any(kw in l for kw in ['import', 'def', 'class', 'from', 'return', 'print', '=', 'if', 'for', 'while', 'sobel', 'img', 'conv', 'max_pool', 'output', 'model', 'opt']):
                new_lines.append('# ' + l.strip())
            else:
                new_lines.append(l)
        pre.string = '\n'.join(new_lines)
    fp9.write_text(str(soup9), encoding='utf-8')
    print("✅ Fixed AST syntax in Week 9")

print("\n🎉 ALL PYTHON AST SYNTAX REPAIRS EXECUTED!")
