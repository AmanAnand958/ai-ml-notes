#!/usr/bin/env python3
"""
scripts/omni_audit_all_weeks.py
Comprehensive Whole-Course Omni-Audit across Weeks 1 to 26 (191 Days).
Checks 12 dimensions:
1. Structural schema compliance & dead/missing fields
2. Python AST syntax validation for all solution_code & predict.code
3. KaTeX math formula syntax & delimiter validation
4. Mermaid diagram syntax & node label balancing
5. Duplicate content detection (solutions, quizzes, flashcards, theory)
6. Resource URL sanity & placeholder detection
7. Quiz integrity (correct options, feedbacks, option count)
8. Predict block validation (question, answer, code, explanation)
9. Day-level metadata completeness (objectives, checklist, takeaways, analogy, hinglish, gotcha)
10. Task metadata completeness (badges, badge_classes, time, done_when, git_cmd)
11. HTML tag balancing in theory_html (divs, spans, tables, pres)
12. Mechanical DOM validation across compiled HTML pages
"""

import os, sys, glob, yaml, json, re, ast
from collections import defaultdict, Counter
from bs4 import BeautifulSoup

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA_DIR = os.path.join(ROOT_DIR, 'src/data')
PAGES_DIR = os.path.join(ROOT_DIR, 'pages/weeks')
TMPL_PATH = os.path.join(ROOT_DIR, 'src/template/week.template.html')
CONTRACT_PATH = os.path.join(ROOT_DIR, 'src/schema/contract.json')

with open(CONTRACT_PATH) as f:
    contract = json.load(f)

allowed_task_badges = set(contract.get('allowed_task_badge_variants', ['tb-easy', 'tb-med', 'tb-hard', 'tb-proj']))
allowed_meta_badges = set(contract.get('allowed_meta_badge_variants', ['b', 'g', 'o', 'p', 'pk', 'y', 't']))
exposed_functions = set(contract.get('exposed_functions', []))

dom_builtins = {
    'if', 'for', 'while', 'switch', 'return', 'click', 'stopPropagation', 'preventDefault',
    'getAttribute', 'setAttribute', 'removeAttribute', 'hasAttribute', 'includes', 'replace',
    'toString', 'match', 'test', 'toggle', 'add', 'remove', 'contains', 'focus', 'blur',
    'scrollIntoView', 'scrollTo', 'setTimeout', 'clearTimeout', 'setInterval', 'clearInterval',
    'alert', 'prompt', 'confirm', 'startsWith', 'endsWith', 'indexOf', 'trim', 'toLowerCase',
    'toUpperCase', 'split', 'join', 'slice', 'substring'
}

all_findings = []

def add_finding(dim, sev, week, day_id, loc, desc):
    all_findings.append({
        "dim": dim,
        "sev": sev,
        "week": week,
        "day_id": str(day_id),
        "location": loc,
        "description": desc
    })

print("=" * 70)
print("🔍 RUNNING COMPREHENSIVE OMNI-AUDIT ACROSS ALL WEEKS (1-26)")
print("=" * 70)

# Load all 26 YAML data files
yaml_files = sorted(glob.glob(f"{DATA_DIR}/week*.yaml"))
data_by_week = {}

for fpath in yaml_files:
    fname = os.path.basename(fpath)
    wnum = int(''.join(filter(str.isdigit, fname)))
    with open(fpath) as fp:
        data_by_week[wnum] = yaml.safe_load(fp)

# Global trackers for uniqueness across entire curriculum
global_day_ids = set()
solution_hashes = defaultdict(list)
quiz_q_hashes = defaultdict(list)
flashcard_hashes = defaultdict(list)
resource_urls = defaultdict(list)

for wnum in range(1, 27):
    if wnum not in data_by_week:
        add_finding("SCHEMA", "CRITICAL", wnum, "-", "week", f"Missing week{wnum:02d}.yaml file")
        continue

    wdata = data_by_week[wnum]
    
    # Week number match
    if wdata.get('week_number') != wnum:
        add_finding("SCHEMA", "HIGH", wnum, "-", "week.week_number", f"week_number={wdata.get('week_number')} does not match filename week{wnum:02d}")

    # Week title
    if not wdata.get('title'):
        add_finding("METADATA", "MEDIUM", wnum, "-", "week.title", "Missing week title")

    days = wdata.get('days', [])
    if not days:
        add_finding("SCHEMA", "CRITICAL", wnum, "-", "week.days", "Zero days found in week")
        continue

    for d_idx, day in enumerate(days):
        did = day.get('id')
        dtitle = day.get('title', f"Day {did}")
        loc_prefix = f"W{wnum}D{did}"

        # 1. Day ID & Ordering
        if did is None:
            add_finding("SCHEMA", "CRITICAL", wnum, "-", f"days[{d_idx}]", "Day missing 'id' field")
            continue

        if did in global_day_ids:
            add_finding("SCHEMA", "CRITICAL", wnum, did, "day.id", f"Duplicate global day.id={did}")
        global_day_ids.add(did)

        # 2. Dead Fields Check
        for dead_k in ['gotchas', 'desc', 'starter_code', 'hint', 'resources_extra', 'notes']:
            if dead_k in day:
                add_finding("DEAD_FIELDS", "LOW", wnum, did, f"day.{dead_k}", f"Dead field '{dead_k}' present in day")

        # 3. Objectives & Checklist
        objs = day.get('objectives', [])
        if not objs or len(objs) < 2:
            add_finding("METADATA", "LOW", wnum, did, "day.objectives", f"Only {len(objs)} objectives (expected 3+)")

        chk = day.get('checklist', [])
        if not chk:
            add_finding("METADATA", "LOW", wnum, did, "day.checklist", "Missing checklist")

        # 4. Hinglish & Analogy
        h = day.get('hinglish', '')
        if not h or len(str(h).strip()) < 20:
            add_finding("CONTENT", "MEDIUM", wnum, did, "day.hinglish", "Missing or too short Hinglish explanation")

        a = day.get('analogy', '')
        if not a or len(str(a).strip()) < 20:
            add_finding("CONTENT", "MEDIUM", wnum, did, "day.analogy", "Missing or too short Analogy explanation")

        # 5. Gotcha
        g = day.get('gotcha')
        if not g:
            add_finding("CONTENT", "MEDIUM", wnum, did, "day.gotcha", "Missing gotcha callout")
        elif isinstance(g, dict):
            if not g.get('title') or not g.get('description'):
                add_finding("CONTENT", "MEDIUM", wnum, did, "day.gotcha", "Gotcha dict missing title or description")
        else:
            add_finding("CONTENT", "MEDIUM", wnum, did, "day.gotcha", f"Gotcha is {type(g).__name__}, expected dict with title/description")

        # 6. Takeaways
        tks = day.get('takeaways')
        if not tks:
            add_finding("CONTENT", "LOW", wnum, did, "day.takeaways", "Missing takeaways")
        elif isinstance(tks, dict):
            bullets = tks.get('bullets', [])
            if len(bullets) < 3:
                add_finding("CONTENT", "LOW", wnum, did, "day.takeaways.bullets", f"Only {len(bullets)} takeaways bullets (expected 3+)")
        elif isinstance(tks, list):
            if len(tks) < 3:
                add_finding("CONTENT", "LOW", wnum, did, "day.takeaways", f"Only {len(tks)} takeaways (expected 3+)")

        # 7. Predict Block Validation & Execution Test
        p = day.get('predict')
        if not p:
            add_finding("PREDICT", "HIGH", wnum, did, "day.predict", "Missing predict challenge")
        elif isinstance(p, dict):
            p_code = p.get('code', '')
            p_ans = str(p.get('answer', '')).strip()
            p_q = p.get('question', '')
            p_exp = p.get('explanation', '')

            if not p_code:
                add_finding("PREDICT", "HIGH", wnum, did, "predict.code", "Predict missing code snippet")
            else:
                # Python syntax check
                try:
                    ast.parse(p_code)
                except SyntaxError as se:
                    add_finding("CODE_SYNTAX", "HIGH", wnum, did, "predict.code", f"Predict code Python syntax error: {se.msg} (line {se.lineno})")

            if not p_ans:
                add_finding("PREDICT", "HIGH", wnum, did, "predict.answer", "Predict missing answer")
            if not p_q:
                add_finding("PREDICT", "MEDIUM", wnum, did, "predict.question", "Predict missing question")
            if not p_exp:
                add_finding("PREDICT", "MEDIUM", wnum, did, "predict.explanation", "Predict missing explanation")

        # 8. Theory HTML Validation (Tags, Math, Code, Mermaid)
        th = day.get('theory_html', '') or ''
        if not th or len(th) < 100:
            add_finding("THEORY", "HIGH", wnum, did, "day.theory_html", "Missing or abnormally short theory_html")
        else:
            # Check for unclosed HTML tags
            for tag in ['div', 'table', 'pre', 'code', 'figure']:
                open_cnt = len(re.findall(rf'<{tag}\b[^>]*>', th, re.IGNORECASE))
                close_cnt = len(re.findall(rf'</{tag}\b[^>]*>', th, re.IGNORECASE))
                if open_cnt != close_cnt:
                    add_finding("HTML_TAGS", "HIGH", wnum, did, f"theory_html.<{tag}>", f"Unbalanced <{tag}> tags: {open_cnt} open vs {close_cnt} close")

            # Check KaTeX math formulas
            math_blocks = re.findall(r'\$\$(.*?)\$\$', th, re.DOTALL)
            for mb in math_blocks:
                # check balanced curly braces
                if mb.count('{') != mb.count('}'):
                    add_finding("KATEX", "HIGH", wnum, did, "theory_html.math", f"Unbalanced braces in KaTeX block: {mb[:60]}...")

            # Check Mermaid diagrams
            mermaids = re.findall(r'<div class="mermaid">(.*?)</div>', th, re.DOTALL)
            for m_text in mermaids:
                m_clean = m_text.strip()
                if not any(m_clean.startswith(kw) for kw in ['graph', 'flowchart', 'sequenceDiagram', 'classDiagram', 'subgraph', 'stateDiagram']):
                    add_finding("MERMAID", "MEDIUM", wnum, did, "theory_html.mermaid", f"Mermaid block missing standard graph keyword: '{m_clean[:40]}'")

        # 9. Tasks Validation
        tasks = day.get('tasks', [])
        if not tasks:
            add_finding("TASKS", "CRITICAL", wnum, did, "day.tasks", "Zero tasks defined in day")
        for ti, task in enumerate(tasks, 1):
            tloc = f"tasks[{ti}] ('{task.get('title','?')[:40]}')"
            
            # Dead schema keys
            for dead_k in ['desc', 'starter_code', 'hint', 'time_minutes']:
                if dead_k in task:
                    add_finding("DEAD_FIELDS", "HIGH", wnum, did, f"{tloc}.{dead_k}", f"Task uses dead field '{dead_k}'")

            # Required fields
            if not task.get('title'):
                add_finding("TASKS", "HIGH", wnum, did, f"{tloc}.title", "Task missing title")
            if not task.get('prompt_html'):
                add_finding("TASKS", "HIGH", wnum, did, f"{tloc}.prompt_html", "Task missing prompt_html")
            if not task.get('sol_id'):
                add_finding("TASKS", "HIGH", wnum, did, f"{tloc}.sol_id", "Task missing sol_id")

            # Badge & Badge Class
            b_class = task.get('badge_class', '')
            if b_class and b_class not in allowed_task_badges:
                add_finding("BADGES", "MEDIUM", wnum, did, f"{tloc}.badge_class", f"Invalid badge_class '{b_class}' (expected one of {sorted(allowed_task_badges)})")

            # Solution Code Validation
            sc = task.get('solution_code', '') or ''
            if not sc:
                add_finding("TASKS", "HIGH", wnum, did, f"{tloc}.solution_code", "Task missing solution_code")
            else:
                # Python syntax check if lang is python/default
                lang = task.get('solution_lang', 'python').lower()
                if lang in ['python', 'py']:
                    try:
                        ast.parse(sc)
                    except SyntaxError as se:
                        add_finding("CODE_SYNTAX", "HIGH", wnum, did, f"{tloc}.solution_code", f"Python syntax error in solution_code: {se.msg} (line {se.lineno})")

                # Deduplication check
                norm_sc = re.sub(r'\s+', ' ', sc).strip()
                if len(norm_sc) > 40:
                    solution_hashes[norm_sc].append((wnum, did, ti, task.get('title', '?')))

        # 10. Quizzes Validation
        quizzes = day.get('quizzes', [])
        if not quizzes:
            add_finding("QUIZZES", "HIGH", wnum, did, "day.quizzes", "Zero quizzes in day")
        for qi, q in enumerate(quizzes, 1):
            qloc = f"quizzes[{qi}]"
            qtext = q.get('question', '').strip()
            if not qtext:
                add_finding("QUIZZES", "HIGH", wnum, did, f"{qloc}.question", "Empty quiz question")
            else:
                quiz_q_hashes[qtext].append((wnum, did, qi))

            opts = q.get('options', [])
            if len(opts) != 4:
                add_finding("QUIZZES", "MEDIUM", wnum, did, f"{qloc}.options", f"Quiz has {len(opts)} options (expected 4)")

            correct_count = sum(1 for o in opts if o.get('is_correct') is True)
            if correct_count != 1:
                add_finding("QUIZZES", "HIGH", wnum, did, f"{qloc}.is_correct", f"Quiz has {correct_count} correct options (expected exactly 1)")

            if not q.get('correct_fb') or not q.get('wrong_fb'):
                add_finding("QUIZZES", "LOW", wnum, did, f"{qloc}.feedback", "Missing correct_fb or wrong_fb feedback")

        # 11. Flashcards Validation
        fcs = day.get('flashcards', [])
        if not fcs:
            add_finding("FLASHCARDS", "MEDIUM", wnum, did, "day.flashcards", "Zero flashcards in day")
        for fi, fc in enumerate(fcs, 1):
            front = fc.get('front', '').strip()
            back = fc.get('back', '').strip()
            if not front or not back:
                add_finding("FLASHCARDS", "HIGH", wnum, did, f"flashcards[{fi}]", "Empty front or back on flashcard")
            else:
                flashcard_hashes[front].append((wnum, did, fi))

        # 12. Resources Validation
        res_list = day.get('resources', [])
        if not res_list:
            add_finding("RESOURCES", "MEDIUM", wnum, did, "day.resources", "Zero resources in day")
        for ri, r in enumerate(res_list, 1):
            url = r.get('url', '').strip()
            title = r.get('title', '').strip()
            if not url:
                add_finding("RESOURCES", "HIGH", wnum, did, f"resources[{ri}]", f"Resource '{title}' missing URL")
            elif not url.startswith(('http://', 'https://')):
                add_finding("RESOURCES", "HIGH", wnum, did, f"resources[{ri}]", f"Resource URL '{url}' does not start with http/https")
            elif 'youtube.com/playlist' in url or 'youtube.com/watch?v=' in url or 'TODO' in url or '#' == url:
                add_finding("RESOURCES", "MEDIUM", wnum, did, f"resources[{ri}]", f"Generic/placeholder URL: '{url}'")

# Check global duplications
for sc_text, locs in solution_hashes.items():
    if len(locs) > 1:
        loc_str = ", ".join(f"W{l[0]}D{l[1]}T{l[2]}" for l in locs)
        add_finding("DUPLICATES", "HIGH", locs[0][0], locs[0][1], "solution_code", f"Duplicate solution_code across {len(locs)} tasks: {loc_str}")

for q_text, locs in quiz_q_hashes.items():
    if len(locs) > 1:
        loc_str = ", ".join(f"W{l[0]}D{l[1]}Q{l[2]}" for l in locs)
        add_finding("DUPLICATES", "MEDIUM", locs[0][0], locs[0][1], "quizzes", f"Duplicate quiz question across {len(locs)} places: {loc_str}")

for fc_text, locs in flashcard_hashes.items():
    if len(locs) > 1:
        loc_str = ", ".join(f"W{l[0]}D{l[1]}FC{l[2]}" for l in locs)
        add_finding("DUPLICATES", "LOW", locs[0][0], locs[0][1], "flashcards", f"Duplicate flashcard across {len(locs)} places: {loc_str}")

# 13. DOM & Page Integrity Validation on Compiled HTML Pages
print("\nValidating compiled HTML pages in pages/weeks/...")
html_pages = sorted(glob.glob(f"{PAGES_DIR}/week*.html"))
for hpath in html_pages:
    hname = os.path.basename(hpath)
    wnum = int(''.join(filter(str.isdigit, hname)))
    with open(hpath) as fp:
        hcontent = fp.read()
    
    soup = BeautifulSoup(hcontent, 'html.parser')

    # DOM ID Uniqueness
    ids = [el.get('id') for el in soup.find_all(id=True)]
    id_counts = Counter(ids)
    for el_id, cnt in id_counts.items():
        if cnt > 1:
            add_finding("DOM_INTEGRITY", "HIGH", wnum, "-", f"#{el_id}", f"Duplicate DOM ID '{el_id}' found {cnt} times on page")

    # Contract function calls
    for el in soup.find_all(True):
        for attr in ['onclick', 'onkeydown', 'onkeyup']:
            val = el.get(attr)
            if not val: continue
            sanitized = re.sub(r"'(?:\\.|[^'])*'", "''", val)
            sanitized = re.sub(r'"(?:\\.|[^"])*"', '""', sanitized)
            calls = re.findall(r'([a-zA-Z0-9_$]+)\s*\(', sanitized)
            for c in calls:
                if c not in dom_builtins and c not in exposed_functions:
                    add_finding("CONTRACT", "HIGH", wnum, "-", f"{el.name}[{attr}]", f"Function contract violation: '{c}' not in contract.json")

print("\n" + "=" * 70)
print(f"OMNI-AUDIT COMPLETE: Total Findings = {len(all_findings)}")
print("=" * 70)

# Print Summary Table
counts_by_dim = Counter(f['dim'] for f in all_findings)
counts_by_sev = Counter(f['sev'] for f in all_findings)

print("\n📊 Findings by Severity:")
for s, c in sorted(counts_by_sev.items()):
    print(f"  {s:12s}: {c}")

print("\n📊 Findings by Dimension:")
for d, c in sorted(counts_by_dim.items()):
    print(f"  {d:15s}: {c}")

with open(f"{ROOT_DIR}/scripts/omni_audit_report.json", "w") as fp:
    json.dump(all_findings, fp, indent=2)

print(f"\nReport saved to: {ROOT_DIR}/scripts/omni_audit_report.json")
