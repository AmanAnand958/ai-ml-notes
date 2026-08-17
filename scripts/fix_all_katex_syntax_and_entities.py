#!/usr/bin/env python3
"""
scripts/fix_all_katex_syntax_and_entities.py
Fixes all LaTeX KaTeX syntax errors across YAML and HTML files:
1. Repairs unbalanced curly braces in RMSE, R^2, Precision, Recall, F1-Score formulas.
2. Unescapes HTML entities (&amp;, &lt;, &gt;) inside LaTeX $$ and $ blocks so KaTeX matrices and alignment work properly.
"""

import glob, yaml, re, os, html

print("=== FIXING ALL KATEX SYNTAX AND MATH ENTITIES ===")

def fix_math_in_text(text):
    # 1. Fix Week 5 Day 32 & 33 unbalanced LaTeX formulas
    text = text.replace(r'\text{RMSE} = \sqrt{\text{MSE}', r'\text{RMSE} = \sqrt{\text{MSE}}')
    text = text.replace(r'\frac{SS_{\text{res}}{SS_{\text{tot}}', r'\frac{SS_{\text{res}}}{SS_{\text{tot}}}')
    text = text.replace(r'\frac{\text{TP}{\text{TP} + \text{FP}', r'\frac{\text{TP}}{\text{TP} + \text{FP}}')
    text = text.replace(r'\frac{\text{TP}{\text{TP} + \text{FN}', r'\frac{\text{TP}}{\text{TP} + \text{FN}}')
    text = text.replace(
        r'\frac{\text{Precision} \times \text{Recall}{\text{Precision} + \text{Recall}',
        r'\frac{\text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}}'
    )
    
    # 2. Fix HTML entities inside $$ ... $$ LaTeX blocks
    def clean_latex(m):
        raw = m.group(0)
        # Unescape &amp; -> &, &lt; -> <, &gt; -> >
        cleaned = raw.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
        return cleaned

    # Apply to $$ ... $$ and \( ... \) and \[ ... \]
    text = re.sub(r'\$\$[\s\S]*?\$\$', clean_latex, text)
    text = re.sub(r'\\\[[\s\S]*?\\\]', clean_latex, text)
    text = re.sub(r'\\\([\s\S]*?\\\)', clean_latex, text)

    return text

# Apply to YAML files
for yf in sorted(glob.glob('src/data/week*.yaml')):
    with open(yf, 'r', encoding='utf-8') as f:
        cy = f.read()
    ny = fix_math_in_text(cy)
    if ny != cy:
        with open(yf, 'w', encoding='utf-8') as f:
            f.write(ny)
        print(f"✓ Fixed KaTeX math syntax in {yf}")

# Apply to HTML files
for hf in sorted(glob.glob('pages/weeks/week*.html')):
    with open(hf, 'r', encoding='utf-8') as f:
        ch = f.read()
    nh = fix_math_in_text(ch)
    if nh != ch:
        with open(hf, 'w', encoding='utf-8') as f:
            f.write(nh)
        print(f"✓ Fixed KaTeX math syntax in {hf}")

print("\n=== ALL KATEX SYNTAX REPAIRED ===")
