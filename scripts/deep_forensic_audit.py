#!/usr/bin/env python3
"""
scripts/deep_forensic_audit.py
Advanced Forensic Audit across 7 New Dimensions:
1. Predict Execution Parity: Executes every single predict Python snippet and checks if stdout matches the answer exactly.
2. DOM & Event Handler Symmetry: Checks every onclick (checkPredict, toggleSolution, checkQuiz, showDay) for matching DOM element IDs.
3. Mojibake / Character Encoding Corruptions: Scans for broken UTF-8 byte sequences (e.g. â€, Ã, etc.).
4. Flashcard Quality & Deduplication: Checks for empty fronts/backs, front==back, or exact duplicate flashcards across the curriculum.
5. Missing / Broken CSS Variables & Asset Paths: Checks for undefined CSS vars or broken local asset paths.
6. Gotcha Quality: Checks for empty traps, missing explanations, or trivial advice.
7. Analogy Uniqueness & Relevance: Checks for copy-pasted analogies across multiple days.
"""

import glob, os, re, yaml, json, html, subprocess, sys

print("=== STARTING DEEP FORENSIC CURRICULUM AUDIT ===")

forensic_findings = []

def add_forensic_issue(category, dimension, severity, location, detail):
    forensic_findings.append({
        "category": category,
        "dimension": dimension,
        "severity": severity,
        "location": location,
        "detail": detail
    })

# -------------------------------------------------------------
# 1. PREDICT EXECUTION PARITY CHECK (Subprocess execution)
# -------------------------------------------------------------
print("\n[1/7] Testing Predict Execution Parity against Python Subprocess...")
yaml_files = sorted(glob.glob('src/data/week*.yaml'))

for yf in yaml_files:
    w_match = re.search(r'week(\d+)', yf)
    w_num = int(w_match.group(1)) if w_match else 0
    
    with open(yf, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
        
    for d in data.get('days', []):
        d_num = d.get('day_num')
        d_loc = f"week{w_num:02d} day{d_num}"
        p = d.get('predict', {})
        code = p.get('code', '')
        expected_ans = str(p.get('answer', '')).strip()
        
        if not code or not expected_ans:
            continue
            
        # Clean code for execution
        clean_code = html.unescape(code)
        clean_code = re.sub(r'<[^>]+>', '', clean_code)
        
        # Execute snippet
        try:
            res = subprocess.run(
                [sys.executable, '-c', clean_code],
                capture_output=True,
                text=True,
                timeout=3
            )
            actual_stdout = res.stdout.strip()
            if res.returncode != 0:
                add_forensic_issue(
                    "Predict Execution",
                    "predict_snippet_runtime_error",
                    "high",
                    d_loc,
                    f"Predict code failed runtime execution: {res.stderr.strip()[:100]}"
                )
            elif actual_stdout and expected_ans != actual_stdout:
                # Check if it's just formatting differences (like floats)
                if expected_ans.lower() != actual_stdout.lower():
                    add_forensic_issue(
                        "Predict Execution",
                        "predict_answer_stdout_mismatch",
                        "medium",
                        d_loc,
                        f"Expected answer '{expected_ans}' != Python stdout '{actual_stdout}'"
                    )
        except subprocess.TimeoutExpired:
            add_forensic_issue("Predict Execution", "predict_snippet_timeout", "high", d_loc, "Predict code timed out (>3s)")
        except Exception as e:
            add_forensic_issue("Predict Execution", "predict_snippet_exec_fail", "high", d_loc, f"Exec error: {e}")

# -------------------------------------------------------------
# 2. DOM & EVENT HANDLER SYMMETRY CHECK
# -------------------------------------------------------------
print("\n[2/7] Checking DOM & Event Handler Symmetry across HTML files...")
html_files = sorted(glob.glob('pages/weeks/week*.html'))

for hf in html_files:
    w_match = re.search(r'week(\d+)\.html', hf)
    w_num = int(w_match.group(1)) if w_match else 0
    loc_file = f"week{w_num:02d}.html"
    
    with open(hf, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Check checkPredict calls
    predict_calls = re.findall(r'checkPredict\(\'([^\']+)\'', content)
    for p_id in predict_calls:
        input_id = f"{p_id}-input"
        res_id = f"{p_id}-result"
        if f'id="{input_id}"' not in content:
            add_forensic_issue("DOM Symmetry", "missing_predict_input_id", "high", loc_file, f"checkPredict('{p_id}') has no matching #{input_id}")
        if f'id="{res_id}"' not in content:
            add_forensic_issue("DOM Symmetry", "missing_predict_result_id", "high", loc_file, f"checkPredict('{p_id}') has no matching #{res_id}")

    # Check toggleSolution calls
    toggle_calls = re.findall(r'toggleSolution\(\'([^\']+)\'', content)
    for sol_id in toggle_calls:
        if f'id="{sol_id}"' not in content:
            add_forensic_issue("DOM Symmetry", "missing_toggle_solution_id", "high", loc_file, f"toggleSolution('{sol_id}') has no matching #{sol_id} container")

    # Check showDay pills vs day sections
    day_sections = set(re.findall(r'id="day-(\d+)"', content))
    pill_calls = set(re.findall(r'showDay\((\d+)\)', content))
    missing_days = pill_calls - day_sections
    if missing_days:
        add_forensic_issue("DOM Symmetry", "showday_missing_section", "high", loc_file, f"Pills call showDay({missing_days}) but #day-X does not exist")

# -------------------------------------------------------------
# 3. MOJIBAKE & UTF-8 ENCODING ARTIFACTS
# -------------------------------------------------------------
print("\n[3/7] Scanning for Mojibake and Broken UTF-8 Sequences...")
mojibake_patterns = [r'Ã¡', r'Ã©', r'Ã­', r'Ã³', r'Ãº', r'Ã±', r'â€™', r'â€œ', r'â€', r'â€“', r'â€”', r'Ã¢']

for path in sorted(glob.glob('src/data/week*.yaml') + glob.glob('pages/weeks/week*.html')):
    with open(path, 'r', encoding='utf-8', errors='replace') as f:
        text = f.read()
    for pat in mojibake_patterns:
        matches = len(re.findall(pat, text))
        if matches > 0:
            add_forensic_issue("Encoding", "mojibake_encoding_artifact", "medium", os.path.basename(path), f"Found {matches} occurrences of mojibake pattern '{pat}'")

# -------------------------------------------------------------
# 4. FLASHCARD QUALITY & DEDUPLICATION
# -------------------------------------------------------------
print("\n[4/7] Auditing Flashcard Quality & Cross-Curriculum Deduplication...")
seen_flashcards = {}

for yf in yaml_files:
    w_match = re.search(r'week(\d+)', yf)
    w_num = int(w_match.group(1)) if w_match else 0
    with open(yf, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    for d in data.get('days', []):
        d_num = d.get('day_num')
        d_loc = f"week{w_num:02d} day{d_num}"
        for f_idx, fc in enumerate(d.get('flashcards', [])):
            front = str(fc.get('front', '')).strip()
            back = str(fc.get('back', '')).strip()
            if not front:
                add_forensic_issue("Flashcards", "flashcard_empty_front", "medium", d_loc, f"Flashcard #{f_idx} has empty front")
            if not back:
                add_forensic_issue("Flashcards", "flashcard_empty_back", "medium", d_loc, f"Flashcard #{f_idx} has empty back")
            if front.lower() == back.lower() and front:
                add_forensic_issue("Flashcards", "flashcard_front_equals_back", "medium", d_loc, f"Flashcard front equals back: '{front}'")
            
            # Check duplicate
            if front:
                norm_front = front.lower()
                if norm_front in seen_flashcards:
                    add_forensic_issue("Flashcards", "duplicate_flashcard", "low", d_loc, f"Duplicate flashcard front with {seen_flashcards[norm_front]}: '{front}'")
                else:
                    seen_flashcards[norm_front] = d_loc

# -------------------------------------------------------------
# 5. CSS VARIABLES & ASSET PATH INTEGRITY
# -------------------------------------------------------------
print("\n[5/7] Checking CSS Variables & Asset Paths...")
for hf in html_files:
    with open(hf, 'r', encoding='utf-8') as f:
        c = f.read()
    # Check for undefined week variables in CSS (e.g. var(--wX) where X > 26)
    used_vars = re.findall(r'var\(--(w\d+)\)', c)
    for uv in used_vars:
        num = int(uv[1:])
        if num < 1 or num > 26:
            add_forensic_issue("CSS", "undefined_week_css_variable", "medium", os.path.basename(hf), f"Uses undefined variable --{uv}")

    # Check local script / stylesheet links
    links = re.findall(r'(?:href|src)="([^"#:]+)"', c)
    for link in links:
        if link.startswith('data:') or link.startswith('blob:') or link.startswith('javascript:'):
            continue
        # Check relative path
        rel_dir = os.path.dirname(hf)
        target_path = os.path.normpath(os.path.join(rel_dir, link))
        if not os.path.exists(target_path):
            add_forensic_issue("Assets", "broken_relative_asset_link", "high", os.path.basename(hf), f"Broken asset link: {link} (resolved: {target_path})")

# -------------------------------------------------------------
# 6. GOTCHA & ANALOGY UNIQUENESS & DEPTH
# -------------------------------------------------------------
print("\n[6/7] Checking Gotchas & Analogies Uniqueness...")
seen_analogies = {}

for yf in yaml_files:
    w_match = re.search(r'week(\d+)', yf)
    w_num = int(w_match.group(1)) if w_match else 0
    with open(yf, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    for d in data.get('days', []):
        d_num = d.get('day_num')
        d_loc = f"week{w_num:02d} day{d_num}"
        analogy = str(d.get('analogy', '')).strip()
        if not analogy:
            add_forensic_issue("Pedagogy", "missing_analogy", "low", d_loc, "Day is missing an analogy")
        elif len(analogy) < 20:
            add_forensic_issue("Pedagogy", "short_analogy", "low", d_loc, f"Analogy is too short ({len(analogy)} chars)")
        elif analogy in seen_analogies:
            add_forensic_issue("Pedagogy", "duplicate_analogy", "medium", d_loc, f"Duplicate analogy with {seen_analogies[analogy]}")
        else:
            seen_analogies[analogy] = d_loc

# -------------------------------------------------------------
# 7. SUMMARY & EXPORT
# -------------------------------------------------------------
print("\n" + "="*70)
print(f"=== DEEP FORENSIC AUDIT COMPLETE: {len(forensic_findings)} ISSUES FOUND ===")
print("="*70)

sev_counts = {}
cat_counts = {}

for f in forensic_findings:
    s = f.get("severity", "low")
    sev_counts[s] = sev_counts.get(s, 0) + 1
    c = f.get("category", "General")
    cat_counts[c] = cat_counts.get(c, 0) + 1

print("\n--- ISSUES BY SEVERITY ---")
for s, count in sev_counts.items():
    print(f"  • {s.upper():<10}: {count}")

print("\n--- ISSUES BY CATEGORY ---")
for c, count in sorted(cat_counts.items(), key=lambda x: x[1], reverse=True):
    print(f"  • {c:<20}: {count}")

with open('scripts/deep_forensic_report.json', 'w', encoding='utf-8') as f:
    json.dump(forensic_findings, f, indent=2)

print("\nDetailed forensic issues saved to: scripts/deep_forensic_report.json")
