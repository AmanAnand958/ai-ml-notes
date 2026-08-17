#!/usr/bin/env python3
"""
scripts/fix_final_cleanups.py
Fixes final 6 items:
1. Fix Day 15 Task 0 string formatting in src/data/week03.yaml
2. Balance <pre> tags in week2.html
3. Update resources.html Week 26 link
4. Update omni_audit_master.py to only parse Python language solutions for Python AST
5. Clean duplicate resource URLs
"""

import yaml, os, re, glob

# 1. Fix week03.yaml Day 15 Task 0
with open('src/data/week03.yaml', 'r', encoding='utf-8') as f:
    w3 = yaml.safe_load(f)
for d in w3.get('days', []):
    if d.get('day_num') == 15:
        for t in d.get('tasks', []):
            if 'Missing Value Report' in t.get('title', ''):
                t['solution_code'] = '''import pandas as pd

url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
df = pd.read_csv(url)

def missing_report(df):
    missing_count = df.isnull().sum()
    missing_pct = (missing_count / len(df) * 100).round(2)
    report = pd.DataFrame({
        "Missing": missing_count,
        "Percent": missing_pct
    })
    report = report[report["Missing"] > 0].sort_values("Percent", ascending=False)
    header = "{:<15} {:<8} {:<8} {:<18} {:<12}".format("Column", "Missing", "Percent", "Flag", "Rec")
    print(header)
    print("=" * 60)
    for col in report.index:
        pct = report.loc[col, "Percent"]
        flag = "DROP CANDIDATE" if pct > 50 else ""
        dtype = df[col].dtype
        if dtype in ["int64", "float64"] and pct <= 50:
            rec = "median" if abs(df[col].skew()) > 1 else "mean"
        elif pct <= 50:
            rec = "most_frequent"
        else:
            rec = "-"
        print("{:<15} {:<8} {:<8} {:<18} {:<12}".format(col, int(report.loc[col, "Missing"]), pct, flag, rec))

missing_report(df)'''
with open('src/data/week03.yaml', 'w', encoding='utf-8') as f:
    yaml.dump(w3, f, allow_unicode=True, sort_keys=False, width=1000)

# 2. Balance <pre> in week2.html
with open('pages/weeks/week2.html', 'r', encoding='utf-8') as f:
    w2_html = f.read()

# Find all <pre> and </pre> indices and remove the first extra </pre> without matching <pre>
pre_opens = [m.start() for m in re.finditer(r'<pre\b', w2_html, re.IGNORECASE)]
pre_closes = [m.start() for m in re.finditer(r'</pre>', w2_html, re.IGNORECASE)]
if len(pre_closes) > len(pre_opens):
    diff = len(pre_closes) - len(pre_opens)
    # Remove the last `diff` closing tags that are duplicated
    w2_html = w2_html.replace('</pre>\n              <pre>', '<pre>')
    # Rebalance
    opens = len(re.findall(r'<pre\b', w2_html, re.IGNORECASE))
    closes = len(re.findall(r'</pre>', w2_html, re.IGNORECASE))
    if closes > opens:
        # Remove first extra </pre>
        for _ in range(closes - opens):
            pos = w2_html.rfind('</pre>')
            w2_html = w2_html[:pos] + w2_html[pos+6:]
    with open('pages/weeks/week2.html', 'w', encoding='utf-8') as f:
        f.write(w2_html)

# 3. Update resources.html
with open('resources.html', 'r', encoding='utf-8') as f:
    res = f.read()
if 'week26.html' not in res:
    res = res.replace('week25.html">Week 25</a>', 'week25.html">Week 25</a>\n      <a class="pill" href="pages/weeks/week26.html">Week 26</a>')
    with open('resources.html', 'w', encoding='utf-8') as f:
        f.write(res)

# 4. Clean duplicate resource URLs in YAML
for yf in sorted(glob.glob('src/data/week*.yaml')):
    with open(yf, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    modified = False
    for d in data.get('days', []):
        seen = set()
        clean_res = []
        for r in d.get('resources', []):
            url = r.get('url', '')
            if url and url not in seen:
                seen.add(url)
                clean_res.append(r)
            elif not url:
                clean_res.append(r)
            else:
                modified = True
        d['resources'] = clean_res
    if modified:
        with open(yf, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, allow_unicode=True, sort_keys=False, width=1000)

# 5. Update omni_audit_master.py to respect solution_lang and markdown
with open('scripts/omni_audit_master.py', 'r', encoding='utf-8') as f:
    audit_script = f.read()

audit_script = audit_script.replace(
    "if sol_code:\n                clean_sol = clean_for_ast(sol_code)\n                try:\n                    ast.parse(clean_sol)",
    "lang = str(t.get('solution_lang', 'python')).lower()\n            if sol_code and lang in ['python', 'py']:\n                clean_sol = clean_for_ast(sol_code)\n                try:\n                    ast.parse(clean_sol)"
)

with open('scripts/omni_audit_master.py', 'w', encoding='utf-8') as f:
    f.write(audit_script)

print("Final cleanups applied.")
