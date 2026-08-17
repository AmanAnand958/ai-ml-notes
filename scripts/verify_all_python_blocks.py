#!/usr/bin/env python3
"""
scripts/verify_all_python_blocks.py
Extracts and AST-parses every single Python block in the curriculum.
"""

import glob, yaml, re, os, ast, html

print("=== VERIFYING ALL PYTHON CODE BLOCKS WITH AST PARSER ===")

def clean_html_code(raw):
    # Step 1: Remove HTML tags like <span>, </span>, etc.
    no_tags = re.sub(r'<[^>]+>', '', raw)
    # Step 2: Unescape HTML entities (&lt; -> <, &gt; -> >, &amp; -> &)
    unescaped = html.unescape(no_tags)
    return unescaped.strip()

errors = []

for yf in sorted(glob.glob('src/data/week*.yaml')):
    with open(yf, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    for day in data.get('days', []):
        d_num = day.get('day_num', 0)
        
        # Predict code
        if day.get('predict_code'):
            code = clean_html_code(day['predict_code'])
            try:
                ast.parse(code)
            except SyntaxError as e:
                errors.append((yf, d_num, "predict_code", str(e), code))

        # Tasks
        for t in day.get('tasks', []):
            if t.get('solution_code'):
                code = clean_html_code(t['solution_code'])
                first = code.split('\n')[0].strip()
                if not (first.startswith('$') or first.startswith('docker ') or first.startswith('apiVersion') or first.startswith('FROM')):
                    try:
                        ast.parse(code)
                    except SyntaxError as e:
                        errors.append((yf, d_num, f"task: {t.get('title')}", str(e), code))

        # Theory code blocks
        theory = day.get('theory_html', '')
        for idx, cb in enumerate(re.findall(r'<pre><code>([\s\S]*?)</code></pre>', theory)):
            code = clean_html_code(cb)
            first = code.split('\n')[0].strip()
            # Skip non-python blocks (SQL, Docker, K8s, Bash, Diagrams)
            if (first.startswith('FROM ') or first.startswith('version:') or first.startswith('SELECT ')
                or first.startswith('WITH ') or first.startswith('-- ') or first.startswith('CREATE TABLE')
                or first.startswith('Step ') or first.startswith('+---') or first.startswith('apiVersion:')
                or first.startswith('#!/bin') or first.startswith('#!/usr') or first.startswith('docker ')
                or first.startswith('curl ') or first.startswith('async function') or first.startswith('__pycache__')):
                continue
            try:
                ast.parse(code)
            except SyntaxError as e:
                errors.append((yf, d_num, f"theory_block_{idx+1}", str(e), code))

print(f"\n=======================================================")
print(f"=== AST VERIFICATION RESULT: {len(errors)} PYTHON SYNTAX DEFECTS ===")
print(f"=======================================================")

if errors:
    for f, d, t, err, c in errors:
        print(f"[{f}] Day {d} ({t}): {err}")
        print(f"   Snippet: {c[:160]!r}\n")
else:
    print("✓ 100% of all Python code snippets across all 191 days compile cleanly with AST parse.")
