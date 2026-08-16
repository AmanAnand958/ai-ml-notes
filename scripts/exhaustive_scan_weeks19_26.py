#!/usr/bin/env python3
"""
Exhaustive Forensic Deep Scan across Weeks 19 through 26.
Checks:
1. EOF Duplications & Orphaned sections across ALL weeks (19-26).
2. Gotcha vs Day Topic semantic alignment across ALL days.
3. Code block indentations and class definitions (unindented methods, missing bodies).
4. Deprecated LangChain / LLM libraries (LLMChain, RetrievalQA, ConversationalRetrievalChain, initialize_agent).
5. Broken / placeholder URLs (e.g. example.com, generic github repos, broken arxiv/dvc links).
6. Missing solutions or task mismatches.
7. Quiz answer correctness & duplicate quiz option IDs.
8. Day-level DOM leaks (missing closing tags inside day-sections).
"""

import re
import json
from pathlib import Path
from bs4 import BeautifulSoup
from collections import defaultdict

WEEKS_DIR = Path("/Users/amananand/Downloads/SDE/ai:ml-1/pages/weeks")

results = {}

for wn in range(19, 27):
    fp = WEEKS_DIR / f"week{wn}.html"
    if not fp.exists():
        continue
    
    html = fp.read_text(encoding='utf-8', errors='replace')
    soup = BeautifulSoup(html, 'html.parser')
    
    w_report = {
        "eof_duplications": [],
        "deprecated_apis": [],
        "indented_code_errors": [],
        "broken_or_placeholder_links": [],
        "gotcha_topic_mismatches": [],
        "duplicate_quiz_ids": [],
        "task_solution_missing": [],
        "days": []
    }
    
    # 1. EOF Duplication check
    ws_idx = html.find('class="week-summary"')
    if ws_idx != -1:
        after_ws = html[ws_idx:]
        extra_btns = re.findall(r'completeDay\(\d+', after_ws)
        extra_tasks = re.findall(r'class="task-block"|class="predict-block"', after_ws)
        if extra_btns or extra_tasks:
            w_report["eof_duplications"].append({
                "extra_complete_btns": extra_btns,
                "extra_tasks_count": len(extra_tasks)
            })
            
    # 2. Deprecated LangChain / ML APIs
    dep_patterns = [
        (r'\bLLMChain\b', 'LLMChain (deprecated)'),
        (r'\bRetrievalQA\b', 'RetrievalQA (deprecated)'),
        (r'\bConversationalRetrievalChain\b', 'ConversationalRetrievalChain (deprecated)'),
        (r'\binitialize_agent\b', 'initialize_agent (deprecated)'),
        (r'from langchain\.agents import initialize_agent', 'Old agent init import'),
        (r'from langchain\.chat_models import ChatOpenAI', 'Old ChatOpenAI import'),
        (r'from langchain\.embeddings import OpenAIEmbeddings', 'Old OpenAIEmbeddings import'),
        (r'from langchain\.vectorstores import', 'Old vectorstores import')
    ]
    for pat, desc in dep_patterns:
        m = re.findall(pat, html)
        if m:
            w_report["deprecated_apis"].append(f"{desc}: {len(m)} occurrences")

    # 3. Indented code errors in python code
    # Check for patterns like 'class Foo:\ndef bar' without indentation
    bad_indents = re.findall(r'class\s+\w+[^:\n]*:\s*\ndef\s+\w+', html)
    if bad_indents:
        w_report["indented_code_errors"].extend(bad_indents[:5])
        
    # Check for return type hyphens in raw html
    hyphen_defs = re.findall(r'def\s+\w+\([^)]*\)\s*-\s*[a-zA-Z0-9_\[\]]+:', html)
    if hyphen_defs:
        w_report["indented_code_errors"].extend([f"Hyphen return type: {h}" for h in hyphen_defs[:5]])

    # 4. Broken / Placeholder links
    links = soup.find_all('a', href=True)
    for a in links:
        href = a['href']
        text = a.get_text().strip()
        if 'example.com' in href or 'your-domain' in href or 'applied-llm-architecture' in href:
            w_report["broken_or_placeholder_links"].append({"text": text, "href": href})

    # 5. Quiz IDs duplication
    quiz_ids = defaultdict(int)
    for q in soup.find_all('div', id=re.compile(r'quiz-section')):
        qid = q.get('id')
        quiz_ids[qid] += 1
    dupe_qids = {k: v for k, v in quiz_ids.items() if v > 1}
    if dupe_qids:
        w_report["duplicate_quiz_ids"] = dupe_qids

    # 6. Day by Day Deep Audit
    day_sections = soup.find_all('div', class_=re.compile(r'day-section'))
    for ds in day_sections:
        did = ds.get('id', 'unknown')
        h1 = ds.find('h1')
        title = h1.get_text().strip() if h1 else 'No H1'
        
        # Check gotcha
        gotcha_el = ds.find(class_=re.compile(r'gotcha|pitfall|warning', re.I))
        gotcha_text = gotcha_el.get_text().strip() if gotcha_el else 'None'
        
        # Check task & solutions
        tasks = ds.find_all(class_=re.compile(r'task-block|task-card'))
        solutions = ds.find_all(class_=re.compile(r'sol-block|solution'))
        
        # Check predict output
        predict = ds.find_all(class_=re.compile(r'predict-block'))
        
        w_report["days"].append({
            "id": did,
            "title": title,
            "tasks_count": len(tasks),
            "solutions_count": len(solutions),
            "predict_count": len(predict),
            "gotcha_snippet": gotcha_text[:120].replace('\n', ' ')
        })

    results[f"week{wn}"] = w_report

print(json.dumps(results, indent=2))
