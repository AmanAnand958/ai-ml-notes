#!/usr/bin/env python3
"""
scripts/sync_yaml_predict_to_html.py
Reads updated authentic predict blocks from src/data/week*.yaml
and updates all predict sections across pages/weeks/week*.html.
"""

import os, glob, yaml, re, html

def sync_predict_to_html():
    print("Syncing updated predict blocks from YAML to HTML...")
    yaml_files = sorted(glob.glob('src/data/week*.yaml'))
    
    for yf in yaml_files:
        week_num_str = re.search(r'week(\d+)\.yaml', yf).group(1)
        week_num = int(week_num_str)
        html_file = f'pages/weeks/week{week_num}.html'
        
        if not os.path.exists(html_file):
            continue
            
        with open(yf, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
            
        days = data.get('days', []) if isinstance(data, dict) else []
        for d in days:
            d_num = d.get('day_num')
            predict = d.get('predict')
            if not predict or not d_num:
                continue
                
            q_text = html.escape(predict.get('question', ''))
            ans_text = str(predict.get('answer', ''))
            expl_text = html.escape(predict.get('explanation', ''))
            code_text = html.escape(predict.get('code', ''))
            
            # Find predict container for this day: id="p{d_num}" or "pred-d{d_num}"
            pattern = re.compile(
                r'(<div class="predict-box"[^>]*id="predict-' + str(d_num) + r'".*?'
                r'<p>).*?'
                r'(</p>\s*<input class="predict-input"[^>]*id="p' + str(d_num) + r'-input"[^>]*/>\s*'
                r'<button class="predict-btn" onclick="checkPredict\(\'p' + str(d_num) + r'\',\s*)\'[^\']*\''
                r'(\).*?'
                r'<div class="solution-box" id="pred-d' + str(d_num) + r'".*?'
                r'<p[^>]*>).*?'
                r'(</p>.*?<pre>).*?'
                r'(</pre>.*?</div>\s*</div>\s*</div>)',
                re.DOTALL
            )
            
            def repl(m):
                return (
                    m.group(1) + q_text +
                    m.group(2) + "'" + ans_text.replace("'", "\\'") + "'" +
                    m.group(3) + f"Expected Output: {ans_text}\nExplanation: {expl_text}" +
                    m.group(4) + code_text +
                    m.group(5)
                )
                
            html_content = pattern.sub(repl, html_content)
            
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
            
    print("HTML predict sections successfully synchronized.")

if __name__ == '__main__':
    sync_predict_to_html()
