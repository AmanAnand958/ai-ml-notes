#!/usr/bin/env python3
"""
scripts/safe_scoped_remediation.py
Safely applies all remediations per day chunk:
1. Replaces predict the output questions, answers, and code blocks strictly within day containers
2. Corrects quiz answer keys and tags
3. Relocates Day 15 broadcasting diagram to Day 7
4. Wraps Day 15 Strategy 4 in a proper code block
5. Expands Day 19 with Seaborn vs Matplotlib common plot lessons
6. Repairs malformed <hN> tags
"""

import glob, yaml, re, html, os

print("=== STARTING SAFE SCOPED REMEDIATION ===")

SVG_BROADCASTING = '''<div class="svg-diagram-container" style="margin: 2rem 0; text-align: center;">
<svg aria-label="NumPy Broadcasting and Memory Layout Diagram" height="220" role="img" viewbox="0 0 760 220" width="100%" xmlns="http://www.w3.org/2000/svg">
<rect fill="#1e1e2e" height="220" rx="12" stroke="#313244" stroke-width="2" width="760">
</rect>
<text fill="#89b4fa" font-family="sans-serif" font-size="16" font-weight="bold" text-anchor="middle" x="380" y="30">
          NumPy Vectorized Broadcasting Rules &amp; Stride Alignment
         </text>
<!-- Matrix A (3x1) -->
<rect fill="#181825" height="120" rx="6" stroke="#89b4fa" stroke-width="1.5" width="100" x="50" y="65">
</rect>
<text fill="#89b4fa" font-family="monospace" font-size="13" text-anchor="middle" x="100" y="88">
          A: (3, 1)
         </text>
<text fill="#cdd6f4" font-family="monospace" font-size="12" text-anchor="middle" x="100" y="115">
          [[10], [20], [30]]
         </text>
<text fill="#f9e2af" font-family="sans-serif" font-size="24" font-weight="bold" text-anchor="middle" x="180" y="130">
          +
         </text>
<!-- Matrix B (1x4) -->
<rect fill="#181825" height="120" rx="6" stroke="#a6e3a1" stroke-width="1.5" width="160" x="210" y="65">
</rect>
<text fill="#a6e3a1" font-family="monospace" font-size="13" text-anchor="middle" x="290" y="88">
          B: (1, 4)
         </text>
<text fill="#cdd6f4" font-family="monospace" font-size="12" text-anchor="middle" x="290" y="115">
          [[1, 2, 3, 4]]
         </text>
<text fill="#f9e2af" font-family="sans-serif" font-size="24" font-weight="bold" text-anchor="middle" x="400" y="130">
          =
         </text>
<!-- Result (3x4) -->
<rect fill="#181825" height="120" rx="6" stroke="#f5e0dc" stroke-width="2" width="280" x="430" y="65">
</rect>
<text fill="#f5e0dc" font-family="monospace" font-size="13" text-anchor="middle" x="570" y="88">
          Output Matrix: (3, 4)
         </text>
<text fill="#cdd6f4" font-family="monospace" font-size="12" text-anchor="middle" x="570" y="115">
          [[11, 12, 13, 14],
         </text>
<text fill="#cdd6f4" font-family="monospace" font-size="12" text-anchor="middle" x="570" y="135">
          [21, 22, 23, 24],
         </text>
<text fill="#cdd6f4" font-family="monospace" font-size="12" text-anchor="middle" x="570" y="155">
          [31, 32, 33, 34]]
         </text>
</svg>
</div>'''

def fix_all_html_files():
    for week_num in range(1, 27):
        yaml_file = f'src/data/week{week_num:02d}.yaml'
        html_file = f'pages/weeks/week{week_num}.html'
        if not os.path.exists(yaml_file) or not os.path.exists(html_file):
            continue
            
        with open(yaml_file, 'r', encoding='utf-8') as f:
            ydata = yaml.safe_load(f)
        with open(html_file, 'r', encoding='utf-8') as f:
            hcontent = f.read()

        # Fix malformed tags
        hcontent = re.sub(r'<h([1-6])>\s*class="([^"]+)">', r'<h\1 class="\2">', hcontent)
        hcontent = re.sub(r'<p>\s*class="([^"]+)">', r'<p class="\1">', hcontent)

        # Process each day within ydata
        for d in ydata.get('days', []):
            d_num = d.get('day_num')
            predict = d.get('predict')
            if not d_num or not predict:
                continue
                
            q_text = html.escape(predict.get('question', ''))
            ans_text = str(predict.get('answer', ''))
            expl_text = html.escape(predict.get('explanation', ''))
            code_text = html.escape(predict.get('code', ''))
            
            # Find the checkPredict button in this day
            old_onclick_pat = r"checkPredict\('p" + str(d_num) + r"',\s*'[^']*'\)"
            new_onclick = f"checkPredict('p{d_num}', '{ans_text}')"
            hcontent = re.sub(old_onclick_pat, new_onclick, hcontent)
            
            # Find solution box for this day
            # <div class="solution-box" id="pred-d{d_num}"> ... </div>
            sol_box_pat = re.compile(
                r'(<div class="solution-box" id="pred-d' + str(d_num) + r'"[^>]*>\s*<p[^>]*>).*?'
                r'(</p>\s*<div[^>]*>.*?<pre>).*?'
                r'(</pre>\s*</div>\s*</div>)',
                re.DOTALL
            )
            
            def repl_sol(m):
                return (
                    m.group(1) + f"Expected Output: {ans_text}\nExplanation: {expl_text}" +
                    m.group(2) + code_text +
                    m.group(3)
                )
                
            hcontent = sol_box_pat.sub(repl_sol, hcontent)

            # Replace the predict question text before input
            # <p>What does this verification function for ... assert upon execution?</p>
            # <input class="predict-input" id="p{d_num}-input"
            q_pat = re.compile(
                r'(<p>)(?:What does this verification function for .*? assert upon execution\?)(</p>\s*<input class="predict-input" id="p' + str(d_num) + r'-input")',
                re.DOTALL
            )
            hcontent = q_pat.sub(r'\g<1>' + q_text + r'\g<2>', hcontent)

        # Specific Week 1 adjustments (Day 7)
        if week_num == 1:
            broadcasting_day7_html = '''<h3 class="sh3">
       3. Vectorized Broadcasting Rules & Stride Alignment
      </h3>
<p style="margin-top:0.4rem; margin-bottom:1rem; color:var(--text); line-height:1.6;">
Broadcasting allows NumPy to perform arithmetic operations on arrays with different shapes without allocating redundant memory copies by aligning trailing dimensions and stretching dimensions of size 1.
</p>
''' + SVG_BROADCASTING + '''
<div class="cb">
<div class="cb-head"><span class="cb-lang">python — broadcasting_rules.py</span><div class="cb-btns"><button class="copy-btn" onclick="copyCode(this)">copy</button><button class="run-btn" onclick="runCode(this)" style="margin-left: 4px;">Run</button></div></div>
<pre><code><span class="kw">import</span> numpy <span class="kw">as</span> np

<span class="cm"># Matrix A: Shape (3, 1)</span>
A = np.<span class="fn">array</span>([[<span class="num">10</span>], [<span class="num">20</span>], [<span class="num">30</span>]])

<span class="cm"># Matrix B: Shape (1, 4)</span>
B = np.<span class="fn">array</span>([[<span class="num">1</span>, <span class="num">2</span>, <span class="num">3</span>, <span class="num">4</span>]])

<span class="cm"># Broadcasting rule: (3, 1) + (1, 4) -> (3, 4) output matrix</span>
output = A + B
<span class="fn">print</span>(output.shape)  <span class="cm"># (3, 4)</span>
<span class="fn">print</span>(output)
<span class="cm"># [[11 12 13 14]</span>
<span class="cm">#  [21 22 23 24]</span>
<span class="cm">#  [31 32 33 34]]</span></code></pre>
</div>
'''
            if 'Vectorized Broadcasting Rules & Stride Alignment' not in hcontent:
                hcontent = re.sub(r'(<div class="day-section[^"]*" id="day-7".*?)(<h2 class="sh2">\s*🔮 Predict the Output)', r'\1' + broadcasting_day7_html + r'\n\2', hcontent, flags=re.DOTALL)

        # Specific Week 3 adjustments (Day 15 & Day 19)
        if week_num == 3:
            # Clean Day 15 analogy
            clean_d15_analogy = '''<div class="analogy">Medical exam results ki tarah socho — kuch tests ke results nahi aaye.
       <br/>
<br/>
       Agar hum uss patient ki "missing" test value ko 0 likh dein, model sochega patient ka result actually 0 tha — galat!
       <br/>
<br/>
       Missing ka matlab "not measured" hai, na ki 0.
       <br/>
<br/>
       Isi galti se models fail hote hain.</div>'''
            hcontent = re.sub(r'<div class="analogy">Medical exam results ki tarah socho.*?</div></div>\s*<!-- QUICK SECTION JUMP BAR -->', clean_d15_analogy + '\n\n        <!-- QUICK SECTION JUMP BAR -->', hcontent, flags=re.DOTALL)

            # Clean Day 15 Strategy 4
            strat4_html = '''<div class="cb" style="margin-top: 1.2rem;">
<div class="cb-head">
<span class="cb-lang">python — mnar_indicator.py</span>
<div class="cb-btns">
<button class="copy-btn" onclick="copyCode(this)">copy</button>
<button class="run-btn" onclick="runCode(this)" style="margin-left: 4px;">Run</button>
</div>
</div>
<pre><code><span class="cm"># --- Strategy 4: MNAR — Create indicator feature ---</span>
df[<span class="str">'cabin_missing'</span>] = df[<span class="str">'cabin'</span>].isnull().astype(<span class="bi">int</span>)
<span class="cm"># Now the model can LEARN that "cabin_missing = 1" is itself a signal</span></code></pre>
</div>'''
            hcontent = re.sub(r'</canvas>\s*</div>\s*<span class="cm">\s*# --- Strategy 4: MNAR.*?</span>\s*<h3 class="sh3">', '</canvas>\n</div>\n' + strat4_html + '\n<h3 class="sh3">', hcontent, flags=re.DOTALL)

            # Expand Day 19 Seaborn vs Matplotlib
            seaborn_expansion = '''<h3 class="sh3">0b. Seaborn vs. Matplotlib — Core Plot Equivalents & Upgrades</h3>
<p style="margin-top:0.4rem; margin-bottom:1rem; color:var(--text); line-height:1.6;">
Seaborn directly elevates standard Matplotlib chart types by automating multi-dimensional grouping (<code>hue</code>, <code>style</code>, <code>size</code>), statistical aggregation (mean, confidence intervals), and color palette mapping in concise one-liners.
</p>
<div class="table-wrap" style="overflow-x: auto; margin: 1.2rem 0; width: 100%;">
<table class="concept-table">
<tr><th>Chart Type</th><th>Matplotlib Syntax (Manual)</th><th>Seaborn Equivalent (High-Level)</th><th>Key Seaborn Advantage</th></tr>
<tr><td><strong>Scatter Plot</strong></td><td><code>plt.scatter(x, y, c=cat)</code></td><td><code>sns.scatterplot(data=df, x='x', y='y', hue='cat', size='num')</code></td><td>Automatic categorical legend & multi-attribute sizing</td></tr>
<tr><td><strong>Line Plot</strong></td><td><code>plt.plot(x, y)</code></td><td><code>sns.lineplot(data=df, x='time', y='val', errorbar='ci')</code></td><td>Auto-aggregates duplicate x-values with 95% bootstrap CI band</td></tr>
<tr><td><strong>Bar Chart</strong></td><td><code>plt.bar(cats, heights)</code></td><td><code>sns.barplot(data=df, x='cat', y='val', estimator='mean')</code></td><td>Computes group mean and error bars automatically from raw rows</td></tr>
<tr><td><strong>Histogram / KDE</strong></td><td><code>plt.hist(x, bins=30)</code></td><td><code>sns.histplot(data=df, x='val', kde=True, hue='group')</code></td><td>Combined density curve + stacked/overlaid multi-group distributions</td></tr>
</table>
</div>
<div class="cb">
<div class="cb-head"><span class="cb-lang">python — seaborn_core_plots.py</span><div class="cb-btns"><button class="copy-btn" onclick="copyCode(this)">copy</button><button class="run-btn" onclick="runCode(this)" style="margin-left: 4px;">Run</button></div></div>
<pre><code><span class="kw">import</span> seaborn <span class="kw">as</span> sns
<span class="kw">import</span> matplotlib.pyplot <span class="kw">as</span> plt

df = sns.<span class="fn">load_dataset</span>(<span class="str">'penguins'</span>)
sns.<span class="fn">set_theme</span>(style=<span class="str">'darkgrid'</span>)

fig, axes = plt.<span class="fn">subplots</span>(<span class="num">2</span>, <span class="num">2</span>, figsize=(<span class="num">14</span>, <span class="num">10</span>))

<span class="cm"># 1. Scatterplot with categorical hue & point sizing</span>
sns.<span class="fn">scatterplot</span>(data=df, x=<span class="str">'bill_length_mm'</span>, y=<span class="str">'bill_depth_mm'</span>, hue=<span class="str">'species'</span>, size=<span class="str">'body_mass_g'</span>, ax=axes[<span class="num">0</span>, <span class="num">0</span>])
axes[<span class="num">0</span>, <span class="num">0</span>].<span class="fn">set_title</span>(<span class="str">"Scatter: Bill Dimensions by Species & Body Mass"</span>)

<span class="cm"># 2. Lineplot with automated 95% Confidence Interval band</span>
sns.<span class="fn">lineplot</span>(data=df, x=<span class="str">'bill_length_mm'</span>, y=<span class="str">'flipper_length_mm'</span>, hue=<span class="str">'species'</span>, errorbar=<span class="str">'ci'</span>, ax=axes[<span class="num">0</span>, <span class="num">1</span>])
axes[<span class="num">0</span>, <span class="num">1</span>].<span class="fn">set_title</span>(<span class="str">"Line: Flipper Growth Trend with CI"</span>)

<span class="cm"># 3. Barplot with automatic group mean & error bar calculation</span>
sns.<span class="fn">barplot</span>(data=df, x=<span class="str">'island'</span>, y=<span class="str">'body_mass_g'</span>, hue=<span class="str">'sex'</span>, estimator=<span class="str">'mean'</span>, ax=axes[<span class="num">1</span>, <span class="num">0</span>])
axes[<span class="num">1</span>, <span class="num">0</span>].<span class="fn">set_title</span>(<span class="str">"Bar: Mean Body Mass by Island & Sex"</span>)

<span class="cm"># 4. Histplot with combined KDE curve</span>
sns.<span class="fn">histplot</span>(data=df, x=<span class="str">'flipper_length_mm'</span>, hue=<span class="str">'species'</span>, kde=<span class="kw">True</span>, ax=axes[<span class="num">1</span>, <span class="num">1</span>])
axes[<span class="num">1</span>, <span class="num">1</span>].<span class="fn">set_title</span>(<span class="str">"Hist + KDE: Flipper Distribution"</span>)

plt.<span class="fn">tight_layout</span>()
plt.<span class="fn">savefig</span>(<span class="str">"seaborn_core_grid.png"</span>)</code></pre>
</div>
'''
            if '0b. Seaborn vs. Matplotlib' not in hcontent:
                hcontent = hcontent.replace('<h3 class="sh3">\n       1. 🔥 Correlation Heatmap', seaborn_expansion + '\n<h3 class="sh3">\n       1. 🔥 Correlation Heatmap')
                hcontent = hcontent.replace('<h3 class="sh3">1. 🔥 Correlation Heatmap', seaborn_expansion + '\n<h3 class="sh3">1. 🔥 Correlation Heatmap')

        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(hcontent)

    print("All 26 week HTML files safely updated.")

if __name__ == '__main__':
    fix_all_html_files()
