#!/usr/bin/env python3
"""
scripts/fix_yaml_svg_style_quotes.py
Escapes double quotes in style=\"max-width: 100%; height: auto;\" inside YAML double-quoted strings.
"""

import glob, re

for yf in sorted(glob.glob('src/data/week*.yaml')):
    with open(yf, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace unescaped style="max-width: 100%; height: auto;" with style=\"max-width: 100%; height: auto;\"
    content = content.replace('style="max-width: 100%; height: auto;"', 'style=\\"max-width: 100%; height: auto;\\"')
    # Also clean any double backslashes if present
    content = content.replace('style=\\\\"max-width', 'style=\\"max-width')

    with open(yf, 'w', encoding='utf-8') as f:
        f.write(content)

print("Fixed SVG style quote escaping in all YAML files.")
