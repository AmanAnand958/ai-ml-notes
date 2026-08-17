#!/usr/bin/env python3
"""
scripts/fix_week05_yaml_latex.py
Fixes double backslash LaTeX formulas in src/data/week05.yaml
"""

w5 = 'src/data/week05.yaml'
with open(w5, 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace(r'\\text{RMSE} = \\sqrt{\\text{MSE}$$', r'\\text{RMSE} = \\sqrt{\\text{MSE}}$$')
text = text.replace(r'\\frac{SS_{\\text{res}}{SS_{\\text{tot}}', r'\\frac{SS_{\\text{res}}}{SS_{\\text{tot}}}')
text = text.replace(r'\\frac{\\text{TP}{\\text{TP} + \\text{FP}', r'\\frac{\\text{TP}}{\\text{TP} + \\text{FP}}')
text = text.replace(r'\\frac{\\text{TP}{\\text{TP} + \\text{FN}', r'\\frac{\\text{TP}}{\\text{TP} + \\text{FN}}')
text = text.replace(
    r'\\frac{\\text{Precision} \\times \\text{Recall}{\\text{Precision} + \\text{Recall}',
    r'\\frac{\\text{Precision} \\times \\text{Recall}}{\\text{Precision} + \\text{Recall}}'
)

with open(w5, 'w', encoding='utf-8') as f:
    f.write(text)

print("Fixed LaTeX syntax in src/data/week05.yaml")
