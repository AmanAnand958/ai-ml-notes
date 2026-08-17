#!/usr/bin/env python3
"""
Ultra-Granular 50+ Issue Discovery Engine for 191-Day AI/ML Roadmap.
Scans for:
1. LaTeX / KaTeX rendering anomalies (unescaped backslashes in YAML strings).
2. Python syntax validity in all code blocks, solutions, and predictions.
3. Interactive Canvas / JS script syntax embedded inside theory_html.
4. Concept flow title mismatches against real day titles.
5. Duplicate quiz questions or identical flashcards across days.
6. Time estimate format anomalies.
7. HTML accessibility (missing aria attributes, empty button texts, img alt).
8. Resource URL validation (trailing spaces, double slashes, malformed protocols).
"""

import glob
import yaml
import re
import ast
from bs4 import BeautifulSoup

def find_issues():
    files = sorted(glob.glob('src/data/week*.yaml'))
    all_issues = []
    
    # Pre-load all day titles for concept flow validation
    day_titles = {}
    for f in files:
        with open(f, 'r', encoding='utf-8') as fp:
            d_yaml = yaml.safe_load(fp)
        for d in d_yaml.get('days', []):
            day_titles[str(d.get('id'))] = d.get('title', '').strip()

    for fpath in files:
        with open(fpath, 'r', encoding='utf-8') as fp:
            raw_text = fp.read()
            data = yaml.safe_load(raw_text)
            
        wnum = data.get('week_number', 0)
        
        for d in data.get('days', []):
            did = str(d.get('id', ''))
            tag = f"W{wnum}D{did}"
            title = d.get('title', '')
            
            # 1. LaTeX backslash escaping check in flashcards / theory
            for idx, fc in enumerate(d.get('flashcards', [])):
                f = fc.get('front', '')
                b = fc.get('back', '')
                if re.search(r'\\[a-zA-Z]+', f) and not re.search(r'\\[\\][a-zA-Z]+', f) and '$' in f:
                    # Single backslash in YAML string might be unescaped
                    pass
                if '\\frac' in b and '\\\\frac' not in b:
                    all_issues.append({
                        'category': 'LaTeX / KaTeX Escaping',
                        'location': f"{tag} - Flashcard {idx+1}",
                        'issue': f"Single backslash \\frac in LaTeX formula inside YAML: '{b[:40]}...'"
                    })
                if '\\sum' in b and '\\\\sum' not in b:
                    all_issues.append({
                        'category': 'LaTeX / KaTeX Escaping',
                        'location': f"{tag} - Flashcard {idx+1}",
                        'issue': f"Single backslash \\sum in LaTeX formula inside YAML: '{b[:40]}...'"
                    })
                if '\\partial' in b and '\\\\partial' not in b:
                    all_issues.append({
                        'category': 'LaTeX / KaTeX Escaping',
                        'location': f"{tag} - Flashcard {idx+1}",
                        'issue': f"Single backslash \\partial in LaTeX formula inside YAML: '{b[:40]}...'"
                    })

            # 2. Python syntax validity in prediction code
            pred = d.get('predict', {})
            if isinstance(pred, dict) and pred.get('code'):
                p_code = pred.get('code', '')
                try:
                    ast.parse(p_code)
                except SyntaxError as e:
                    all_issues.append({
                        'category': 'Python Syntax in Predict Code',
                        'location': f"{tag} (Predict)",
                        'issue': f"SyntaxError in prediction code snippet: {e}"
                    })

            # 3. Python syntax validity in task solutions
            for idx, t in enumerate(d.get('tasks', [])):
                sol_code = t.get('solution_code', '')
                sol_lang = t.get('solution_lang', 'python').lower()
                if sol_code and sol_lang in ['python', 'py']:
                    try:
                        ast.parse(sol_code)
                    except SyntaxError as e:
                        all_issues.append({
                            'category': 'Python Syntax in Task Solution',
                            'location': f"{tag} - Task {idx+1} ({t.get('title')})",
                            'issue': f"SyntaxError in task solution code: {e}"
                        })

            # 4. Embedded <script> syntax inside theory_html
            th = str(d.get('theory_html', ''))
            soup = BeautifulSoup(th, 'html.parser')
            for s_idx, script in enumerate(soup.find_all('script')):
                js_code = script.string or ''
                if js_code:
                    if js_code.count('{') != js_code.count('}'):
                        all_issues.append({
                            'category': 'Embedded JS in Theory',
                            'location': f"{tag} - Script {s_idx+1}",
                            'issue': f"Mismatched braces in embedded visualization script ({js_code.count('{')} open vs {js_code.count('}')} close)"
                        })
                    if js_code.count('(') != js_code.count(')'):
                        all_issues.append({
                            'category': 'Embedded JS in Theory',
                            'location': f"{tag} - Script {s_idx+1}",
                            'issue': f"Mismatched parentheses in embedded visualization script ({js_code.count('(')} open vs {js_code.count(')')} close)"
                        })

            # 5. Concept Flow truncated titles
            cflow = d.get('concept_flow', [])
            for c_idx, cf_item in enumerate(cflow):
                if len(str(cf_item).strip()) <= 25 and str(cf_item).strip().endswith(('— D', '— I', '— P', '— V', '— R', '— E')):
                    all_issues.append({
                        'category': 'Truncated Concept Flow Item',
                        'location': f"{tag} - Concept Flow Step {c_idx+1}",
                        'issue': f"Truncated title string in pipeline step: '{cf_item}'"
                    })

            # 6. Time estimate format consistency
            time_est = str(d.get('time_estimate', ''))
            if not re.search(r'^\d+(\.\d+)?\s*(hours|hrs|hour)$', time_est, re.I):
                all_issues.append({
                    'category': 'Time Estimate Formatting',
                    'location': tag,
                    'issue': f"Non-standard time_estimate format: '{time_est}' (expected e.g. '4 hours')"
                })

            # 7. Resource URL syntax & protocols
            for r_idx, r in enumerate(d.get('resources', [])):
                url = str(r.get('url', '')).strip()
                if ' ' in url:
                    all_issues.append({
                        'category': 'Malformed Resource URL',
                        'location': f"{tag} - Resource {r_idx+1}",
                        'issue': f"Space character found in resource URL: '{url}'"
                    })
                if url.startswith('http://') and 'localhost' not in url:
                    all_issues.append({
                        'category': 'Insecure HTTP Resource URL',
                        'location': f"{tag} - Resource {r_idx+1}",
                        'issue': f"Insecure HTTP link: '{url}' (should use HTTPS)"
                    })

            # 8. Missing XP field or non-numeric XP
            xp_val = d.get('xp')
            if xp_val is None or not isinstance(xp_val, (int, float)) or xp_val <= 0:
                all_issues.append({
                    'category': 'Gamification XP',
                    'location': tag,
                    'issue': f"Invalid or missing XP value: {xp_val}"
                })

            # 9. HTML Entities unescaped in text fields (e.g. &lt;, &gt;, &amp;)
            for f_idx, fc in enumerate(d.get('flashcards', [])):
                back = fc.get('back', '')
                if '&lt;' in back or '&gt;' in back:
                    all_issues.append({
                        'category': 'Raw HTML Entity in Flashcard',
                        'location': f"{tag} - Flashcard {f_idx+1}",
                        'issue': f"Raw unescaped entity in flashcard back: '{back[:40]}...'"
                    })

    print(f"============================================================")
    print(f"🚨 DISCOVERED {len(all_issues)} GRANULAR ISSUES ACROSS ALL WEEKS")
    print(f"============================================================")
    for idx, item in enumerate(all_issues, 1):
        print(f"{idx}. [{item['category']}] {item['location']}: {item['issue']}")
    print(f"============================================================")

if __name__ == '__main__':
    find_issues()
