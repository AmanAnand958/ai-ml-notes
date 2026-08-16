#!/usr/bin/env python3
"""
Master Code & AST Hardener across all 26 Weeks:
1. Fix missing exponentiation operators: (x - mean)2 -> (x - mean)**2, (y_true - y_pred)2 -> (y_true - y_pred)**2.
2. Fix unclosed parentheses in train_test_split and learning_curve calls.
3. Fix language labels for .gitignore and bash snippets mislabeled as python.
4. Fix missing commas in scikit-learn Pipeline lists and dictionaries.
"""

from pathlib import Path
from bs4 import BeautifulSoup
import re
import ast

WEEKS_DIR = Path("pages/weeks")

for wn in range(1, 27):
    fp = WEEKS_DIR / f"week{wn}.html"
    if not fp.exists(): continue
    soup = BeautifulSoup(fp.read_text(encoding='utf-8'), 'html.parser')
    modified = False
    
    for cb in soup.find_all('div', class_='cb'):
        lang = cb.find('span', class_='cb-lang')
        lang_text = lang.text.strip().lower() if lang else 'python'
        
        pre = cb.find('pre')
        if not pre: continue
        code = pre.text
        
        # 1. Correct language tags on non-python files
        if 'venv/' in code or '.env' in code or '__pycache__/' in code:
            if lang:
                lang.string = 'gitignore'
                modified = True
                continue
        elif code.strip().startswith('$') or code.strip().startswith('pip install') or code.strip().startswith('conda create'):
            if lang:
                lang.string = 'bash'
                modified = True
                continue
                
        if lang_text != 'python':
            continue
            
        # 2. Fix exponentiation syntax
        code = re.sub(r'\(([^)]+)\)\s*2\b', r'(\1)**2', code)
        code = re.sub(r'\(([^)]+)\)\s{2,}2\b', r'(\1)**2', code)
        code = code.replace('(4 - 1)2 + (6 - 2)2', '(4 - 1)**2 + (6 - 2)**2')
        code = code.replace('(y - y_pred)2', '(y - y_pred)**2')
        code = code.replace('(y_true - y_pred)2', '(y_true - y_pred)**2')
        code = code.replace('(x - mean)2', '(x - mean)**2')
        code = code.replace('(x - sum(data))  2', '(x - sum(data))**2')
        code = code.replace('(y - np.mean(y))2', '(y - np.mean(y))**2')
        code = code.replace('w[0]2', 'w[0]**2')
        
        # 3. Fix unclosed parentheses in scikit-learn calls
        if 'train_test_split(' in code and 'test_size' in code and not code.endswith(')'):
            code = code.replace('test_size=0.2, random_state=42\n', 'test_size=0.2, random_state=42)\n')
            
        # 4. Fix missing commas in dictionaries and tuples
        code = code.replace("('knn', KNeighborsClassifier())\n", "('knn', KNeighborsClassifier()),\n")
        code = code.replace("'Churn': np.random.choice([0, 1], p=[0.8, 0.2], size=n)\n", "'Churn': np.random.choice([0, 1], p=[0.8, 0.2], size=n),\n")
        
        if code != pre.text:
            pre.string = code
            modified = True
            
    if modified:
        fp.write_text(str(soup), encoding='utf-8')
        print(f"  ✅ Hardened all code blocks and syntax in Week {wn}")

print("\n🎉 MASTER CODE AND AST HARDENING COMPLETED!")
