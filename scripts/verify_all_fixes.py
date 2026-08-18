#!/usr/bin/env python3
"""
verify_all_fixes.py
Verifies that all targeted boilerplate issues have been properly remediated.
"""

import glob
import re
from bs4 import BeautifulSoup

WEEKS_DIR = "pages/weeks"

def verify_production_engine():
    files = glob.glob(f"{WEEKS_DIR}/*.html")
    count = 0
    for f in files:
        html = open(f).read()
        if 'class ProductionEngine:' in html:
            count += html.count('class ProductionEngine:')
    return count

def verify_efficiency_score():
    files = glob.glob(f"{WEEKS_DIR}/*.html")
    count = 0
    for f in files:
        html = open(f).read()
        if 'EfficiencyScore(S) = \sum_{i=1}^{N}' in html:
            count += html.count('EfficiencyScore(S) = \sum_{i=1}^{N}')
        if 'EfficiencyScore(S) = \\sum_{i=1}^{N}' in html:
            count += html.count('EfficiencyScore(S) = \\sum_{i=1}^{N}')
        # Check text format
        if 'EfficiencyScore' in html and 'Throughput_i' in html and 'Latency_i' in html:
            # Let's count exact matches of the old boilerplate
            count += len(re.findall(r'\\text\{EfficiencyScore\}\(S\)\s*=\s*\\sum', html))
    return count

def verify_decision_matrix():
    files = glob.glob(f"{WEEKS_DIR}/*.html")
    count = 0
    for f in files:
        html = open(f).read()
        # Look for the exact old boilerplate
        if 'Low initial complexity &amp; rapid prototyping' in html and 'Sub-optimal scaling under high concurrency' in html:
            count += html.count('Low initial complexity &amp; rapid prototyping')
    return count

def verify_resource_links():
    files = glob.glob(f"{WEEKS_DIR}/*.html")
    links = set()
    for f in files:
        html = open(f).read()
        soup = BeautifulSoup(html, 'html.parser')
        for a in soup.find_all('a', class_='resource-card'):
            links.add(a.get('href'))
    return len(links)

def verify_pyodide_mocks():
    files = glob.glob(f"{WEEKS_DIR}/*.html")
    unmocked = 0
    for f in files:
        html = open(f).read()
        for match in re.finditer(r'(<pre(?:[^>]*)>)(?:<code(?:[^>]*)>)?(.*?)(?:</code>)?</pre>', html, re.DOTALL):
            code_content = match.group(2)
            bad_imports = []
            if re.search(r'^\s*(import|from)\s+torch\b', code_content, re.MULTILINE): bad_imports.append('torch')
            if re.search(r'^\s*(import|from)\s+mlflow\b', code_content, re.MULTILINE): bad_imports.append('mlflow')
            if re.search(r'^\s*(import|from)\s+faiss\b', code_content, re.MULTILINE): bad_imports.append('faiss')
            if re.search(r'^\s*(import|from)\s+boto3\b', code_content, re.MULTILINE): bad_imports.append('boto3')
            
            if bad_imports:
                if 'sys.modules[' not in code_content or 'MagicMock' not in code_content:
                    unmocked += 1
    return unmocked

def main():
    print("========================================")
    print("        REMEDIATION VERIFICATION        ")
    print("========================================")
    
    pe_count = verify_production_engine()
    print(f"[1] ProductionEngine Stubs: {pe_count} remaining (Expected: 0)")
    
    es_count = verify_efficiency_score()
    print(f"[2] EfficiencyScore Stubs: {es_count} remaining (Expected: 0)")
    
    dm_count = verify_decision_matrix()
    print(f"[3] Boilerplate Decision Matrices: {dm_count} remaining (Expected: 0)")
    
    rl_count = verify_resource_links()
    print(f"[4] Unique Resource Links: {rl_count} total (Expected: > 26)")
    
    pm_count = verify_pyodide_mocks()
    print(f"[5] Unmocked Pyodide Imports (torch/faiss/mlflow/boto3): {pm_count} remaining (Expected: 0)")
    
    print("========================================")
    if pe_count == 0 and es_count == 0 and dm_count == 0 and rl_count > 26 and pm_count == 0:
        print("✅ ALL FIXES SUCCESSFULLY VERIFIED!")
    else:
        print("❌ SOME FIXES FAILED OR ARE INCOMPLETE.")
        
if __name__ == '__main__':
    main()
