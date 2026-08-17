#!/usr/bin/env python3
"""
scripts/remediate_all_tag_syntax_errors.py
Fixes all malformed HTML tag headers (e.g. <h3 class=, <h2 class=) across all YAML and HTML files.
"""

import glob, re, os, yaml

print("=== REMEDIATING ALL TAG SYNTAX ERRORS ===")

all_yaml = sorted(glob.glob('src/data/week*.yaml'))
all_html = sorted(glob.glob('pages/weeks/week*.html') + ['index.html', 'roadmap.html', 'dashboard.html', 'resources.html'])

# 1. FIX YAML FILES
fixed_yaml = 0
for yf in all_yaml:
    with open(yf, 'r', encoding='utf-8') as f:
        content = f.read()

    new_content = re.sub(r'<h([1-6])>\s*class=', r'<h\1 class=', content)
    new_content = re.sub(r'<p>\s*class=', r'<p class=', new_content)
    new_content = re.sub(r'<div>\s*class=', r'<div class=', new_content)

    if new_content != content:
        fixed_yaml += 1
        with open(yf, 'w', encoding='utf-8') as f:
            f.write(new_content)

print(f"✓ Fixed tag syntax errors across {fixed_yaml} YAML files.")

# 2. FIX HTML FILES
fixed_html = 0
for hf in all_html:
    with open(hf, 'r', encoding='utf-8') as f:
        content = f.read()

    new_content = re.sub(r'<h([1-6])>\s*class=', r'<h\1 class=', content)
    new_content = re.sub(r'<p>\s*class=', r'<p class=', new_content)
    new_content = re.sub(r'<div>\s*class=', r'<div class=', new_content)

    if new_content != content:
        fixed_html += 1
        with open(hf, 'w', encoding='utf-8') as f:
            f.write(new_content)

print(f"✓ Fixed tag syntax errors across {fixed_html} HTML files.")
print("=== REMEDIATION COMPLETE ===")
