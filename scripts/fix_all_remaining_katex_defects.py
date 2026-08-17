#!/usr/bin/env python3
"""
scripts/fix_all_remaining_katex_defects.py
Fixes specific KaTeX formatting issues in Week 5 Days 32 & 33 in YAML and HTML.
"""

import glob, os

files = ['src/data/week05.yaml', 'pages/weeks/week5.html']

for fp in files:
    with open(fp, 'r', encoding='utf-8') as f:
        t = f.read()

    # Fix Day 32
    t = t.replace(r'\frac{SS_{\text{res}}{SS_{\text{tot}}', r'\frac{SS_{\text{res}}}{SS_{\text{tot}}}')
    t = t.replace(r'\\frac{SS_{\\text{res}}{SS_{\\text{tot}}', r'\\frac{SS_{\\text{res}}}{SS_{\\text{tot}}}')
    t = t.replace(r'SS_{\text{res}', r'SS_{\text{res}}')
    t = t.replace(r'SS_{\\text{res}', r'SS_{\\text{res}}')
    t = t.replace(r'SS_{\text{tot}', r'SS_{\text{tot}}')
    t = t.replace(r'SS_{\\text{tot}', r'SS_{\\text{tot}}')

    # Fix Day 33
    t = t.replace(r'\frac{\text{TP}{\text{TP} + \text{FP}', r'\frac{\text{TP}}{\text{TP} + \text{FP}}')
    t = t.replace(r'\\frac{\\text{TP}{\\text{TP} + \\text{FP}', r'\\frac{\\text{TP}}{\\text{TP} + \\text{FP}}')

    with open(fp, 'w', encoding='utf-8') as f:
        f.write(t)

    print(f"✓ Fixed remaining KaTeX formatting in {fp}")

print("=== ALL REMAINING KATEX DEFECTS REPAIRED ===")
