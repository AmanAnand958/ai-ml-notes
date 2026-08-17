#!/usr/bin/env python3
"""
scripts/fix_all_malformed_code_properly.py
Fixes all malformed code snippets directly within theory_html strings in YAML and HTML.
"""

import glob, yaml, re, os, html

print("=== FIXING ALL CODE DEFECTS PROPERLY ===")

def fix_content(text):
    # Day 22 fixes
    text = re.sub(r'\(salaries\s+upper_fence\)', '(salaries > upper_fence) | (salaries < lower_fence)', text)
    text = re.sub(r'\(x\s*-\s*mean\)2', '(x - mean)**2', text)
    text = re.sub(r'\(y_true\s*-\s*y_pred\)2', '(y_true - y_pred)**2', text)
    
    # Day 24 & 25
    text = re.sub(r'np\.dot\(A,\s*v\)\s+lambda_val', 'np.dot(A, v) == lambda_val * v', text)
    
    # Day 34 learning curve
    text = re.sub(
        r'train_sizes,\s*train_scores,\s*val_scores\s*=\s*learning_curve\(model,\s*X,\s*y,\s*cv=5\)\s+Ridge\(alpha=1\.0\)[^)]*\)',
        'train_sizes, train_scores, val_scores = learning_curve(\n    Ridge(alpha=1.0), X, y, cv=5, train_sizes=np.linspace(0.1, 1.0, 10),\n    scoring="neg_mean_squared_error"\n)',
        text
    )
    
    # Day 35 param grid
    text = re.sub(
        r'param_grid\s*=\s*\{[^}]*knn__weights[^}]*\}',
        'param_grid = {\n    "knn__n_neighbors": [3, 5, 7, 9, 11],\n    "knn__weights": ["uniform", "distance"],\n    "knn__metric": ["euclidean", "manhattan"]\n}',
        text
    )
    
    # Day 38 Decision Tree condition
    text = re.sub(r'gini\s*=\s*1\.0\s*-\s*sum\(\[p2\s*for\s*p\s*in\s*probs\]\)', 'gini = 1.0 - sum([p**2 for p in probs])', text)
    
    # Day 42 Huber loss
    text = re.sub(
        r'is_small\s*=\s*np\.abs\(errors\)\s+where\(is_small,\s*0\.5\s*\*?\s*errors\*\*2,\s*delta\s*\*\s*\(np\.abs\(errors\)\s*-\s*0\.5\s*\*\s*delta\)\)',
        'is_small = np.abs(errors) <= delta\n    huber = np.where(is_small, 0.5 * errors**2, delta * (np.abs(errors) - 0.5 * delta))',
        text
    )

    # Day 60 MaxPool
    text = re.sub(
        r'dummy_img\s*=\s*np\.array\(\[\s+\[1,\s*3,\s*2,\s*4\],[\s\S]*?\[4,\s*0,\s*7,\s*2\]\s*',
        'dummy_img = np.array([\n    [1, 3, 2, 4],\n    [5, 6, 1, 0],\n    [2, 1, 8, 9],\n    [4, 0, 7, 2]\n])',
        text
    )
    
    # Day 61 Conv2D
    text = re.sub(
        r'x\s*=\s*layers\.Conv2D\([\s\S]*?padding=\'same\'[\s\S]*?\)\(inputs\)',
        'x = layers.Conv2D(32, (3, 3), padding="same")(inputs)',
        text
    )
    
    # Day 62 ResNet block
    text = re.sub(
        r'#\s*hidden_dim,[\s\S]*?use_bias=False[\s\S]*?\)\(input_tensor\)',
        'x = layers.Conv2D(hidden_dim, (1, 1), padding="same", use_bias=False)(input_tensor)',
        text
    )
    
    # Day 63 NMS
    text = re.sub(r'inds\s*=\s*np\.where\(iou\s*0\]', 'inds = np.where(iou <= iou_threshold)[0]', text)
    text = re.sub(r'inds\s*=\s*np\.where\(iou\s*<=\s*iou_threshold\s*0\]', 'inds = np.where(iou <= iou_threshold)[0]', text)

    # Day 64 U-Net Transpose
    text = re.sub(
        r'x\s*=\s*layers\.Conv2DTranspose\([\s\S]*?strides=2,[\s\S]*?padding=\'same\'',
        'x = layers.Conv2DTranspose(num_filters, (2, 2), strides=2, padding="same")(input_tensor)',
        text
    )
    
    # Day 65 Callbacks
    text = re.sub(
        r'callbacks\.ReduceLROnPlateau\(monitor=\'val_loss\',\s*factor=0\.2,\s*patience=3,\s*min_lr=1e-6\)\s*#\s*\]',
        'callbacks.ReduceLROnPlateau(monitor="val_loss", factor=0.2, patience=3, min_lr=1e-6)\n]',
        text
    )

    return text

# Apply to all YAML files
for yf in sorted(glob.glob('src/data/week*.yaml')):
    with open(yf, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    for day in data.get('days', []):
        theory = day.get('theory_html', '')
        day['theory_html'] = fix_content(theory)
        for t in day.get('tasks', []):
            if t.get('solution_code'):
                t['solution_code'] = fix_content(t['solution_code'])

    with open(yf, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)

print("✓ Fixed all code defects in YAML source files.")

# Apply to all HTML week files
for hf in sorted(glob.glob('pages/weeks/week*.html')):
    with open(hf, 'r', encoding='utf-8') as f:
        content = f.read()

    new_content = fix_content(content)
    if new_content != content:
        with open(hf, 'w', encoding='utf-8') as f:
            f.write(new_content)

print("✓ Fixed all code defects in HTML week portal files.")
