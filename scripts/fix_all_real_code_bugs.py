#!/usr/bin/env python3
"""
scripts/fix_all_real_code_bugs.py
Directly edits and fixes all genuine Python code syntax issues across YAML files:
1. Day 34 (Week 05): learning_curve call formatting
2. Day 35 (Week 05): param_grid and pipeline code formatting
3. Day 37 (Week 05): churn dataset creation
4. Day 60 (Week 09): MaxPool dummy_img matrix
5. Day 61 (Week 09): Conv2D layer call
6. Day 62 (Week 09): ResNet identity block
7. Day 63 (Week 09): NMS threshold filtering
8. Day 64 (Week 09): Conv2DTranspose block
9. Day 65 (Week 09): Keras callbacks list
"""

import yaml, re, os, glob, html

print("=== FIXING ALL GENUINE PYTHON CODE BUGS IN DATASETS ===")

# Fix Week 05
w5_path = 'src/data/week05.yaml'
with open(w5_path, 'r', encoding='utf-8') as f:
    d5 = yaml.safe_load(f)

for day in d5['days']:
    if day['day_num'] == 34:
        day['theory_html'] = re.sub(
            r'train_sizes,\s*train_scores,\s*val_scores\s*=\s*learning_curve\(model,\s*X,\s*y,\s*cv=5\)\s+Ridge\(alpha=1\.0\)[^;)]*\)',
            'train_sizes, train_scores, val_scores = learning_curve(\n    Ridge(alpha=1.0), X, y, cv=5, train_sizes=np.linspace(0.1, 1.0, 10),\n    scoring="neg_mean_squared_error"\n)',
            day['theory_html']
        )
    elif day['day_num'] == 35:
        day['theory_html'] = re.sub(
            r'param_grid\s*=\s*\{[\s\S]*?knn__weights[\s\S]*?\}',
            'param_grid = {\n    "knn__n_neighbors": [3, 5, 7, 9, 11],\n    "knn__weights": ["uniform", "distance"],\n    "knn__metric": ["euclidean", "manhattan"]\n}',
            day['theory_html']
        )
    elif day['day_num'] == 37:
        day['theory_html'] = re.sub(
            r'\'Churn\':\s*np\.random\.choice\(\[0,\s*1\],\s*p=\[0\.8,\s*0\.2\],\s*size=n\)\s+#\s*\}\)',
            "'Churn': np.random.choice([0, 1], p=[0.8, 0.2], size=n)\n})",
            day['theory_html']
        )

with open(w5_path, 'w', encoding='utf-8') as f:
    yaml.dump(d5, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
print("✓ Fixed all code in week05.yaml")

# Fix Week 09
w9_path = 'src/data/week09.yaml'
with open(w9_path, 'r', encoding='utf-8') as f:
    d9 = yaml.safe_load(f)

for day in d9['days']:
    if day['day_num'] == 60:
        day['theory_html'] = re.sub(
            r'dummy_img\s*=\s*np\.array\(\[[\s\S]*?\[4,\s*0,\s*7,\s*2\]',
            'dummy_img = np.array([\n    [1, 3, 2, 4],\n    [5, 6, 1, 0],\n    [2, 1, 8, 9],\n    [4, 0, 7, 2]\n])',
            day['theory_html']
        )
    elif day['day_num'] == 61:
        day['theory_html'] = re.sub(
            r'x\s*=\s*layers\.Conv2D\([\s\S]*?padding=[\'\"]same[\'\"][\s\S]*?\)\(inputs\)',
            'x = layers.Conv2D(32, (3, 3), padding="same")(inputs)',
            day['theory_html']
        )
    elif day['day_num'] == 62:
        day['theory_html'] = re.sub(
            r'#\s*hidden_dim,[\s\S]*?use_bias=False[\s\S]*?\)\(input_tensor\)',
            'x = layers.Conv2D(filters, (1, 1), padding="same", use_bias=False)(input_tensor)',
            day['theory_html']
        )
    elif day['day_num'] == 63:
        day['theory_html'] = re.sub(r'inds\s*=\s*np\.where\(iou\s*0\]', 'inds = np.where(iou <= iou_threshold)[0]', day['theory_html'])
        day['theory_html'] = re.sub(r'inds\s*=\s*np\.where\(iou\s*<=\s*iou_threshold\s*0\]', 'inds = np.where(iou <= iou_threshold)[0]', day['theory_html'])
    elif day['day_num'] == 64:
        day['theory_html'] = re.sub(
            r'x\s*=\s*layers\.Conv2DTranspose\([\s\S]*?strides=2,[\s\S]*?padding=[\'\"]same[\'\"]',
            'x = layers.Conv2DTranspose(num_filters, (2, 2), strides=2, padding="same")(input_tensor)',
            day['theory_html']
        )
    elif day['day_num'] == 65:
        day['theory_html'] = re.sub(
            r'callbacks\.ReduceLROnPlateau\(monitor=[\'\"]val_loss[\'\"],\s*factor=0\.2,\s*patience=3,\s*min_lr=1e-6\)\s*#\s*\]',
            'callbacks.ReduceLROnPlateau(monitor="val_loss", factor=0.2, patience=3, min_lr=1e-6)\n]',
            day['theory_html']
        )

with open(w9_path, 'w', encoding='utf-8') as f:
    yaml.dump(d9, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
print("✓ Fixed all code in week09.yaml")

print("\n=== ALL REAL CODE BUGS REPAIRED ===")
