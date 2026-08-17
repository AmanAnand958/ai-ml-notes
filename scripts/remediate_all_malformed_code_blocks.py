#!/usr/bin/env python3
"""
scripts/remediate_all_malformed_code_blocks.py
Fixes all malformed Python code snippets across YAML and HTML files.
"""

import glob, yaml, re, os

print("=== REMEDIATING ALL MALFORMED CODE BLOCKS ===")

# 1. REMEDIATE YAML FILES
fixes_yaml = [
    # Week 04 - Day 22
    ('src/data/week04.yaml', [
        (r'outliers = salaries\[\(salaries\s+upper_fence\)\]', 'outliers = salaries[(salaries > upper_fence) | (salaries < lower_fence)]'),
        (r'variance = sum\(\[\(x - mean\)2 for x in data\]\)', 'variance = sum([(x - mean)**2 for x in data])')
    ]),
    # Week 05 - Day 34, 35, 37
    ('src/data/week05.yaml', [
        (r'train_sizes, train_scores, val_scores = learning_curve\(model, X, y, cv=5\)\s+Ridge\(alpha=1\.0\), X, y, cv=5, train_sizes=np\.linspace\(0\.1, 1\.0, 10\),\s+scoring=\'neg_mean_squared_error\'\s+# \)',
         'train_sizes, train_scores, val_scores = learning_curve(\n    Ridge(alpha=1.0), X, y, cv=5, train_sizes=np.linspace(0.1, 1.0, 10),\n    scoring=\'neg_mean_squared_error\'\n)'),
        (r'param_grid = \{\s+# \'knn__n_neighbors\': \[3, 5, 7, 9, 11\],\s+\'knn__weights\': \[\'uniform\', \'distance\'\],\s+# \'knn__metric\': \[\'euclidean\', \'manhattan\'\]\s+# \}',
         'param_grid = {\n    \'knn__n_neighbors\': [3, 5, 7, 9, 11],\n    \'knn__weights\': [\'uniform\', \'distance\'],\n    \'knn__metric\': [\'euclidean\', \'manhattan\']\n}'),
        (r'\'Churn\': np\.random\.choice\(\[0, 1\], p=\[0\.8, 0\.2\], size=n\)\s+# \}\)',
         '\'Churn\': np.random.choice([0, 1], p=[0.8, 0.2], size=n)\n})')
    ]),
    # Week 06 - Day 42
    ('src/data/week06.yaml', [
        (r'mse\s*=\s*np\.mean\(\(y_true - y_pred\)2\)', 'mse   = np.mean((y_true - y_pred)**2)'),
        (r'is_small = np\.abs\(errors\)\s+where\(is_small,\s+0\.5 \* errors\*\*2,\s+delta \* \(np\.abs\(errors\) - 0\.5 \* delta\)\)',
         'is_small = np.abs(errors) <= delta\n    huber = np.where(is_small, 0.5 * errors**2, delta * (np.abs(errors) - 0.5 * delta))')
    ]),
    # Week 09 - Day 60, 61, 62, 63, 64, 65
    ('src/data/week09.yaml', [
        (r'dummy_img = np\.array\(\[\s+# \[1, 3, 2, 4\],\s+# \[5, 6, 1, 0\],\s+# \[2, 1, 8, 9\],\s+# \[4, 0, 7, 2\]',
         'dummy_img = np.array([\n    [1, 3, 2, 4],\n    [5, 6, 1, 0],\n    [2, 1, 8, 9],\n    [4, 0, 7, 2]\n])'),
        (r'x = layers\.Conv2D\(\s+# 32,\s+# \(3, 3\),\s+padding=\'same\'\s+# \)\(inputs\)',
         'x = layers.Conv2D(32, (3, 3), padding=\'same\')(inputs)'),
        (r'# hidden_dim,\s+# \(1, 1\),\s+padding=\'same\',\s+use_bias=False\s+# \)\(input_tensor\)',
         'x = layers.Conv2D(hidden_dim, (1, 1), padding=\'same\', use_bias=False)(input_tensor)'),
        (r'inds = np\.where\(iou 0\]',
         'inds = np.where(iou <= iou_threshold)[0]'),
        (r'x = layers\.Conv2DTranspose\(\s+# num_filters,\s+# \(2, 2\),\s+strides=2,\s+padding=\'same\'',
         'x = layers.Conv2DTranspose(num_filters, (2, 2), strides=2, padding=\'same\')(input_tensor)'),
        (r'callbacks\.ReduceLROnPlateau\(monitor=\'val_loss\', factor=0\.2, patience=3, min_lr=1e-6\)\s+# \]',
         'callbacks.ReduceLROnPlateau(monitor=\'val_loss\', factor=0.2, patience=3, min_lr=1e-6)\n]')
    ])
]

for file_path, replacements in fixes_yaml:
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        for pat, rep in replacements:
            content = re.sub(pat, rep, content)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✓ Remediated malformed code in {file_path}")

# 2. SYNCHRONIZE TO HTML PAGES
html_fixes = [
    ('pages/weeks/week4.html', [
        (r'outliers = salaries\[\(salaries\s+upper_fence\)\]', 'outliers = salaries[(salaries > upper_fence) | (salaries < lower_fence)]'),
        (r'variance = sum\(\[\(x - mean\)2 for x in data\]\)', 'variance = sum([(x - mean)**2 for x in data])')
    ]),
    ('pages/weeks/week5.html', [
        (r'train_sizes, train_scores, val_scores = learning_curve\(model, X, y, cv=5\)\s+Ridge\(alpha=1\.0\), X, y, cv=5, train_sizes=np\.linspace\(0\.1, 1\.0, 10\),\s+scoring=\'neg_mean_squared_error\'\s+# \)',
         'train_sizes, train_scores, val_scores = learning_curve(\n    Ridge(alpha=1.0), X, y, cv=5, train_sizes=np.linspace(0.1, 1.0, 10),\n    scoring=\'neg_mean_squared_error\'\n)'),
        (r'param_grid = \{\s+# \'knn__n_neighbors\': \[3, 5, 7, 9, 11\],\s+\'knn__weights\': \[\'uniform\', \'distance\'\],\s+# \'knn__metric\': \[\'euclidean\', \'manhattan\'\]\s+# \}',
         'param_grid = {\n    \'knn__n_neighbors\': [3, 5, 7, 9, 11],\n    \'knn__weights\': [\'uniform\', \'distance\'],\n    \'knn__metric\': [\'euclidean\', \'manhattan\']\n}'),
        (r'\'Churn\': np\.random\.choice\(\[0, 1\], p=\[0\.8, 0\.2\], size=n\)\s+# \}\)',
         '\'Churn\': np.random.choice([0, 1], p=[0.8, 0.2], size=n)\n})')
    ]),
    ('pages/weeks/week6.html', [
        (r'mse\s*=\s*np\.mean\(\(y_true - y_pred\)2\)', 'mse   = np.mean((y_true - y_pred)**2)'),
        (r'is_small = np\.abs\(errors\)\s+where\(is_small,\s+0\.5 \* errors\*\*2,\s+delta \* \(np\.abs\(errors\) - 0\.5 \* delta\)\)',
         'is_small = np.abs(errors) <= delta\n    huber = np.where(is_small, 0.5 * errors**2, delta * (np.abs(errors) - 0.5 * delta))')
    ]),
    ('pages/weeks/week9.html', [
        (r'dummy_img = np\.array\(\[\s+# \[1, 3, 2, 4\],\s+# \[5, 6, 1, 0\],\s+# \[2, 1, 8, 9\],\s+# \[4, 0, 7, 2\]',
         'dummy_img = np.array([\n    [1, 3, 2, 4],\n    [5, 6, 1, 0],\n    [2, 1, 8, 9],\n    [4, 0, 7, 2]\n])'),
        (r'x = layers\.Conv2D\(\s+# 32,\s+# \(3, 3\),\s+padding=\'same\'\s+# \)\(inputs\)',
         'x = layers.Conv2D(32, (3, 3), padding=\'same\')(inputs)'),
        (r'# hidden_dim,\s+# \(1, 1\),\s+padding=\'same\',\s+use_bias=False\s+# \)\(input_tensor\)',
         'x = layers.Conv2D(hidden_dim, (1, 1), padding=\'same\', use_bias=False)(input_tensor)'),
        (r'inds = np\.where\(iou 0\]',
         'inds = np.where(iou <= iou_threshold)[0]'),
        (r'x = layers\.Conv2DTranspose\(\s+# num_filters,\s+# \(2, 2\),\s+strides=2,\s+padding=\'same\'',
         'x = layers.Conv2DTranspose(num_filters, (2, 2), strides=2, padding=\'same\')(input_tensor)'),
        (r'callbacks\.ReduceLROnPlateau\(monitor=\'val_loss\', factor=0\.2, patience=3, min_lr=1e-6\)\s+# \]',
         'callbacks.ReduceLROnPlateau(monitor=\'val_loss\', factor=0.2, patience=3, min_lr=1e-6)\n]')
    ])
]

for file_path, replacements in html_fixes:
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        for pat, rep in replacements:
            content = re.sub(pat, rep, content)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✓ Remediated malformed code in {file_path}")

print("\n=== MALFORMED CODE REMEDIATION COMPLETE ===")
