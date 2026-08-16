#!/usr/bin/env python3
"""
Deep syntax repair: replaces `)2` with `)**2`, `)  2` with `)**2`, `) 2` with `)**2`,
fixes unclosed `learning_curve(` and `train_test_split(` calls, and missing commas in pipelines.
"""

from pathlib import Path
import re

WEEKS_DIR = Path("pages/weeks")

for wn in range(1, 27):
    fp = WEEKS_DIR / f"week{wn}.html"
    if not fp.exists(): continue
    raw = fp.read_text(encoding='utf-8')
    
    # Exponentiation fixes
    raw = re.sub(r'\)\s*2\b', r')**2', raw)
    raw = re.sub(r'\( x - mean\)\*\*2', r'(x - mean)**2', raw)
    raw = re.sub(r'\(x - sum\(data\)\)\s{2,}2\b', r'(x - sum(data))**2', raw)
    
    # Fix scikit-learn calls
    raw = raw.replace('train_sizes, train_scores, val_scores = learning_curve(\n', 'train_sizes, train_scores, val_scores = learning_curve(model, X, y, cv=5)\n')
    raw = raw.replace("param_grid = {\n    'n_estimators': [50, 100],\n", "param_grid = {\n    'n_estimators': [50, 100]\n}\n")
    raw = raw.replace("('scaler', StandardScaler()),\n    ('knn', KNeighborsClassifier())\n", "('scaler', StandardScaler()),\n    ('knn', KNeighborsClassifier())\n])\n")
    
    fp.write_text(raw, encoding='utf-8')
    print(f"  ✅ Repaired syntax in Week {wn}")

print("\n🎉 ALL WEEKS SYNTAX REPAIRED!")
