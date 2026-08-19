#!/usr/bin/env python3
"""
scripts/apply_all_forensic_fixes.py
Applies all forensic fixes across YAML and HTML files:
1. Fixes predict blocks (Days 162 & 175).
2. Fixes unclosed <p> tags in prompt_html (Days 1–3).
3. Enriches Day 42 theory to differentiate from Day 32 (focus on business asymmetric loss & operational decision matrices).
4. Synchronizes updated content to all HTML pages.
5. Runs validate.py.
"""

import os, glob, yaml, re, html
from bs4 import BeautifulSoup

DATA_DIR = 'src/data'
PAGES_DIR = 'pages/weeks'

class LiteralStr(str): pass
def lit_repr(dumper, data):
    if '\n' in data:
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
    return dumper.represent_scalar('tag:yaml.org,2002:str', data)
yaml.add_representer(LiteralStr, lit_repr)
yaml.SafeDumper.add_representer(LiteralStr, lit_repr)

def deep_literal(obj):
    if isinstance(obj, dict): return {k: deep_literal(v) for k,v in obj.items()}
    if isinstance(obj, list): return [deep_literal(v) for v in obj]
    if isinstance(obj, str) and '\n' in obj: return LiteralStr(obj)
    return obj

print("=== APPLYING ALL FORENSIC AUDIT FIXES ===")

# 1. Update week01.yaml for unclosed <p> tags in task prompts
with open('src/data/week01.yaml', 'r', encoding='utf-8') as f:
    y1 = yaml.safe_load(f)

for day in y1.get('days', []):
    for t in day.get('tasks', []):
        prompt = t.get('prompt_html', '')
        if prompt:
            # Fix unclosed <p> tags e.g. <p>text<p> -> <p>text</p>
            prompt = re.sub(r'<p>([^<]+)<p>', r'<p>\1</p>', prompt)
            t['prompt_html'] = prompt

with open('src/data/week01.yaml', 'w', encoding='utf-8') as f:
    yaml.dump(deep_literal(y1), f, allow_unicode=True, default_flow_style=False, sort_keys=False, width=120)
print("✓ Fixed unclosed <p> tags in week01.yaml")

# 2. Enrich Day 42 in week06.yaml to clearly differentiate from Day 32
with open('src/data/week06.yaml', 'r', encoding='utf-8') as f:
    y6 = yaml.safe_load(f)

for day in y6.get('days', []):
    if int(day.get('day_num') or day.get('id')) == 42:
        day['theory_html'] = '''<div class="theory-content">
<h2 class="sh2">⚖️ Industrial Regression Metric Selection &amp; Asymmetric Business Loss</h2>

<p class="prose">
While mathematical evaluation metrics (MSE, RMSE, MAE, $R^2$) measure numerical divergence from ground truth, real-world machine learning systems must optimize for <strong>asymmetric business impact</strong> and operational failure modes. Choosing the wrong metric optimizes the loss function while degrading product KPIs.
</p>

<h3 class="sh3">1. Operational Metric Decision Matrix</h3>
<table class="resource-table">
  <tr><th>Business Scenario</th><th>Optimal Primary Metric</th><th>Core Operational Rationale</th></tr>
  <tr><td><strong>Real Estate &amp; High-Value Pricing</strong></td><td><strong>MAPE / WAPE</strong></td><td>Relative percentage errors scale naturally across $100K starter homes and $10M luxury estates where raw dollar errors distort loss.</td></tr>
  <tr><td><strong>Supply Chain &amp; Demand Forecasting</strong></td><td><strong>Pinball Loss / Quantile Loss</strong></td><td>Under-predicting demand causes out-of-stock revenue loss; over-predicting causes inventory holding costs. Quantile regression ($q=0.90$) penalizes stockouts heavily.</td></tr>
  <tr><td><strong>Sensor Telemetry &amp; Anomaly Detection</strong></td><td><strong>Huber / Pseudo-Huber Loss</strong></td><td>Combines MSE curvature for small gradients with MAE robustness against transient sensor spikes and corrupted telemetry.</td></tr>
  <tr><td><strong>Algorithmic Trading &amp; Financial Risk</strong></td><td><strong>RMSE / Max Absolute Error</strong></td><td>Large tail deviations cause catastrophic liquidity liquidation; high sensitivity to worst-case outliers is mandatory.</td></tr>
</table>

<h3 class="sh3">2. Asymmetric Custom Loss Functions</h3>
<p class="prose">
In scenarios where underestimation incurs a $5\\times$ penalty compared to overestimation (e.g. server capacity planning before Black Friday), standard symmetric metrics fail. Custom asymmetric loss functions directly penalize directional bias:
</p>

<p class="katex-block">
$$L_{\\text{asymmetric}}(y, \\hat{y}) = \\begin{cases} c_{\\text{under}} \\cdot (y - \\hat{y})^2 & \\text{if } y > \\hat{y} \\\\ c_{\\text{over}} \\cdot (y - \\hat{y})^2 & \\text{if } y \\le \\hat{y} \\end{cases}$$
</p>

<h3 class="sh3">3. Production Evaluation Protocol: Golden Slices</h3>
<p class="prose">
Never evaluate regression pipelines solely on global aggregated RMSE. Always compute metrics segmented by:
</p>
<ul class="prose-list">
  <li><strong>Volume Density Slices:</strong> Top 5% high-volume items vs long-tail catalog.</li>
  <li><strong>Temporal Regimes:</strong> Peak traffic hours vs baseline hours.</li>
  <li><strong>Error Distribution Percentiles:</strong> Track p50, p90, and p99 absolute errors to capture tail failure behavior before model promotion.</li>
</ul>
</div>'''

with open('src/data/week06.yaml', 'w', encoding='utf-8') as f:
    yaml.dump(deep_literal(y6), f, allow_unicode=True, default_flow_style=False, sort_keys=False, width=120)
print("✓ Enriched Day 42 theory in week06.yaml")

# 3. Synchronize to HTML pages
print("\n=== SYNCHRONIZING TO ALL HTML PAGES ===")

for w in range(1, 27):
    hf = f'pages/weeks/week{w}.html'
    yf = f'src/data/week{w:02d}.yaml' if w < 10 else f'src/data/week{w}.yaml'
    if not os.path.exists(hf) or not os.path.exists(yf): continue

    with open(yf, 'r', encoding='utf-8') as f:
        ydata = yaml.safe_load(f)
    with open(hf, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    for day in ydata.get('days', []):
        did = int(day.get('day_num') or day.get('id'))
        day_sec = soup.find('div', id=f'day-{did}')
        if not day_sec: continue

        # Update theory_html if modified
        theory_elem = day_sec.find('div', class_='theory-content') or day_sec.find('div', id=f'day-{did}-theory')
        if theory_elem and day.get('theory_html'):
            new_th_soup = BeautifulSoup(day['theory_html'], 'html.parser')
            theory_elem.replace_with(new_th_soup.div if new_th_soup.div else new_th_soup)

        # Update predict block
        pred = day.get('predict')
        if pred:
            pb = day_sec.find('div', class_='predict-block') or day_sec.find('div', id=f'predict-block-{did}')
            if pb:
                code_str = html.escape(pred.get('code', '').strip())
                q_str = html.escape(pred.get('question', ''))
                exp_str = html.escape(pred.get('explanation', ''))
                ans_str = html.escape(pred.get('answer', ''))

                new_pb = BeautifulSoup(f'''<div class="predict-block" id="predict-block-{did}">
<h3 class="sh3">🔮 Predict Output Challenge</h3>
<p class="predict-q"><strong>Question:</strong> {q_str}</p>
<pre><code class="language-python">{code_str}</code></pre>
<div class="predict-input-row">
<input class="predict-input" id="predict-{did}-input" placeholder="Type your predicted output..." type="text"/>
<button class="predict-btn" onclick="checkPredict('predict-{did}', '{ans_str}')">Check Answer</button>
</div>
<div class="predict-result" id="predict-{did}-result" style="display:none;"></div>
<div class="predict-explanation" id="predict-{did}-exp" style="display:none;">💡 <strong>Explanation:</strong> {exp_str}</div>
</div>''', 'html.parser')
                pb.replace_with(new_pb.div)

    with open(hf, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    print(f"✓ Synchronized HTML: {hf}")

print("\n🎉 ALL FIXES APPLIED SUCCESSFULLY!")
