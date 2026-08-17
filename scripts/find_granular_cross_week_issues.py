#!/usr/bin/env python3
"""
scripts/find_granular_cross_week_issues.py
Deep static inspection across 7 specialized cross-week dimensions:
1. Code Container Ergonomics (.cb wrapper, .cb-head, language tag, copy/run buttons)
2. Mobile Responsiveness & Table Wrappers (<div class="table-wrap"> on tables)
3. Concept Flow vs H3 Heading Synchronization (YAML concept_flow vs theory_html headings)
4. Task Deliverables & Time Estimation (done_when completeness, time_minutes presence)
5. Quiz Answer Letter Distribution & Typographical Consistency (Option casing, trailing punctuation)
6. Flashcard Formatting & Question Syntax (Front question mark, formatting parity)
7. SVG & Canvas Accessibility Attributes (aria-label, role="img", viewBox, canvas fallback)
"""

import glob, yaml, re, os, json, html

print("=== STARTING GRANULAR CROSS-WEEK AUDIT ===")

findings = []
issue_id = 1

def add_issue(dimension, severity, location, title, problem, evidence, recommendation):
    global issue_id
    findings.append({
        "id": f"XWEEK-{issue_id:03d}",
        "dimension": dimension,
        "severity": severity,
        "location": location,
        "title": title,
        "problem": problem,
        "evidence": str(evidence)[:250],
        "recommendation": recommendation
    })
    issue_id += 1

yaml_files = sorted(glob.glob('src/data/week*.yaml'))
html_files = sorted(glob.glob('pages/weeks/week*.html'))

# -------------------------------------------------------------
# 1. CODE CONTAINER ERGONOMICS (<div class="cb">, buttons, language tags)
# -------------------------------------------------------------
print("1. Auditing Code Container Ergonomics...")
for hf in html_files:
    w_name = os.path.basename(hf)
    with open(hf, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Find all <pre> tags and check if they are inside a <div class="cb">
    # Search for naked <pre> not immediately preceded by <div class="cb">
    pres = re.findall(r'(<pre\b[^>]*>.*?<\/pre>)', content, re.DOTALL)
    cb_count = len(re.findall(r'<div class="cb"', content))
    pre_count = len(pres)
    
    # Check if there are code blocks missing copy/run headers
    naked_pres = re.findall(r'(?<!<div class="cb-head">)\s*<pre><code>', content)
    if pre_count > cb_count + 15: # allow predict/solution custom pres
        add_issue(
            "Code Ergonomics",
            "Medium",
            w_name,
            "Unwrapped / Naked `<pre>` Elements Missing `.cb` Container",
            f"Page has {pre_count} `<pre>` blocks but only {cb_count} standard `.cb` code containers.",
            f"Pre count: {pre_count}, .cb container count: {cb_count}",
            "Wrap raw code snippets in `<div class=\"cb\"><div class=\"cb-head\"><span class=\"cb-lang\">...</span><button class=\"copy-btn\">copy</button></div><pre><code>...</code></pre></div>`."
        )

# -------------------------------------------------------------
# 2. MOBILE RESPONSIVENESS & TABLE WRAPPERS
# -------------------------------------------------------------
print("2. Auditing Table Mobile Responsive Wrappers...")
for hf in html_files:
    w_name = os.path.basename(hf)
    with open(hf, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Find tables not inside <div class="table-wrap">
    tables = re.findall(r'<table\b', content, re.IGNORECASE)
    table_wraps = re.findall(r'<div class="table-wrap"', content, re.IGNORECASE)
    
    if len(tables) > len(table_wraps):
        add_issue(
            "Mobile Layout",
            "Medium",
            w_name,
            "Unwrapped `<table>` Elements Prone to Mobile Horizontal Cutoff",
            f"Found {len(tables)} tables but only {len(table_wraps)} wrapped in `<div class=\"table-wrap\">` (overflow-x container).",
            f"Tables: {len(tables)}, Wrappers: {len(table_wraps)}",
            "Wrap all standalone `<table>` elements in `<div class=\"table-wrap\" style=\"overflow-x:auto;\">` to prevent mobile layout breaking."
        )

# -------------------------------------------------------------
# 3. CONCEPT FLOW VS H3 HEADINGS SYNCHRONIZATION
# -------------------------------------------------------------
print("3. Auditing YAML Concept Flow vs Theory Headings...")
for yf in yaml_files:
    w_match = re.search(r'week(\d+)', yf)
    w_num = int(w_match.group(1)) if w_match else 0
    with open(yf, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
        
    for d in data.get('days', []):
        d_num = d.get('day_num', 0)
        d_title = d.get('title', f"Day {d_num}")
        d_loc = f"Week {w_num:02d} / Day {d_num:03d} ({d_title})"
        
        flow = d.get('concept_flow', [])
        theory = d.get('theory_html', '')
        
        # Extract all H3 headings from theory
        h3s = re.findall(r'<h3[^>]*>(.*?)</h3>', theory, re.DOTALL)
        clean_h3s = [re.sub(r'^\s*\d+\.\s*', '', re.sub(r'<[^>]+>', '', h)).strip().lower() for h in h3s]
        
        if not flow and len(h3s) > 1:
            add_issue(
                "Curriculum Schema",
                "Low",
                d_loc,
                "Missing YAML `concept_flow` Array",
                "Day defines multiple theoretical subsections but has an empty `concept_flow` array.",
                f"Headings count: {len(h3s)}, concept_flow: {flow}",
                "Populate `concept_flow` with the ordered sequence of learning checkpoints."
            )

# -------------------------------------------------------------
# 4. TASK DELIVERABLES & TIME ESTIMATION AUDIT
# -------------------------------------------------------------
print("4. Auditing Task Verification Criteria & Time Estimates...")
for yf in yaml_files:
    w_match = re.search(r'week(\d+)', yf)
    w_num = int(w_match.group(1)) if w_match else 0
    with open(yf, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
        
    for d in data.get('days', []):
        d_num = d.get('day_num', 0)
        d_title = d.get('title', f"Day {d_num}")
        d_loc = f"Week {w_num:02d} / Day {d_num:03d} ({d_title})"
        
        for t_idx, t in enumerate(d.get('tasks', [])):
            t_title = t.get('title', f"Task {t_idx+1}")
            t_loc = f"{d_loc} -> Task #{t_idx+1} ({t_title})"
            
            # Check for time_minutes estimate
            if not t.get('time_minutes') and not t.get('estimated_minutes'):
                add_issue(
                    "Task Ergonomics",
                    "Low",
                    t_loc,
                    "Task Missing Estimated Completion Time (`time_minutes`)",
                    "Task does not specify an estimated completion time for student planning.",
                    f"Task keys: {list(t.keys())}",
                    "Add `time_minutes: 30` (or appropriate duration estimate) to task metadata."
                )

            # Check for empty or missing done_when
            done_when = t.get('done_when', [])
            if not done_when or len(done_when) == 0:
                add_issue(
                    "Task Verifiability",
                    "Medium",
                    t_loc,
                    "Task Missing Explicit `done_when` Completion Checklist",
                    "Task does not provide actionable self-evaluation criteria for students.",
                    f"done_when: {done_when}",
                    "Add 2-3 specific verification criteria (e.g. 'Model achieves F1 > 0.85', 'Unit tests pass without warning')."
                )

# -------------------------------------------------------------
# 5. QUIZ ANSWER OPTION DISTRIBUTION & TYPOGRAPHY
# -------------------------------------------------------------
print("5. Auditing Quiz Option Distribution & Punctuation...")
quiz_letters = {'a': 0, 'b': 0, 'c': 0, 'd': 0, 'e': 0}

for yf in yaml_files:
    w_match = re.search(r'week(\d+)', yf)
    w_num = int(w_match.group(1)) if w_match else 0
    with open(yf, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
        
    for d in data.get('days', []):
        d_num = d.get('day_num', 0)
        d_title = d.get('title', f"Day {d_num}")
        d_loc = f"Week {w_num:02d} / Day {d_num:03d} ({d_title})"
        
        for q_idx, q in enumerate(d.get('quizzes', [])):
            corr = str(q.get('correct', '')).lower()
            if corr in quiz_letters:
                quiz_letters[corr] += 1
            
            opts = q.get('options', [])
            # Check for trailing period inconsistency across options within same quiz
            has_period = [str(o.get('text', '')).endswith('.') for o in opts]
            if any(has_period) and not all(has_period):
                add_issue(
                    "Quiz Typography",
                    "Low",
                    f"{d_loc} -> Quiz #{q_idx+1}",
                    "Inconsistent Trailing Punctuation in Quiz Options",
                    "Some options end with a period while others do not within the same question.",
                    f"Option texts: {[o.get('text') for o in opts]}",
                    "Standardize option typography (e.g., remove trailing periods from all single-clause options)."
                )

# -------------------------------------------------------------
# 6. FLASHCARD QUESTION SYNTAX & PUNCTUATION
# -------------------------------------------------------------
print("6. Auditing Flashcard Question Syntax...")
for yf in yaml_files:
    w_match = re.search(r'week(\d+)', yf)
    w_num = int(w_match.group(1)) if w_match else 0
    with open(yf, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
        
    for d in data.get('days', []):
        d_num = d.get('day_num', 0)
        d_title = d.get('title', f"Day {d_num}")
        d_loc = f"Week {w_num:02d} / Day {d_num:03d} ({d_title})"
        
        for f_idx, fc in enumerate(d.get('flashcards', [])):
            front = str(fc.get('front', '')).strip()
            # If front looks like a question but lacks '?'
            if any(front.lower().startswith(w) for w in ['what', 'why', 'how', 'when', 'which', 'explain']) and not front.endswith('?'):
                add_issue(
                    "Flashcard Typography",
                    "Low",
                    f"{d_loc} -> Flashcard #{f_idx+1}",
                    "Flashcard Question Missing Trailing Question Mark ('?')",
                    "Flashcard prompt begins with an interrogative word but lacks a trailing question mark.",
                    f"Front: '{front}'",
                    "Append '?' to standardize active recall prompts."
                )

# -------------------------------------------------------------
# 7. SVG & CANVAS ACCESSIBILITY ATTRIBUTES
# -------------------------------------------------------------
print("7. Auditing SVG & Canvas Accessibility Attributes...")
for hf in html_files:
    w_name = os.path.basename(hf)
    with open(hf, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Check SVGs missing aria-label or role="img"
    svgs = re.findall(r'<svg\b([^>]*)>', content, re.IGNORECASE)
    for s_idx, svg_attrs in enumerate(svgs):
        if 'aria-label' not in svg_attrs and 'aria-labelledby' not in svg_attrs:
            add_issue(
                "Accessibility",
                "Low",
                f"{w_name} -> SVG #{s_idx+1}",
                "SVG Element Missing Accessible `aria-label`",
                "Inline SVG diagram lacks accessibility label for screen readers.",
                f"Attributes: {svg_attrs[:100]}",
                "Add `aria-label=\"Description of diagram\"` and `role=\"img\"`."
            )
            
    # Check Canvas missing fallback content
    canvases = re.findall(r'<canvas\b([^>]*)>(.*?)</canvas>', content, re.DOTALL | re.IGNORECASE)
    for c_idx, (c_attrs, c_inner) in enumerate(canvases):
        if not c_inner.strip():
            add_issue(
                "Accessibility",
                "Low",
                f"{w_name} -> Canvas #{c_idx+1}",
                "Canvas Element Missing Screen Reader Fallback Text",
                "Interactive `<canvas>` lacks text inside container for non-canvas browsers.",
                f"Attributes: {c_attrs[:100]}",
                "Insert `<p>Interactive simulation showing [topic]. Your browser does not support canvas.</p>` inside `<canvas>`."
            )

print(f"\nTotal Cross-Week Granular Issues Discovered: {len(findings)}")

with open('scripts/granular_cross_week_issues.json', 'w', encoding='utf-8') as f:
    json.dump(findings, f, indent=2)

print("Exported findings to: scripts/granular_cross_week_issues.json")
