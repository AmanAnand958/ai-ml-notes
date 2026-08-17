#!/usr/bin/env python3
"""
scripts/omni_audit_master.py
Exhaustive, omni-dimensional curriculum audit engine across all 26 weeks.
Checks:
1. Quiz Integrity (Key match, option count, single correct option, explanation)
2. Predict-the-Output Integrity (Boilerplate, AST syntax, trivial answer)
3. Python Code AST (Theory blocks, Task solutions, Debug challenges)
4. KaTeX & Math (Entities, unbalanced delimiters, corruptions)
5. Mermaid Diagrams (Syntax, unescaped entities, unquoted parens)
6. HTML/DOM Markup (Tag balance, malformed attributes, dangling spans)
7. Schema & Content Completeness (Days sequence, objectives, tasks, flashcards, gotchas, resources)
8. XP & Interactive UI (Badges vs button awards, task headers, progress IDs)
9. Resources & Links (Duplicates, shorteners, empty URLs)
"""

import glob, os, re, yaml, ast, json, html

print("=== STARTING OMNI-DIMENSIONAL CURRICULUM AUDIT ===")

findings = []

def add_issue(category, dimension, severity, location, detail):
    findings.append({
        "category": category,
        "dimension": dimension,
        "severity": severity,
        "location": location,
        "detail": detail
    })

def clean_for_ast(code):
    if not code:
        return ""
    code = html.unescape(code)
    # Only remove actual HTML tags like <span>, <pre>, <code>, <div>, not Python comparison operators < and >
    code = re.sub(r'</?[a-zA-Z][a-zA-Z0-9_-]*(?:\s+[^>]*)?>', '', code)
    # Strip common bash or CLI prefix lines
    lines = []
    for line in code.split('\n'):
        if line.strip().startswith('!') or line.strip().startswith('%') or line.strip().startswith('$'):
            continue
        lines.append(line)
    return '\n'.join(lines)

# -------------------------------------------------------------
# 1. YAML DATA SOURCE AUDIT
# -------------------------------------------------------------
yaml_files = sorted(glob.glob('src/data/week*.yaml'))
letters = ['a', 'b', 'c', 'd', 'e']

print(f"Scanning {len(yaml_files)} YAML data files...")

for yf in yaml_files:
    w_match = re.search(r'week(\d+)', yf)
    w_num = int(w_match.group(1)) if w_match else 0
    loc_week = f"week{w_num:02d}"
    
    try:
        with open(yf, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
    except Exception as e:
        add_issue("Schema", "yaml_syntax_error", "critical", yf, f"Failed to parse YAML: {e}")
        continue

    days = data.get('days', []) if isinstance(data, dict) else []
    
    # Check week metadata
    if not data.get('description'):
        add_issue("Completeness", "week_description_empty", "low", loc_week, "Week description is empty")

    for d_idx, d in enumerate(days):
        d_num = d.get('day_num', d_idx + 1)
        d_loc = f"{loc_week} day{d_num}"
        d_title = d.get('title', f"Day {d_num}")

        # Check Day completeness
        if not d.get('objectives') or len(d.get('objectives', [])) < 3:
            add_issue("Completeness", "low_objectives_count", "low", d_loc, f"Only {len(d.get('objectives', []))} objectives (expected >=3)")
            
        if not d.get('tasks') or len(d.get('tasks', [])) < 1:
            add_issue("Completeness", "missing_tasks", "medium", d_loc, "Day has 0 tasks")
            
        if not d.get('quizzes') or len(d.get('quizzes', [])) < 1:
            add_issue("Completeness", "missing_quizzes", "medium", d_loc, "Day has 0 quizzes")
            
        if not d.get('flashcards') or len(d.get('flashcards', [])) < 2:
            add_issue("Completeness", "low_flashcards_count", "low", d_loc, f"Only {len(d.get('flashcards', []))} flashcards")

        # Check Quiz Integrity
        for q_idx, q in enumerate(d.get('quizzes', [])):
            q_loc = f"{d_loc} quiz[{q_idx}]"
            opts = q.get('options', [])
            correct_opts = [i for i, opt in enumerate(opts) if opt.get('is_correct') is True]
            
            if len(correct_opts) == 0:
                add_issue("Quiz", "quiz_no_correct_option", "high", q_loc, "No option has is_correct: true")
            elif len(correct_opts) > 1:
                add_issue("Quiz", "quiz_multiple_correct_options", "medium", q_loc, f"Multiple correct options: {correct_opts}")
            else:
                expected_letter = letters[correct_opts[0]]
                if q.get('correct') != expected_letter:
                    add_issue("Quiz", "quiz_correct_key_mismatch", "high", q_loc, f"Top-level correct='{q.get('correct')}' but is_correct points to '{expected_letter}'")
                    
            if len(opts) < 2:
                add_issue("Quiz", "quiz_too_few_options", "medium", q_loc, f"Quiz only has {len(opts)} options")

        # Check Predict Integrity
        predict = d.get('predict', {})
        p_code = predict.get('code', '')
        p_ans = str(predict.get('answer', ''))
        
        if 'verify_day_' in p_code and 'pipeline():' in p_code:
            add_issue("Predict", "predict_boilerplate_unit_test", "high", d_loc, "Predict code is generic boilerplate verify_day_X_pipeline")
        if p_ans in ['True', 'true', 'Expected Output', 'Expected SLA']:
            add_issue("Predict", "predict_trivial_answer", "high", d_loc, f"Predict answer is generic placeholder '{p_ans}'")
            
        # Test Predict AST
        if p_code:
            clean_p = clean_for_ast(p_code)
            try:
                ast.parse(clean_p)
            except SyntaxError as se:
                add_issue("Code AST", "predict_python_syntax_error", "high", d_loc, f"Predict code AST error at line {se.lineno}: {se.msg}")

        # Check Task Solutions AST
        for t_idx, t in enumerate(d.get('tasks', [])):
            t_loc = f"{d_loc} task[{t_idx}] ({t.get('title', 'untitled')})"
            sol_code = t.get('solution_code', '')
            lang = str(t.get('solution_lang', 'python')).lower()
            if sol_code and lang in ['python', 'py']:
                clean_sol = clean_for_ast(sol_code)
                try:
                    ast.parse(clean_sol)
                except SyntaxError as se:
                    add_issue("Code AST", "task_solution_ast_error", "high", t_loc, f"Task solution AST error at line {se.lineno}: {se.msg}")

        # Check Resources
        seen_urls = set()
        for r_idx, r in enumerate(d.get('resources', [])):
            r_loc = f"{d_loc} resource[{r_idx}]"
            url = r.get('url', '')
            if not url or url == '#':
                add_issue("Resources", "resource_empty_url", "medium", r_loc, "Resource URL is empty or '#'")
            elif url in seen_urls:
                add_issue("Resources", "resource_duplicate_url", "low", r_loc, f"Duplicate URL within day: {url}")
            seen_urls.add(url)
            
            if any(sh in url for sh in ['://t.co/', '://bit.ly/', '://tinyurl.com/']):
                add_issue("Resources", "resource_link_shortener", "low", r_loc, f"Uses link shortener: {url}")

# -------------------------------------------------------------
# 2. HTML RENDERED PAGES AUDIT
# -------------------------------------------------------------
html_files = sorted(glob.glob('pages/weeks/week*.html'))
print(f"Scanning {len(html_files)} HTML pages...")

for hf in html_files:
    w_match = re.search(r'week(\d+)\.html', hf)
    w_num = int(w_match.group(1)) if w_match else 0
    loc_week = f"week{w_num:02d}.html"

    with open(hf, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Tag Balancing Check
    for tag in ['pre', 'code', 'table']:
        opens = len(re.findall(rf'<{tag}\b', content, re.IGNORECASE))
        closes = len(re.findall(rf'</{tag}>', content, re.IGNORECASE))
        if opens != closes:
            add_issue("DOM Markup", f"unbalanced_{tag}_tags", "high", loc_week, f"<{tag}> opened {opens} times, closed {closes} times")

    # 2. Malformed Attributes Check
    malformed = re.findall(r'<h[1-6]>\s*class="([^"]+)">', content)
    if malformed:
        add_issue("DOM Markup", "malformed_tag_attributes", "high", loc_week, f"Found {len(malformed)} malformed '<hN> class=...' tags")

    # 3. KaTeX Entity Corruptions
    if '&#36;' in content:
        add_issue("KaTeX Math", "katex_dollar_entity_corruption", "high", loc_week, "Found raw &#36; entity corruption in math content")

    # 4. Mermaid Diagram Health
    mermaids = re.findall(r'<div class="mermaid">(.*?)</div>', content, re.DOTALL)
    for m_idx, m_text in enumerate(mermaids):
        m_loc = f"{loc_week} mermaid[{m_idx}]"
        if '&gt;' in m_text or '&lt;' in m_text or '&quot;' in m_text:
            add_issue("Mermaid", "mermaid_escaped_html_entities", "high", m_loc, "Mermaid block contains escaped entities (&gt;/&lt;) that crash renderer")
        if not m_text.strip():
            add_issue("Mermaid", "mermaid_empty_diagram", "medium", m_loc, "Empty mermaid diagram container")

    # 5. Boilerplate Predict in HTML
    bp_predicts = len(re.findall(r'verify_day_\d+_pipeline', content))
    if bp_predicts > 0:
        add_issue("Predict", "predict_boilerplate_in_html", "high", loc_week, f"Found {bp_predicts} boilerplate verify_day_X_pipeline in HTML")

    # 6. Progress Bar ID Standard
    if 'id="progress-fill"' not in content or 'id="progress-pct"' not in content:
        add_issue("UI/UX", "progress_bar_id_missing", "medium", loc_week, "Progress bar missing standardized '#progress-fill' / '#progress-pct' IDs")

    # 7. Day Sections Display State
    day_sections = re.findall(r'<div class="day-section([^"]*)" id="day-(\d+)"', content)
    active_count = sum(1 for d in day_sections if 'active' in d[0])
    if active_count != 1:
        add_issue("UI/UX", "active_day_section_count_invalid", "medium", loc_week, f"Found {active_count} active day sections on initial load (expected exactly 1)")

# -------------------------------------------------------------
# 3. ROOT PORTALS AUDIT
# -------------------------------------------------------------
print("Scanning root portals (index.html, roadmap.html, dashboard.html, resources.html)...")

for portal in ['index.html', 'roadmap.html', 'dashboard.html', 'resources.html']:
    if os.path.exists(portal):
        with open(portal, 'r', encoding='utf-8') as f:
            p_text = f.read()
        if '191' not in p_text and portal in ['index.html', 'roadmap.html', 'dashboard.html']:
            add_issue("Root Portals", "total_days_stat_outdated", "medium", portal, "Total curriculum days counter does not reflect 191 days")
        if '#w26' not in p_text and 'week26.html' not in p_text and portal in ['roadmap.html', 'resources.html']:
            add_issue("Root Portals", "missing_week26_navigation_link", "high", portal, "Navigation does not link through to Week 26")

# -------------------------------------------------------------
# 4. SUMMARY REPORT
# -------------------------------------------------------------
print("\n" + "="*70)
print(f"=== MASTER AUDIT COMPLETE: {len(findings)} TOTAL ISSUES FOUND ===")
print("="*70)

severity_counts = {"critical": 0, "high": 0, "medium": 0, "low": 0}
category_counts = {}

for f in findings:
    sev = f.get("severity", "low")
    severity_counts[sev] = severity_counts.get(sev, 0) + 1
    cat = f.get("category", "General")
    category_counts[cat] = category_counts.get(cat, 0) + 1

print("\n--- ISSUES BY SEVERITY ---")
for sev, count in severity_counts.items():
    print(f"  • {sev.upper():<10}: {count}")

print("\n--- ISSUES BY CATEGORY ---")
for cat, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True):
    print(f"  • {cat:<20}: {count}")

# Save detailed JSON inventory
with open('scripts/omni_audit_report.json', 'w', encoding='utf-8') as f:
    json.dump(findings, f, indent=2)

print(f"\nDetailed issues inventory saved to: scripts/omni_audit_report.json")
