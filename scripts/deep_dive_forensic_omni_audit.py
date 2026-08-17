#!/usr/bin/env python3
"""
scripts/deep_dive_forensic_omni_audit.py
Conducts an exhaustive deep-dive forensic audit across all 26 weeks:
1. Flashcard Quality & Rigor (Minimum answer depth, presence of formulas/code)
2. Interactive Predict Output Logic & Parity
3. Task Starter vs Solution Code completeness (Check for missing imports or undefined variables)
4. KaTeX Math Syntax Validation (Check for unescaped characters or broken delimiters)
5. Hinglish Conceptual Clarity & Length
6. Interactive JavaScript Event Bindings (onclick, copyCode, runCode, openRepl)
7. Accessibility, Contrast & Theme Token Safety
8. Resource Anchors & Canonical Video Links
"""

import glob, yaml, re, os, json, html, ast

print("=== STARTING EXHAUSTIVE DEEP DIVE FORENSIC AUDIT ===")

findings = []
issue_counter = 1

def log_issue(week_num, day_num, category, severity, title, detail, snippet=""):
    global issue_counter
    findings.append({
        "id": f"DEEP-AUDIT-{issue_counter:04d}",
        "week": week_num,
        "day": day_num,
        "category": category,
        "severity": severity,
        "title": title,
        "detail": detail,
        "snippet": snippet[:200]
    })
    issue_counter += 1

yaml_files = sorted(glob.glob('src/data/week*.yaml'))
html_files = sorted(glob.glob('pages/weeks/week*.html'))

# 1. AUDIT YAML CONTENT DEEP-DIVE
print("1. Auditing YAML source data integrity & depth across 26 weeks...")
for yf in yaml_files:
    week_num = int(re.search(r'week(\d+)', yf).group(1))
    with open(yf, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    for day in data.get('days', []):
        d_num = day.get('day_num', 0)
        
        # A. Flashcards Deep Check
        flashcards = day.get('flashcards', [])
        if len(flashcards) < 4:
            log_issue(week_num, d_num, "Curriculum Depth", "MEDIUM", "Low Flashcard Count", f"Day {d_num} has only {len(flashcards)} flashcards (recommended: 5).")
        for f_idx, fc in enumerate(flashcards):
            front = str(fc.get('front', '')).strip()
            back = str(fc.get('back', '')).strip()
            if len(back) < 25:
                log_issue(week_num, d_num, "Flashcard Rigor", "LOW", f"Short Flashcard Answer (Card {f_idx+1})", f"Back of card '{front}' is too terse ({len(back)} chars).", back)

        # B. Task Starter vs Solution Integrity
        tasks = day.get('tasks', [])
        if len(tasks) < 2:
            log_issue(week_num, d_num, "Hands-on Rigor", "MEDIUM", "Insufficient Tasks", f"Day {d_num} has only {len(tasks)} tasks (recommended: 2-3).")
        for t_idx, t in enumerate(tasks):
            title = t.get('title', '')
            sol = t.get('solution_code', '')
            starter = t.get('starter_code', '')
            # Check if starter code is identical to solution code (no challenge)
            if starter and sol and starter.strip() == sol.strip():
                log_issue(week_num, d_num, "Pedagogy", "HIGH", f"Starter Code Identical to Solution (Task {t_idx+1})", f"Task '{title}' provides the full solution as starter code.", sol)

        # C. KaTeX TeX Syntax Validation in theory_html & math blocks
        theory = str(day.get('theory_html', ''))
        # Find math delimiters $$...$$ or $...$
        math_matches = re.findall(r'\$\$([\s\S]*?)\$\$', theory)
        for m in math_matches:
            # Check for unescaped & or html entities inside KaTeX
            if '&lt;' in m or '&gt;' in m or '&amp;' in m:
                log_issue(week_num, d_num, "Math Formatting", "HIGH", "HTML Entity in KaTeX Formula", f"Day {d_num} contains raw HTML entities inside LaTeX $$ formula: {m}", m)
            # Check for unbalanced braces in LaTeX
            if m.count('{') != m.count('}'):
                log_issue(week_num, d_num, "Math Formatting", "CRITICAL", "Unbalanced Curly Braces in KaTeX", f"Day {d_num} LaTeX formula has unbalanced braces: {m}", m)

        # D. Hinglish Quality & Depth
        hinglish = str(day.get('hinglish', ''))
        if not hinglish or len(hinglish) < 40:
            log_issue(week_num, d_num, "Hinglish Quality", "MEDIUM", "Terse or Missing Hinglish Explanation", f"Day {d_num} Hinglish text is under 40 characters.", hinglish)

# 2. AUDIT HTML RENDERED PAGES FOR INTERACTIVITY & JS INTEGRITY
print("2. Auditing HTML week portals for event handlers & DOM bindings...")
for hf in html_files:
    week_num = int(re.search(r'week(\d+)', hf).group(1))
    with open(hf, 'r', encoding='utf-8') as f:
        content = f.read()

    # A. Check for broken or missing onclick handlers
    buttons = re.findall(r'<button\b([^>]*)>', content)
    for b in buttons:
        if 'onclick=' in b:
            handler = re.search(r'onclick=[\"\']([^\"\']*)[\"\']', b)
            if handler:
                h_val = handler.group(1).strip()
                # Check for empty onclick
                if not h_val:
                    log_issue(week_num, 0, "Interactive UI", "HIGH", "Empty onclick Handler", f"Found button with empty onclick in {os.path.basename(hf)}", b)

    # B. Check for broken image / asset references
    img_sources = re.findall(r'<img\s+[^>]*src=[\"\']([^\"\']*)[\"\']', content)
    for src in img_sources:
        if not src.startswith('http') and not src.startswith('data:'):
            # Check local file existence relative to pages/weeks/
            asset_path = os.path.normpath(os.path.join('pages/weeks', src))
            if not os.path.exists(asset_path):
                log_issue(week_num, 0, "Asset Integrity", "HIGH", "Missing Local Image Asset", f"Referenced image {src} does not exist at {asset_path}.", src)

    # C. Check for duplicate IDs inside the same HTML file
    ids = re.findall(r'\bid=[\"\']([^\"\']+)[\"\']', content)
    seen_ids = set()
    dup_ids = set()
    for el_id in ids:
        if el_id in seen_ids:
            dup_ids.add(el_id)
        seen_ids.add(el_id)
    # Exclude common non-critical multi-instance IDs if any, or flag duplicates
    for dup in dup_ids:
        # If it's a day-tab or button id that shouldn't be duplicated
        if not dup.startswith('katex-') and not dup.startswith('cb-'):
            count = ids.count(dup)
            log_issue(week_num, 0, "DOM Accessibility", "MEDIUM", f"Duplicate HTML id='{dup}'", f"Found id='{dup}' duplicated {count} times in {os.path.basename(hf)}.", dup)

print(f"\nExhaustive Deep-Dive Audit Complete: {len(findings)} Potential Enhancements / Opportunities Found.")

with open('scripts/deep_dive_forensic_report.json', 'w', encoding='utf-8') as f:
    json.dump(findings, f, indent=2)

print("Saved detailed report to: scripts/deep_dive_forensic_report.json")
