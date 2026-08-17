#!/usr/bin/env python3
"""
scripts/fix_all_math_exponents_and_syntax.py
Fixes missing exponents (**2) and malformed syntax across YAML and HTML files.
"""

import glob, yaml, re, os

print("=== FIXING MATH EXPONENTS AND SYNTAX DEFECTS ===")

all_yaml = sorted(glob.glob('src/data/week*.yaml'))
all_html = sorted(glob.glob('pages/weeks/week*.html'))

def repair_text(text):
    # 1. Fix missing exponent **2
    text = re.sub(r'\(x\s*-\s*mean\)\s*(?:<span[^>]*>)?2(?:</span>)?', '(x - mean)**2', text)
    text = re.sub(r'\(y_true\s*-\s*y_pred\)\s*(?:<span[^>]*>)?2(?:</span>)?', '(y_true - y_pred)**2', text)
    text = re.sub(r'\[p\s*(?:<span[^>]*>)?2(?:</span>)?\s+for\s+p\s+in\s+probs\]', '[p**2 for p in probs]', text)
    text = re.sub(r'errors\s*(?:<span[^>]*>)?2(?:</span>)?', 'errors**2', text)
    
    # 2. Fix Day 34 Learning curve unclosed / broken syntax
    text = re.sub(
        r'train_sizes,\s*train_scores,\s*val_scores\s*=\s*learning_curve\(model,\s*X,\s*y,\s*cv=5\)\s+Ridge\(alpha=1\.0\)[^;)]*\)',
        'train_sizes, train_scores, val_scores = learning_curve(\n    Ridge(alpha=1.0), X, y, cv=5, train_sizes=np.linspace(0.1, 1.0, 10),\n    scoring="neg_mean_squared_error"\n)',
        text
    )
    
    # 3. Fix Day 35 Param grid
    text = re.sub(
        r'param_grid\s*=\s*\{[\s\S]*?knn__weights[\s\S]*?\}',
        'param_grid = {\n    "knn__n_neighbors": [3, 5, 7, 9, 11],\n    "knn__weights": ["uniform", "distance"],\n    "knn__metric": ["euclidean", "manhattan"]\n}',
        text
    )
    
    # 4. Fix Day 60 MaxPool dummy array
    text = re.sub(
        r'dummy_img\s*=\s*np\.array\(\[\s+\[1,\s*3,\s*2,\s*4\],[\s\S]*?\[4,\s*0,\s*7,\s*2\]\s*',
        'dummy_img = np.array([\n    [1, 3, 2, 4],\n    [5, 6, 1, 0],\n    [2, 1, 8, 9],\n    [4, 0, 7, 2]\n])',
        text
    )
    
    # 5. Fix Day 63 NMS inds
    text = re.sub(r'inds\s*=\s*np\.where\(iou\s*<=\s*iou_threshold\s*0\]', 'inds = np.where(iou <= iou_threshold)[0]', text)
    text = re.sub(r'inds\s*=\s*np\.where\(iou\s*0\]', 'inds = np.where(iou <= iou_threshold)[0]', text)
    
    # 6. Fix Day 65 Callbacks
    text = re.sub(
        r'callbacks\.ReduceLROnPlateau\(monitor=[\'\"]val_loss[\'\"],\s*factor=0\.2,\s*patience=3,\s*min_lr=1e-6\)\s*#\s*\]',
        'callbacks.ReduceLROnPlateau(monitor="val_loss", factor=0.2, patience=3, min_lr=1e-6)\n]',
        text
    )

    return text

for yf in all_yaml:
    with open(yf, 'r', encoding='utf-8') as f:
        cy = f.read()
    ny = repair_text(cy)
    if ny != cy:
        with open(yf, 'w', encoding='utf-8') as f:
            f.write(ny)
        print(f"✓ Repaired math/syntax defects in {yf}")

for hf in all_html:
    with open(hf, 'r', encoding='utf-8') as f:
        ch = f.read()
    nh = repair_text(ch)
    if nh != ch:
        with open(hf, 'w', encoding='utf-8') as f:
            f.write(nh)
        print(f"✓ Repaired math/syntax defects in {hf}")

print("\n=== REPAIRS COMPLETED ===")
