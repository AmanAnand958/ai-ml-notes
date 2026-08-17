#!/usr/bin/env python3
"""
scripts/fix_final_katex_formulas.py
Fixes final LaTeX KaTeX formula braces in src/data/week05.yaml and pages/weeks/week5.html
"""

files = ['src/data/week05.yaml', 'pages/weeks/week5.html']

for fp in files:
    with open(fp, 'r', encoding='utf-8') as f:
        t = f.read()

    # Day 32 R^2 formula
    t = t.replace(
        r'R^2 = 1 - \frac{SS_{\text{res}}}{SS_{\text{tot}}$$',
        r'R^2 = 1 - \frac{SS_{\text{res}}}{SS_{\text{tot}}}$$'
    )
    t = t.replace(
        r'R^2 = 1 - \\frac{SS_{\\text{res}}}{SS_{\\text{tot}}$$',
        r'R^2 = 1 - \\frac{SS_{\\text{res}}}{SS_{\\text{tot}}}$$'
    )
    
    # Day 33 Precision formula
    t = t.replace(
        r'\text{Precision} = \frac{\text{TP}{\text{TP} + \text{FP}$$',
        r'\text{Precision} = \frac{\text{TP}}{\text{TP} + \text{FP}}$$'
    )
    t = t.replace(
        r'\\text{Precision} = \\frac{\\text{TP}{\\text{TP} + \\text{FP}$$',
        r'\\text{Precision} = \\frac{\\text{TP}}{\\text{TP} + \\text{FP}}$$'
    )
    t = t.replace(
        r'\\text{Precision} = \\frac{\\text{TP}{\\text{TP}\   \ + \\text{FP}$$',
        r'\\text{Precision} = \\frac{\\text{TP}}{\\text{TP} + \\text{FP}}$$'
    )

    with open(fp, 'w', encoding='utf-8') as f:
        f.write(t)
    print(f"✓ Fixed final formulas in {fp}")

print("=== FINAL KATEX FORMULAS FIXED ===")
