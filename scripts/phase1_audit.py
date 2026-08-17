#!/usr/bin/env python3
"""
Phase 1 Audit Script — 191-Day AI/ML Course
============================================
READ-ONLY. Produces a structured findings report.
Does NOT modify any files.

Checks:
  KNOWN ISSUES (confirm + count):
    K1  theory_html boilerplate (enterprise scale opener, LatencyPenalty formula,
        3-row trade-off table, generic mermaid, TopicEngine class)
    K2  Tasks with wrong schema (desc/starter_code/hint instead of prompt_html/sol_id/done_when/git_cmd)
    K3  Generic RandomForest solution_code boilerplate
    K4  Duplicate concept-flow callout embedded inside theory_html
    K5  Generic/placeholder done_when / git_cmd text
    K6  week25 day184 near-duplicate capstone tasks
    K7  badge_class / meta-badge variant mismatches vs contract.json

  UNKNOWN ISSUES (discovery):
    U1  Missing required fields (schema compliance, per-section null/empty checks)
    U2  Dead data — fields present in YAML never read by template
    U3  Broken rendering — template variables the data never provides
    U4  Quiz integrity (exactly one is_correct, no duplicates, no empty)
    U5  Resource URL sanity
    U6  XP value sanity
    U7  day.id / day_num uniqueness and sequential ordering
    U8  week_number matches filename
    U9  Hardcoded/fake data patterns (TODO, placeholder, lorem ipsum)
    U10 Exact / near-duplicate content (theory_html, solution_code, quiz q, flashcard front)
    U11 Inline CSS styles baked into YAML content fields (CSS drift indicator)
    U12 Day IDs monotonically increasing across all 26 weeks (no gaps/overlaps)
"""

import os
import re
import sys
import json
import yaml
import hashlib
from collections import defaultdict
from difflib import SequenceMatcher

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA_DIR  = os.path.join(ROOT, 'src/data')
TMPL_PATH = os.path.join(ROOT, 'src/template/week.template.html')
SCHEMA_PATH    = os.path.join(ROOT, 'src/schema/week.schema.json')
CONTRACT_PATH  = os.path.join(ROOT, 'src/schema/contract.json')

# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def load_yaml(path):
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_text(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def similarity(a, b):
    """0-1 similarity ratio between two strings."""
    if not a or not b:
        return 0.0
    return SequenceMatcher(None, a[:3000], b[:3000]).ratio()

def strip_topic(text, topic):
    """Remove the topic name from text for near-dupe comparison."""
    if not text or not topic:
        return text
    return text.replace(topic, 'TOPIC').replace(topic.lower(), 'TOPIC')

def normalize(text):
    """Collapse whitespace for comparison."""
    if not text:
        return ''
    return re.sub(r'\s+', ' ', text).strip()

def md5(text):
    return hashlib.md5((text or '').encode()).hexdigest()

# ─────────────────────────────────────────────────────────────────────────────
# Load everything
# ─────────────────────────────────────────────────────────────────────────────

print("Loading data files …")
weeks_data = {}   # week_number -> raw YAML dict
week_files = {}   # week_number -> filename

for n in range(1, 27):
    fname = f"week{n:02d}.yaml"
    fpath = os.path.join(DATA_DIR, fname)
    if not os.path.exists(fpath):
        print(f"  WARNING: {fname} not found — skipping")
        continue
    weeks_data[n] = load_yaml(fpath)
    week_files[n] = fname

template_text = load_text(TMPL_PATH)
contract = load_json(CONTRACT_PATH)
schema   = load_json(SCHEMA_PATH)

allowed_task_badge_variants = set(contract.get('allowed_task_badge_variants', []))
allowed_meta_badge_variants = set(contract.get('allowed_meta_badge_variants', []))

# ─────────────────────────────────────────────────────────────────────────────
# Extract template variables (what the template actually reads)
# ─────────────────────────────────────────────────────────────────────────────

TEMPLATE_VAR_RE = re.compile(r'\{\{.*?\}\}', re.DOTALL)

# Collect day.X, task.X, q.X, fc.X, opt.X references
DAY_FIELDS_RE  = re.compile(r'day\.(\w+)')
TASK_FIELDS_RE = re.compile(r'task\.(\w+)')
Q_FIELDS_RE    = re.compile(r'q\.(\w+)')
FC_FIELDS_RE   = re.compile(r'fc\.(\w+)')
OPT_FIELDS_RE  = re.compile(r'opt\.(\w+)')

template_day_fields  = set(DAY_FIELDS_RE.findall(template_text))
template_task_fields = set(TASK_FIELDS_RE.findall(template_text))
template_q_fields    = set(Q_FIELDS_RE.findall(template_text))
template_fc_fields   = set(FC_FIELDS_RE.findall(template_text))
template_opt_fields  = set(OPT_FIELDS_RE.findall(template_text))

print(f"\n📋 Template reads:")
print(f"  day.*    : {sorted(template_day_fields)}")
print(f"  task.*   : {sorted(template_task_fields)}")
print(f"  q.*      : {sorted(template_q_fields)}")
print(f"  fc.*     : {sorted(template_fc_fields)}")
print(f"  opt.*    : {sorted(template_opt_fields)}")

# ─────────────────────────────────────────────────────────────────────────────
# Findings collector
# ─────────────────────────────────────────────────────────────────────────────

findings = []   # list of dicts

def add(issue_id, severity, week_n, day_id, location, description, example=''):
    findings.append({
        'issue_id':    issue_id,
        'severity':    severity,
        'week':        week_n,
        'day_id':      day_id,
        'location':    location,
        'description': description,
        'example':     example[:200] if example else ''
    })

# ─────────────────────────────────────────────────────────────────────────────
# K1 — theory_html boilerplate detection
# ─────────────────────────────────────────────────────────────────────────────

print("\n[K1] Checking theory_html boilerplate …")

BOILERPLATE_MARKERS = [
    ('enterprise_opener',
     r'at enterprise scale requires a rigorous understanding',
     'Fixed enterprise-scale opening sentence'),
    ('latency_penalty_formula',
     r'LatencyPenalty',
     'Fake LatencyPenalty formula in theory_html'),
    ('generic_engine_class',
     r'np\.random\.uniform\(0\.85,\s*0\.99\)',
     'Generic Engine class returning np.random.uniform(0.85, 0.99)'),
    ('concept_flow_duplicate',
     r'Concept Progression &(?:amp;)? Architecture Path',
     'Duplicate concept-flow callout embedded inside theory_html'),
    ('boilerplate_tradeoff_table',
     r'Standard Baseline.*?Asynchronous Distributed Worker.*?Quantized',
     'Fixed 3-row trade-off table'),
]

for wn, wdata in sorted(weeks_data.items()):
    days = wdata.get('days', [])
    for day in days:
        th = day.get('theory_html', '') or ''
        day_id = day.get('id', '?')
        for marker_name, pattern, desc in BOILERPLATE_MARKERS:
            if re.search(pattern, th, re.DOTALL | re.IGNORECASE):
                add('K1', 'HIGH', wn, day_id, 'theory_html',
                    f'{desc}',
                    th[:120])

# ─────────────────────────────────────────────────────────────────────────────
# K2 — Tasks with wrong schema (desc/starter_code/hint vs prompt_html etc.)
# ─────────────────────────────────────────────────────────────────────────────

print("[K2] Checking task schema mismatches …")

WRONG_TASK_FIELDS = {'desc', 'starter_code', 'hint'}
REQUIRED_TASK_FIELDS = set(template_task_fields)  # what the template reads

for wn, wdata in sorted(weeks_data.items()):
    days = wdata.get('days', [])
    for day in days:
        day_id = day.get('id', '?')
        for ti, task in enumerate(day.get('tasks', []), 1):
            task_keys = set(str(k) for k in task.keys())
            dead_keys = task_keys & WRONG_TASK_FIELDS
            missing_render_keys = REQUIRED_TASK_FIELDS - task_keys - {'default'}

            if dead_keys:
                add('K2', 'HIGH', wn, day_id,
                    f'tasks[{ti}] title="{task.get("title","?")[:60]}"',
                    f'Task uses dead fields not read by template: {sorted(dead_keys)}. '
                    f'Missing template fields: {sorted(missing_render_keys & {"prompt_html","sol_id","done_when","git_cmd"})}',
                    str(dead_keys))

# ─────────────────────────────────────────────────────────────────────────────
# K3 — Generic RandomForest solution_code boilerplate
# ─────────────────────────────────────────────────────────────────────────────

print("[K3] Checking for generic RandomForest solution_code …")

RF_PATTERN_1 = 'make_classification(n_samples=500, n_features=10, n_informative=8'
RF_PATTERN_2 = 'RandomForestClassifier'
RF_GENERIC_INDICATORS = [
    RF_PATTERN_1,
    'from sklearn.datasets import make_classification',
]

for wn, wdata in sorted(weeks_data.items()):
    days = wdata.get('days', [])
    for day in days:
        day_id = day.get('id', '?')
        for ti, task in enumerate(day.get('tasks', []), 1):
            sc = task.get('solution_code', '') or ''
            # Check for the specific make_classification pattern
            if RF_PATTERN_1 in sc:
                add('K3', 'HIGH', wn, day_id,
                    f'tasks[{ti}] title="{task.get("title","?")[:60]}"',
                    'Generic RandomForest/make_classification boilerplate in solution_code '
                    '(n_samples=500, n_features=10, n_informative=8)',
                    sc[:120])
            # Also flag where RandomForest is used but task topic is unrelated
            elif RF_PATTERN_2 in sc and 'forest' not in (task.get('title', '') + day.get('title', '')).lower():
                add('K3', 'MEDIUM', wn, day_id,
                    f'tasks[{ti}] title="{task.get("title","?")[:60]}"',
                    'RandomForestClassifier in solution_code for non-forest task — likely boilerplate',
                    sc[:120])

# ─────────────────────────────────────────────────────────────────────────────
# K4 — Duplicate concept-flow callout inside theory_html
# (already caught under K1 but count separately for clarity)
# ─────────────────────────────────────────────────────────────────────────────

print("[K4] Checking duplicate concept-flow callout in theory_html …")

CF_PATTERN = re.compile(
    r'Concept Progression\s*(?:&amp;|&)\s*Architecture Path',
    re.IGNORECASE
)

k4_days = set()
for wn, wdata in sorted(weeks_data.items()):
    for day in wdata.get('days', []):
        th = day.get('theory_html', '') or ''
        if CF_PATTERN.search(th):
            day_id = day.get('id', '?')
            k4_days.add((wn, day_id))
            add('K4', 'MEDIUM', wn, day_id, 'theory_html',
                'Duplicate concept-flow "Concept Progression & Architecture Path" callout '
                'baked into theory_html — template already renders this from day.concept_flow')

# ─────────────────────────────────────────────────────────────────────────────
# K5 — Generic placeholder done_when / git_cmd text
# ─────────────────────────────────────────────────────────────────────────────

print("[K5] Checking generic done_when / git_cmd placeholders …")

DONE_WHEN_GENERIC = 'output matches expected verification metrics and unit tests pass'
GIT_CMD_GENERIC   = 'complete hands-on task implementation'

for wn, wdata in sorted(weeks_data.items()):
    for day in wdata.get('days', []):
        day_id = day.get('id', '?')
        for ti, task in enumerate(day.get('tasks', []), 1):
            dw = task.get('done_when', '') or ''
            gc = task.get('git_cmd', '') or ''
            loc = f'tasks[{ti}] title="{task.get("title","?")[:60]}"'

            if DONE_WHEN_GENERIC in dw:
                add('K5', 'MEDIUM', wn, day_id, loc,
                    'Generic placeholder done_when text',
                    dw[:120])
            if GIT_CMD_GENERIC in gc:
                add('K5', 'LOW', wn, day_id, loc,
                    'Generic placeholder git_cmd text',
                    gc[:120])

# ─────────────────────────────────────────────────────────────────────────────
# K6 — week25 day184 near-duplicate capstone tasks
# ─────────────────────────────────────────────────────────────────────────────

print("[K6] Checking week25 day184 capstone task duplication …")

if 25 in weeks_data:
    w25 = weeks_data[25]
    for day in w25.get('days', []):
        if str(day.get('id', '')) == '184' or day.get('day_num') == 184:
            tasks = day.get('tasks', [])
            print(f"  day184 has {len(tasks)} tasks")
            for ti, task in enumerate(tasks, 1):
                add('K6', 'INFO', 25, day.get('id','184'),
                    f'tasks[{ti}]',
                    f'Day184 Task {ti}: "{task.get("title","?")}"',
                    (task.get('prompt_html') or task.get('desc') or '')[:200])

            # Compare prompts pairwise
            prompts = [(t.get('title',''), t.get('prompt_html') or t.get('desc') or '') for t in tasks]
            for i in range(len(prompts)):
                for j in range(i+1, len(prompts)):
                    sim = similarity(prompts[i][1], prompts[j][1])
                    if sim > 0.6:
                        add('K6', 'HIGH', 25, day.get('id','184'),
                            f'tasks[{i+1}] vs tasks[{j+1}]',
                            f'Near-duplicate tasks detected (similarity={sim:.2f}): '
                            f'"{prompts[i][0]}" vs "{prompts[j][0]}"')

# ─────────────────────────────────────────────────────────────────────────────
# K7 — badge_class / meta-badge variant mismatches
# ─────────────────────────────────────────────────────────────────────────────

print("[K7] Checking badge_class / meta-badge variant mismatches …")

for wn, wdata in sorted(weeks_data.items()):
    for day in wdata.get('days', []):
        day_id = day.get('id', '?')
        # meta badges
        for b in day.get('badges', []):
            variant = b.get('variant', '')
            if variant and variant not in allowed_meta_badge_variants:
                add('K7', 'HIGH', wn, day_id, f'badges[variant={variant}]',
                    f'Invalid meta-badge variant "{variant}" — allowed: {sorted(allowed_meta_badge_variants)}')
        # task badges
        for ti, task in enumerate(day.get('tasks', []), 1):
            bc = task.get('badge_class', '')
            if bc and bc not in allowed_task_badge_variants:
                add('K7', 'HIGH', wn, day_id,
                    f'tasks[{ti}].badge_class="{bc}"',
                    f'Invalid task badge_class "{bc}" — allowed: {sorted(allowed_task_badge_variants)}')

# ─────────────────────────────────────────────────────────────────────────────
# U1 — Missing required fields (schema compliance)
# ─────────────────────────────────────────────────────────────────────────────

print("\n[U1] Checking missing required fields …")

# Per schema: week requires week_number, title, days
# day requires id, title
# quiz requires question, options; option requires text, is_correct
# flashcard requires front, back

for wn, wdata in sorted(weeks_data.items()):
    if not isinstance(wdata, dict):
        add('U1', 'CRITICAL', wn, '-', 'week root', 'YAML failed to parse as dict')
        continue
    for req in ('week_number', 'title', 'days'):
        if not wdata.get(req):
            add('U1', 'CRITICAL', wn, '-', f'week.{req}', f'Missing required week field: {req}')

    days = wdata.get('days', [])
    if not days:
        add('U1', 'HIGH', wn, '-', 'week.days', 'No days found in week YAML')
        continue

    for day in days:
        day_id = day.get('id', '?')
        # Required day fields per schema
        for req in ('id', 'title'):
            if not day.get(req):
                add('U1', 'HIGH', wn, day_id, f'day.{req}', f'Missing required day field: {req}')

        # Important optional but commonly expected fields
        IMPORTANT_DAY_FIELDS = [
            'theory_html', 'objectives', 'concept_flow', 'hinglish',
            'tasks', 'quizzes', 'flashcards', 'gotcha', 'takeaways', 'resources'
        ]
        for field in IMPORTANT_DAY_FIELDS:
            val = day.get(field)
            if val is None:
                add('U1', 'LOW', wn, day_id, f'day.{field}',
                    f'Missing optional-but-important field: {field}')
            elif isinstance(val, (list, str)) and len(val) == 0:
                add('U1', 'LOW', wn, day_id, f'day.{field}',
                    f'Empty field: {field}')

        # Quiz checks
        for qi, q in enumerate(day.get('quizzes', []), 1):
            if not q.get('question', '').strip():
                add('U1', 'HIGH', wn, day_id, f'quizzes[{qi}].question',
                    'Empty quiz question')
            opts = q.get('options', [])
            if not opts:
                add('U1', 'HIGH', wn, day_id, f'quizzes[{qi}].options',
                    'Quiz has no options')
            else:
                for req in ('text', 'is_correct'):
                    for oi, opt in enumerate(opts, 1):
                        if req not in opt or opt[req] is None:
                            add('U1', 'HIGH', wn, day_id,
                                f'quizzes[{qi}].options[{oi}].{req}',
                                f'Option missing required field: {req}')

        # Flashcard checks
        for fi, fc in enumerate(day.get('flashcards', []), 1):
            for req in ('front', 'back'):
                if not (fc.get(req) or '').strip():
                    add('U1', 'HIGH', wn, day_id, f'flashcards[{fi}].{req}',
                        f'Flashcard missing/empty {req}')

        # Task checks
        for ti, task in enumerate(day.get('tasks', []), 1):
            if not (task.get('title') or '').strip():
                add('U1', 'HIGH', wn, day_id, f'tasks[{ti}].title',
                    'Task missing title')
            if not task.get('prompt_html') and not task.get('desc'):
                add('U1', 'MEDIUM', wn, day_id, f'tasks[{ti}]',
                    f'Task "{task.get("title","?")[:50]}" has neither prompt_html nor desc')

# ─────────────────────────────────────────────────────────────────────────────
# U2 — Dead data: fields in YAML never read by template
# ─────────────────────────────────────────────────────────────────────────────

print("[U2] Checking for dead data fields …")

DEAD_TASK_FIELDS = set()
DEAD_DAY_FIELDS  = set()

for wn, wdata in sorted(weeks_data.items()):
    for day in wdata.get('days', []):
        day_keys = set(str(k) for k in day.keys())
        # Day-level fields not in template
        for k in day_keys:
            if k not in template_day_fields and k not in (
                'id', 'day_num', 'title', 'subtitle', 'time_estimate', 'difficulty',
                'xp', 'objectives', 'checklist', 'concept_flow', 'hinglish', 'analogy',
                'theory_html', 'predict', 'tasks', 'quizzes', 'flashcards', 'gotcha',
                'takeaways', 'resources', 'badges'
            ):
                DEAD_DAY_FIELDS.add(k)

        for task in day.get('tasks', []):
            task_keys = set(str(k) for k in task.keys())
            for k in task_keys:
                if k not in template_task_fields and k not in (
                    'title', 'badge', 'badge_class', 'time', 'prompt_html',
                    'done_when', 'git_cmd', 'sol_id', 'solution_title',
                    'solution_code', 'solution_lang'
                ):
                    DEAD_TASK_FIELDS.add(k)

if DEAD_DAY_FIELDS:
    add('U2', 'INFO', 'ALL', '-', 'day.*',
        f'Day-level fields in YAML not read by template: {sorted(DEAD_DAY_FIELDS)}')
if DEAD_TASK_FIELDS:
    add('U2', 'INFO', 'ALL', '-', 'task.*',
        f'Task-level fields in YAML not read by template: {sorted(DEAD_TASK_FIELDS)}')

# Specifically flag desc/starter_code/hint across all weeks
for wn, wdata in sorted(weeks_data.items()):
    for day in wdata.get('days', []):
        day_id = day.get('id', '?')
        for ti, task in enumerate(day.get('tasks', []), 1):
            for dead_field in ('desc', 'starter_code', 'hint', 'time_minutes'):
                if dead_field in task:
                    add('U2', 'MEDIUM' if dead_field in ('desc','starter_code','hint') else 'LOW',
                        wn, day_id,
                        f'tasks[{ti}].{dead_field}',
                        f'Dead field "{dead_field}" found in task — template never reads it',
                        str(task.get(dead_field, ''))[:100])

# ─────────────────────────────────────────────────────────────────────────────
# U3 — Broken rendering: template reads fields the data never provides
# ─────────────────────────────────────────────────────────────────────────────

print("[U3] Checking template fields missing from data …")

# Key rendering fields that must be present for the task block to render correctly
CRITICAL_TASK_RENDER_FIELDS = ['prompt_html', 'sol_id', 'done_when', 'git_cmd',
                                'solution_code', 'solution_lang', 'solution_title']

task_field_missing_counts = defaultdict(int)
for wn, wdata in sorted(weeks_data.items()):
    for day in wdata.get('days', []):
        day_id = day.get('id', '?')
        for ti, task in enumerate(day.get('tasks', []), 1):
            for field in CRITICAL_TASK_RENDER_FIELDS:
                if not task.get(field):
                    task_field_missing_counts[field] += 1
                    if field == 'prompt_html':
                        add('U3', 'HIGH', wn, day_id,
                            f'tasks[{ti}] title="{task.get("title","?")[:50]}"',
                            f'Task missing prompt_html — will render as empty block',
                            '')

# ─────────────────────────────────────────────────────────────────────────────
# U4 — Quiz integrity
# ─────────────────────────────────────────────────────────────────────────────

print("[U4] Checking quiz integrity …")

for wn, wdata in sorted(weeks_data.items()):
    for day in wdata.get('days', []):
        day_id = day.get('id', '?')
        for qi, q in enumerate(day.get('quizzes', []), 1):
            opts = q.get('options', [])
            correct_count = sum(1 for o in opts if o.get('is_correct', False))
            if correct_count == 0:
                add('U4', 'HIGH', wn, day_id, f'quizzes[{qi}]',
                    'No correct answer (is_correct: true) in quiz options',
                    q.get('question', '')[:100])
            elif correct_count > 1:
                add('U4', 'HIGH', wn, day_id, f'quizzes[{qi}]',
                    f'Multiple correct answers ({correct_count}) in quiz — should be exactly 1',
                    q.get('question', '')[:100])

            # Duplicate option text
            texts = [o.get('text', '') for o in opts]
            seen = set()
            for oi, t in enumerate(texts, 1):
                if t in seen:
                    add('U4', 'MEDIUM', wn, day_id, f'quizzes[{qi}].options[{oi}]',
                        f'Duplicate option text: "{t[:80]}"')
                seen.add(t)

            # Empty question
            if not (q.get('question') or '').strip():
                add('U4', 'HIGH', wn, day_id, f'quizzes[{qi}]',
                    'Empty quiz question text')

# ─────────────────────────────────────────────────────────────────────────────
# U5 — Resource URL sanity
# ─────────────────────────────────────────────────────────────────────────────

print("[U5] Checking resource URLs …")

DEAD_DOMAINS = re.compile(
    r'(example\.com|placeholder|TODO|localhost|127\.0\.0\.1|#|'
    r'your-domain|FILL_IN|INSERT_URL|mysite)', re.IGNORECASE
)

for wn, wdata in sorted(weeks_data.items()):
    for day in wdata.get('days', []):
        day_id = day.get('id', '?')
        for ri, res in enumerate(day.get('resources', []), 1):
            url = res.get('url', '') or ''
            if not url:
                add('U5', 'MEDIUM', wn, day_id, f'resources[{ri}].url',
                    f'Resource "{res.get("title","?")[:50]}" has no URL')
            elif not url.startswith(('https://', 'http://')):
                add('U5', 'MEDIUM', wn, day_id, f'resources[{ri}].url="{url[:60]}"',
                    'Resource URL does not start with https:// or http://')
            elif DEAD_DOMAINS.search(url):
                add('U5', 'HIGH', wn, day_id, f'resources[{ri}].url="{url[:80]}"',
                    f'Suspicious/placeholder domain in resource URL')

# ─────────────────────────────────────────────────────────────────────────────
# U6 — XP value sanity
# ─────────────────────────────────────────────────────────────────────────────

print("[U6] Checking XP values …")

XP_EXPECTED = 150   # default per contract
XP_VALID = {50, 100, 150, 200, 250, 300, 500}

for wn, wdata in sorted(weeks_data.items()):
    for day in wdata.get('days', []):
        day_id = day.get('id', '?')
        xp = day.get('xp')
        if xp is None:
            pass  # default is fine
        elif not isinstance(xp, int) or xp <= 0:
            add('U6', 'MEDIUM', wn, day_id, 'day.xp',
                f'Invalid XP value: {xp!r}')
        elif xp not in XP_VALID and xp != XP_EXPECTED:
            add('U6', 'LOW', wn, day_id, 'day.xp',
                f'Unusual XP value: {xp} (expected one of {sorted(XP_VALID)})')

# ─────────────────────────────────────────────────────────────────────────────
# U7 — day.id / day_num uniqueness within each week
# ─────────────────────────────────────────────────────────────────────────────

print("[U7] Checking day.id uniqueness and ordering within each week …")

for wn, wdata in sorted(weeks_data.items()):
    days = wdata.get('days', [])
    seen_ids = {}
    seen_nums = {}
    for idx, day in enumerate(days):
        day_id  = day.get('id')
        day_num = day.get('day_num')

        if day_id in seen_ids:
            add('U7', 'CRITICAL', wn, day_id, 'day.id',
                f'Duplicate day.id={day_id} at positions {seen_ids[day_id]} and {idx}')
        else:
            seen_ids[day_id] = idx

        if day_num is not None:
            if day_num in seen_nums:
                add('U7', 'HIGH', wn, day_id, 'day.day_num',
                    f'Duplicate day_num={day_num}')
            seen_nums[day_num] = day_id

# ─────────────────────────────────────────────────────────────────────────────
# U8 — week_number matches filename
# ─────────────────────────────────────────────────────────────────────────────

print("[U8] Checking week_number matches filename …")

for wn, wdata in sorted(weeks_data.items()):
    declared = wdata.get('week_number')
    if declared != wn:
        add('U8', 'CRITICAL', wn, '-', 'week.week_number',
            f'week_number={declared} does not match filename week{wn:02d}.yaml')

# ─────────────────────────────────────────────────────────────────────────────
# U9 — Hardcoded/fake data patterns
# ─────────────────────────────────────────────────────────────────────────────

print("[U9] Checking hardcoded/fake data patterns …")

FAKE_PATTERNS = [
    (re.compile(r'\bTODO\b', re.IGNORECASE), 'TODO placeholder'),
    (re.compile(r'\bplaceholder\b', re.IGNORECASE), 'placeholder text'),
    (re.compile(r'\blorem\b', re.IGNORECASE), 'lorem ipsum text'),
    (re.compile(r'\bFILL IN\b|\bINSERT HERE\b|\bXXX\b'), 'unfilled template marker'),
]

TEXT_FIELDS_TO_CHECK = ['theory_html', 'hinglish', 'analogy']

for wn, wdata in sorted(weeks_data.items()):
    for day in wdata.get('days', []):
        day_id = day.get('id', '?')
        for field in TEXT_FIELDS_TO_CHECK:
            text = day.get(field, '') or ''
            for pattern, desc in FAKE_PATTERNS:
                if pattern.search(text):
                    add('U9', 'MEDIUM', wn, day_id, f'day.{field}',
                        f'Fake/placeholder content detected: {desc}',
                        text[:120])

        for ti, task in enumerate(day.get('tasks', []), 1):
            for field in ('prompt_html', 'done_when', 'solution_code'):
                text = task.get(field, '') or ''
                for pattern, desc in FAKE_PATTERNS:
                    if pattern.search(text):
                        add('U9', 'MEDIUM', wn, day_id,
                            f'tasks[{ti}].{field}',
                            f'Fake/placeholder content: {desc}',
                            text[:120])

# ─────────────────────────────────────────────────────────────────────────────
# U10 — Exact/near-duplicate content detection
# ─────────────────────────────────────────────────────────────────────────────

print("[U10] Checking for duplicate content …")

# Collect theory_html hashes and near-dupes
theory_hashes = defaultdict(list)   # md5 -> [(week, day_id)]
solution_hashes = defaultdict(list) # md5 -> [(week, day_id, task_i)]
quiz_q_hashes   = defaultdict(list)
flashcard_hashes = defaultdict(list)

for wn, wdata in sorted(weeks_data.items()):
    week_title = wdata.get('title', '')
    for day in wdata.get('days', []):
        day_id = day.get('id', '?')
        day_title = day.get('title', '')

        # theory_html: normalize and strip topic
        th = normalize(day.get('theory_html', '') or '')
        th_norm = strip_topic(th, day_title)
        th_norm = strip_topic(th_norm, week_title)
        if th_norm:
            h = md5(th_norm[:2000])   # hash first 2k chars for speed
            theory_hashes[h].append((wn, day_id, day_title))

        for ti, task in enumerate(day.get('tasks', []), 1):
            sc = normalize(task.get('solution_code', '') or '')
            if sc and len(sc) > 50:
                h = md5(sc[:2000])
                solution_hashes[h].append((wn, day_id, ti, task.get('title', '?')))

        for qi, q in enumerate(day.get('quizzes', []), 1):
            qtext = normalize(q.get('question', '') or '')
            if qtext:
                quiz_q_hashes[md5(qtext)].append((wn, day_id, qi))

        for fi, fc in enumerate(day.get('flashcards', []), 1):
            front = normalize(fc.get('front', '') or '')
            if front:
                flashcard_hashes[md5(front)].append((wn, day_id, fi))

# Report duplicates
for h, locs in theory_hashes.items():
    if len(locs) > 1:
        weeks_str = ', '.join(f'W{l[0]}D{l[1]}({l[2][:30]})' for l in locs)
        add('U10', 'HIGH', locs[0][0], locs[0][1], 'theory_html',
            f'Exact/near-exact duplicate theory_html across {len(locs)} days (after topic removal): {weeks_str}')

for h, locs in solution_hashes.items():
    if len(locs) > 1:
        example = ', '.join(f'W{l[0]}D{l[1]}T{l[2]}({l[3][:25]})' for l in locs[:4])
        add('U10', 'HIGH', locs[0][0], locs[0][1], 'solution_code',
            f'Exact duplicate solution_code in {len(locs)} tasks: {example}')

for h, locs in quiz_q_hashes.items():
    if len(locs) > 1:
        add('U10', 'MEDIUM', locs[0][0], locs[0][1], 'quizzes',
            f'Duplicate quiz question in {len(locs)} places: '
            f'{", ".join(f"W{l[0]}D{l[1]}Q{l[2]}" for l in locs)}')

for h, locs in flashcard_hashes.items():
    if len(locs) > 1:
        add('U10', 'MEDIUM', locs[0][0], locs[0][1], 'flashcards',
            f'Duplicate flashcard front in {len(locs)} places: '
            f'{", ".join(f"W{l[0]}D{l[1]}FC{l[2]}" for l in locs)}')

# ─────────────────────────────────────────────────────────────────────────────
# U11 — Inline CSS baked into YAML content (CSS drift indicator)
# ─────────────────────────────────────────────────────────────────────────────

print("[U11] Checking for inline CSS styles baked into YAML content …")

INLINE_STYLE_RE = re.compile(r'style\s*=\s*["\']([^"\']{10,})["\']', re.IGNORECASE)

CONTENT_FIELDS = ['theory_html', 'analogy', 'hinglish']
TASK_CONTENT_FIELDS = ['prompt_html', 'solution_code']

inline_style_weeks = defaultdict(int)   # week -> count
inline_style_examples = {}              # week -> first example

for wn, wdata in sorted(weeks_data.items()):
    for day in wdata.get('days', []):
        day_id = day.get('id', '?')
        for field in CONTENT_FIELDS:
            text = day.get(field, '') or ''
            matches = INLINE_STYLE_RE.findall(text)
            if matches:
                inline_style_weeks[wn] += len(matches)
                if wn not in inline_style_examples:
                    inline_style_examples[wn] = matches[0]
                add('U11', 'MEDIUM', wn, day_id, f'day.{field}',
                    f'{len(matches)} inline style= attributes baked into {field} — '
                    'bypasses course.css, causes CSS drift',
                    matches[0][:120])

print("\n  Inline style counts per week:")
for wn in sorted(inline_style_weeks.keys()):
    era = 'weeks 1-17' if wn <= 17 else 'weeks 18-26'
    print(f"    Week {wn:2d} ({era}): {inline_style_weeks[wn]} inline styles")

# ─────────────────────────────────────────────────────────────────────────────
# U12 — Day IDs monotonically increasing across all 26 weeks (no gaps/overlaps)
# ─────────────────────────────────────────────────────────────────────────────

print("[U12] Checking day ID monotonic ordering across all weeks …")

all_day_nums = []   # list of (week_n, day_id, day_num)
for wn in range(1, 27):
    if wn not in weeks_data:
        continue
    for day in weeks_data[wn].get('days', []):
        day_num = day.get('day_num')
        day_id  = day.get('id')
        if day_num is not None:
            all_day_nums.append((wn, day_id, day_num))

# Check uniqueness across all weeks
seen_global = {}
for wn, day_id, day_num in all_day_nums:
    if day_num in seen_global:
        add('U12', 'CRITICAL', wn, day_id, f'day_num={day_num}',
            f'Duplicate day_num={day_num} across weeks: '
            f'also in Week {seen_global[day_num][0]}, day_id={seen_global[day_num][1]}')
    else:
        seen_global[day_num] = (wn, day_id)

# Check for gaps
if all_day_nums:
    sorted_nums = sorted(d[2] for d in all_day_nums)
    expected = list(range(sorted_nums[0], sorted_nums[-1]+1))
    actual_set = set(sorted_nums)
    gaps = [n for n in expected if n not in actual_set]
    if gaps:
        add('U12', 'HIGH', 'ALL', '-', 'day_num sequence',
            f'Gaps in day_num sequence: {gaps[:20]}{"..." if len(gaps)>20 else ""}')
    else:
        print(f"  ✓ Day nums {sorted_nums[0]}-{sorted_nums[-1]}: no gaps found")

    # Check total count
    print(f"  Total days found: {len(all_day_nums)} (expected 191)")
    if len(all_day_nums) != 191:
        add('U12', 'HIGH', 'ALL', '-', 'day count',
            f'Expected 191 total days, found {len(all_day_nums)}')

# ─────────────────────────────────────────────────────────────────────────────
# Additional: Boilerplate confirmation — 0% in weeks 1-17?
# ─────────────────────────────────────────────────────────────────────────────

print("\n[VERIFY] Confirming boilerplate is absent in weeks 1-17 …")
boilerplate_in_early_weeks = [f for f in findings
    if f['issue_id'] in ('K1','K4')
    and isinstance(f['week'], int) and f['week'] <= 17]
if boilerplate_in_early_weeks:
    print(f"  ⚠️  BOILERPLATE FOUND IN EARLY WEEKS ({len(boilerplate_in_early_weeks)} instances)!")
    for f in boilerplate_in_early_weeks:
        print(f"    Week {f['week']} Day {f['day_id']}: {f['description'][:80]}")
else:
    print("  ✓ No K1/K4 boilerplate found in weeks 1-17.")

# ─────────────────────────────────────────────────────────────────────────────
# Summary table generation
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "="*80)
print("PHASE 1 AUDIT — SUMMARY")
print("="*80)

# Aggregate by issue_id
from collections import Counter
summary = defaultdict(lambda: {'count': 0, 'weeks': set(), 'max_severity': 'LOW', 'examples': []})

SEVERITY_ORDER = {'CRITICAL': 5, 'HIGH': 4, 'MEDIUM': 3, 'LOW': 2, 'INFO': 1}

for f in findings:
    key = f['issue_id']
    summary[key]['count'] += 1
    if isinstance(f['week'], int):
        summary[key]['weeks'].add(f['week'])
    if SEVERITY_ORDER.get(f['severity'], 0) > SEVERITY_ORDER.get(summary[key]['max_severity'], 0):
        summary[key]['max_severity'] = f['severity']
    if len(summary[key]['examples']) < 2 and f.get('example'):
        summary[key]['examples'].append(f['example'][:80])

ISSUE_NAMES = {
    'K1': 'theory_html boilerplate (enterprise opener, LatencyPenalty, generic Engine)',
    'K2': 'Tasks with wrong schema (desc/starter_code/hint instead of prompt_html)',
    'K3': 'Generic RandomForest solution_code boilerplate',
    'K4': 'Duplicate concept-flow callout in theory_html',
    'K5': 'Generic placeholder done_when / git_cmd text',
    'K6': 'week25 day184 near-duplicate capstone tasks',
    'K7': 'badge_class / meta-badge variant mismatches',
    'U1': 'Missing required fields (schema non-compliance)',
    'U2': 'Dead data fields (YAML fields template never reads)',
    'U3': 'Broken rendering (template fields data never provides)',
    'U4': 'Quiz integrity failures (0 or >1 correct, dupes, empty)',
    'U5': 'Resource URL problems (missing, placeholder, non-https)',
    'U6': 'XP value anomalies',
    'U7': 'day.id / day_num uniqueness issues within weeks',
    'U8': 'week_number mismatch with filename',
    'U9': 'Hardcoded/fake content (TODO, placeholder, lorem)',
    'U10':'Exact/near-duplicate content (theory, solution, quiz, flashcard)',
    'U11':'Inline CSS styles baked into YAML content (CSS drift)',
    'U12':'day_num global uniqueness / monotonic ordering issues',
}

# Print markdown table
print("\n| Issue | Name | Weeks Affected | Count | Severity | Example |")
print("|-------|------|----------------|-------|----------|---------|")
for issue_id in ['K1','K2','K3','K4','K5','K6','K7',
                  'U1','U2','U3','U4','U5','U6','U7','U8','U9','U10','U11','U12']:
    if issue_id not in summary:
        print(f"| {issue_id} | {ISSUE_NAMES.get(issue_id,'?')} | — | 0 | OK | — |")
        continue
    s = summary[issue_id]
    weeks_str = ', '.join(str(w) for w in sorted(s['weeks'])) if s['weeks'] else 'ALL'
    if len(weeks_str) > 40:
        wlist = sorted(s['weeks'])
        weeks_str = f"W{wlist[0]}-W{wlist[-1]} ({len(wlist)} weeks)"
    example = (s['examples'][0] if s['examples'] else '').replace('|','│').replace('\n', ' ')[:60]
    print(f"| {issue_id} | {ISSUE_NAMES.get(issue_id,'?')[:50]} | {weeks_str} | {s['count']} | {s['max_severity']} | {example} |")

print(f"\nTotal findings: {len(findings)}")

# ─────────────────────────────────────────────────────────────────────────────
# Detailed breakdown by issue
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "="*80)
print("DETAILED FINDINGS BY ISSUE TYPE")
print("="*80)

# Group findings by issue_id
by_issue = defaultdict(list)
for f in findings:
    by_issue[f['issue_id']].append(f)

for issue_id in ['K1','K2','K3','K4','K5','K6','K7',
                  'U1','U2','U3','U4','U5','U6','U7','U8','U9','U10','U11','U12']:
    items = by_issue.get(issue_id, [])
    if not items:
        print(f"\n### {issue_id}: 0 issues ✓")
        continue
    sev = summary[issue_id]['max_severity']
    print(f"\n### {issue_id} [{sev}] — {len(items)} issues")
    print(f"    {ISSUE_NAMES.get(issue_id,'')}")
    for f in items[:30]:   # cap display at 30 per category
        wstr = f"W{f['week']}" if isinstance(f['week'], int) else str(f['week'])
        print(f"    {wstr} D{f['day_id']} @ {f['location'][:50]}: {f['description'][:100]}")
    if len(items) > 30:
        print(f"    ... and {len(items)-30} more")

# ─────────────────────────────────────────────────────────────────────────────
# Save full findings to JSON
# ─────────────────────────────────────────────────────────────────────────────

out_path = os.path.join(ROOT, 'scripts', 'phase1_audit_report.json')
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump({
        'total_findings': len(findings),
        'summary': {k: {
            'count': v['count'],
            'max_severity': v['max_severity'],
            'weeks': sorted(v['weeks']),
            'examples': v['examples']
        } for k, v in summary.items()},
        'task_field_missing_counts': dict(task_field_missing_counts),
        'inline_style_per_week': dict(inline_style_weeks),
        'dead_task_fields': sorted(DEAD_TASK_FIELDS),
        'dead_day_fields': sorted(DEAD_DAY_FIELDS),
        'template_fields': {
            'day': sorted(template_day_fields),
            'task': sorted(template_task_fields),
            'quiz_q': sorted(template_q_fields),
            'flashcard': sorted(template_fc_fields),
            'option': sorted(template_opt_fields),
        },
        'findings': findings
    }, f, indent=2, default=str)

print(f"\n✅ Full findings saved to: {out_path}")
print(f"   Total issues found: {len(findings)}")
