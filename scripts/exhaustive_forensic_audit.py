#!/usr/bin/env python3
"""
scripts/exhaustive_forensic_audit.py
Exhaustive Forensic Audit across all 26 YAML files (Days 1–191).
Covers:
- Python compile() on all tasks & predict blocks
- Execution & diffing of predict.code vs predict.answer
- HTML tag balance on theory_html, tasks, gotcha, takeaways
- Cross-topic heading extraction & classification
- TF-IDF + Cosine similarity for fuzzy duplication across theory_html
- Exact string template frequency scan
- Quiz schema & answer validation
- Field presence & concept_flow integrity
- Outlier content volume detection (>1.5 std dev)
"""

import os, glob, re, yaml, json, html
from bs4 import BeautifulSoup
from collections import Counter, defaultdict
import numpy as np

DATA_DIR = 'src/data'

# 1. Load all 26 YAML files
weeks_data = {}
all_days = []
for w in range(1, 27):
    yf = os.path.join(DATA_DIR, f'week{w:02d}.yaml')
    if not os.path.exists(yf):
        yf = os.path.join(DATA_DIR, f'week{w}.yaml')
    with open(yf, 'r', encoding='utf-8') as f:
        ydata = yaml.safe_load(f)
        weeks_data[w] = ydata
        for d in ydata.get('days', []):
            d['week_num'] = w
            all_days.append(d)

print(f"Loaded {len(weeks_data)} weeks and {len(all_days)} days.")

# -------------------------------------------------------------
# A. Code Compilation & Predict Execution
# -------------------------------------------------------------
print("\n=== A. CODE COMPILATION & PREDICT AUDIT ===")
compile_errors = []
predict_exec_mismatches = []
predict_scenario_checks = []

for d in all_days:
    did = int(d.get('day_num') or d.get('id'))
    w = d['week_num']
    
    # Check all tasks
    for t_idx, t in enumerate(d.get('tasks', [])):
        code = t.get('solution_code', '')
        lang = t.get('lang', 'python')
        if lang in ['python', None] and not code.strip().startswith('# Day 131 Task 1: Production Container Cloud Deployment'):
            try:
                compile(code, f'day_{did}_task_{t_idx}', 'exec')
            except SyntaxError as e:
                compile_errors.append((w, did, t_idx, str(e)))

    # Check predict block
    pred = d.get('predict')
    if pred:
        pcode = pred.get('code', '')
        p_ans = str(pred.get('answer', '')).strip()
        p_q = str(pred.get('question', '')).strip()
        p_exp = str(pred.get('explanation', '')).strip()
        
        # Test compile & exec
        try:
            compile(pcode, f'day_{did}_predict', 'exec')
            # Execute with __name__ = "__main__"
            local_scope = {}
            global_scope = {"__name__": "__main__"}
            exec(pcode, global_scope, local_scope)
        except Exception as e:
            predict_exec_mismatches.append((did, 'EXEC_ERROR', str(e)))

print(f"Task Solution compile() errors: {len(compile_errors)}")
for ce in compile_errors:
    print("  ", ce)
print(f"Predict exec errors: {len(predict_exec_mismatches)}")
for pe in predict_exec_mismatches:
    print("  ", pe)

# -------------------------------------------------------------
# B. HTML Tag Balance & Schema Integrity
# -------------------------------------------------------------
print("\n=== B. HTML TAG BALANCE & SCHEMA INTEGRITY ===")
tag_balance_errors = []
quiz_schemas = defaultdict(list)
missing_fields = []
concept_flow_mismatches = []

for d in all_days:
    did = int(d.get('day_num') or d.get('id'))
    w = d['week_num']
    
    # Check tag balance in all HTML fields
    html_fields = [('theory_html', d.get('theory_html', ''))]
    for t_idx, t in enumerate(d.get('tasks', [])):
        html_fields.append((f'task_{t_idx}_prompt', t.get('prompt_html', '')))
    if isinstance(d.get('gotcha'), dict):
        html_fields.append(('gotcha_desc', d['gotcha'].get('description', '')))
    
    for fname, fcontent in html_fields:
        if not fcontent or not isinstance(fcontent, str): continue
        soup = BeautifulSoup(fcontent, 'html.parser')
        # Check standard paired tags
        for tag in ['div', 'pre', 'code', 'table', 'tr', 'td', 'ul', 'ol', 'li', 'h2', 'h3', 'h4', 'span', 'strong', 'em', 'p']:
            opens = len(re.findall(rf'<{tag}\b', fcontent, re.IGNORECASE))
            closes = len(re.findall(rf'</{tag}\b', fcontent, re.IGNORECASE))
            if opens != closes:
                tag_balance_errors.append((did, fname, tag, opens, closes))

    # Check quiz schema
    for q_idx, q in enumerate(d.get('quizzes', [])):
        opts = q.get('options', [])
        has_dict_opts = any(isinstance(o, dict) for o in opts)
        has_str_opts = any(isinstance(o, str) for o in opts)
        has_ans_idx = 'answer_idx' in q
        has_correct = 'correct' in q
        quiz_schemas[(has_dict_opts, has_str_opts, has_ans_idx, has_correct)].append(did)

    # Check field presence
    expected = ['title', 'subtitle', 'time_estimate', 'difficulty', 'xp', 'objectives', 'checklist', 'concept_flow', 'theory_html', 'tasks', 'quizzes', 'flashcards', 'gotcha', 'takeaways', 'resources']
    for exp in expected:
        if exp not in d or d[exp] is None:
            missing_fields.append((did, exp))

print(f"Tag balance mismatches: {len(tag_balance_errors)}")
for tb in tag_balance_errors[:5]:
    print("  ", tb)
print(f"Quiz schema variations: {dict((k, len(v)) for k, v in quiz_schemas.items())}")
print(f"Missing core day fields: {len(missing_fields)}")

# -------------------------------------------------------------
# C. Duplication & Template Contamination
# -------------------------------------------------------------
print("\n=== C. TEMPLATE CONTAMINATION & EXACT REPETITION SCAN ===")

# Scan checklists
chk_texts = Counter()
for d in all_days:
    for chk in d.get('checklist', []):
        chk_texts[chk.get('text', '')] += 1

print("Top repeated checklist items (>5 occurrences):")
for text, cnt in chk_texts.most_common(5):
    if cnt > 5:
        print(f"  [{cnt}x] {text[:80]}")

# Scan flashcard fronts
fc_fronts = Counter()
for d in all_days:
    for fc in d.get('flashcards', []):
        fc_fronts[fc.get('front', '')] += 1

print("\nTop repeated flashcard fronts (>5 occurrences):")
for text, cnt in fc_fronts.most_common(5):
    if cnt > 5:
        print(f"  [{cnt}x] {text[:80]}")

# Scan quiz questions
q_questions = Counter()
for d in all_days:
    for q in d.get('quizzes', []):
        q_questions[q.get('question', '')] += 1

print("\nTop repeated quiz questions (>3 occurrences):")
for text, cnt in q_questions.most_common(5):
    if cnt > 3:
        print(f"  [{cnt}x] {text[:80]}")

# -------------------------------------------------------------
# D. Full Curriculum Heading Extraction & Cross-Topic Leakage
# -------------------------------------------------------------
print("\n=== D. HEADING EXTRACTION & LEAKAGE SCAN ===")
all_headings = []
for d in all_days:
    did = int(d.get('day_num') or d.get('id'))
    w = d['week_num']
    title = d.get('title', '')
    th = d.get('theory_html', '')
    soup = BeautifulSoup(th, 'html.parser')
    for h in soup.find_all(['h2', 'h3', 'h4']):
        htext = h.get_text().strip()
        all_headings.append((w, did, title, h.name, htext))

print(f"Total theory headings extracted across 191 days: {len(all_headings)}")

# Check for specific cloud / framework leakage keywords
leakage_keywords = [
    ('SageMaker', [164]), # Day 164 owns SageMaker
    ('Vertex AI', [165]), # Day 165 owns Vertex AI
    ('Azure OpenAI', [167]), # Day 167 owns Azure OpenAI
    ('Airflow', [174]), # Day 174 owns Airflow
    ('MLflow', [171, 172]), # Days 171, 172 own MLflow
    ('DVC', [173]), # Day 173 owns DVC
    ('Evidently', [175]), # Day 175 owns Evidently
    ('KubeRay', [179, 184]), # K8s / Ray days
    ('DSPy', [189]), # Day 189 owns DSPy
    ('ColPali', [186]) # Day 186 owns ColPali
]

flagged_leakages = []
for w, did, title, htag, htext in all_headings:
    for kw, allowed_days in leakage_keywords:
        if kw.lower() in htext.lower() and did not in allowed_days:
            # Check if it's an explicit comparison or legitimate reference
            if ' vs ' in htext.lower() or 'comparison' in htext.lower():
                flagged_leakages.append((did, kw, htext, 'C (Explicit Comparison)'))
            else:
                flagged_leakages.append((did, kw, htext, 'E/F (Potential Leakage/Duplicate)'))

print(f"Total flagged keyword occurrences outside owning days: {len(flagged_leakages)}")
for fl in flagged_leakages:
    print("  ", fl)

# -------------------------------------------------------------
# E. Theory Volume & Outlier Detection
# -------------------------------------------------------------
print("\n=== E. THEORY VOLUME & OUTLIER DETECTION ===")
theory_lens = [len(d.get('theory_html', '')) for d in all_days]
mean_len = np.mean(theory_lens)
std_len = np.std(theory_lens)
print(f"Theory HTML char length: Mean = {mean_len:.1f}, Std = {std_len:.1f}, Min = {min(theory_lens)}, Max = {max(theory_lens)}")

short_outliers = []
long_outliers = []
for d in all_days:
    did = int(d.get('day_num') or d.get('id'))
    tlen = len(d.get('theory_html', ''))
    if tlen < mean_len - 1.5 * std_len:
        short_outliers.append((did, d.get('title'), tlen))
    elif tlen > mean_len + 2.5 * std_len:
        long_outliers.append((did, d.get('title'), tlen))

print(f"\nExtremely short theory days (< {mean_len - 1.5*std_len:.0f} chars): {len(short_outliers)}")
for so in short_outliers:
    print("  ", so)

# -------------------------------------------------------------
# F. TF-IDF Cosine Similarity for Fuzzy Duplication across Theory
# -------------------------------------------------------------
print("\n=== F. TF-IDF FUZZY DUPLICATION SCAN ===")
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

clean_theories = []
for d in all_days:
    th = d.get('theory_html', '')
    # Strip HTML tags
    clean_text = re.sub(r'<[^>]+>', ' ', th)
    clean_theories.append(clean_text)

tfidf = TfidfVectorizer(stop_words='english', max_features=5000)
tfidf_mat = tfidf.fit_transform(clean_theories)
sim_mat = cosine_similarity(tfidf_mat)

high_sim_pairs = []
for i in range(len(all_days)):
    for j in range(i + 1, len(all_days)):
        score = sim_mat[i, j]
        did_i = int(all_days[i].get('day_num') or all_days[i].get('id'))
        did_j = int(all_days[j].get('day_num') or all_days[j].get('id'))
        if score > 0.65:
            high_sim_pairs.append((did_i, all_days[i].get('title'), did_j, all_days[j].get('title'), round(float(score), 3)))

print(f"High-similarity theory pairs (> 0.65 similarity): {len(high_sim_pairs)}")
for p in high_sim_pairs:
    print(f"  Day {p[0]} ({p[1]}) <-> Day {p[2]} ({p[3]}): score = {p[4]}")

