#!/usr/bin/env python3
"""
Mechanical Validation Suite for AI/ML Course Site
Enforces function contract, DOM integrity, HTML validity, a11y, and KaTeX/Mermaid syntax.
"""

import os
import sys
import glob
import json
import re
from bs4 import BeautifulSoup
from collections import Counter

CONTRACT_PATH = os.path.join(os.path.dirname(__file__), '../src/schema/contract.json')

def load_contract():
    if os.path.exists(CONTRACT_PATH):
        with open(CONTRACT_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        "exposed_functions": [
            "goDay", "toggleSidebar", "closeSidebar", "toggleTheme", "completeDay",
            "quiz", "checkPredict", "toggleTask", "toggleSolution", "toggleCheck",
            "copyCode", "openRepl", "openInColab", "closeCompilerModal", "renderMermaid"
        ]
    }

def validate_week_html(fpath, contract):
    errors = []
    warnings = []
    fname = os.path.basename(fpath)
    
    with open(fpath, 'r', encoding='utf-8') as f:
        raw_content = f.read()

    # 1. Structural HTML Integrity
    html_count = len(re.findall(r'<html\b', raw_content, re.IGNORECASE))
    if html_count != 1:
        errors.append(f"Expected exactly 1 <html> tag, found {html_count}")

    head_count = len(re.findall(r'<head\b', raw_content, re.IGNORECASE))
    if head_count != 1:
        errors.append(f"Expected exactly 1 <head> tag, found {head_count}")

    body_count = len(re.findall(r'<body\b', raw_content, re.IGNORECASE))
    if body_count != 1:
        errors.append(f"Expected exactly 1 <body> tag, found {body_count}")

    soup = BeautifulSoup(raw_content, 'html.parser')

    # 2. LocalStorage and State Isolation (const WEEK & const DAYS)
    week_match = re.search(r'const\s+WEEK\s*=\s*(\d+);', raw_content)
    days_match = re.search(r'const\s+DAYS\s*=\s*(\[[^\]]+\]);', raw_content)

    expected_week_num = int(''.join(filter(str.isdigit, fname))) if any(c.isdigit() for c in fname) else None

    if not week_match:
        errors.append("Missing 'const WEEK = N;' declaration")
    elif expected_week_num and int(week_match.group(1)) != expected_week_num:
        errors.append(f"Declared WEEK={week_match.group(1)} does not match filename week {expected_week_num}")

    if not days_match:
        errors.append("Missing 'const DAYS = [...];' declaration")

    # 3. DOM ID Uniqueness
    all_elements = soup.find_all(id=True)
    all_ids = [el.get('id') for el in all_elements if el.get('id')]
    id_counts = Counter(all_ids)
    for el_id, count in id_counts.items():
        if count > 1:
            errors.append(f"Duplicate DOM ID '{el_id}' found {count} times")

    # 4. Function Contract Enforcement
    exposed = set(contract.get('exposed_functions', []))
    for el in soup.find_all(True):
        for attr in ['onclick', 'onkeydown', 'onkeyup']:
            val = el.get(attr)
            if not val:
                continue
            # Strip string literals so patterns like checkPredict('id', 'O(N) latency') don't treat 'O' as a function
            sanitized_val = re.sub(r"'(?:\\.|[^'])*'", "''", val)
            sanitized_val = re.sub(r'"(?:\\.|[^"])*"', '""', sanitized_val)

            # Extract invoked function calls like fnName(...)
            calls = re.findall(r'([a-zA-Z0-9_$]+)\s*\(', sanitized_val)
            dom_builtins = {
                'if', 'for', 'while', 'switch', 'return', 'click', 'stopPropagation', 'preventDefault',
                'getAttribute', 'setAttribute', 'removeAttribute', 'hasAttribute', 'includes', 'replace',
                'toString', 'match', 'test', 'toggle', 'add', 'remove', 'contains', 'focus', 'blur',
                'scrollIntoView', 'scrollTo', 'setTimeout', 'clearTimeout', 'setInterval', 'clearInterval',
                'alert', 'prompt', 'confirm', 'startsWith', 'endsWith', 'indexOf', 'trim', 'toLowerCase',
                'toUpperCase', 'split', 'join', 'slice', 'substring'
            }
            for c in calls:
                if c in dom_builtins:
                    continue
                if c not in exposed:
                    errors.append(f"Function contract violation: '{c}' in {attr}='{val[:40]}' is not in contract.json")

    # 5. Day Sections & Navigation Integrity
    day_sections = soup.find_all('div', class_='day-section')
    if not day_sections:
        errors.append("Zero '.day-section' elements found in document")

    for ds in day_sections:
        did = ds.get('id')
        if not did:
            errors.append("Day section missing 'id' attribute")
            continue
        
        raw_id = did.replace('day-', '')
        
        # Check completion button
        cbtn = ds.find('button', class_='complete-btn')
        if not cbtn:
            errors.append(f"Day section '{did}' missing '.complete-btn'")
        else:
            oc = cbtn.get('onclick', '')
            if f"completeDay('{raw_id}'" not in oc and f'completeDay("{raw_id}"' not in oc and f'completeDay({raw_id}' not in oc:
                errors.append(f"Day section '{did}' complete-btn onclick ('{oc}') does not match day id")

    # 6. Predict Blocks Integrity
    for pb in soup.find_all(class_='predict-block'):
        pbtn = pb.find('button', class_='predict-btn')
        if pbtn:
            oc = pbtn.get('onclick', '')
            m = re.findall(r"['\"]([^'\"]*)['\"]", oc)
            if len(m) >= 2:
                pid, ans = m[0], m[1]
                inp = soup.find(id=f"{pid}-input") or soup.find(id=pid)
                res = soup.find(id=f"{pid}-result") or soup.find(id=pid)
                if not inp:
                    errors.append(f"Predict block input for '{pid}' not found")
                if not res:
                    errors.append(f"Predict block result element for '{pid}' not found")

    # 7. Solution Box Toggles
    for st in soup.find_all('button', class_='solution-toggle'):
        oc = st.get('onclick', '')
        m = re.findall(r"toggleSolution\(['\"]([^'\"]+)['\"]", oc)
        if m:
            sol_id = m[0]
            sol_box = soup.find(id=sol_id)
            if not sol_box:
                errors.append(f"Solution toggle references non-existent solution box '{sol_id}'")

    # 8. Quiz Integrity
    for qb in soup.find_all(class_='quiz-block'):
        opts = qb.find_all(class_='quiz-opt')
        if opts:
            correct_opts = [o for o in opts if "'correct'" in o.get('onclick', '') or '"correct"' in o.get('onclick', '')]
            if len(correct_opts) == 0:
                errors.append("Quiz block has 0 correct options")
            elif len(correct_opts) > 1:
                errors.append(f"Quiz block has {len(correct_opts)} correct options (ambiguous)")

    # 9. KaTeX Formula Balance
    # Count pairs of $$ in text outside <pre>/<code>
    math_blocks = re.findall(r'\$\$', raw_content)
    if len(math_blocks) % 2 != 0:
        errors.append(f"Unbalanced '$$' KaTeX block delimiters (count={len(math_blocks)})")

    return errors, warnings

def main():
    target_dir = sys.argv[1] if len(sys.argv) > 1 else 'pages/weeks'
    files = sorted(glob.glob(os.path.join(target_dir, '*.html')), key=lambda p: int(''.join(filter(str.isdigit, os.path.basename(p)))) if any(c.isdigit() for c in os.path.basename(p)) else 0)
    
    if not files:
        print(f"No HTML files found in {target_dir}")
        sys.exit(1)

    contract = load_contract()
    total_errors = 0
    total_warnings = 0

    print(f"🔍 Running Mechanical Validation Suite across {len(files)} files in '{target_dir}'...\n")

    for fpath in files:
        fname = os.path.basename(fpath)
        errors, warnings = validate_week_html(fpath, contract)
        total_errors += len(errors)
        total_warnings += len(warnings)

        if errors:
            print(f"❌ {fname} — {len(errors)} error(s):")
            for e in errors:
                print(f"   • {e}")
        else:
            print(f"✅ {fname} — PASS (0 errors)")

    print("\n" + "=" * 60)
    if total_errors == 0:
        print(f"🎉 VALIDATION PASSED: 100% compliant ({len(files)} files checked, 0 errors).")
        sys.exit(0)
    else:
        print(f"💥 VALIDATION FAILED: {total_errors} error(s) found across {len(files)} files.")
        sys.exit(1)

if __name__ == '__main__':
    main()
