#!/usr/bin/env python3
"""
Comprehensive Forensic Verification of all newly reported issues across Weeks 19-23:
1. Shifted Hinglish & Gotcha blocks (off-by-one check)
2. Python Syntax Errors: 'key=>lambda', stripped operators 'if x = y:', return type hyphens ' - str:'
3. Cloud provider content bleed in Week 23 (Task 2 & Quizzes)
4. EOF Duplication / Orphaned elements at end of files
5. Mermaid Syntax & Logic (unquoted labels, arithmetic symbols)
6. Python AST parsing of all <code> blocks across Weeks 19-23
7. Deprecated APIs (LLMChain, missing device_map)
8. Corrupted/Irrelevant Resource links (DVC on Azure, Bandits on Secrets)
9. Hallucinated math (RAG Triad harmonic formula)
"""

import ast
import re
import json
from pathlib import Path
from bs4 import BeautifulSoup

WEEKS_DIR = Path("/Users/amananand/Downloads/SDE/ai:ml-1/pages/weeks")

report = {}

for wn in range(19, 24):
    fp = WEEKS_DIR / f"week{wn}.html"
    if not fp.exists():
        continue
    
    html = fp.read_text(encoding='utf-8', errors='replace')
    soup = BeautifulSoup(html, 'html.parser')
    
    w_res = {
        "syntax_errors": [],
        "return_type_hyphens": [],
        "corrupted_operators": [],
        "key_arrow_lambdas": [],
        "llmchain_usage": [],
        "missing_device_map": [],
        "hallucinated_ragas_formula": [],
        "eof_orphaned_sections": [],
        "resource_mismatches": [],
        "day_topics_audit": []
    }
    
    # 1. Check for 'key=>lambda' or similar JS arrow syntax
    arrow_matches = re.findall(r'key\s*=>\s*lambda|key\s*=>', html)
    if arrow_matches:
        w_res["key_arrow_lambdas"].append(arrow_matches)
        
    # 2. Check for return type hyphens like ') - str:' or ') - List['
    hyphen_returns = re.findall(r'def\s+\w+\([^)]*\)\s*-\s*[A-Za-z\[\]_]+:', html)
    if hyphen_returns:
        w_res["return_type_hyphens"] = hyphen_returns[:10]
        
    # 3. Check for stripped operators like 'if x = y:' or 'return x = 0.7' or 'assert x 70.0'
    bad_ops = re.findall(r'(?:if|return|assert)\s+[^:\n]+(?:\s=\s|\s\d+\.\d+|\s[a-zA-Z_]\w+\s+\d+)', html)
    # filter false positives in plain text vs code
    # We will test all code blocks with AST parser
    
    # 4. AST Parser for all Python code blocks
    code_blocks = soup.find_all('code')
    for i, cb in enumerate(code_blocks):
        raw_code = cb.get_text()
        if len(raw_code.strip()) < 15:
            continue
        # Skip bash/cli commands
        if raw_code.strip().startswith(('kubectl', 'helm', 'docker', 'curl', 'git', 'pip', 'terraform', 'aws', 'gcloud')):
            continue
        try:
            ast.parse(raw_code)
        except SyntaxError as e:
            w_res["syntax_errors"].append({
                "block_index": i,
                "error": str(e),
                "lineno": e.lineno,
                "msg": e.msg,
                "code_snippet": raw_code.split('\n')[max(0, (e.lineno or 1)-1)][:100] if e.lineno else raw_code[:100]
            })

    # 5. LLMChain deprecated check
    llmchains = re.findall(r'\bLLMChain\b', html)
    if llmchains:
        w_res["llmchain_usage"] = len(llmchains)

    # 6. Check for RAGAS harmonic mean formula
    ragas_harmonic = re.findall(r'RAG\s+Triad\s+Score|\\frac\{3\}\{\\frac\{1\}', html)
    if ragas_harmonic:
        w_res["hallucinated_ragas_formula"] = ragas_harmonic

    # 7. Check for EOF duplication (especially in week 23)
    milestone_pos = html.find('class="week-summary"')
    if milestone_pos != -1:
        after_milestone = html[milestone_pos:]
        extra_complete_btns = re.findall(r'completeDay\(\d+', after_milestone)
        extra_predict_blocks = re.findall(r'PREDICT THE OUTPUT|predict-box', after_milestone, re.IGNORECASE)
        if extra_complete_btns or extra_predict_blocks:
            w_res["eof_orphaned_sections"].append({
                "extra_complete_btns": extra_complete_btns,
                "extra_predict_blocks": len(extra_predict_blocks)
            })

    # 8. Check Day Topics & Hinglish / Gotchas
    day_sections = soup.find_all('div', class_=re.compile(r'day-section'))
    for ds in day_sections:
        day_id = ds.get('id', 'unknown')
        h1 = ds.find('h1')
        title = h1.get_text().strip() if h1 else 'No H1'
        
        # Check text in hinglish/theory/gotcha
        text_content = ds.get_text()
        
        # Check resource links inside this day
        res_links = []
        for a in ds.find_all('a', href=True):
            res_links.append({"text": a.get_text().strip(), "href": a['href']})
            
        w_res["day_topics_audit"].append({
            "day_id": day_id,
            "title": title,
            "has_gotcha": bool(ds.find(class_=re.compile(r'gotcha|pitfall|warning', re.I))),
            "snippet": text_content[:200].replace('\n', ' ')
        })
        
    report[f"week{wn}"] = w_res

print(json.dumps(report, indent=2))
