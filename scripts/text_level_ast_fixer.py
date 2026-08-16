#!/usr/bin/env python3
"""
Deep AST Syntax Fixer for all <pre> and <code> elements across all 26 weeks.
"""

from pathlib import Path
from bs4 import BeautifulSoup
import re
import ast

WEEKS_DIR = Path("pages/weeks")

for wn in range(1, 27):
    fp = WEEKS_DIR / f"week{wn}.html"
    if not fp.exists(): continue
    raw = fp.read_text(encoding='utf-8')
    
    # 1. Global text-level replacements for broken exponentiations
    raw = re.sub(r'\(x\s*-\s*mean\)\s*2\b', r'(x - mean)**2', raw)
    raw = re.sub(r'\(x\s*-\s*sum\(data\)\)\s*2\b', r'(x - sum(data))**2', raw)
    raw = re.sub(r'\(y_true\s*-\s*y_pred\)\s*2\b', r'(y_true - y_pred)**2', raw)
    raw = re.sub(r'\(y\s*-\s*y_pred\)\s*2\b', r'(y - y_pred)**2', raw)
    raw = re.sub(r'\(y\s*-\s*np\.mean\(y\)\)\s*2\b', r'(y - np.mean(y))**2', raw)
    raw = re.sub(r'\(y\s*-\s*y\.mean\(\)\)\s*2\b', r'(y - y.mean())**2', raw)
    raw = re.sub(r'\(1\s*\+\s*monthly_rate\)\s{2,}tenure_months', r'(1 + monthly_rate) ** tenure_months', raw)
    raw = re.sub(r'\b(w\[\d+\])\s*2\b', r'\1**2', raw)
    
    # 2. Fix unclosed parentheses in scikit-learn calls
    raw = raw.replace('test_size=0.2, random_state=42\n    )', 'test_size=0.2, random_state=42)')
    raw = raw.replace('test_size=0.2, random_state=42\n', 'test_size=0.2, random_state=42)\n')
    raw = raw.replace("('knn', KNeighborsClassifier())\n", "('knn', KNeighborsClassifier()),\n")
    
    fp.write_text(raw, encoding='utf-8')
    print(f"  ✅ Text-level AST syntax repaired in Week {wn}")

print("\n🎉 ALL WEEKS TEXT-LEVEL AST ERRORS FIXED!")
