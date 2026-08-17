#!/usr/bin/env python3
"""
scripts/fix_day13_layout_and_tags.py
Fixes the malformed README template code block and HTML tag balancing in Day 13.
"""

import yaml, re

print("=== FIXING DAY 13 LAYOUT & TAG NESTING ===")

clean_readme_code = """<span class="cm"># 🚢 Titanic Data Analysis</span>

<span class="cm">## 📌 Overview</span>
Complete EDA on the Titanic dataset exploring survival rates
by passenger <span class="kw">class</span>, gender, <span class="kw">and</span> age.

<span class="cm">## 🔍 Key Findings</span>
- Women had 3x higher survival rate than <span class="fn">men</span> (<span class="num">74</span>% vs <span class="num">19</span>%)
- 1st <span class="kw">class</span> <span class="cls">passengers</span> survived at <span class="num">63</span>% vs <span class="num">24</span>% <span class="kw">in</span> 3rd <span class="kw">class</span>
- Children under <span class="num">10</span> had <span class="num">60</span>% survival rate

<span class="cm">## 🛠️ Tech Stack</span>
Python · Pandas · Pandas plotting · Jupyter

<span class="cm">## 📂 Files</span>
- `eda_titanic.ipynb` — Main analysis notebook
- `data/train.csv` — <span class="fn">Dataset</span> (<span class="kw">from</span> Kaggle)

<span class="cm">## ▶️ Run Locally</span>
git clone &lt;repo-url&gt;
pip install -r requirements.txt
jupyter notebook eda_titanic.ipynb"""

# 1. Update YAML
w2_path = 'src/data/week02.yaml'
with open(w2_path, 'r', encoding='utf-8') as f:
    d2 = yaml.safe_load(f)

for day in d2['days']:
    if day['day_num'] == 13:
        theory = day['theory_html']
        # Replace the broken pre/code block
        pattern = r'<pre><code><span class="cm"># 🚢 Titanic Data Analysis[\s\S]*?</code></pre>bash[\s\S]*?</pre></pre>'
        replacement = f'<pre><code>{clean_readme_code}</code></pre>'
        theory = re.sub(pattern, replacement, theory)
        # Also clean any remaining </pre></pre>
        theory = theory.replace('</pre></pre>', '</pre>')
        day['theory_html'] = theory

with open(w2_path, 'w', encoding='utf-8') as f:
    yaml.dump(d2, f, allow_unicode=True, default_flow_style=False, sort_keys=False)

print("✓ Fixed Day 13 theory in src/data/week02.yaml")

# 2. Update HTML
h2_path = 'pages/weeks/week2.html'
with open(h2_path, 'r', encoding='utf-8') as f:
    h2 = f.read()

pattern_html = r'<pre><span class="cm"># 🚢 Titanic Data Analysis[\s\S]*?</pre>bash[\s\S]*?</pre>'
replacement_html = f'<pre><code>{clean_readme_code}</code></pre>'
h2 = re.sub(pattern_html, replacement_html, h2)
h2 = re.sub(r'<pre><code><span class="cm"># 🚢 Titanic Data Analysis[\s\S]*?</pre>bash[\s\S]*?</pre>', replacement_html, h2)

with open(h2_path, 'w', encoding='utf-8') as f:
    f.write(h2)

print("✓ Fixed Day 13 theory in pages/weeks/week2.html")
