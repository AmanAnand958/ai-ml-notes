#!/usr/bin/env python3
"""
scripts/fix_yaml_quoted_strings.py
Fixes any literal unescaped newlines inside YAML double-quoted string fields.
"""

import glob, re, os

# Fix week05.yaml
w5_path = 'src/data/week05.yaml'
with open(w5_path, 'r', encoding='utf-8') as f:
    t = f.read()

# Replace the literal multiline in week05.yaml with escaped \n
t = t.replace(
'''param_grid = {
    "knn__n_neighbors": [3, 5, 7, 9, 11],
    "knn__weights": ["uniform", "distance"],
    "knn__metric": ["euclidean", "manhattan"]
}''',
'param_grid = {\\n    \\"knn__n_neighbors\\": [3, 5, 7, 9, 11],\\n    \\"knn__weights\\": [\\"uniform\\", \\"distance\\"],\\n    \\"knn__metric\\": [\\"euclidean\\", \\"manhattan\\"]\\n}'
)

with open(w5_path, 'w', encoding='utf-8') as f:
    f.write(t)

print("Fixed week05.yaml string formatting.")
