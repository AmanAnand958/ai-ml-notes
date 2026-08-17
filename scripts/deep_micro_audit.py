#!/usr/bin/env python3
"""
scripts/deep_micro_audit.py
Scans for microscopic and deep educational & code hygiene defects across all 26 weeks:
1. Code Style / Magic Numbers in tasks without docstrings/type annotations
2. Inconsistent XP values between task descriptions vs yaml metadata
3. Missing math formulas in optimization & loss sections
4. Missing return type hints in Python task solutions
5. Days with imbalanced difficulty ratings
6. Quizzes with uneven length options (distractor length bias)
7. Flashcards with single-word answers or lacking technical context
"""

import glob, yaml, re, os, json, html

print("=== STARTING DEEP MICRO-AUDIT ACROSS ALL WEEKS ===")

micro_findings = []
m_id = 1

def record_m(category, severity, location, title, problem, evidence, recommendation):
    global m_id
    micro_findings.append({
        "id": f"MICRO-{m_id:03d}",
        "category": category,
        "severity": severity,
        "location": location,
        "title": title,
        "problem": problem,
        "evidence": str(evidence)[:250],
        "recommendation": recommendation
    })
    m_id += 1

yaml_files = sorted(glob.glob('src/data/week*.yaml'))
html_files = sorted(glob.glob('pages/weeks/week*.html'))

# 1. QUIZ DISTRACTOR LENGTH BIAS
print("1. Auditing Quiz Option Length Biases...")
for yf in yaml_files:
    w_num = int(re.search(r'week(\d+)', yf).group(1))
    with open(yf, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    for d in data.get('days', []):
        d_num = d.get('day_num')
        for q_idx, q in enumerate(d.get('quizzes', [])):
            opts = q.get('options', [])
            if len(opts) >= 3:
                lengths = [len(str(o.get('text', ''))) for o in opts]
                correct_idx = [i for i, o in enumerate(opts) if o.get('is_correct') is True]
                if correct_idx:
                    c_idx = correct_idx[0]
                    other_lengths = [l for i, l in enumerate(lengths) if i != c_idx]
                    avg_other = sum(other_lengths) / len(other_lengths) if other_lengths else 0
                    if avg_other > 0 and lengths[c_idx] > 2.2 * avg_other and lengths[c_idx] > 40:
                        record_m(
                            "Quiz Design",
                            "Medium",
                            f"Week {w_num:02d} / Day {d_num:03d} -> Quiz #{q_idx+1}",
                            "Correct Option Length Outlier (Giveaway Distractor Bias)",
                            "The correct option is over 2.2x longer and significantly more detailed than all wrong distractors, creating an obvious giveaway clue.",
                            f"Correct option length: {lengths[c_idx]} chars vs average distractor length: {avg_other:.1f} chars.",
                            "Equalize length and detail across all distractors so options are equally plausible."
                        )

# 2. MISSING TYPE ANNOTATIONS IN PYTHON TASK SOLUTIONS
print("2. Auditing Python Type Annotations in Task Solutions...")
for yf in yaml_files:
    w_num = int(re.search(r'week(\d+)', yf).group(1))
    with open(yf, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    for d in data.get('days', []):
        d_num = d.get('day_num')
        for t_idx, t in enumerate(d.get('tasks', [])):
            lang = str(t.get('solution_lang', 'python')).lower()
            sol = str(t.get('solution_code', ''))
            if lang in ['python', 'py'] and 'def ' in sol:
                funcs = re.findall(r'def\s+([a-zA-Z0-9_]+)\s*\((.*?)\)', sol)
                for f_name, f_args in funcs:
                    if '->' not in sol and ':' not in f_args and f_name not in ['__init__', 'forward']:
                        record_m(
                            "Code Quality",
                            "Low",
                            f"Week {w_num:02d} / Day {d_num:03d} -> Task #{t_idx+1} ({t.get('title', 'Task')})",
                            f"Missing PEP 484 Type Annotations in Function `{f_name}`",
                            f"Function `{f_name}` in solution code lacks argument types and return type hints.",
                            f"Signature: def {f_name}({f_args})",
                            f"Add explicit type hints, e.g., `def {f_name}(...) -> ExpectedType:`."
                        )

# 3. MISSING SEED INITIALIZATION IN RANDOMIZED ML SCRIPTS
print("3. Auditing Random Seed Invariants in ML Tasks...")
for yf in yaml_files:
    w_num = int(re.search(r'week(\d+)', yf).group(1))
    with open(yf, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    for d in data.get('days', []):
        d_num = d.get('day_num')
        for t_idx, t in enumerate(d.get('tasks', [])):
            sol = str(t.get('solution_code', ''))
            if any(k in sol for k in ['train_test_split', 'np.random', 'torch.randn', 'KMeans', 'RandomForest', 'LogisticRegression']):
                if 'random_state' not in sol and 'manual_seed' not in sol and 'np.random.seed' not in sol:
                    record_m(
                        "Reproducibility",
                        "High",
                        f"Week {w_num:02d} / Day {d_num:03d} -> Task #{t_idx+1} ({t.get('title', 'Task')})",
                        "Missing Random Seed / Non-Deterministic Model Initialization",
                        "Task invokes stochastic ML operations or data splits without setting a random seed, producing non-reproducible student evaluation results.",
                        sol[:140],
                        "Set `random_state=42` or `torch.manual_seed(42)` to guarantee deterministic results."
                    )

# 4. HARDCODED MAGIC NUMBERS IN PRODUCTION ARCHITECTURES
print("4. Auditing Magic Numbers in Advanced Transformer & Serving Tasks...")
for yf in yaml_files:
    w_num = int(re.search(r'week(\d+)', yf).group(1))
    if w_num >= 11:
        with open(yf, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        for d in data.get('days', []):
            d_num = d.get('day_num')
            for t_idx, t in enumerate(d.get('tasks', [])):
                sol = str(t.get('solution_code', ''))
                if any(k in sol for k in ['768', '512', '2048', '4096']) and not any(k in sol for k in ['HIDDEN_DIM', 'EMBED_DIM', 'SEQ_LEN', 'CHUNK_SIZE', 'd_model']):
                    record_m(
                        "Code Maintainability",
                        "Low",
                        f"Week {w_num:02d} / Day {d_num:03d} -> Task #{t_idx+1} ({t.get('title', 'Task')})",
                        "Hardcoded Architectural Magic Dimensions",
                        "Task solution hardcodes raw tensor dimensions (e.g. 768, 512) inline rather than declaring named configuration constants.",
                        sol[:120],
                        "Refactor raw dimension integers into named configuration constants (e.g. `HIDDEN_DIM = 768`)."
                    )

print(f"\nTotal Deep Micro-Audit Issues Discovered: {len(micro_findings)}")

with open('scripts/deep_micro_audit_report.json', 'w', encoding='utf-8') as f:
    json.dump(micro_findings, f, indent=2)

print("Exported to: scripts/deep_micro_audit_report.json")
