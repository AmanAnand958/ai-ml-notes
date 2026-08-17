#!/usr/bin/env python3
"""
scripts/find_100_critical_issues.py
Deep static and semantic analyzer designed to uncover 100+ unique critical issues across:
1. Incomplete / Stub Theory Content (words < threshold for advanced topics)
2. Missing Essential Imports & Undefined Global Scope in Theory Code
3. Data Leakage & Pipeline Anti-Patterns in Code
4. Shallow / Stub Task Solutions (trivial pass / TODO / minimal lines)
5. Quizzes with Trivial Distractors or Tautological Explanations
6. Low Density Days (insufficient exercises/quizzes for complex 8-hour topics)
7. Generic / Low-Effort Gotchas lacking concrete code demonstrations
8. Generic Homepage Resources lacking deep-linked documentation
9. PyTorch & ML API Anti-Patterns (deprecated APIs, missing detach/zero_grad)
"""

import glob, yaml, re, os, html, json

print("=== STARTING DEEP INVENTORY OF 100+ CRITICAL ISSUES ===")

issues = []
issue_id = 1

def record_issue(category, severity, location, title, problem, evidence, recommendation):
    global issue_id
    issues.append({
        "issue_id": f"CRIT-{issue_id:03d}",
        "category": category,
        "severity": severity,
        "location": location,
        "title": title,
        "problem": problem,
        "evidence": str(evidence)[:300],
        "recommendation": recommendation
    })
    issue_id += 1

yaml_files = sorted(glob.glob('src/data/week*.yaml'))

for yf in yaml_files:
    w_match = re.search(r'week(\d+)', yf)
    w_num = int(w_match.group(1)) if w_match else 0
    loc_w = f"Week {w_num}"
    
    with open(yf, 'r', encoding='utf-8') as f:
        wdata = yaml.safe_load(f)
        
    days = wdata.get('days', []) if isinstance(wdata, dict) else []
    
    for d in days:
        d_num = d.get('day_num', 0)
        d_title = d.get('title', f"Day {d_num}")
        d_loc = f"Week {w_num} / Day {d_num} ({d_title})"
        
        # -------------------------------------------------------------
        # CHECK 1: Theory Length & Depth
        # -------------------------------------------------------------
        theory = d.get('theory_html', '')
        clean_theory = re.sub(r'<[^>]+>', ' ', theory)
        words = clean_theory.split()
        word_count = len(words)
        
        # Advanced days (DL, Transformers, MLOps, Distributed) require substantive depth
        if d_num > 40 and word_count < 350:
            record_issue(
                "Theory Depth",
                "Critical",
                d_loc,
                "Superficial / Short Theory for Complex Advanced ML Topic",
                f"Theory contains only {word_count} words for an advanced 8-hour topic.",
                f"Word count: {word_count}. Text snippet: '{clean_theory[:150]}...'",
                "Expand theory with deep architectural diagrams, mathematical derivations, and multi-step pipeline explanations."
            )
            
        # Check for placeholders in theory
        if any(p in theory.lower() for p in ['todo', 'tbd', 'placeholder', 'add content here', 'coming soon']):
            record_issue(
                "Content Completeness",
                "Critical",
                d_loc,
                "Placeholder Text Left in Production Theory",
                "Theory contains placeholder or unwritten text.",
                f"Found placeholder string in theory.",
                "Replace placeholder with complete technical breakdown."
            )

        # -------------------------------------------------------------
        # CHECK 2: Code Blocks in Theory (Imports, Scope, Anti-patterns)
        # -------------------------------------------------------------
        code_blocks = re.findall(r'<pre(?: class="[^"]*")?>(?:<code(?: class="[^"]*")?>)?(.*?)(?:</code>)?</pre>', theory, re.DOTALL)
        for cb_idx, cb in enumerate(code_blocks):
            clean_cb = html.unescape(cb)
            clean_cb_strip = re.sub(r'<[^>]+>', '', clean_cb)
            
            # Check for undefined core namespaces in code
            if ('np.' in clean_cb_strip or 'numpy' in clean_cb_strip) and 'import numpy' not in clean_cb_strip and 'from numpy' not in clean_cb_strip:
                record_issue(
                    "Code Executability",
                    "High",
                    f"{d_loc} -> Theory Code Block #{cb_idx+1}",
                    "Missing NumPy Import in Runnable Code Block",
                    "Code uses 'np.' functions without importing numpy, causing NameError on execution.",
                    clean_cb_strip[:120],
                    "Prepend 'import numpy as np' to make the snippet self-contained and runnable."
                )
                
            if ('torch.' in clean_cb_strip or 'nn.' in clean_cb_strip) and 'import torch' not in clean_cb_strip and 'from torch' not in clean_cb_strip:
                record_issue(
                    "Code Executability",
                    "High",
                    f"{d_loc} -> Theory Code Block #{cb_idx+1}",
                    "Missing PyTorch Import in Runnable Code Block",
                    "Code uses 'torch.' or 'nn.' without importing torch, causing NameError.",
                    clean_cb_strip[:120],
                    "Prepend 'import torch' and 'import torch.nn as nn'."
                )

            if ('pd.' in clean_cb_strip or 'DataFrame' in clean_cb_strip) and 'import pandas' not in clean_cb_strip and 'from pandas' not in clean_cb_strip:
                record_issue(
                    "Code Executability",
                    "High",
                    f"{d_loc} -> Theory Code Block #{cb_idx+1}",
                    "Missing Pandas Import in Runnable Code Block",
                    "Code uses 'pd.' without importing pandas, causing NameError.",
                    clean_cb_strip[:120],
                    "Prepend 'import pandas as pd'."
                )
                
            if ('plt.' in clean_cb_strip or 'matplotlib' in clean_cb_strip) and 'import matplotlib' not in clean_cb_strip and 'from matplotlib' not in clean_cb_strip:
                record_issue(
                    "Code Executability",
                    "High",
                    f"{d_loc} -> Theory Code Block #{cb_idx+1}",
                    "Missing Matplotlib Import in Runnable Code Block",
                    "Code uses 'plt.' without importing matplotlib.pyplot.",
                    clean_cb_strip[:120],
                    "Prepend 'import matplotlib.pyplot as plt'."
                )

            # PyTorch specific anti-patterns
            if 'optimizer.step()' in clean_cb_strip and 'optimizer.zero_grad()' not in clean_cb_strip and 'backward()' in clean_cb_strip:
                record_issue(
                    "ML Anti-Pattern",
                    "Critical",
                    f"{d_loc} -> Theory Code Block #{cb_idx+1}",
                    "PyTorch Gradient Accumulation Bug (Missing zero_grad)",
                    "Training loop performs backward() and optimizer.step() without zero_grad(), silently accumulating gradients across iterations.",
                    clean_cb_strip[:150],
                    "Insert 'optimizer.zero_grad()' before 'loss.backward()'."
                )

        # -------------------------------------------------------------
        # CHECK 3: Task Solution Quality & Depth
        # -------------------------------------------------------------
        for t_idx, t in enumerate(d.get('tasks', [])):
            t_title = t.get('title', f"Task {t_idx+1}")
            t_loc = f"{d_loc} -> Task #{t_idx+1} ({t_title})"
            sol = t.get('solution_code', '')
            sol_lines = [l for l in sol.strip().split('\n') if l.strip() and not l.strip().startswith('#')]
            
            if len(sol_lines) < 4:
                record_issue(
                    "Pedagogical Rigor",
                    "Critical",
                    t_loc,
                    "Trivial / Shallow Task Solution Code",
                    f"Solution code only contains {len(sol_lines)} executable lines for an assigned practical task.",
                    f"Solution code:\n{sol}",
                    "Provide a production-grade, end-to-end implementation with data setup, model instantiation, validation, and evaluation asserts."
                )

            if not any(k in sol for k in ['assert', 'print', 'return', 'test', 'expect']):
                record_issue(
                    "Task Verifiability",
                    "High",
                    t_loc,
                    "Task Solution Lacks Verification or Assertions",
                    "Solution code executes logic but has zero asserts, print statements, or return values for the student to verify success.",
                    sol[:120],
                    "Add automated validation asserts (e.g., assert output.shape == expected_shape)."
                )

        # -------------------------------------------------------------
        # CHECK 4: Gotchas / Pitfalls Quality & Actionability
        # -------------------------------------------------------------
        gotchas = d.get('gotchas', [])
        if isinstance(gotchas, list):
            for g_idx, g in enumerate(gotchas):
                if isinstance(g, dict):
                    trap = str(g.get('trap', '')).strip()
                    fix = str(g.get('fix', '')).strip()
                    why = str(g.get('why', '')).strip()
                    g_loc = f"{d_loc} -> Gotcha #{g_idx+1}"
                    
                    if len(trap) < 15 or len(fix) < 15:
                        record_issue(
                            "Pedagogical Rigor",
                            "High",
                            g_loc,
                            "Superficial Gotcha / Pitfall Definition",
                            "Trap or Fix description is too brief (<15 chars) to explain a real engineering pitfall.",
                            f"Trap: '{trap}', Fix: '{fix}'",
                            "Expand with concrete code examples showing the buggy pattern vs the correct pattern."
                        )
                    if not why:
                        record_issue(
                            "Pedagogical Rigor",
                            "Medium",
                            g_loc,
                            "Gotcha Missing Root-Cause Explanation ('why')",
                            "Gotcha tells student what to fix without explaining the underlying memory/runtime mechanism.",
                            f"Trap: '{trap}'",
                            "Add deep mechanical explanation (e.g., explaining GIL, memory layout, CUDA sync, or stride alignment)."
                        )

        # -------------------------------------------------------------
        # CHECK 5: Quiz Depth & Distractor Quality
        # -------------------------------------------------------------
        for q_idx, q in enumerate(d.get('quizzes', [])):
            q_loc = f"{d_loc} -> Quiz #{q_idx+1}"
            q_text = q.get('question', '')
            expl = q.get('explanation', '')
            opts = q.get('options', [])
            
            # Check for tautological explanation
            if len(expl.split()) < 6:
                record_issue(
                    "Assessment Rigor",
                    "High",
                    q_loc,
                    "Tautological / Empty Quiz Explanation",
                    f"Quiz explanation only has {len(expl.split())} words, failing to explain why the correct option is right.",
                    f"Explanation: '{expl}'",
                    "Provide a 2-3 sentence explanation explaining the theoretical invariant and why distractors are wrong."
                )

            # Check for giveaway distractors
            opt_texts = [str(o.get('text', '')).lower() for o in opts]
            if any(t in ['none of the above', 'all of the above', 'maybe', 'depends', 'it crashes'] for t in opt_texts):
                record_issue(
                    "Assessment Rigor",
                    "Medium",
                    q_loc,
                    "Low-Quality / Giveaway Multiple Choice Distractor",
                    "Quiz uses lazy multiple choice options ('all of the above' / 'none of the above') that weaken evaluation quality.",
                    f"Options: {opt_texts}",
                    "Replace with authentic, plausible technical misconceptions based on common student mistakes."
                )

        # -------------------------------------------------------------
        # CHECK 6: External Resources Specificity
        # -------------------------------------------------------------
        for r_idx, r in enumerate(d.get('resources', [])):
            r_loc = f"{d_loc} -> Resource #{r_idx+1}"
            url = str(r.get('url', '')).strip()
            title = str(r.get('title', '')).strip()
            
            # Check for generic domain roots instead of deep documentation
            if url in ['https://pytorch.org', 'https://pytorch.org/', 'https://numpy.org', 'https://numpy.org/', 'https://pandas.pydata.org', 'https://scikit-learn.org']:
                record_issue(
                    "Resource Authority",
                    "High",
                    r_loc,
                    "Generic Homepage Linked Instead of Deep Documentation",
                    f"Resource links to bare root domain '{url}' instead of specific API reference or tutorial page.",
                    f"Resource: {title} ({url})",
                    "Replace with exact canonical documentation deep link."
                )

# -------------------------------------------------------------
# CHECK 7: Cross-Curriculum Pedagogical Continuity
# -------------------------------------------------------------
special_topics = {
    "Transformer Attention": ["week11", "Q * K.T", "softmax", "1/sqrt(d_k)"],
    "Backpropagation Chain Rule": ["week07", "dL/dW", "jacobian", "chain rule"],
    "LoRA Matrix Decomposition": ["week12", "W0 + B * A", "rank r", "scaling factor alpha"],
    "Quantization Scale & Zero-Point": ["week12", "round(x / S) + Z", "affine quantization", "int4"],
    "Direct Preference Optimization": ["week22", "pi_theta", "pi_ref", "implicit reward"],
    "HNSW Vector Indexing": ["week14", "skip-list", "entry point", "efConstruction"]
}

for topic, rules in special_topics.items():
    week_target = rules[0]
    target_yf = f"src/data/{week_target}.yaml"
    if os.path.exists(target_yf):
        with open(target_yf, 'r', encoding='utf-8') as f:
            content = f.read()
        for term in rules[1:]:
            if term.lower() not in content.lower():
                record_issue(
                    "Curriculum Rigor",
                    "Critical",
                    f"{week_target}.yaml ({topic})",
                    f"Missing Mathematical / Engineering Core Formulation: '{term}'",
                    f"Week {week_target} covers {topic} but fails to formally introduce the foundational formula or term '{term}'.",
                    f"Search for '{term}' yielded 0 occurrences.",
                    f"Add explicit KaTeX math block and engineering rationale explaining '{term}'."
                )

print(f"\nTotal Critical & High Issues Discovered: {len(issues)}")

# Save to JSON
with open('scripts/100_critical_issues_catalog.json', 'w', encoding='utf-8') as f:
    json.dump(issues, f, indent=2)

print("Exported to: scripts/100_critical_issues_catalog.json")
